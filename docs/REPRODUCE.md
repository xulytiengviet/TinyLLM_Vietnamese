# Tái lập smoke test trên PC (không phải benchmark phần cứng)

Python >=3.10, torch >=2.3. Chạy từ thư mục gốc repo:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python tools/base27.py CVNSS_BASE27
python tools/memory_budget.py --params 28900000 --bits 4 --flash-mib 4 --reserve-mib 1
python training/prepare_data.py --input data/example.jsonl --output artifacts/prepared.jsonl
python training/train.py --data artifacts/prepared.jsonl --field cvnss --steps 20 --context 16
python training/train.py --data artifacts/prepared.jsonl --field cqn --steps 20 --context 16 --output artifacts/cqn_smoke
python training/train.py --data artifacts/prepared.jsonl --field cvnss --steps 20 --context 16 --ternary-ffn --output artifacts/ternary_smoke
```

Output: `artifacts/prepared.manifest.json` (sha/split), `artifacts/smoke_model/model.pt`, `vocab.json`, `metrics.json`. Tập dữ liệu minh họa chỉ gồm vài câu: train loss không phải bằng chứng về năng lực đối thoại tiếng Việt.

Khi nghiên cứu nghiêm túc phải có corpus được cấp phép, data card, nhiều seed, tokenizer ablation, CER/WER, bits/byte, parity Python-C-ESP32 và benchmark trên thiết bị thật.
