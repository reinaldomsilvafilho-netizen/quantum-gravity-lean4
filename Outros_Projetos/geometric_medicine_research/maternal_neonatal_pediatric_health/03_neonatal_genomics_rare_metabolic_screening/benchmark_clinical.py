"""
CLINICAL BENCHMARK: NEWBORN METABOLIC SCREENING & RARE INBORN ERRORS
Cohort: n = 600 Neonates at 48h (300 Confirmed IEMs, 300 Controls with Prematurity/TPN Confounders)
Clinical Challenge: Standard Univariate Cutoffs Produce High False-Positive Recall Rates
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
import time
from model_engine import NeonatalMetabolicSimplexEngine

def calc_auc(y_true, scores):
    pos = scores[y_true == 1]
    neg = scores[y_true == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))

def calc_accuracy(y_true, y_pred):
    return float(np.mean(y_true == y_pred))

def run_clinical_benchmark():
    print("=" * 90)
    print("CLINICAL BENCHMARK: RAPID 48-HOUR NEWBORN METABOLIC & GENOMIC SCREENING")
    print("Cohort Architecture: n = 600 Neonates (300 Confirmed IEMs, 300 Controls with Confounders)")
    print("Challenge: Eliminate False-Positive Recalls while Detecting Fatal Metabolic Decompensations")
    print("=" * 90)

    np.random.seed(303)
    n_samples = 600
    n_pos = 300
    n_neg = 300
    y_true = np.array([1]*n_pos + [0]*n_neg)

    engine = NeonatalMetabolicSimplexEngine()
    baseline = np.array([35.0, 18.0, 0.15, 0.10, 0.12, 0.15, 60.0, 75.0])

    # Generate synthetic patient DBS analyte matrices
    raw_data = []
    cadd_scores = []
    
    for i in range(n_samples):
        noise = np.random.normal(1.0, 0.15, 8)
        sample = baseline * noise
        is_iem = (y_true[i] == 1)
        
        if is_iem:
            # Substrate surge (e.g. C8 elevated 10x-50x, or Phe elevated)
            surge_idx = np.random.choice([3, 6]) # C8 or Phe
            sample[surge_idx] *= np.random.uniform(8.0, 40.0)
            cadd = np.random.uniform(0.70, 0.98)
        else:
            # Healthy or TPN/premature confounders (transient mild elevation of multiple amino acids)
            if np.random.rand() < 0.35: # Confounder
                sample *= np.random.uniform(1.8, 3.5) # Total TPN volume effect
            cadd = np.random.uniform(0.01, 0.25)
            
        raw_data.append(sample)
        cadd_scores.append(cadd)
        
    raw_data = np.array(raw_data)
    cadd_scores = np.array(cadd_scores)

    # ---------------------------------------------------------
    # Method 1: Standard Univariate Cutoff Thresholding
    # ---------------------------------------------------------
    t0 = time.time()
    # Simple C8 cutoff > 0.45 or Phe cutoff > 120
    scores_cutoff = np.maximum(raw_data[:, 3] / 2.0, raw_data[:, 6] / 150.0)
    scores_cutoff_norm = np.clip(scores_cutoff, 0.0, 1.0)
    time_cutoff = time.time() - t0
    auc_cutoff = calc_auc(y_true, scores_cutoff_norm)
    acc_cutoff = calc_accuracy(y_true, (scores_cutoff_norm >= 0.50).astype(int))

    print(f"\n[METHOD 1] Standard Univariate Cutoff Thresholding...")
    print(f"  -> CPU Time: {time_cutoff:.3f}s | IEM Detection AUC: {auc_cutoff:.3f} | Accuracy: {acc_cutoff:.3f}")

    # ---------------------------------------------------------
    # Method 2: Multivariate Percentile Ratio Scoring (CLIR-like)
    # ---------------------------------------------------------
    t0 = time.time()
    # Ratio C8/C10 and Phe/Tyr without simplex normalization
    r1 = raw_data[:, 3] / np.maximum(raw_data[:, 4], 1e-4)
    r2 = raw_data[:, 6] / np.maximum(raw_data[:, 7], 1e-4)
    scores_clir = np.clip((r1 / 4.0 + r2 / 1.5) / 3.0, 0.0, 1.0)
    time_clir = time.time() - t0
    auc_clir = calc_auc(y_true, scores_clir)
    acc_clir = calc_accuracy(y_true, (scores_clir >= 0.50).astype(int))

    print(f"\n[METHOD 2] Multivariate Analyte Ratio Scoring (CLIR-like)...")
    print(f"  -> CPU Time: {time_clir:.3f}s | IEM Detection AUC: {auc_clir:.3f} | Accuracy: {acc_clir:.3f}")

    # ---------------------------------------------------------
    # Method 3: Simplex Dirichlet-Barnes Genomic-Metabolomic Engine (Ours)
    # ---------------------------------------------------------
    t0 = time.time()
    scores_simplex = []
    for i in range(n_samples):
        res = engine.fuse_genomic_metabolomic_evidence(raw_data[i], genomic_pathogenicity_score=cadd_scores[i])
        scores_simplex.append(res['prob_iem'])
        
    scores_simplex = np.array(scores_simplex)
    time_simplex = time.time() - t0
    auc_simplex = calc_auc(y_true, scores_simplex)
    acc_simplex = calc_accuracy(y_true, (scores_simplex >= 0.50).astype(int))

    print(f"\n[METHOD 3] Simplex Dirichlet-Barnes Engine (Ours)...")
    print(f"  -> CPU Time: {time_simplex:.3f}s | IEM Detection AUC: {auc_simplex:.3f} | Accuracy: {acc_simplex:.3f}")

    print("\n" + "=" * 90)
    print("CONSOLIDATED CLINICAL BENCHMARK COMPARISON TABLE")
    print("=" * 90)
    print(f"{'Method / Framework':<42} | {'Time (s)':<10} | {'IEM Detection AUC':<18} | {'Accuracy':<10}")
    print("-" * 90)
    print(f"{'Standard Univariate Cutoff Threshold':<42} | {time_cutoff:<10.3f} | {auc_cutoff:<18.3f} | {acc_cutoff:<10.3f}")
    print(f"{'Multivariate Ratio Scoring (CLIR-like)':<42} | {time_clir:<10.3f} | {auc_clir:<18.3f} | {acc_clir:<10.3f}")
    print(f"{'Simplex Dirichlet-Barnes Engine (Ours)':<42} | {time_simplex:<10.3f} | {auc_simplex:<18.3f} | {acc_simplex:<10.3f}")
    print("=" * 90)

if __name__ == '__main__':
    run_clinical_benchmark()
