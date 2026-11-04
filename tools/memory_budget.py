"""Theoretical weight-storage lower bound, NOT hardware benchmark."""
import argparse, json
def estimate(params, bits, flash_mib, reserve_mib):
    if params<=0 or bits<=0 or flash_mib<=0 or reserve_mib<0:
        raise ValueError("Invalid budgets")
    weights=params*bits/8/1048576
    available=flash_mib-reserve_mib
    return {"weight_lower_bound_mib":round(weights,5),
      "flash_available_assumed_mib":round(available,5),
      "raw_weights_fit":weights<=available,"status":"THEORETICAL_ONLY",
      "excluded":["scales","kernel","firmware","alignment","tokenizer","KV-cache","RAM"]}
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--params",type=int,default=118784)
    p.add_argument("--bits",type=float,default=8)
    p.add_argument("--flash-mib",type=float,default=4)
    p.add_argument("--reserve-mib",type=float,default=1.5)
    a=p.parse_args()
    print(json.dumps(estimate(a.params,a.bits,a.flash_mib,a.reserve_mib),indent=2))
