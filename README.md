# TinyLLM Vietnamese · CVNSS4.0 × Base27 × Ternary × ESP32-S3

**Tác giả / Maintainer:** Long Ngo · **Giấy phép mã nguồn:** MIT · **Trạng thái:** research prototype / chưa có benchmark TinyLLM tiếng Việt trên ESP32-S3.

[📖 Website nghiên cứu (GitHub Pages)](https://xulytiengviet.github.io/TinyLLM_Vietnamese/) · [💬 Thảo luận](https://github.com/xulytiengviet/TinyLLM_Vietnamese/issues) · [CVNSS4.0 Knowledge Hub](https://github.com/xulytiengviet/CVNSS40_Tutor)

## Mục tiêu
Nghiên cứu mô hình ngôn ngữ siêu nhỏ chạy offline trên ESP32-S3. Kiểm chứng bốn biểu diễn **Unicode, byte/BPE, CVNSS4.0 character, CVNSS4.0 hybrid**; nghiên cứu **Base27 (27 ký hiệu ↔ 3 trit cân bằng)** và trọng số tam phân **{-1,0,+1}** trong một thí nghiệm độc lập. CVNSS4.0 không tự tạo bộ suy luận ternary; và ánh xạ 27 ký hiệu không tự chứng minh tiết kiệm Flash trên chip nhị phân.

## Phân biệt hai cấu hình
| Target | Nền tảng | Ngân sách |
|---|---|---|
| **Micro / ESP32-S3 Super Mini** | 4 MB Flash, không cần PSRAM | mô hình 0.1–1M tham số (mục tiêu); cần đo chính xác phân vùng |
| **PLE / ESP32-S3 N16R8** | 16 MB Flash, 8 MB PSRAM | tham khảo PLE 28.9M / 14.9 MB, **không** vừa Flash 4 MB |

Hai dự án tham chiếu là [Ngducok/esp32s3-Super-mini-AI](https://github.com/Ngducok/esp32s3-Super-mini-AI) (**118,784 tham số**, vocab 128) và [slvDev/esp32-ai](https://github.com/slvDev/esp32-ai) (**28.9M tham số lưu trữ, 25M PLE**, 16MB Flash + 8MB PSRAM). **Không được ghép thông số của hai dự án thành một cấu hình giả.** Các số tok/s trong tài liệu gốc là kết quả do tác giả nguồn công bố, không phải benchmark của repo này.

## Bắt đầu trên máy tính
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python tools/base27.py "ABCXYZ_"
python tools/memory_budget.py --params 118784 --bits 8 --flash-mib 4 --reserve-mib 1.5
python training/prepare_data.py --input data/example.jsonl --output artifacts/prepared.jsonl
python training/train.py --data artifacts/prepared.jsonl --field cvnss --steps 50 --device cpu
```
Dữ liệu `data/example.jsonl` chỉ là **smoke test**, tuyệt đối không phải tập huấn luyện đủ chất lượng. Cần corpus được cấp phép, hash và chia train/validation/test theo nguồn tài liệu trước khi công bố kết quả.

## Ranh giới đã thực hiện
- ✅ Website GitHub Pages tĩnh, diễn giải kiến trúc, bản đồ tiến trình, bảng dữ liệu, mô phỏng 27 ký hiệu–3 trit và bộ tính ngân sách bộ nhớ.
- ✅ Mã nguồn Python: quy đổi Base27/balanced ternary, chuẩn bị dữ liệu cặp CQN/CVNSS, tokenizer ký tự, Transformer decoder PyTorch mẫu, thí nghiệm fake-quant ternary, tính bộ nhớ, kiểm thử.
- 🧪 CVNSS4.0 dùng **oracle ngoài** hoặc corpus đã được xác minh; demo **không tự nhận** đã triển khai đầy đủ quy tắc CVNSS.
- 🧪 Ternary trong training là thử nghiệm *fake quantization* (straight-through estimator); chưa có kernel ESP32-S3, chưa phải BitNet b1.58 hoàn chỉnh.
- ⛔ Chưa có trọng số mô hình tiếng Việt đã được huấn luyện và đánh giá, chưa có firmware ESP-IDF hoặc kết quả đo trên chip. Không suy diễn từ animation website.

## Rủi ro dữ liệu và kiểm chứng
CVNSS4.0 oracle `5.0.0-audit-safe` hiện báo **56 nhóm đa nghĩa**, gồm 5 va chạm trọng yếu. Không ép `decode(encode(x)) = x` cho mọi đầu vào khi chưa giải quyết đa nghĩa; lưu cả CQN và CVNSS, nhãn/ứng viên và mã phiên bản. Kiểm chứng bằng CER/WER, bits/byte, chất lượng tác vụ và bộ nhớ thực.

## Cấu trúc
- `index.html`: site nghiên cứu + dashboard mô phỏng (static, offline nếu không mở liên kết ngoài).
- `training/`: làm sạch dữ liệu, huấn luyện language-model thử nghiệm, fake-quant ternary.
- `tools/base27.py`: ánh xạ minh hoạ 27 trạng thái thành 3 trit, không giả định là bảng chữ CVNSS chính thức.
- `tools/memory_budget.py`: ước tính lý thuyết, không thay thế đo trên board.
- `tests/`: kiểm thử đơn vị.
- `docs/`: nghiên cứu, triển khai và giới hạn.

## Giấy phép và ghi nhận
Mã nguồn **do dự án này tự viết** theo MIT © 2026 Long Ngo. Các dự án, mô hình, bộ dữ liệu và thư viện bên ngoài giữ nguyên giấy phép của tác giả; MIT của repository **không tự cấp phép lại** dữ liệu hoặc mã bên thứ ba. Xem [LICENSE](LICENSE).

## Tài liệu tham khảo
1. [Ngducok, ESP32-S3 Super Mini AI](https://github.com/Ngducok/esp32s3-Super-mini-AI).
2. [slvDev, ESP32 AI / PLE](https://github.com/slvDev/esp32-ai).
3. [BitNet b1.58, JMLR](https://jmlr.org/beta/papers/v26/24-2050.html).
4. [CVNSS40_Tutor](https://github.com/xulytiengviet/CVNSS40_Tutor).
5. [Espressif ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/).

## Kích hoạt website trên GitHub Pages (một lần)
Chủ repository cần vào **Settings → Pages → Build and deployment → Source → GitHub Actions → Save**.
Sau đó vào **Actions → Deploy TinyLLM Vietnamese website → Run workflow**.
Địa chỉ dự kiến: https://xulytiengviet.github.io/TinyLLM_Vietnamese/ .

Nếu Pages chưa bật, `actions/configure-pages@v5` báo `Get Pages site failed`; đó là lỗi thiết lập Pages chưa tạo, không phải lỗi website. Workflow GitHub Actions mặc định **không thể tự bật Pages** bằng GITHUB_TOKEN. Xem `docs/ESP32.md` và `docs/REPRODUCE.md` để tái lập mã Python.
