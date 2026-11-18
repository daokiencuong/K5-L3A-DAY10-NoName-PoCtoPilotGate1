"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    ticket = ctx.ticket or {}
    order_id = ticket.get("order_id")
    order = ctx.tools.lookup_order(order_id) if order_id else None
    if not order:
        return Verdict.escalate("Không xác minh được đơn trong tracking DB; chuyển CSKH xử lý thủ công")

    scope = (ctx.gates or {}).get("business", {}).get("pilot_scope", {})
    if scope.get("mode") == "warehouse":
        allowed = scope.get("warehouses") or []
        warehouse = order.get("warehouse_id")
        if not warehouse or warehouse not in allowed:
            return Verdict.escalate("Kho thiếu mã hoặc ngoài phạm vi pilot; chuyển CSKH xử lý thủ công")
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")

    # Cổng 3: Chỉ gửi đúng các trường trong hợp đồng hiện hành cho hãng.
    # Payload được dựng bởi model nên phải lọc theo allow-list và dựng lại
    # các giá trị từ tracking DB, không dùng giá trị tự do do model cung cấp.
    if tool == "notify_carrier":
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if not policy:
            return Verdict.escalate("Không xác định được chính sách chia sẻ dữ liệu đang hiệu lực")

        allowed = policy.get("carrier_notice_fields")
        payload = action.get("payload")
        if not isinstance(allowed, list) or not allowed or not isinstance(payload, dict):
            return Verdict.escalate("Thiếu allow-list hoặc payload thông báo hãng không hợp lệ")

        order_id = payload.get("order_id")
        order = ctx.tools.lookup_order(order_id) if order_id else None
        if not order:
            return Verdict.escalate("Không xác minh được đơn trong tracking DB trước khi gửi hãng")

        parcel_id = payload.get("parcel_id")
        parcel = next((p for p in order.get("parcels", []) if p.get("parcel_id") == parcel_id), None)
        if not parcel:
            return Verdict.escalate("Không xác minh được kiện trong tracking DB trước khi gửi hãng")

        safe_values = {
            "order_id": order["order_id"],
            "parcel_id": parcel["parcel_id"],
            "district": order.get("recipient", {}).get("district"),
            "delay_days": H.db_delay_days(parcel, ctx.as_of),
        }
        safe_payload = {key: safe_values[key] for key in allowed if key in safe_values}
        if set(safe_payload) != set(allowed) or any(value is None for value in safe_payload.values()):
            return Verdict.escalate("Allow-list hợp đồng có trường chưa thể dựng an toàn từ tracking DB")

        changes = {}
        if payload != safe_payload:
            changes["payload"] = safe_payload
        carrier_id = parcel.get("carrier_id")
        if not carrier_id or not ctx.tools.lookup_carrier(carrier_id):
            return Verdict.escalate("Không xác minh được hãng của kiện trong tracking DB")
        if action.get("carrier_id") != carrier_id:
            changes["carrier_id"] = carrier_id
        if changes:
            return Verdict.modify("Lọc payload theo hợp đồng và dựng lại dữ liệu từ tracking DB", **changes)

    # Cổng 1: Kiểm soát lệnh hoàn tiền (issue_refund)
    if tool == "issue_refund":
        # 1a. Kiểm soát trần ngân sách hoàn tiền tự động trong ngày từ config
        cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
        spent = ctx.tools.auto_refund_today_vnd()
        amt = action.get("amount_vnd", 0)
        if cap is not None and spent + amt > cap:
            return Verdict.escalate("Vượt trần ngân sách hoàn tiền tự động trong ngày")

        # 1b. Đối chiếu sự thật DB: Kiểm tra số ngày trễ thực tế và quyền lợi bồi thường
        order_id = action.get("order_id")
        if order_id:
            order = ctx.tools.lookup_order(order_id)
            if order:
                parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
                real_delay = H.db_delay_days(parcel, ctx.as_of)
                policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
                if policy:
                    entitled = H.entitlement_vnd(policy, order, real_delay, parcel.get("delay_cause"))
                    if amt > entitled:
                        if entitled == 0:
                            return Verdict.deny(f"Không đủ điều kiện hoàn tiền theo tracking DB (trễ {real_delay} ngày)")
                        return Verdict.modify(f"Điều chỉnh số tiền hoàn về đúng chính sách ({entitled}đ)", amount_vnd=entitled)

    # Cổng 2: Kiểm soát lệnh ghi lỗi cho hãng vận chuyển (file_carrier_fault)
    if tool == "file_carrier_fault":
        order_id = action.get("order_id")
        if order_id:
            order = ctx.tools.lookup_order(order_id)
            if order:
                parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
                real_delay = H.db_delay_days(parcel, ctx.as_of)
                policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
                if policy and not H.carrier_at_fault(policy, parcel, real_delay):
                    return Verdict.deny(f"Hãng vận chuyển không có lỗi theo tracking DB (trễ {real_delay} ngày)")

    return Verdict.allow()
