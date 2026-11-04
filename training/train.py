"""Run a PyTorch character-level baseline on CQN or preconverted CVNSS JSONL.
No firmware, inference runtime, or hardware benchmark is provided.
"""
import argparse,hashlib,json,random
from pathlib import Path
import torch
from torch.nn import functional as F
from model import TinyDecoder

def run(a):
    if min(a.steps,a.context,a.dim,a.layers,a.heads,a.batch,a.threads)<=0:
        raise ValueError("All sizes must be positive")
    torch.manual_seed(a.seed);random.seed(a.seed);torch.set_num_threads(a.threads)
    rows=[json.loads(line) for line in a.data.read_text(encoding="utf-8").splitlines() if line.strip()]
    train=[r[a.field] for r in rows if r["split"]=="train"]
    val=[r[a.field] for r in rows if r["split"]=="val"]
    if not train:raise ValueError("No training records")
    chars=sorted(set("\n".join(train)));stoi={"<unk>":0}
    stoi.update({c:i+1 for i,c in enumerate(chars)})
    def encode(lines):
        return torch.tensor([stoi.get(c,0) for c in "\n".join(lines)],dtype=torch.long)
    seq=encode(train)
    if len(seq)<3:raise ValueError("Need more training text")
    context=min(a.context,len(seq)-1)
    model=TinyDecoder(len(stoi),a.context,a.dim,a.layers,a.heads,a.ternary_ffn)
    optimizer=torch.optim.AdamW(model.parameters(),lr=a.lr)
    def sample(data):
        n=min(context,len(data)-1)
        if n<2:raise ValueError("Not enough validation text")
        ix=torch.randint(0,len(data)-n,(a.batch,))
        x=torch.stack([data[i:i+n] for i in ix])
        y=torch.stack([data[i+1:i+n+1] for i in ix])
        return x,y
    for step in range(a.steps):
        x,y=sample(seq)
        loss=F.cross_entropy(model(x).reshape(-1,len(stoi)),y.reshape(-1))
        optimizer.zero_grad(set_to_none=True);loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
        optimizer.step()
        if (step+1)%10==0 or step==a.steps-1:
            print("step",step+1,"train_loss",round(loss.item(),4),flush=True)
    val_loss=None
    if val and len(encode(val))>=3:
        model.eval()
        with torch.no_grad():
            x,y=sample(encode(val))
            val_loss=F.cross_entropy(model(x).reshape(-1,len(stoi)),y.reshape(-1)).item()
    a.output.mkdir(parents=True,exist_ok=True)
    config={"vocab":len(stoi),"context":a.context,"dim":a.dim,
       "layers":a.layers,"heads":a.heads,"ternary_ffn":a.ternary_ffn}
    torch.save({"state_dict":model.state_dict(),"config":config},a.output/"model.pt")
    (a.output/"vocab.json").write_text(json.dumps(stoi,ensure_ascii=False,indent=2),encoding="utf-8")
    metric={"status":"SMOKE_TEST_ONLY" if len(rows)<10000 else "UNVALIDATED_RESEARCH",
      "dataset_sha256":hashlib.sha256(a.data.read_bytes()).hexdigest(),
      "train_records":len(train),"validation_records":len(val),
      "model_parameters":sum(p.numel() for p in model.parameters()),
      "train_loss":loss.item(),"validation_loss":val_loss,
      "esp32s3_performance":"NOT_MEASURED"}
    (a.output/"metrics.json").write_text(json.dumps(metric,indent=2),encoding="utf-8")
    return metric

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data",type=Path,default=Path("artifacts/prepared.jsonl"))
    p.add_argument("--field",choices=["cqn","cvnss"],default="cvnss")
    p.add_argument("--steps",type=int,default=50)
    p.add_argument("--context",type=int,default=32)
    p.add_argument("--dim",type=int,default=64)
    p.add_argument("--layers",type=int,default=3)
    p.add_argument("--heads",type=int,default=4)
    p.add_argument("--batch",type=int,default=8)
    p.add_argument("--threads",type=int,default=2)
    p.add_argument("--lr",type=float,default=.001)
    p.add_argument("--seed",type=int,default=42)
    p.add_argument("--ternary-ffn",action="store_true")
    p.add_argument("--output",type=Path,default=Path("artifacts/smoke_model"))
    a=p.parse_args()
    print(json.dumps(run(a),ensure_ascii=False,indent=2))

if __name__=="__main__":main()
