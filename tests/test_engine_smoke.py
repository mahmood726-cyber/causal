"""Smoke tests for the CaMeA engine helpers and fail-closed contracts.

These avoid running MCMC sampling: they exercise the deterministic TruthCert
hash helper and the missing-anchor guard only, so they stay fast and offline.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# The engine imports PyMC/ArviZ; skip cleanly if the heavy stack is unavailable.
model_causal = pytest.importorskip("model_causal")


def test_truthcert_hash_is_deterministic_and_order_independent():
    a = {"location": "USA", "x": 1, "y": 2}
    b = {"y": 2, "x": 1, "location": "USA"}
    h1 = model_causal.generate_truthcert_hash(a)
    h2 = model_causal.generate_truthcert_hash(b)
    assert h1 == h2  # sort_keys=True makes hashing order-independent
    assert len(h1) == 64  # SHA-256 hex digest length
    assert model_causal.generate_truthcert_hash({"x": 1}) != h1


def test_missing_statin_anchor_fails_closed():
    bad_input = {
        "rct_anchors": [
            {"intervention": "Antihypertensive", "hr": 0.78,
             "lower_95": 0.72, "upper_95": 0.85},
        ],
        "observational_ihme": [
            {"location": "USA", "year": 2022, "dalys_cvd": 12000,
             "mortality_cvd": 900, "exposure_statin": 0.35},
        ],
        "confounders_wb": [
            {"location": "USA", "gdp_per_capita": 76000,
             "uhc_index": 85, "health_exp_pct": 16.6},
        ],
    }
    with pytest.raises(ValueError, match="Statin"):
        model_causal.run_causal_meta_analysis(bad_input)
