import numpy as np

def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    expected_perc, _ = np.histogram(expected, bins=buckets)
    actual_perc, _ = np.histogram(actual, bins=buckets)

    expected_perc = expected_perc / np.maximum(expected_perc.sum(), 1)
    actual_perc = actual_perc / np.maximum(actual_perc.sum(), 1)

    psi = 0.0
    for e, a in zip(expected_perc, actual_perc):
        if e == 0 or a == 0:
            continue
        psi += (a - e) * np.log(a / e)
    return psi
