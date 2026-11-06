import torch
import pytest
from hc_kernels import squared_distances_reference, squared_distances_vectorized, gaussian_activations, ThreeRoundMessagePassing

@pytest.mark.parametrize('batch,k,d',[(1,8,4),(16,16,8),(64,32,16),(256,8,16),(64,16,4)])
@pytest.mark.parametrize('seed',[11,29,47])
def test_distance_and_gradient_equivalence(batch,k,d,seed):
    torch.manual_seed(seed)
    z0=torch.randn(batch,d); c0=torch.randn(k,d); p0=torch.nn.functional.softplus(torch.randn(k,d))+.2
    outputs=[]; grads=[]
    for fn in [squared_distances_reference,squared_distances_vectorized]:
        z=z0.clone().requires_grad_(True); c=c0.clone().requires_grad_(True); p=p0.clone().requires_grad_(True)
        out=fn(z,c,p); loss=(out.square().mean()+.17*out.mean())
        g=torch.autograd.grad(loss,(z,c,p))
        outputs.append(out.detach()); grads.append(g)
    assert torch.allclose(outputs[0],outputs[1],atol=1e-6,rtol=1e-6)
    for a,bv in zip(grads[0],grads[1]): assert torch.allclose(a,bv,atol=1e-6,rtol=1e-6)

@pytest.mark.parametrize('batch,k,d',[(1,8,4),(16,16,8),(64,32,16)])
def test_three_round_message_pass_shape_and_finite(batch,k,d):
    torch.manual_seed(100+batch+k+d)
    z=torch.randn(batch,d); c=torch.randn(k,d); p=torch.ones(k,d)
    d2=squared_distances_vectorized(z,c,p); phi=gaussian_activations(d2)
    rel=z[:,None,:]-c[None,:,:]; dist=torch.sqrt(d2.clamp_min(1e-12)); fp=torch.randn(k,d+7)
    model=ThreeRoundMessagePassing(d,k,d+7,seed=77)
    out=model(rel,dist,phi,fp)
    assert out.shape==(batch,k,16)
    assert torch.isfinite(out).all()

def test_vectorized_broadcast_exact_close_to_loop():
    from hc_kernels import squared_distances_vectorized_broadcast
    torch.manual_seed(919)
    z=torch.randn(64,16); c=torch.randn(32,16); p=torch.nn.functional.softplus(torch.randn(32,16))+.2
    a=squared_distances_reference(z,c,p); b=squared_distances_vectorized_broadcast(z,c,p)
    assert torch.allclose(a,b,atol=1e-6,rtol=1e-6)
