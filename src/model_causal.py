import json
import os
import hashlib
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az

def generate_truthcert_hash(data):
    """
    Generate a SHA-256 hash for data to satisfy TruthCert requirements.
    """
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def run_causal_meta_analysis(input_data):
    """
    Unified Causal Meta-Analysis (CaMeA) with Target Trial Emulation.
    Combines RCT Anchors + Observational G-computation + Spatio-Temporal Effects.
    """
    rcts = input_data['rct_anchors']
    obs = pd.DataFrame(input_data['observational_ihme'])
    wb = pd.DataFrame(input_data['confounders_wb'])
    
    # Merge Observational data with Confounders
    df = pd.merge(obs, wb, on="location")
    
    # Standardize covariates for DPCM stability
    df['gdp_log'] = np.log(df['gdp_per_capita'])
    df['uhc_z'] = (df['uhc_index'] - df['uhc_index'].mean()) / df['uhc_index'].std()
    
    # Extract RCT anchor for Statin (HR 0.81 -> logHR -0.21)
    statin_rct = [r for r in rcts if r['intervention'] == 'Statin'][0]
    log_hr_prior = np.log(statin_rct['hr'])
    log_hr_se = (np.log(statin_rct['upper_95']) - np.log(statin_rct['lower_95'])) / 3.92
    
    locations = df['location'].unique()
    loc_map = {name: i for i, name in enumerate(locations)}
    df['loc_idx'] = df['location'].map(loc_map)
    
    with pm.Model() as model:
        # 1. Causal Estimand (Statin effect anchored by RCT)
        # Using a prior anchored by the gold-standard RCT evidence
        beta_statin = pm.Normal("beta_statin", mu=log_hr_prior, sigma=log_hr_se)
        
        # 2. Confounder effects (World Bank covariates)
        beta_uhc = pm.Normal("beta_uhc", mu=0, sigma=1)
        beta_gdp = pm.Normal("beta_gdp", mu=0, sigma=1)
        
        # 3. Spatio-Temporal Latent Factor (Discrete proxy for GP for speed)
        tau_loc = pm.HalfNormal("tau_loc", sigma=0.5)
        delta_loc = pm.Normal("delta_loc", mu=0, sigma=tau_loc, shape=len(locations))
        
        # 4. Outcome model (Mortality)
        intercept = pm.Normal("intercept", mu=7, sigma=2)
        mu = intercept + \
             beta_statin * df['exposure_statin'].values + \
             beta_uhc * df['uhc_z'].values + \
             beta_gdp * df['gdp_log'].values + \
             delta_loc[df['loc_idx'].values]
        
        # Observed CVD mortality (log scale)
        pm.Normal("obs", mu=mu, sigma=0.1, observed=np.log(df['mortality_cvd'].values))
        
        # 5. Target Trial Emulation (G-computation)
        # Emulate a trial where exposure_statin is set to 1 (full coverage) vs 0 (no coverage)
        # Counterfactual: Full Coverage
        mu_cf1 = intercept + beta_statin * 1.0 + beta_uhc * df['uhc_z'].values + \
                 beta_gdp * df['gdp_log'].values + delta_loc[df['loc_idx'].values]
        # Counterfactual: No Coverage
        mu_cf0 = intercept + beta_statin * 0.0 + beta_uhc * df['uhc_z'].values + \
                 beta_gdp * df['gdp_log'].values + delta_loc[df['loc_idx'].values]
        
        causal_effect = pm.Deterministic("causal_effect", np.exp(mu_cf1 - mu_cf0))
        
        # Sampling
        print("Starting Causal MCMC sampling (CaMeA Framework)...")
        trace = pm.sample(200, tune=100, cores=1, chains=1, random_seed=42, progressbar=False)
    
    # Extract causal results
    results = []
    causal_posterior = trace.posterior['causal_effect'].values.reshape(-1, len(df))
    
    for i, row in df.iterrows():
        post = causal_posterior[:, i]
        results.append({
            "location": row['location'],
            "causal_effect_or": round(float(np.mean(post)), 4),
            "ci_low": round(float(np.percentile(post, 2.5)), 4),
            "ci_high": round(float(np.percentile(post, 97.5)), 4),
            "uhc_index": row['uhc_index'],
            "evidence_hash": generate_truthcert_hash(row.to_dict())
        })
    
    return results, generate_truthcert_hash(input_data)

def main():
    input_path = "causal/data/causal_synthesis_input.json"
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return
        
    with open(input_path, 'r') as f:
        input_data = json.load(f)
    
    results, input_hash = run_causal_meta_analysis(input_data)
    
    output = {
        "model": "CaMeA-TTE-v1.0",
        "description": "Causal Meta-Analysis with Target Trial Emulation (Berenfeld 2025/2026)",
        "results": results,
        "truthcert": {
            "input_hash": input_hash,
            "timestamp": "2026-04-08"
        }
    }
    
    output_path = "causal/output/causal_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)
    print(f"Causal Model execution complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()
