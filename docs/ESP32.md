# ESP32-S3: kế hoạch triển khai (chưa có firmware)

Hai mục tiêu thiết bị khác nhau:
- **Super Mini 4MB Flash, không cần PSRAM**: dùng Micro model nhỏ (0.1–1M params chỉ là ngân sách đề xuất).
- **N16R8 16MB Flash + 8MB PSRAM**: nghiên cứu PLE. Mô hình 28.9M / 14.9MB của slvDev được huấn luyện tiếng Anh; không thể cho vừa 4MB.

## Các cổng thực hiện
1. Khóa model/tokenizer/codec manifest và SHA-256.
2. Implement exporter checkpoint → INT8/INT4 có header tensor, scales, endian, CRC, version; **chưa triển khai**.
3. Viết runtime C/C++/Rust để parity logits Python↔native và tối ưu Xtensa LX7; benchmark GEMV, memory bandwidth và unpack ternary.
4. Tạo ESP-IDF project, partition table theo board, trừ firmware, web assets, OTA khỏi Flash; đo SRAM khả dụng thay vì coi tổng 512KB là heap tự do.
5. Cố định KV-cache, chặn vượt context; thêm watchdog, CRC/model ABI validation.
6. Đo TTFT, p50/p95 ms/token, Unicode chars/s, peak heap, mJ/token bằng thiết bị đo; so sánh Wi-Fi bật và tắt.

**Không nạp** `artifacts/smoke_model/model.pt` lên ESP32-S3: file PyTorch chưa có firmware suy luận, chưa có định dạng deploy.

Giao diện `index.html` chỉ trình bày board 3D kiểu CSS, bài toán 27 ký hiệu/3 trit và bộ nhớ tính toán; không chạy ESP32 firmware, không giả lập silicon, không xuất benchmark tok/s.
