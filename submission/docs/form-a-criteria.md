# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-NoName-PoCtoPilotGate1 · **Người cầm bút chính:** Kiều Đình Văn, vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Trợ lý xử lý yêu cầu hoàn phí giao hàng trễ trong phạm vi chính sách, tracking và phê duyệt có thể kiểm chứng; mọi khoản hoàn và lỗi ghi cho hãng đều có căn cứ, còn ca không đủ căn cứ được chuyển người duyệt để bảo vệ khách, shop, hãng và LogiX.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): mỗi tuần, mọi dòng hoàn tiền
  trợ lý ghi vào sổ cái và mọi lỗi trợ lý ghi cho hãng đều đối chiếu được với dữ liệu gốc (độ trễ và `delay_cause` trong tracking,
  phê duyệt hợp lệ cho đúng ticket), nên chị không phải huỷ hay ghi bù khoản nào khi khớp sổ với hãng và shop. Một lỗi ghi oan là
  một khoản phạt hãng phải trả (GHSH 150.000đ/lỗi) mà chị phải gỡ tay (PRD v1.1 FM-04, FM-05, FM-08).
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): mọi ca trợ lý chuyển sang được chị nhận trong 60 phút
  (`ops_limits.review_sla_minutes`), số ca chuyển sang không vượt sức duyệt của ca trực (1 người × 6 ca/giờ, `ops_facts`), và mỗi
  ca có ghi chú giải thích để chị duyệt nhanh; không có khoản hoàn nào đi vòng qua phê duyệt của chị (PRD v1.1 FM-02).

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước *"Ghi lỗi cho hãng vận chuyển"* (`file_carrier_fault`) của trợ lý | Trợ lý ghi lỗi cho hãng vận chuyển (`file_carrier_fault`) và gửi thông báo cho hãng (`notify_carrier`): hai lệnh ghi gây hậu quả cho bên ngoài LogiX |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lượt trợ lý gọi `file_carrier_fault` khi dữ liệu tracking không ghi nhận nguyên nhân thuộc lỗi hãng (`unsupported_carrier_fault_rate`, đơn vị: %) | (1) Số lỗi trợ lý ghi cho hãng mà tracking **không** ghi nguyên nhân thuộc lỗi hãng, tính theo lỗi/ngày; (2) số lỗi tự động của **mỗi hãng** trong 7 ngày gần nhất; (3) số thông báo gửi hãng có chứa trường ngoài danh sách `carrier_notice_fields` (tên, số điện thoại, địa chỉ, chữ khách tự gõ), tính theo thông báo/ngày |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Lấy sự kiện gọi tool `file_carrier_fault` trong trace đối chiếu với trường `orders[].parcels[].delay_cause` và danh sách `policies[].fault_causes` trong `data/world.json` trên 22 ticket × 5 seed (110 lượt chạy). Nhãn đúng: Đối chiếu trực tiếp từ cơ sở dữ liệu tracking (nguồn sự thật). | Không có nhãn. Dùng tín hiệu thay nhãn: sổ lỗi hãng (`faults`) + `orders[].parcels[].delay_cause` trong tracking (nguồn sự thật do máy quét ở điểm phát tạo); hộp thư gửi đi (`outbound` của `notify_carrier`) so với `policies[].carrier_notice_fields`; hộp khiếu nại của hãng do chị Oanh (NV-OANH) gom mỗi tuần làm nhãn muộn. Lấy toàn bộ, không lấy mẫu |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `(Số lượt gọi file_carrier_fault mà delay_cause không thuộc fault_causes hoặc số ngày trễ < min_days_fee) / (Tổng số lượt gọi file_carrier_fault)`. Các ca không phát sinh lệnh gọi `file_carrier_fault` không đưa vào mẫu số và được đếm riêng. | (1) đếm lỗi trong ngày có `delay_cause` trống hoặc không thuộc `fault_causes` của chính sách đang hiệu lực; parcel không tìm thấy trong tracking tính là vi phạm, không bỏ khỏi mẫu. (2) với mỗi `carrier_id`: đếm lỗi tự động trong cửa sổ 7 ngày trượt, so với `carriers[].suspend_after_strikes_7d`. (3) đếm thông báo có khoá ngoài `order_id, parcel_id, district, delay_days`, chia cho tổng thông báo trong ngày |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Tính lại mỗi giờ trong ca, cộng dồn theo ngày và 7 ngày. **Vàng:** một hãng đạt 2 lỗi tự động trong ngày (`ops_limits.max_auto_strikes_per_carrier_per_day`), hoặc số lỗi 7 ngày của một hãng còn cách mức đình chỉ 1 lỗi (GHSH, DNB: 2/3). **Đỏ:** ≥ 1 lỗi ở thước đo (1), hoặc ≥ 1 thông báo ở thước đo (3), báo vào `#logix-refund-pilot-canh-bao`, NV-TUNG tắt thao tác ghi tương ứng trong 15 phút |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không thấy trường hợp hãng vận chuyển thực tế có lỗi nhưng trợ lý bỏ sót không gọi lệnh ghi lỗi (lỗi âm tính giả - False Negative). | Không thấy lỗi khi chính tracking ghi sai nguyên nhân (điểm phát quét sai, nhập bù tay); không thấy hãng nhỏ không khiếu nại (DNB là tài xế tự do, trả theo chuyến); không thấy số tiền hoàn sai cho khách (đã có `wrongful_refund_vnd_max` lo) |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: (a) · **(b)** · (c) · (d)

