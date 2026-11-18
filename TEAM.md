# Team

## Thông tin nhóm

* Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): NoName
* Lớp: `L3A` / `L3B`
* Repo của bàn: [K5-L3A-DAY10-NoName-PoCtoPilotGate1](https://github.com/daokiencuong/K5-L3A-DAY10-NoName-PoCtoPilotGate1)
* Thẻ sự cố đã bốc (S1–S8):

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

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

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

- Mã commit: `33cdb03` (cổng: Phiếu A (1.3)).
- Dòng trong phiếu: Phiếu A (Mục A2 - Câu 1.3), Phiếu B (B0, B1, B2, B7.1–B7.3), Phiếu C (C0, C1, C2, C7, C8).

### Exit ticket

- Một điều học được: Các chốt chặn an toàn (guardrails) cấp hệ thống nằm ngoài mô hình ngôn ngữ đóng vai trò sống còn trong việc ngăn chặn các hành vi vượt rào (model override) và bảo vệ an toàn tài chính, pháp lý cho doanh nghiệp.
- Một điều còn chưa chắc: Làm thế nào để tối ưu hóa việc phân luồng giữa tự động hóa bằng guards và chuyển duyệt thủ công (escalation) để vừa đảm bảo an toàn vừa không làm quá tải đội ngũ vận hành trong các đợt cao điểm.

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
