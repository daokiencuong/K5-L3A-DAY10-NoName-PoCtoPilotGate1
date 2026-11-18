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
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")

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
