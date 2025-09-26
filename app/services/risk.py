def score(cvss: float = 0, epss: float = 0, kev: bool = False, crit: int = 1) -> float:
    # weights: cvss, epss, KEV, asset criticality
    w1, w2, w3, w4 = 0.45, 0.25, 0.20, 0.10
    raw = (w1 * cvss) + (w2 * (epss * 10)) + (w3 * (10 if kev else 0)) + (w4 * (crit * 2))
    return max(0, min(100, raw * 2))  # normalize 0..100
