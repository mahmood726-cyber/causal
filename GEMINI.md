# GEMINI.md — causal Research Pipeline Rules

## Purpose
Ship a state-of-the-art **Causal Meta-Analysis (CaMeA)** of Cardiovascular Disease (CVD) as an **E156 micro-paper + GitHub repo + interactive HTML dashboard**.

## Session Workflow
Before you use any tool or make changes, briefly say what you're about to do, then do it. After each tool call, summarize what you found and what's next.

## Statistical Framework: Unified Causal Meta-Analysis
- **Methods:** Bayesian G-computation + Spatio-Temporal Gaussian Processes (ST-GPR) + Deep Latent Factors.
- **Reference:** Berenfeld et al. (2025/2026) — CaMeA Framework.
- **Data:** IHME (Outcome), CT.gov (Anchor RCTs), World Bank (Confounders), WHO (Context).
- **Target Trial Emulation:** Estimate causal effects by emulating target trials on observational IHME data, benchmarked against gold-standard RCTs.

## Non-negotiables
1. **OA-only**: no paywalls.
2. **No secrets**: redact before logs.
3. **Memory ≠ evidence**: certified claims cite evidence hashes.
4. **Fail-closed**: if validation incomplete, REJECT + reasons.
5. **Determinism**: fixed seeds (seed=42), stable sorting.

## TruthCert (proof-carrying numbers)
- **Every number must be certified.**
- Evidence locator + hash + transformation + validator.

## Quality Loop
- **Fix ALL issues in one pass.**
- **Test after EACH change.**

## SHIP Ritual
1. Run full test suite.
2. Perform TruthCert audit.
3. Deploy HTML dashboard to GitHub Pages.
4. Update master `INDEX.md` and workbook.

## Platform Defaults
- Python-first (PyMC 5.28.2).
- Offline-first tests + fixtures.
