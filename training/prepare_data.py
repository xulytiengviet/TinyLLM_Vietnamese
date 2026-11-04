"""Prepare preconverted CQN/CVNSS JSONL pairs, never fake codec output."""
import argparse, hashlib, json, unicodedata
from pathlib import Path

def normalize(s):
    if not isinstance(s,str): raise ValueError("Expected string")
    return unicodedata.normalize("NFC",s).strip()

def split_of(source):
    bucket=int(hashlib.sha256(source.encode()).hexdigest()[:8],16)%100
    return "train" if bucket<80 else "val" if bucket<90 else "test"

def prepare(src,dst):
    output,seen,licenses=[],set(),set()
    for n,line in enumerate(src.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():continue
        row=json.loads(line)
        for key in ("cqn","cvnss","codec","source_id","license"):
            if not row.get(key):raise ValueError(f"line {n} missing {key}")
        cqn,cvnss=normalize(row["cqn"]),normalize(row["cvnss"])
        if not cqn or not cvnss:raise ValueError(f"line {n} empty")
        if (cqn,cvnss) in seen:continue
        seen.add((cqn,cvnss))
        licenses.add(str(row["license"]))
        output.append({"id":str(row.get("id",n)),"cqn":cqn,"cvnss":cvnss,
          "codec":row["codec"],"source_id":row["source_id"],
          "license":row["license"],"ambiguity":row.get("ambiguity","unverified"),
          "split":split_of(str(row["source_id"]))})
    if not output:raise ValueError("No usable pairs")
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in output),encoding="utf-8")
    manifest={"records":len(output),
      "split":{s:sum(r["split"]==s for r in output) for s in ("train","val","test")},
      "licenses":sorted(licenses),"sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),
      "status":"UNVERIFIED_EXAMPLE_ONLY",
      "warning":"No independent CVNSS oracle/rights verification performed"}
    dst.with_suffix(".manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    return manifest

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(prepare(a.input,a.output),ensure_ascii=False,indent=2))