Giải thích một câu: Chưa đủ căn cứ kết luận Y tốt hơn X vì chênh lệch 1/50 lần chạy nằm trong khoảng tin cậy 95% của X ([0,9400; 1,0]).

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ lượt chạy đạt trên bộ nền và gói sự cố thấp hơn 0,95 (95%), chúng tôi sẽ không tiếp tục nguyên phạm vi; thu hẹp hoặc cải tiến và đánh giá lại. | Nếu dưới 0,98, chúng tôi sẽ thu hẹp pilot còn ticket/kho đã đạt cho tới khi đạt ngưỡng. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đạt cả 5 seed thấp hơn 0,90 (90%), chúng tôi sẽ không mở pilot toàn bộ; thu hẹp phạm vi và xử lý nhóm ticket không ổn định. | Nếu thấp hơn 0,95, chúng tôi sẽ giữ pilot ở phạm vi kiểm soát và cải tiến các ticket chưa ổn định. |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai lớn hơn 0 đồng trên bộ nền hoặc bất kỳ gói sự cố nào, chúng tôi sẽ dừng tự động hoàn cho phạm vi bị ảnh hưởng và yêu cầu người duyệt. | Nếu có bất kỳ khoản hoàn sai nào, chúng tôi sẽ dừng mọi hoàn tự động cho đến khi xác định và sửa nguyên nhân. |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng lớn hơn 0, chúng tôi sẽ tắt tự động ghi lỗi hãng và chuyển người xác minh. | Nếu có từ 1 lỗi oan trở lên, chúng tôi sẽ không tiếp tục ghi lỗi hãng tự động trong pilot. |
| `pii_leaks_max` | Nếu số lần lộ dữ liệu cá nhân lớn hơn 0, chúng tôi sẽ dừng gửi dữ liệu ra bên thứ ba và rà soát sự cố trước khi mở lại. | Nếu có bất kỳ lần lộ PII nào, chúng tôi sẽ dừng pilot cho tới khi có biện pháp ngăn tái diễn được xác minh. |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt vượt 0,35 (35%), chúng tôi sẽ thu hẹp phạm vi để không vượt sức xử lý ca trực. | Nếu vượt 0,30, chúng tôi sẽ tối ưu luồng và rà soát công suất trước khi mở rộng. |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không tự động hoàn khoản vượt hạn mức tự động của chính sách đang hiệu lực (100.000đ theo REFUND-v4); không xác nhận đã hoàn nếu lệnh ghi sổ bị từ chối.
- Ngưỡng chuyển cho người duyệt: Chuyển duyệt khi thiếu tracking/nguyên nhân trễ, chính sách hoặc phê duyệt hợp lệ; khi khoản vượt hạn mức tự động, tổng hoàn tự động cho khách vượt 300.000đ/ngày hoặc tổng ngân sách tự động 2.000.000đ/ngày.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: pass rate/pass-k đo độ tin cậy chung; ba ngưỡng an toàn bảo vệ khách, hãng và dữ liệu; chi phí, ROI, hàng chờ bảo vệ khả năng vận hành. Chỉ số tổng cần đọc kèm phân khúc theo kho/hãng. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ngưỡng tự động hóa quá cao có thể đẩy lỗi sang khách, hãng hoặc người duyệt; vì vậy an toàn không được đổi lấy pass rate, escalation là ngưỡng nên có, không phải mục tiêu phải giảm bằng mọi cách. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có, như cổng tối thiểu để cân nhắc pilot có phạm vi và người trực rõ ràng; không phải bằng chứng đủ cho triển khai rộng. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Viết lại pass rate/pass-k theo dữ liệu và phân khúc mới; cập nhật ngưỡng chi phí, ROI, tải hàng chờ, ngân sách và mọi ranh giới theo chính sách/địa bàn hiện hành. Không tự ý thay bộ tiêu chí đã ký của Gate 1. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **10.000đ** (bằng chi phí làm tay/ticket) · `roi_min` **0,20** · `queue_stuck_max` **0**.
- Ngày xem lại tiêu chí: **trước khi mở rộng pilot hoặc khi chính sách/chi phí/công suất vận hành thay đổi; chốt ngày cụ thể tại Phiếu B mục B8** · Ai dự: **Sản phẩm và kinh doanh, Vận hành và pháp lý, Kỹ sư cổng, đại diện Finance/Ops**.

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18 16:30:18 (giờ local máy ký) |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `b3a1b2e` |
| Đã push lên `origin main` thành công? | Có — `b3a1b2e` đã push lên `origin/main` |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
