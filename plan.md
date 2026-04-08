# Implementation Plan: causal (Unified Causal Meta-Analysis)

## Objective
Implement a state-of-the-art **Causal Meta-Analysis (CaMeA)** framework to synthesize Cardiovascular Disease (CVD) data. This project integrates:
1. **Target Trial Emulation (TTE):** G-computation to harmonize RCTs (ct.gov) with observational data (IHME).
2. **Spatio-Temporal Gaussian Processes (ST-GPR):** Continuous spatial borrowing (Matern kernels) and temporal dynamics.
3. **Deep Probabilistic Causal Model (DPCM):** Hierarchical latent space capture for World Bank/WHO covariates.

## Data Ingestion (Open Access)
- **CT.gov:** Gold-standard CVD trial efficacy.
- **IHME:** Global Burden of Disease (GBD) - DALYs/Mortality.
- **World Bank:** Economic/Infrastructure covariates (e.g., GDP, UHC index).
- **WHO:** Regional policy and infectious/non-communicable disease (NCD) guidelines.

## Statistical Framework (PyMC 5.28.2)
- **Causal DAG:** $Outcome \sim G(Treatment, Covariates, GPR(Space, Time))$.
- **Spatial:** Gaussian Process with Matern 5/2 kernel for regional correlation.
- **Temporal:** Autoregressive temporal decay (AR1) or continuous GP.
- **Causal Inference:** Target trial emulation using Bayesian G-computation on the posterior predictive distribution.

## Deliverables
- **E156 Micro-Paper:** 7-sentence summary with **TruthCert** proof-carrying numbers.
- **GitHub Repository:** `causal` with full reproducible pipeline.
- **Interactive Dashboard:** High-quality visualization of the causal estimates.

## Verification
- **Trace Diagnostics:** MCMC convergence (R-hat < 1.05).
- **TruthCert:** SHA-256 evidence locators + hashes for all estimated effects.
- **Sensitivity:** Posterior predictive checks (PPCs) against known RCT values.
