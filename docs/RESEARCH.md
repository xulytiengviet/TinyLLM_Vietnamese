# TinyLLM Vietnamese — Phương pháp và kế hoạch nghiên cứu

**Tác giả:** Long Ngo · MIT chỉ cho phần mã viết mới. *Chưa có checkpoint tiếng Việt được kiểm chứng trên chip.*

## Giới thiệu và lịch sử
CVNSS4.0 là lớp biểu diễn có quy tắc của tiếng Việt (CQN→CVN→KHD). Oracle audit-safe 5.0.0 báo 758 dòng vần gốc, 336 patch entries, 56 nhóm đa nghĩa (gồm 5 va chạm trọng yếu). Đây là số kiểm toán codec, không phải thước đo chất lượng LM.

Tiền lệ:
- Ngducok/esp32s3-Super-mini-AI: 118.784 tham số INT8, vocab 128, Super Mini không PSRAM; tốc độ 9.33–20 tok/s là tác giả gốc công bố.
- slvDev/esp32-ai: 28,9M tham số lưu trữ, ~14,9MB INT4, 16MB Flash + 8MB PSRAM và TinyStories tiếng Anh, phần lớn tham số là bảng PLE.
- BitNet b1.58 (JMLR 2025): trọng số {-1,0,+1}, phương pháp huấn luyện chuyên biệt.

## Câu hỏi nghiên cứu
**RQ1:** CVNSS giảm bits per original Unicode byte hoặc cải thiện quality/compute không?
**RQ2:** Bộ giải mã theo ứng viên/bi-gram Viterbi giảm CER/WER so với canonical không?
**RQ3:** PLE flash-resident và embedding hybrid có hiệu quả với từ vựng CVNSS hay không?
**RQ4:** Ternary fake-quant và native packed ternary trên Xtensa LX7 có cải thiện năng lượng/câu đúng không?

## Data cần và đủ
Nguồn từng được ghi nhận *trong quá trình nghiên cứu trước*, **chưa đưa vào repo, chưa kiểm toán giấy phép**: VTB-50K (50.000 câu / 1.070.975 token), VTB (201.594 câu), VCor (17.095.994 câu), candidate CVNSS 500K (7.962.890 token). Đơn vị token cần đo lại với tokenizer mới. Tất cả phải có license/provenance, checksum, NFC, khử trùng lặp, split theo tài liệu, kiểm soát PII, CQN gốc và CVNSS version + ambiguity candidates.

## Phương pháp
Baseline PyTorch hiện có: char-level causal Transformer 3 layers, width 64, 4 heads, positional embeddings, tied head, AdamW. Tập sample chỉ là smoke. Thử nghiệm ternary hiện chỉ dùng STE cho feed-forward linear; **không phải BitNet b1.58 đầy đủ hoặc kernel trên ESP32**.

| Arm | Encoder/Token | Decoder | Đánh giá |
|---|---|---|---|
| E0 | Unicode char/byte | native | BPB, CER, intent |
| E1 | CVNSS-character | candidate aware | BPB, WER |
| E2 | CVNSS hybrid/BPE (TODO) | candidate aware | vocab/Flash |
| E3 | E2 + FST/Viterbi (TODO) | n-gram | WER/ambiguity |
| E4 | E3 + PLE (TODO) | native | SRAM/PSRAM/latency |
| E5 | E3 + ternary (STE smoke) | native after kernel | loss/energy |

Giữ seed, nguồn tài liệu, cùng ngân sách train/test, so sánh BPB theo byte của Unicode gốc; perplexity giữa tokenizer khác nhau không đối chiếu trực tiếp. Mục tiêu intent >=90% *chỉ trong miền hẹp và sau khi có held-out evaluation*, không phải kết quả đã đạt.

## Tiến trình
G0 khóa oracle → G1 data audit → G2 tokenizer A/B/C/D → G3 pretrain/distill → G4 INT8/INT4/ternary → G5 Python/WASM/C parity → G6 ESP-IDF hardware → G7 paper/release.

## Trách nhiệm kiểm chứng
Không lấy số tok/s, mJ/token, 384KB SRAM, 24.5KB KV của nguồn này đưa sang kiến trúc khác như thành tích riêng. Trình duyệt HTML chỉ mô phỏng tương tác lý thuyết; hệ thống chưa có firmware hoặc WASM inference.

## Tham khảo
1. https://github.com/xulytiengviet/CVNSS40_Tutor
2. https://github.com/Ngducok/esp32s3-Super-mini-AI
3. https://github.com/slvDev/esp32-ai
4. https://github.com/slvDev/esp32-ai/blob/main/RESULTS.md
5. https://jmlr.org/beta/papers/v26/24-2050.html
6. https://arxiv.org/abs/2305.07759
7. https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/
