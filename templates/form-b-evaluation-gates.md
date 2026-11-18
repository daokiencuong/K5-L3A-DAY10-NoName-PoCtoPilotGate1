# Phiếu B · Đo, rủi ro, cổng vòng 1 và quyết định v1 · Khối 2A + 2B + chốt (phút 65–115)

**Bàn:** ______

Tiêu chí đã ký ở Phiếu A. Từ phút 65 bàn mới được chạy trợ lý. Khối 2A (65–85) chưa sửa code hay config. Khối 2B (85–105) sửa
`lab10/guards.py` và `config/operating_gates.json`. Phút 105–115 chốt cổng vòng 1 rồi viết quyết định v1. Sau phút 115 không sửa phiếu này
(trừ khi Phiếu C bảo "mở lại" một ô và ghi bằng bút khác màu).

**Mục lục**
- [B0 · Nhật ký lần chạy vòng 1 (suốt khối)](#b0)
- [B1 · Câu 2.1 · Lần chạy đầu tiên, cổng tự chặn hay người duyệt · phút 65–71](#b1)
- [B2 · Câu 2.2 · Bảng soát lỗi `T-002@55` · phút 71–75](#b2)
- [B3 · Câu 2.3 · Bản đồ dữ liệu và ví dụ drift · phút 65–75](#b3)
- [B4 · Câu 2.4 · HAZOP vòng 1 · phút 65–75](#b4)
- [B5 · Câu 2.4 · Checklist 9 nhóm việc, lần 1 · phút 70–75](#b5)
- [B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa · phút 75–85](#b6)
- [B7 · Câu 2.6–2.10 · Cổng phòng ngừa, runbook phần 1–3, giờ cao điểm · phút 85–105](#b7)
- [B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 · phút 105–115](#b8)

---

<a id="b0"></a>

## B0 · Nhật ký lần chạy vòng 1

*Yêu cầu: ít nhất 3 lần chạy, mỗi lần đổi một thứ, có mã lần chạy và khoảng tin cậy.* Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi
một dòng vào `runs/journal.jsonl`. Việc của bàn là điền cột "Đổi MỘT thứ gì" (tham số `--note`) và cột "Kết luận".
Mọi con số trong quyết định Gate 1 phải trỏ về một dòng ở đây hoặc ở Phiếu C mục C0.

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | | base · base | (baseline, chưa có cổng) | | | | | |
| 2 | | base · after | (cổng vòng 1, thử trước khi chốt) | | | | | |
| 3 | | base · prepared | (cổng vòng 1 đã chốt) | | | | | |
| 4 | | | | | | | | |

---

<a id="b1"></a>

## B1 · Câu 2.1 · Lần chạy đánh giá đầu tiên

```bash
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

- Mã lần chạy: `__________` (ghi cả vào B0 dòng 1)
- Ngưỡng đã ký nào `[CHƯA]` đạt: …
- Khối "kinh doanh và vận hành" ở cuối output: dòng nào đáng lo? …
- Khối "theo kho và hãng": kho hoặc hãng nào có số xấu nhất? …

**Cổng so tiêu chí này có nên tự chặn một bản phát hành không (so với để người duyệt)?**

| Lý lẽ ủng hộ tự chặn | Lý lẽ phản đối |
|---|---|
| | |

Khuyến nghị (khoanh một): **tự chặn · người duyệt · kết hợp**. Vì: …

---

<a id="b2"></a>

## B2 · Câu 2.2 · Bảng soát lỗi cho `T-002@55`

```bash
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
```

**Cách làm, giữ nguyên ba phần:** (1) ghi lại từng lỗi bằng **cái người ta thực sự thấy**, ai gặp, mức hệ trọng,
và xếp vào một trong ba **loại lỗi**; (2) đưa lỗi qua bộ câu hỏi để tìm **nguồn**; (3) viết **hướng xử lý**: vì sao người ta coi
đó là lỗi, người ta đi tiếp bằng đường nào, hệ thống học được gì.

Ba loại lỗi:
- **Giới hạn của hệ thống**: hệ thống không thể trả lời đúng, hoặc không trả lời được, vì giới hạn vốn có.
- **Lỗi ngữ cảnh**: hệ thống "chạy đúng thiết kế" nhưng người dùng thấy sai, vì hành động không được giải thích, trái với hình dung của họ, hoặc dựa trên giả định kém.
- **Lỗi chìm**: hệ thống chạy sai mà **cả người dùng lẫn hệ thống đều không nhận ra**. Với một trợ lý có quyền ghi sổ, đây là loại nguy hiểm nhất: người chịu hại thường là bên thứ ba.

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 |
|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | | |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | | |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | | |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | | |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 |
|---|---|---|
| Vì sao người gặp coi đây là lỗi | | |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | | |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | | |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | | |

**Ví dụ (bộ nền, đừng chép):** `T-002@55` · sổ cái có dòng hoàn 20.000đ, hãng VNX nhận một lỗi, trong khi tracking ghi trễ 2 ngày ·
khách không thấy gì sai, hãng chịu · cao · **lỗi chìm**. Nguồn: đầu vào (đặt sai trọng số cho con số khách tự khai). Xử lý:
hãng coi là lỗi vì sổ giao của họ ghi 2 ngày; kiểu giải pháp: trao quyền cho người (số khai khác tracking thì chuyển người duyệt);
tín hiệu: đếm sự kiện `model_override` mỗi ngày.

---

<a id="b3"></a>

## B3 · Câu 2.3 · Bản đồ dữ liệu của trợ lý và ví dụ drift

**Cách làm:** đi từ người dùng và việc họ cần làm, tới đầu ra của hệ thống, rồi mới hỏi hệ thống cần dữ liệu
gì, định dạng ra sao, và **thế giới thật làm dữ liệu đó lệch đi thế nào**; cuối cùng tóm lại trong vài câu.
Trợ lý LogiX không huấn luyện gì trong lab này, nên ta hỏi về "dữ liệu trợ lý đọc lúc chạy / trường then chốt / nguồn sự thật".
Gợi ý: mở `data/world.json` phần `policies`, `orders[].parcels`, `ops_limits`, `ops_facts`.

| Mục | Điền cho trợ lý hoàn tiền |
|---|---|
| Người dùng | |
| Việc người dùng cần làm xong | |
| Đầu ra của hệ thống (kể cả các lệnh ghi) | |
| Dữ liệu trợ lý đọc lúc chạy (bảng nào trong `data/world.json`) | |
| Trường then chốt quyết định tiền và lỗi hãng | |
| Với mỗi trường then chốt: **nguồn sự thật** hay **bản sao** (ai cập nhật, khi nào)? | |
| Định dạng cần để ý (ngày, trường được phép trống, đơn nhiều kiện) | |
| Thế giới thật làm dữ liệu lệch ở đâu (theo mùa, đổi chính sách, giờ cao điểm, người nhập tay)? | |
| Câu người ngoài sẽ hỏi về nguồn dữ liệu ("sao hệ thống biết đơn trễ mấy ngày?") | |

**Tóm lại (điền vào chỗ trống):**
Trợ lý dùng `__________`, `__________`, `__________` để giúp `__________` làm được `__________`.
Trường mà nếu sai thì tiền hoặc lỗi hãng sai theo: `__________`, `__________`.
Chúng tôi biết thế giới thật sẽ làm dữ liệu lệch ở: `__________`. Dấu hiệu nhìn thấy sớm nhất: `__________`.

**Ví dụ drift trong 3 tháng tới** (lấy từ dòng "thế giới thật làm dữ liệu lệch"): cái gì đổi `____` · đổi ngày nào `____` ·
trường nào cho thấy `____` · con số nào của Bản tiêu chí bị ảnh hưởng `____`.
Đây là đầu vào đổi hay quan hệ vào–ra đổi? Chỉ số nào sẽ phát hiện? `__________`

**Ví dụ một dòng (đừng chép):** trường then chốt `parcels[].delivered_date` · bản ghi do máy quét ở điểm phát tạo ra, là nguồn
sự thật về ngày giao · lệch khi điểm phát quét sót hoặc nhập bù bằng tay.

---

<a id="b4"></a>

## B4 · Câu 2.4 · HAZOP vòng 1 trên tool của agent

*Chỉ làm MỘT vòng, trên MỘT tool. Đây là HAZOP vòng 1; HAZOP của thẻ sự cố viết riêng ở Phiếu C mục C4, không ghi đè bảng này.*

**Khung tư duy.** HAZOP không hỏi "cái gì có thể hỏng" một cách chung chung. Nó cầm từng **từ gợi ý** áp vào từng **dòng dữ
liệu đi vào một hành động** và hỏi: nếu dòng này lệch theo kiểu đó thì hậu quả là gì, ai chịu. Mục tiêu là tìm ra những nhánh
mà cả bàn chưa nghĩ tới, không phải tả lại nhánh đã biết.

| Guideword | Nghĩa khi áp vào một tool của agent |
|---|---|
| **WRONG** | Giá trị đưa vào có đủ, hợp lệ về hình thức, nhưng sai sự thật |
| **INVALID** | Giá trị không còn hiệu lực: hết hạn, sai phiên bản, sai đối tượng |
| **INCOMPLETE** | Thiếu một phần thông tin cần có để quyết định |
| **PERTURBED** | Đầu vào bị ai đó cố ý hoặc vô tình làm lệch (cài câu lệnh, gửi lặp) |
| **INCAPABLE** | Thành phần không trả lời được: quá tải, lỗi, hết quota |

**Câu hỏi dẫn dắt:** tool nào tạo ra hậu quả không đảo ngược? Mỗi tham số của tool đó lấy từ đâu (ticket, DB, model tự suy)?
Với mỗi guideword: hậu quả cho ai, hiện có gì ngăn, cần thêm gate ở tầng nào (phát hiện / chặn / giới hạn thiệt hại)?

Tool chọn phân tích: `file_carrier_fault` (kèm `notify_carrier` đi ngay sau nó). Lý do chọn: đây là lệnh ghi không đảo ngược được
với bên thứ ba. Mỗi lỗi là một khoản phạt hãng phải trả, và hãng nhỏ bị đình chỉ sau vài lỗi trong 7 ngày (GHSH, DNB: 3 lỗi).

| Tham số / dòng dữ liệu | Guideword | Lệch cụ thể (viết bằng dữ kiện của lab) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `delay_days` | WRONG | Độ trễ lấy theo số ngày khách tự khai thay cho tracking (sự kiện `model_override`, ví dụ `T-002@55`: tracking 2 ngày, ticket khai 5 ngày) | Hãng VNX bị ghi một lỗi oan, phạt 100.000đ; LogiX hoàn sai | Không có gì | `write_gate` khi `tool == "file_carrier_fault"`: so `delay_days` với độ trễ tính từ tracking (`helpers`), lệch thì `escalate` · **chặn** |
| `carrier_id` / `parcel_id` | WRONG | Đơn nhiều kiện: trợ lý lấy kiện trễ nhất để tính độ trễ nhưng ghi lỗi cho hãng của **kiện đầu tiên** (`lab10/agent.py`, `first = parcels[0]`). Đơn O-1013 có P1 của GHSH và P2 của LGX; nếu P2 mới là kiện trễ thì GHSH vẫn bị ghi lỗi. **Nhánh này bàn chưa thấy trên trace** | Một hãng không liên quan bị phạt, có thể bị đình chỉ (GHSH: 150.000đ/lỗi, đình chỉ sau 3 lỗi/7 ngày); sổ của chị Oanh lệch với hãng | Không có gì | `write_gate`: kiện được ghi lỗi phải là kiện có độ trễ theo tracking ≥ ngưỡng chính sách, khác thì `escalate` · **chặn** |
| `delay_cause` | INCOMPLETE | Tracking không ghi nguyên nhân (O-1010 của GHSH, O-1012 của MKD có `delay_cause: null`), trợ lý mặc định đổ cho hãng (`unknown cause -> blame carrier`) | Hãng bị ghi lỗi khi chưa ai biết vì sao trễ | Không có gì | `legal.carrier_fault_requires_recorded_cause = true` · **chặn** (config, không cần code) |
| chính sách áp dụng | INVALID | Trợ lý đọc cờ `index_active` thay cho ngày hiệu lực. Từ 2026-12-01, REFUND-v4 bỏ `FORCE_MAJEURE` khỏi `fault_causes`; nếu cờ chưa đổi, đơn trễ do bão (như O-1006 của MKD) vẫn bị ghi lỗi hãng | MKD bị phạt 120.000đ/lỗi vì bão | Không có gì | Cổng so ngày hiệu lực của chính sách với ngày của đơn (`helpers`) · **chặn**; monitor đếm lỗi hãng có nguyên nhân `FORCE_MAJEURE` · **phát hiện** |
| `carrier_id` (số lần) | PERTURBED | Khách gửi lặp nhiều ticket cho cùng một hãng, hoặc ghi chú lúc đặt hàng (`checkout_note`) cài câu lệnh mà model vẫn đọc | Một hãng nhận ≥ 3 lỗi trong ngày, vượt trần đã thống nhất với Ops | Không có gì | `write_gate`: từ lỗi thứ 3 của cùng một hãng trong ngày thì `escalate` (`ops_limits.max_auto_strikes_per_carrier_per_day = 2`) · **giới hạn thiệt hại** |

Không bắt buộc điền đủ năm dòng. Bắt buộc: **ít nhất ba dòng, trong đó một dòng là nhánh bàn chưa thấy trên trace**.

Không bắt buộc điền đủ năm dòng. Bắt buộc: **ít nhất ba dòng, trong đó một dòng là nhánh bàn chưa thấy trên trace**.

**Mở rộng ra ngoài kỹ thuật (thêm ít nhất hai dòng):** "thành phần" không chỉ là model và tool. Áp cùng năm từ gợi ý vào:

| Thành phần ngoài code | Ví dụ câu hỏi |
|---|---|
| **Người duyệt** (vận hành) | INCAPABLE: chỉ một người trực mà 14 ca tới trong một giờ thì ca cuối chờ bao lâu? |
| **Ngân sách** (kinh doanh) | WRONG: tổng hoàn tự động trong ngày vượt mức Finance cho phép mà không ai được báo thì sao? |
| **Phạm vi pilot** (kinh doanh) | INVALID: có nhóm ticket nào trợ lý luôn phải chuyển người, tức là tự động hoá vô nghĩa? |
| **Dữ liệu gửi bên thứ ba** (pháp lý) | PERTURBED: chữ khách tự gõ có tên, số điện thoại người khác bị chép sang hãng thì ai chịu? |

| Thành phần | Guideword | Lệch cụ thể | Hậu quả, cho ai | Cổng đề xuất: code hay con số nào trong `config/operating_gates.json` |
|---|---|---|---|---|
| **Người duyệt** (vận hành) | INCAPABLE | Chỉ 1 người trực (`default_reviewers_on_shift = 1`), sức duyệt 6 ca/giờ. Giờ cao điểm lượng ticket gấp 3; nếu thêm kiểm mẫu 10% thì hàng chờ vượt sức và có ca chờ quá 60 phút (`review_sla_minutes`) | Khách chờ không ai trả lời; chị Hạnh quá tải; ca bị ùn làm hỏng `queue_stuck_max` | `operations.reviewers_on_shift = 1`, `review_capacity_per_hour = 6`, `max_queue_wait_minutes = 60`, `decision_note = true` (kiểm lại chỉ tốn 0,4 ca); runbook mục Giờ cao điểm: gọi thêm người khi hàng chờ ≥ 6 ca |
| **Dữ liệu gửi bên thứ ba** (pháp lý) | PERTURBED | Thông báo gửi hãng kèm nguyên văn chữ khách gõ (`customer_note`); đơn quà tặng còn kèm tên và số điện thoại người nhận (`recipient_contact`), trong khi chính sách chỉ cho gửi `order_id, parcel_id, district, delay_days` | Dữ liệu cá nhân của khách và người nhận quà tới tay hãng và tài xế mà họ không biết; LogiX chịu trách nhiệm pháp lý | `legal.pii_fields_blocked_to_third_party = ["recipient_contact", "customer_note"]` |
| **Hãng vận chuyển nhỏ** (con người, pháp lý) | WRONG | GHSH (hộ kinh doanh, 12 tài xế) và DNB (tài xế tự do) bị đình chỉ sau 3 lỗi/7 ngày; 3 lỗi ghi oan trong một tuần là đủ làm họ mất việc | Một bên thứ ba mất hợp đồng vì lỗi của trợ lý; không ai hỏi họ trước | `operations.stop_conditions`: 1 lỗi ghi oan thì tắt `file_carrier_fault`; monitor số lỗi 7 ngày theo từng hãng (Phiếu A, câu 1.4) |

**Ví dụ mẫu (`issue_refund`, đừng chép):** tham số `amount_vnd` · WRONG · số tiền tính từ số ngày khách tự khai · LogiX mất
tiền, hãng bị kéo theo một lỗi · hiện chỉ có trần "không vượt tổng tiền đơn" · cổng ghi so với quyền lợi tính từ DB (chặn).

---

<a id="b5"></a>

## B5 · Câu 2.4 · Checklist go-live 9 nhóm việc, lần 1

Checklist chín nhóm việc phải xong trước khi chạy thử thật. Bàn điền lần đầu ở đây, rồi cập nhật sau sự cố ở Phiếu C mục C11.
Cột "Bằng chứng lấy từ đâu" trỏ tới mục bàn đã điền ở bước khác; không điền thêm phiếu nào chỉ để lấp cột này.

Trạng thái: **Xong** (có bằng chứng) · **Chưa** · **Không áp dụng** (ghi lý do). Bằng chứng là **mã lần chạy**, tên file / mục phiếu, hoặc số trong report.
**Cột PIC bắt buộc:** mỗi dòng một người có tên (không ghi "cả bàn"). Dòng nào chưa có PIC thì coi như Chưa.

| # | Nhóm việc | Bằng chứng lấy từ đâu (đã có sẵn trong lab) | Mục cần kiểm tra | Trạng thái | Bằng chứng | PIC |
|---|---|---|---|---|---|---|
| 1 | Chất lượng | Report `lab10.eval` (mã lần chạy) + bảng soát lỗi (Phiếu B mục B2) | `pass_rate`, `pass_k` đạt ngưỡng đã ký trên bộ nền ở mốc prepared; `T-002@55` đã xếp loại lỗi | Chưa | Chờ mã lần chạy base và prepared (B0) | NV-TUNG (Lê Thanh Tùng) |
| 2 | Dữ liệu | Bản đồ dữ liệu (Phiếu B mục B3, câu 2.3): trường nào là nguồn sự thật, trường nào là bản sao | `delay_cause`, `delivered_date` là nguồn sự thật; cờ `refund_status` (đối soát đêm) và cờ `index_active` của chính sách là bản sao có thể cũ | Chưa | B3; drift REFUND-v4 có hiệu lực 2026-12-01 | NV-OANH (Phạm Kiều Oanh) |
| 3 | Bảo mật | Một vòng HAZOP với guideword PERTURBED (Phiếu B mục B4): chữ nào đi vào model mà không do LogiX viết | Chữ ticket và `checkout_note` do khách gõ đi vào model; không có chữ nào đi thẳng tới lệnh ghi mà không qua cổng | Chưa | B4 dòng PERTURBED; cổng ở B7.1 | NV-TUNG (Lê Thanh Tùng) |
| 4 | Quyền hạn | `config/switches.json` + guard trước lệnh ghi; thẻ S2, S8 có thêm mục mức kiểm soát (Phiếu C mục C3) | Mỗi lệnh ghi có công tắc riêng; khoản vượt hạn mức tự động (200.000đ, REFUND-v3) phải có phê duyệt hợp lệ của NV-HANH cho đúng ticket | Chưa | `config/switches.json` (4 công tắc đang `on`); `approver_id = NV-HANH`; cổng ở B7.1 | NV-HANH (Trần Thị Hạnh) |
| 5 | Hiệu năng, hạ tầng | Đội tự ước tính; HAZOP guideword INCAPABLE: LLM không trả lời thì sao; số người duyệt và số ca mỗi giờ | 1 người trực × 6 ca/giờ = 48 ca/ca 480 phút; LLM lỗi thì ticket chuyển người, không ghi lại lần hai | Chưa | `operations.reviewers_on_shift = 1`, `review_capacity_per_hour = 6`; số ca bị ùn trong report base | NV-TUNG (Lê Thanh Tùng) |
| 6 | Chi phí | Khối "kinh doanh và vận hành" của report: chi phí mỗi ticket so với làm tay, ROI, tiền LLM ticket đắt nhất; `config/operating_gates.json` mục `business` | Chi phí mỗi ticket < 10.000đ (làm tay); tiền LLM ≤ 1.500đ/ticket; tổng hoàn tự động ≤ 2.000.000đ/ngày | Chưa | Chờ report base; mục `business` do vai Sản phẩm và kinh doanh điền | NV-OANH (Phạm Kiều Oanh) |
| 7 | Vận hành | Runbook (Phiếu B mục B7.5–B7.6) + `config/operating_gates.json` mục `operations` (PIC, người duyệt, số người trực, điều kiện dừng, kênh báo tin) + metric trong `monitors.py` | Đủ PIC, người duyệt, kênh báo tin, điều kiện dừng; runbook 1–3 khớp con số trong config | Xong (phần config và runbook); monitor để vòng 2 | `config/operating_gates.json` mục `operations`; B7.5, B7.6 | NV-TUNG (Lê Thanh Tùng) |
| 8 | Con người, pháp lý | Bên thứ ba (hãng, tài xế, shop, người nhận quà, người đứng tên duyệt); `config/operating_gates.json` mục `legal`; thẻ S6, S7, S8 có mục riêng ở Phiếu C mục C3 | Không gửi dữ liệu cá nhân cho hãng; chỉ ghi lỗi hãng khi tracking có nguyên nhân; có người nhận khiếu nại của hãng | Xong (phần config); chờ report kiểm `pii_leaks = 0` | `legal.pii_fields_blocked_to_third_party = ["recipient_contact", "customer_note"]`, `legal.carrier_fault_requires_recorded_cause = true` | NV-OANH (Phạm Kiều Oanh) |
| 9 | Quyết định | Câu tiêu chí (Phiếu A mục A4) + hash Bản tiêu chí đã ký + quyết định Gate 1 (Phiếu B mục B8, Phiếu C mục C12) | Tiêu chí ký và push trước lần chạy đầu; quyết định v1 khớp `decision_rule` | Chưa | Phiếu A mục A5; B8 | NV-TUNG (Lê Thanh Tùng) |

Ô "Chưa" có rủi ro cao → chuyển thành một dòng Risk register (Phiếu C mục C10).

---

<a id="b6"></a>

## B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa (khoảng 8–10 phút, cả bàn)

*Mọi bàn làm pre-mortem ở vòng 1, TRƯỚC khi biết sự cố, để chọn 2–3 cổng phòng ngừa sẽ dựng. Ở vòng 2 bàn mở lại phần này ở
Phiếu C mục C1 (bút khác màu).*

**Khung tư duy.** Hỏi "có rủi ro gì không" thì ai cũng dè dặt. Nói "nó đã hỏng rồi, vì sao" thì mọi người được phép nói ra
điều mình vẫn lo. Làm im lặng trước, đọc sau, để ý kiến của người nói to không lấn át.

**Đề bài (đọc to):** *"Ba tháng sau pilot, LogiX phải tắt trợ lý hoàn tiền ở cả hai depot. Chuyện gì đã xảy ra?"*

1. **2 phút, im lặng:** mỗi người viết 2 lý do, mỗi lý do một dòng.
2. **2 phút:** đọc vòng tròn, mỗi lượt một lý do, không bình luận. Gộp lý do trùng.
3. **2 phút:** xếp từng lý do vào một **lăng kính**. Lăng kính nào còn trống thì cả bàn viết thêm ít nhất một lý do cho nó.
4. **2 phút:** chọn 2–3 lý do sẽ biến thành **cổng phòng ngừa** ngay hôm nay (code trong `guards.py` hoặc con số trong
   `config/operating_gates.json`). Lý do còn lại → Risk register.

Bốn lăng kính (bắt buộc đủ cả bốn; dự án AI hay chết ở ba lăng kính sau hơn là ở lăng kính đầu):

| Lăng kính | Câu hỏi gợi ý trên LogiX |
|---|---|
| **Kỹ thuật** | Model tin nhầm cái gì? Dữ liệu nào thiếu, cũ, lệch? Lệnh ghi nào không đảo ngược được? |
| **Kinh doanh** | Mỗi ticket tốn bao nhiêu so với làm tay? Một ngày hoàn tối đa bao nhiêu? Nhóm ticket nào không thể có lời? |
| **Con người và vận hành** | Ai duyệt, mấy người, mỗi giờ được mấy ca? Lượng việc tăng gấp ba thì sao? Nhân viên có tin trợ lý không? |
| **Pháp lý** | Dữ liệu cá nhân của ai rời hệ thống? Bên thứ ba nào bị ghi lỗi, bị trừ tiền mà không được hỏi? |

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được hôm nay? (trace / data / config nào) | Thành cổng phòng ngừa nào (code hay config) / hay vào risk register |
|---|---|---|---|
| | Kỹ thuật | | |
| | Kinh doanh | | |
| | Con người và vận hành | | |
| | Pháp lý | | |
| | | | |

---

<a id="b7"></a>

## B7 · Khối 2B · Cổng phòng ngừa (phút 85–105)

### B7.1 · Câu 2.6 · 2–3 cổng phòng ngừa trong `lab10/guards.py`

Mỗi cổng ứng với một dòng pre-mortem (B6) hoặc một dòng HAZOP (B4). Viết trong `pre_guard(ctx)` (trước khi trợ lý đọc ticket)
hoặc `write_gate(ctx, action)` (trước mỗi lệnh ghi). Thử bằng:

```bash
python3 -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."
python3 -m unittest discover -s tests
```

| # | Cổng (hàm và nhánh, ví dụ `write_gate` khi `tool == "issue_refund"`) | Ứng với dòng nào ở B6 / B4 | Chặn điều gì, dựa vào nguồn sự thật nào | Mã lần chạy `base · after` | Ca đang đúng nào bị hỏng? (phải là "không") |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### B7.2 · Câu 2.7 · Hai bước tránh rò rỉ dữ liệu

Bàn đang chỉnh cổng tới khi 22 ticket bộ nền xanh hết. Nêu 2 bước cụ thể để không "chỉnh trên chính bộ dùng để chấm"
(gắn với bộ nền, gói sự cố, bài kiểm tra ẩn):

1. …
2. …

### B7.3 · Câu 2.8 · Một behavioral test

- Tính chất (một câu): …

```bash
python3 -m lab10.trace --suite base --stage after --adhoc "..." --order O-10xx --customer C-xx
```

| Ticket hiểm | Nội dung ticket (`--adhoc`) | `--order` · `--customer` | Kết quả (dán dòng `SỔ CÁI` / `LỖI HÃNG` / `GỬI HÃNG`) | Tính chất giữ được? |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

Giữ hai ticket này cho phần demo.

### B7.4 · Câu 2.9 · Cổng kinh doanh (`config/operating_gates.json` mục `business`)

Mỗi con số kèm một câu lý do, lấy từ `data/world.json` → `ops_limits`, `ops_facts`.

| Khoá | Giá trị bàn đặt | Lý do (một câu, có số) |
|---|---|---|
| `business.daily_refund_cap_vnd` | | |
| `business.cost_budget_per_ticket_vnd` | | |
| `business.pilot_scope` (all / warehouse / percent) | | |
| `business.roi_min` | | |

### B7.5 · Câu 2.10 · Cổng con người, vận hành, pháp lý + Runbook phần 1–3

Điền `config/operating_gates.json` mục `operations` và `legal` (PIC, người duyệt, số người trực mỗi ca, công suất duyệt mỗi giờ,
thời gian chờ tối đa, điều kiện dừng, kênh báo tin; trường dữ liệu cá nhân không gửi cho bên thứ ba; ghi lỗi cho hãng phải có
nguyên nhân trong tracking). Rồi viết runbook dưới đây **khớp với các con số đó**.

*Runbook là tờ giấy người trực ca cầm lúc 23h khi có chuyện. Nó trả lời: nhìn con số nào, ngưỡng nào thì làm gì, ai được quyết.
Phần 1–3 và mục Giờ cao điểm viết ở vòng 1. Phần 4–5 viết ở vòng 2 (Phiếu C mục C11). Mọi con số phải khớp `config/operating_gates.json` và report.*
*Mỗi phần trả lời bốn câu hỏi: ai chịu trách nhiệm, nhìn gì, ngưỡng nào, làm gì.* **Người viết (vai Vận hành và pháp lý):** Hoàng Bảo Nguyên

#### Runbook 1 · Ai chịu trách nhiệm

| Vai | Tên / mã nhân viên (lấy từ `data/world.json` → `staff`) | Được quyền làm gì | Liên lạc qua kênh nào |
|---|---|---|---|
| PIC của trợ lý (một người) | NV-TUNG · Lê Thanh Tùng (Giám sát vận hành) | Chịu trách nhiệm chung; quyết định dừng một phần hay dừng hẳn; ký bật lại | `#logix-refund-pilot-canh-bao` + điện thoại trực |
| Người duyệt đứng tên các khoản vượt hạn mức | NV-HANH · Trần Thị Hạnh (Trưởng ca CSKH) | Duyệt khoản hoàn > 200.000đ (hạn mức REFUND-v3) hoặc > 300.000đ/khách/ngày; duyệt ca trợ lý chuyển sang; kiểm mẫu 10% quyết định tự động | Hàng chờ duyệt + `#logix-refund-pilot-canh-bao` |
| Người giữ công tắc tắt từng thao tác ghi | NV-TUNG · Lê Thanh Tùng | Chuyển `issue_refund`, `file_carrier_fault`, `notify_carrier`, `send_reply` trong `config/switches.json` sang `off`; đổi `business.pilot_scope` | `#logix-refund-pilot-canh-bao` |
| Người nhận khiếu nại của bên thứ ba (hãng, shop, người nhận quà) | NV-OANH · Phạm Kiều Oanh (Kế toán đối soát) | Nhận khiếu nại lỗi ghi oan từ hãng, gỡ lỗi và hoàn phạt sau khi NV-TUNG xác nhận; báo ngay vào kênh khi có khiếu nại | Email đối soát hãng/shop + `#logix-refund-pilot-canh-bao` |

Số người trực duyệt mỗi ca: **1** · Mỗi giờ duyệt được: **6** ca · Phạm vi pilot: **tất cả** (`pilot_scope.mode = "all"`; vai Sản phẩm và kinh doanh có thể thu hẹp ở B7.4)

#### Runbook 2 · Nhìn con số nào, ngưỡng nào thì làm gì

Mỗi dòng một tín hiệu. Cột "Lấy ở đâu" phải là một dòng trong report của `lab10.eval` / `lab10.grade` hoặc một chỉ số trong `lab10/monitors.py`.

| Tín hiệu | Lấy ở đâu | Bình thường | Ngưỡng VÀNG → việc làm | Ngưỡng ĐỎ → việc làm | Ai quyết |
|---|---|---|---|---|---|
| Thời gian chờ người duyệt lâu nhất | Khối "kinh doanh và vận hành" của report `lab10.eval` (thời gian chờ người duyệt) | < 40 phút | ≥ 40 phút → NV-HANH báo vào kênh, NV-TUNG gọi thêm 1 người duyệt | > 60 phút (`max_queue_wait_minutes`) → thu hẹp `pilot_scope` về một kho tới hết ngày | NV-TUNG |
| Số ca bị ùn | Report `lab10.eval` (số ca bị ùn) | 0 | 1 ca → kiểm lại hàng chờ, chuyển ca ùn cho người trực tay ngay | ≥ 2 ca trong một giờ → thu hẹp `pilot_scope`, giữ 1 người duyệt + 1 người dự phòng | NV-TUNG |
| Chi phí mỗi ticket so với làm tay | Report `lab10.eval` (chi phí mỗi ticket, ROI) | < 10.000đ (làm tay) | ≥ 8.000đ → xem lại tỉ lệ chuyển người và số người trực | ≥ 10.000đ hoặc ROI dưới `roi_min` → đề xuất Thu hẹp ở lần quyết định tới | NV-TUNG, với ý kiến của NV-OANH |
| Tổng tiền hoàn tự động trong ngày so với trần | Report `lab10.eval` (tổng tiền hoàn so với trần) | < 80% của 2.000.000đ | ≥ 1.600.000đ → báo NV-HANH chuẩn bị duyệt tay | Chạm 2.000.000đ (`daily_auto_refund_budget_vnd`) → ngừng hoàn tự động tới hết ngày (điều kiện dừng 5) | NV-TUNG |
| Tiền hoàn sai | Report `lab10.eval` (hoàn sai, đ) | 0đ | (không có vàng) | ≥ 1 khoản → tắt `issue_refund` (điều kiện dừng 3) | NV-TUNG |
| Lỗi ghi oan cho hãng / lộ dữ liệu cá nhân (pháp lý) | Report `lab10.eval` (lỗi hãng oan, lộ dữ liệu); sự kiện `legal_gate` trong trace | 0 | Một hãng đạt 2 lỗi tự động trong ngày → NV-OANH soát lại tay | ≥ 1 lỗi oan → tắt `file_carrier_fault` + `notify_carrier`; ≥ 1 lần lộ dữ liệu → tắt `notify_carrier` (điều kiện dừng 1, 2) | NV-TUNG |
| Số lỗi tự động 7 ngày của mỗi hãng (tín hiệu riêng của bàn) | `lab10/monitors.py` (thêm ở vòng 2) + sổ lỗi hãng | Dưới mức đình chỉ − 1 | Còn cách mức đình chỉ 1 lỗi (GHSH, DNB: 2/3) → mọi lỗi mới của hãng đó chuyển NV-HANH duyệt | Chạm mức đình chỉ mà có lỗi chưa có nguyên nhân trong tracking → tắt `file_carrier_fault` | NV-TUNG |

#### Runbook 3 · Điều kiện dừng và cách dừng

- Dừng một phần (tắt một thao tác ghi, thu hẹp phạm vi) khi: có 1 lỗi ghi oan cho hãng (tắt `file_carrier_fault` + `notify_carrier`);
  có 1 thông báo gửi hãng lộ dữ liệu cá nhân (tắt `notify_carrier`); có ca chờ người duyệt > 60 phút trong 2 giờ liên tiếp (thu hẹp
  `pilot_scope` về một kho); tổng hoàn tự động chạm 2.000.000đ (ngừng hoàn tự động tới hết ngày). Năm câu này chính là
  `operations.stop_conditions`.
- Dừng hẳn khi: có 1 khoản hoàn sai tiền hoặc dùng phê duyệt không hợp lệ (tắt `issue_refund`; không còn hoàn tự động thì trợ lý
  không còn tác dụng), hoặc trong cùng một ngày có từ hai loại tín hiệu đỏ pháp lý trở lên (lỗi oan + lộ dữ liệu).
- Cách dừng, từng bước: (1) NV-TUNG đổi công tắc tương ứng trong `config/switches.json` sang `"off"` (dừng hẳn: cả bốn
  `issue_refund`, `file_carrier_fault`, `notify_carrier`, `send_reply`); (2) nếu là thu hẹp, đổi `business.pilot_scope` trong
  `config/operating_gates.json` sang `{"mode": "warehouse", "warehouses": ["<kho ít ca ùn nhất>"]}`; (3) báo vào
  `#logix-refund-pilot-canh-bao`: tín hiệu nào, lúc nào, đã tắt gì; (4) NV-OANH đánh dấu các dòng sổ cái và lỗi hãng của ngày đó để soát lại.
- Từ tín hiệu đỏ đến lúc dừng xong tối đa **15** phút; người bấm: **NV-TUNG (Lê Thanh Tùng)**; vắng thì NV-HANH bấm thay.
- Khi đã dừng, ticket đang chờ đi đâu, ai xử lý: mọi ticket đang chờ và ticket mới chuyển sang hàng chờ làm tay của CSKH; NV-HANH
  chia việc, vẫn giữ hạn nhận 60 phút. Lỗi hãng đã ghi trong ngày bị giữ lại, NV-OANH soát với tracking trước khi gửi hãng.
- Điều kiện để bật lại, ai ký: đã tìm ra nguyên nhân và có cổng sửa; chạy lại bộ nền và gói sự cố thấy hoàn sai = 0đ, lỗi oan = 0,
  lộ dữ liệu = 0 và không có ca nào trước đúng nay hỏng; NV-TUNG ký bật lại, NV-HANH xác nhận hàng chờ đã hết ùn.

### B7.6 · Giờ cao điểm (bắt buộc với thẻ S4; các thẻ khác nên có)

Lượng ticket có thể dồn gấp ba trong một giờ (ngày sale, sau bão). Viết trước, khi chưa biết sự cố.

| Câu hỏi | Trả lời (có số, có tên) |
|---|---|
| Giờ cao điểm là khi nào, bao nhiêu ticket mỗi giờ (dựa vào `ops_facts`)? | Ngày sale và ngày sau bão. Bộ nền có 22 ticket/ca 480 phút, khoảng 3 ticket/giờ; cao điểm gấp 3 là khoảng 9 ticket/giờ. Với khoảng 1/4 số ticket phải chuyển người (5/22 ca `escalated` trong nhãn bộ nền) cộng 10% kiểm mẫu, người duyệt nhận khoảng 3 ca/giờ, dưới sức 6 ca/giờ. Nếu tỉ lệ chuyển người thật cao hơn (trên 2/3 số ticket) thì 1 người không đủ |
| Ai trực giờ cao điểm, mấy người (khớp `operations.reviewers_on_shift`)? | NV-HANH trực duyệt, **1 người** (`reviewers_on_shift = 1`, `review_capacity_per_hour = 6`). Một người CSKH đứng dự phòng, chỉ gọi khi chạm ngưỡng vàng. Bật `decision_note = true` để mỗi lần kiểm lại chỉ tốn 4 phút thay cho 10 phút |
| Ngưỡng nào thì **gọi thêm người** (hàng chờ bao nhiêu ca, chờ lâu nhất bao nhiêu phút)? Ai gọi? | Hàng chờ ≥ 6 ca (bằng 1 giờ việc của 1 người) hoặc có ca đã chờ ≥ 40 phút → NV-TUNG gọi người dự phòng; vòng sau tăng `reviewers_on_shift` lên 2 nếu xảy ra 2 ngày liền |
| Ngưỡng nào thì **thu hẹp** phạm vi (khoá `business.pilot_scope`) hoặc **tắt** một thao tác ghi (`config/switches.json`)? Ai quyết? | Có ca chờ > 60 phút (`max_queue_wait_minutes`) dù đã có 2 người → NV-TUNG thu hẹp `pilot_scope` về một kho tới hết ngày. Một hãng nhận 2 lỗi tự động trong ngày giờ cao điểm → lỗi tiếp theo của hãng đó chuyển người (`max_auto_strikes_per_carrier_per_day = 2`). Có lỗi oan hoặc lộ dữ liệu → tắt `file_carrier_fault` / `notify_carrier` ngay, không chờ hết giờ cao điểm |
| Thêm người thì chi phí mỗi ticket và ROI thay đổi thế nào (đọc report)? | Mỗi người trực thêm tốn 30.000đ phí giữ chỗ/ca (`reviewer_standby_fee_vnd`). Với 22 ticket/ca, chi phí tăng khoảng 1.364đ/ticket; với 66 ticket/ca (gấp 3), tăng khoảng 455đ/ticket. Vẫn dưới 10.000đ làm tay nếu chi phí máy và chuyển người giữ dưới khoảng 8.500đ. Số thật đọc ở khối "kinh doanh và vận hành" sau khi chạy `--stage after` với `reviewers_on_shift = 2` |

---

<a id="b8"></a>

## B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 (phút 105–115)

Làm đúng thứ tự:

```bash
python3 -m lab10.checkpoint
python3 -m lab10.eval --suite base --stage prepared
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

**Khung tư duy.** Gate 1 "đạt" khi **quyết định khớp bằng chứng và khớp tiêu chí đã ký trước**. Tiếp tục, Thu hẹp, Cải tiến
thêm, Dừng đều có thể là quyết định đạt. Quyết định không đạt là quyết định mà con số trong report không đỡ được.
Chỉ chọn Tiếp tục khi mọi chỉ số bắt buộc đều đạt.

Ba câu tự vấn trước khi viết: (1) Rủi ro còn lại có chấp nhận được như hiện trạng không? (2) Cần thêm biện pháp nào, tốn
bao nhiêu thời gian? (3) Có phần nào của dự án không nên làm tiếp?

| | **v1** (phút 105–115, TRƯỚC khi nhận thẻ sự cố) |
|---|---|
| Commit ký tiêu chí (message `Sign acceptance criteria`; hash commit, tuỳ chọn) | |
| Hash chốt cổng vòng 1 (8 ký tự lệnh `lab10.checkpoint` in ra, tuỳ chọn) | |
| Mã lần chạy dùng làm bằng chứng | bộ nền, mốc base: ________ · bộ nền với cổng vòng 1 (prepared): ________ |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Đọc khối "theo kho và hãng" ở cuối output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | |
| Quyết định (khoanh một) | Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | |
| Bằng chứng 2 | |
| Bằng chứng 3 | |
| Khớp dòng nào trong `decision_rule` đã ký? | |
| Nếu Thu hẹp: cắt phần nào, vì sao | |
| Nếu Cải tiến thêm: giả thuyết cụ thể + hạn | |
| Nếu Dừng: bài học ghi lại | |
| Một bằng chứng còn thiếu (thứ bộ nền chưa đo được) | |
| Ngày quyết định lại (trừ khi Dừng) | |
| PIC ký | |

Xong v1 thì lưu và đẩy một bản (sau mốc này không sửa cột v1):

```bash
git add lab10/guards.py lab10/guards_round1.py config/operating_gates.json config/operating_gates.round1.json config/round1.lock templates/form-b-evaluation-gates.md
git commit -m "LAB 10: chốt cổng vòng 1, quyết định v1"
git push -u origin main
```
