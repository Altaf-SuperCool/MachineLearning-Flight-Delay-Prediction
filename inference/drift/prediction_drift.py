import numpy as np

def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    # Expand p to match q length
    if p.size == 1:
        p = np.repeat(p, q.size)

    p = p / max(p.sum(), 1e-9)
    q = q / max(q.sum(), 1e-9)

    mask = (p > 0) & (q > 0)
    return float(np.sum(p[mask] * np.log(p[mask] / q[mask])))
