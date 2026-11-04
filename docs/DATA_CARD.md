# Data card — tập thử nghiệm

Repository mới chỉ có `data/example.jsonl` gồm ba câu từ các ví dụ chuyển đổi của oracle CVNSS4.0 5.0.0-audit-safe, tất cả đánh dấu `VERIFY_BEFORE_TRAIN`. Dữ liệu có tác dụng smoke test việc đọc JSONL, Unicode, splits, train loop.

Các corpus VTB, VCor, VTB-50K và candidate 500K **không** có trong repo và không được cấp phép lại bởi MIT. Nghiên cứu thật cần kiểm tra quyền dùng, trùng lặp, PII, provenance, phiên bản, nguồn/khối lượng, chất lượng nhãn và split không rò rỉ tài liệu.

Schema: id, cqn, cvnss, codec, source_id, license, ambiguity. Công cụ prepare_data.py gán split theo source_id và xuất SHA256. Oracle thực sự là phụ thuộc bên ngoài: script không tự tạo phép chuyển CQN↔CVNSS và không tuyên bố lossless cho trường hợp đa nghĩa.
