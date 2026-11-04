# Đối chiếu bản HTML NEON SIM tham chiếu

Người dùng cung cấp bản minh họa `ESP32-S3 · Vietnamese TinyLLM · NEON SIM v1.0` với bo mạch 3D Three.js, HUD neon và KPI chuyển động. Bản HTML đó sử dụng token ngẫu nhiên và số đo tok/s, latency lấy từ `Math.random()`, do đó **không thể dùng làm kết quả benchmark**.

Giao diện nghiên cứu hiện tại giữ ngôn ngữ thiết kế cyberpunk/neon và hình minh họa board 3D bằng CSS, nhưng thay KPI ngẫu nhiên bằng thông tin nguồn, mô phỏng Base27 ↔ balanced 3-trit và bộ tính ngân sách Flash có nhãn lý thuyết. Không khẳng định chạy firmware hoặc PLE trên trình duyệt.

Các thông số dễ nhầm:
- Micro Super Mini: nguồn Ngducok là 118.784 tham số, vocab 128, không PSRAM. Không phải PLE 28,9M.
- PLE 28,9M/14,9 MB của slvDev cần bo có 16MB Flash và 8MB PSRAM theo bản công bố, không vừa 4MB Flash.
- Phát biểu 'SIMD 128-bit' trong dự án khác phải kiểm tra kỹ thao tác SIMD và đo kiểm trên Xtensa; không được tự nhận bằng chứng phần cứng ở đây.
- 3 trit cân bằng ánh xạ 27 trạng thái, không đồng nghĩa bộ nhớ nhị phân 3 bit hoặc BitNet b1.58.

Việc tái lập trực tiếp firmware trên một emulator yêu cầu xác minh hỗ trợ kiến trúc, ngoại vi và mạng; website này chỉ là mô phỏng minh họa.
