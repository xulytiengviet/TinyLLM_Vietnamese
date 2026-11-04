"""Tiny causal Transformer + optional FFN ternary STE (not BitNet b1.58)."""
import torch
from torch import nn
from torch.nn import functional as F

def ternary_ste(w):
    scale=w.detach().abs().mean().clamp_min(1e-6)
    q=torch.where(w>0.7*scale,1.0,torch.where(w<(-0.7*scale),-1.0,0.0))
    return w+(q*scale-w).detach()

class TernaryLinear(nn.Linear):
    def forward(self,x):
        return F.linear(x,ternary_ste(self.weight),self.bias)

class TinyDecoder(nn.Module):
    def __init__(self,vocab,context=32,dim=64,layers=3,heads=4,ternary_ffn=False):
        super().__init__()
        if dim%heads:raise ValueError("dim not divisible by heads")
        self.context=context
        self.emb=nn.Embedding(vocab,dim)
        self.pos=nn.Embedding(context,dim)
        block=nn.TransformerEncoderLayer(dim,heads,dim*4,dropout=0.0,
          batch_first=True,norm_first=True,activation="gelu")
        self.blocks=nn.TransformerEncoder(block,layers,enable_nested_tensor=False)
        self.norm=nn.LayerNorm(dim)
        self.out=nn.Linear(dim,vocab,bias=False)
        self.out.weight=self.emb.weight
        if ternary_ffn:
            for layer in self.blocks.layers:
                for name in ("linear1","linear2"):
                    old=getattr(layer,name)
                    new=TernaryLinear(old.in_features,old.out_features,
                       bias=old.bias is not None)
                    new.load_state_dict(old.state_dict())
                    setattr(layer,name,new)
    def forward(self,x):
        t=x.shape[1]
        if t>self.context:raise ValueError("Context exceeded")
        h=self.emb(x)+self.pos(torch.arange(t,device=x.device))[None,:,:]
        causal=torch.ones(t,t,device=x.device,dtype=torch.bool).triu(1)
        return self.out(self.norm(self.blocks(h,mask=causal)))
