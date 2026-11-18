# Team

## Thông tin nhóm

* Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): NoName
* Lớp: `L3A` / `L3B`
* Repo của bàn: [K5-L3A-DAY10-NoName-PoCtoPilotGate1](https://github.com/daokiencuong/K5-L3A-DAY10-NoName-PoCtoPilotGate1)
* Thẻ sự cố đã bốc (S1–S8): S7

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên         | MSSV        | Vai                    | Trưởng nhóm |
| --: | ----------------- | ----------- | ---------------------- | :---------: |
|   1 | Đào Kiên Cường    | 2A202603396 | Vận hành và pháp lý    |      X      |
|   2 | Kiều Đình Văn     | 2A202603376 | Sản phẩm và kinh doanh |             |
|   3 | Nguyễn Thế Trường | 2A202603393 | Kỹ sư cổng             |             |
|   4 | Hoàng Bảo Nguyên  | 2A202603384 | Vận hành và pháp lý    |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Các mục dưới đây được tổng hợp từ phân vai, phiếu và lịch sử commit. Cả bàn đã dùng trợ lý AI để rà soát logic cổng và hoàn thiện câu chữ; mỗi thành viên cần đọc lại, chỉnh exit ticket theo trải nghiệm thật của mình trước khi nộp cá nhân.

## DaoKienCuong-2A202603396

### Phần việc phụ trách

- Vai trong bàn: Trưởng nhóm, Vận hành và pháp lý.
- Phụ trách điều phối hồ sơ cuối, kiểm sự cố S7, tổng hợp quyết định v2, điều kiện dừng và nội dung nộp.
- File/mục liên quan: Phiếu C C0–C2, C10–C12; `submission/submission.json`; `TEAM.md`.

### Đóng góp cụ thể

- Điều phối chạy lại grade S7 sau khi sửa; đối chiếu report với tiêu chí đã ký và ghi lại quyết định cùng điều kiện theo dõi pilot.
- Chốt cách chuyển thủ công các ticket thiếu mã đơn/kho và đầu mối xử lý khi có cảnh báo dữ liệu.

### Bằng chứng

- Commit hồ sơ nhóm: `a5385cd`; bài nộp/phiếu C: `73aac9c`; kết quả mới nhất được ghi tại Phiếu C và `submission/runs/`.

### Exit ticket

- Một điều học được: quyết định pilot phải đi cùng phạm vi cụ thể, người chịu trách nhiệm và hành động dừng có thời hạn.
- Một điều còn chưa chắc: dữ liệu mock chưa cho biết tải thật của nhóm ticket phải chuyển người trong giờ cao điểm.
- AI: trợ lý được dùng để rà soát cổng và câu chữ; phần exit ticket này là bản nháp tổng hợp, cần thành viên xác nhận/chỉnh lại.

## KieuDinhVan-2A202603376

### Phần việc phụ trách

- Vai trong bàn: Sản phẩm và kinh doanh.
- Phụ trách tiêu chí chấp nhận, chỉ số kinh doanh và giải thích quyết định theo ngưỡng đã ký.
- Phiếu & câu phụ trách: Phiếu A câu 1.1 và 1.6, ký tiêu chí ở A5; Phiếu B câu 2.3 (B3: bản đồ dữ liệu/drift), câu 2.9 (B7.4: cổng kinh doanh), phối hợp bằng chứng v1 ở B8; Phiếu C đọc chi phí/ROI/hàng chờ/phân khúc, ghi đánh giá kinh doanh ở C7 và bằng chứng cho v2 ở C12.
- File liên quan: `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`, `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`.

### Đóng góp cụ thể

- Đặt ngưỡng pass rate, pass-k, an toàn, chi phí, ROI và hàng chờ trước khi xem kết quả đánh giá.
- Ký tiêu chí chấp nhận trước lần đánh giá đầu tiên; xác minh hash chữ ký và không sửa tiêu chí sau khi ký.
- Lập bản đồ dữ liệu chính và nêu drift REFUND-v4 có hiệu lực ngày 2026-12-01, ảnh hưởng `auto_limit_vnd` và `fault_causes`.
- Đối chiếu chi phí theo phân khúc; đề xuất loại đơn thiếu dữ liệu khỏi phạm vi tự động hóa và chuyển xử lý thủ công.
- Đọc report S7: chi phí 5.005đ/ticket, ROI 1,0, hàng chờ ùn 0; kiến nghị giữ ngân sách và một người duyệt, đồng thời theo dõi riêng phân khúc kho `?` của bộ nền có chi phí 10.359đ/ticket.

### Bằng chứng

- Commit: `b3a1b2e` (ký tiêu chí), `4271a7f` (ghi nhận push chữ ký), `a4dc911` (bản đồ dữ liệu Phiếu B), `ffa5307` (bằng chứng kinh doanh S7).
- Mã run mới nhất: `R-S7-grade-20261118-214317-5c1125`; các chỉ số kinh doanh đạt, nhưng report tự kiểm tra còn FAIL integrity do các incident S1–S6/S8 lệch lock.
- Dòng trong phiếu: Phiếu A (A1, A4–A5), Phiếu B (B3, B7.4, B8), Phiếu C (C7, C12).

### Exit ticket

- Một điều học được: ngưỡng tổng thể có thể che khuất một phân khúc không có hiệu quả kinh tế, nên cần đọc cả số theo kho/hãng.
- Một điều còn chưa chắc: cần bao nhiêu tuần dữ liệu thật mới đủ để hiệu chỉnh ROI và ngưỡng chi phí theo từng kho.
- AI: Trợ lý hỗ trợ tổng hợp ngưỡng và số liệu từ config/report, rà soát tính nhất quán và biên tập câu chữ; số liệu được đối chiếu với report. Exit ticket là bản nháp, cần bạn đọc và chỉnh theo trải nghiệm thật trước khi nộp.

## NguyenTheTruong-2A202603393

### Phần việc phụ trách

- Vai trong bàn: Kỹ sư cổng.
- Phiếu & câu phụ trách:
  - Phiếu A: Câu 1.3 (Thiết kế offline metric cho bước gọi tool ghi lỗi hãng `file_carrier_fault`).
  - Phiếu B: Mục B0 (Nhật ký lần chạy vòng 1), Câu 2.1 (Mục B1: Lần chạy đầu tiên mốc base), Câu 2.2 (Mục B2: Soát lỗi ticket T-002@55), Câu 2.6 (Mục B7.1: Code 2–3 cổng bảo vệ trong `lab10/guards.py`), Câu 2.7 (Mục B7.2: Hai bước tránh rò rỉ dữ liệu), Câu 2.8 (Mục B7.3: Behavioral test và ticket hiểm).
  - Phiếu C: Câu 3.0 (Mục C0 & C1: Chạy grade đo mốc prepared), Câu 3.1 (Mục C2: Dò trace lỗi sự cố), Câu 3.5 (Mục C7: Sửa code cổng bảo vệ vòng 2), Câu 3.6 (Mục C8: Viết chỉ số giám sát mới trong `lab10/monitors.py`).
- File chính phụ trách: `lab10/guards.py`, `lab10/monitors.py`.

### Đóng góp cụ thể

- Thiết kế offline metric đo tỉ lệ ghi lỗi hãng không có căn cứ tracking (`unsupported_carrier_fault_rate`).
- Quản lý các lượt chạy đánh giá (baseline, after, prepared), dò vết trace lỗi model override và thiết kế cổng kiểm tra thực tế (ground truth) tại `write_gate` và `pre_guard`.
- Thực hiện các bài test hành vi (behavioral tests) đối kháng và xây dựng hàm telemetry giám sát sự cố trong `lab10/monitors.py`.

### Bằng chứng

- Mã commit: `33cdb03` (cổng: Phiếu A (1.3)), `0ba90f8` (LAB 10: chốt cổng vòng 1, quyết định v1), `73aac9c` (LAB 10: hoàn thành phiếu C, cổng vòng 2 sự cố S7 và bài nộp submission).
- Dòng trong phiếu: Phiếu A (Mục A2 - Câu 1.3), Phiếu B (B0, B1, B2, B7.1–B7.3), Phiếu C (C0, C1, C2, C7, C8, C9–C12).
- Sử dụng AI: Dùng trợ lý AI hỗ trợ rà soát câu chữ trong Phiếu B & C, kiểm tra logic các nhánh fault tree và tham khảo cấu trúc hàm monitor telemetry.

### Exit ticket

- Một điều học được: Các chốt chặn an toàn (guardrails) cấp hệ thống nằm ngoài mô hình ngôn ngữ đóng vai trò sống còn trong việc ngăn chặn các hành vi vượt rào (model override) và bảo vệ an toàn tài chính, pháp lý cho doanh nghiệp.
- Một điều còn chưa chắc: Làm thế nào để tối ưu hóa việc phân luồng giữa tự động hóa bằng guards và chuyển duyệt thủ công (escalation) để vừa đảm bảo an toàn vừa không làm quá tải đội ngũ vận hành trong các đợt cao điểm.
- AI: trợ lý được dùng để rà soát logic allow-list, monitor và câu chữ trong hồ sơ; thành viên xác nhận nội dung phản ánh đúng phần việc của mình.

## HoangBaoNguyen-2A202603384

### Phần việc phụ trách

- Vai trong bàn: Vận hành và pháp lý.
- Phụ trách mục tiêu của kế toán/trưởng ca, HAZOP và checklist rủi ro con người/pháp lý, cổng vận hành và runbook.
- File/mục liên quan: Phiếu A A1–A2; Phiếu B B4–B5, B7.5–B7.6; Phiếu C C4, C10–C11.

### Đóng góp cụ thể

- Ghi rõ PIC, approver, sức duyệt, ngưỡng hàng chờ, kênh cảnh báo và các bước dừng/tắt thao tác khi có sự cố.
- Đối chiếu phạm vi dữ liệu được gửi hãng với trường hợp người nhận quà không phải người đặt hàng.

### Bằng chứng

- Commit phân vai vận hành/pháp lý: `d621c11`; phần Phiếu A/B liên quan: `9c84fb0`; evidence chi tiết tại Phiếu B B4–B7.6 và Phiếu C C4/C11.

### Exit ticket

- Một điều học được: mỗi điều kiện dừng cần có người nhận cảnh báo, thao tác tắt rõ ràng và thời hạn thực hiện.
- Một điều còn chưa chắc: quy trình liên hệ người nhận quà bị ảnh hưởng cần được kiểm chứng với Pháp chế và kênh hỗ trợ thực tế.
- AI: trợ lý được dùng để rà soát logic và câu chữ; phần exit ticket này là bản nháp tổng hợp, cần thành viên xác nhận/chỉnh lại.
