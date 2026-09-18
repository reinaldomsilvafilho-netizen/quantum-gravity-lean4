"""
CLINICAL BENCHMARK: CHILDHOOD STUNTING & METAGENOMIC RISK INTERCEPTION
Cohort: n = 500 Infants at 12 Months (250 Severe Linear Stunting HAZ < -2 at 24m, 250 Healthy Growth)
Clinical Challenge: Anthropometric WAZ Scoring Fails to Detect Early Gut-Barrier Breakdown
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
import time
from model_engine import StuntingMicrobiomeEngine

def calc_auc(y_true, scores):
    pos = scores[y_true == 1]
    neg = scores[y_true == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))

def calc_accuracy(y_true, y_pred):
    return float(np.mean(y_true == y_pred))

def run_clinical_benchmark():
    print("=" * 90)
    print("CLINICAL BENCHMARK: CHILDHOOD STUNTING (HAZ < -2) & GUT-BRAIN IGF-1 PROJECTION")
    print("Cohort Architecture: n = 500 Infants Screened at 12 Months for 24-Month Outcome")
    print("Goal: Timely Metagenomic Interception before Irreversible Linear & Cognitive Deficits")
    print("=" * 90)

    np.random.seed(304)
    n_samples = 500
    n_pos = 250
    n_neg = 250
    y_true = np.array([1]*n_pos + [0]*n_neg)

    engine = StuntingMicrobiomeEngine()

    # Generate synthetic 12-month microbiome profiles
    samples = []
    waz_scores = [] # Weight-for-Age Z-scores
    shannon_scores = []
    
    for i in range(n_samples):
        is_stunted = (y_true[i] == 1)
        if is_stunted:
            # Shifted towards stunted basin with pathobiont elevation
            p_base = np.copy(engine.p_stunted_basin)
            p_base += np.random.uniform(0, 0.05, 10)
            p_sample = engine.project_to_simplex(p_base)
            waz = np.random.normal(-1.8, 0.7) # Modest lag at 12m
        else:
            p_base = np.copy(engine.p_healthy_basin)
            p_base += np.random.uniform(0, 0.05, 10)
            p_sample = engine.project_to_simplex(p_base)
            waz = np.random.normal(-0.2, 0.6)
            
        # Shannon diversity
        p_safe = np.maximum(p_sample, 1e-12)
        shannon = -np.sum(p_safe * np.log(p_safe))
        
        samples.append(p_sample)
        waz_scores.append(waz)
        shannon_scores.append(shannon)

    samples = np.array(samples)
    waz_scores = np.array(waz_scores)
    shannon_scores = np.array(shannon_scores)

    # ---------------------------------------------------------
    # Method 1: Weight-for-Age Z-Score (WAZ Alone)
    # ---------------------------------------------------------
    t0 = time.time()
    scores_waz = np.clip((-waz_scores - 0.5) / 2.0, 0.0, 1.0)
    time_waz = time.time() - t0
    auc_waz = calc_auc(y_true, scores_waz)
    acc_waz = calc_accuracy(y_true, (scores_waz >= 0.50).astype(int))

    print(f"\n[METHOD 1] Anthropometric Weight-for-Age Z-Score (WAZ Alone)...")
    print(f"  -> CPU Time: {time_waz:.3f}s | Stunting AUC: {auc_waz:.3f} | Accuracy: {acc_waz:.3f}")

    # ---------------------------------------------------------
    # Method 2: Ecological Shannon Alpha-Diversity Alone
    # ---------------------------------------------------------
    t0 = time.time()
    # Lower diversity correlates with dysbiosis
    scores_shannon = np.clip((2.2 - shannon_scores) / 1.0, 0.0, 1.0)
    time_shannon = time.time() - t0
    auc_shannon = calc_auc(y_true, scores_shannon)
    acc_shannon = calc_accuracy(y_true, (scores_shannon >= 0.50).astype(int))

    print(f"\n[METHOD 2] Ecological Shannon Alpha-Diversity Alone...")
    print(f"  -> CPU Time: {time_shannon:.3f}s | Stunting AUC: {auc_shannon:.3f} | Accuracy: {acc_shannon:.3f}")

    # ---------------------------------------------------------
    # Method 3: Simplicial Fractional Microbiome Engine (Ours)
    # ---------------------------------------------------------
    t0 = time.time()
    scores_simplex = []
    for i in range(n_samples):
        res = engine.predict_stunting_and_igf1(samples[i])
        scores_simplex.append(res['prob_stunting'])
        
    scores_simplex = np.array(scores_simplex)
    time_simplex = time.time() - t0
    auc_simplex = calc_auc(y_true, scores_simplex)
    acc_simplex = calc_accuracy(y_true, (scores_simplex >= 0.50).astype(int))

    print(f"\n[METHOD 3] Simplicial Fractional Microbiome Engine (Ours)...")
    print(f"  -> CPU Time: {time_simplex:.3f}s | Stunting AUC: {auc_simplex:.3f} | Accuracy: {acc_simplex:.3f}")

    print("\n" + "=" * 90)
    print("CONSOLIDATED CLINICAL BENCHMARK COMPARISON TABLE")
    print("=" * 90)
    print(f"{'Method / Framework':<42} | {'Time (s)':<10} | {'Stunting AUC':<18} | {'Accuracy':<10}")
    print("-" * 90)
    print(f"{'Anthropometric WAZ Monitoring':<42} | {time_waz:<10.3f} | {auc_waz:<18.3f} | {acc_waz:<10.3f}")
    print(f"{'Shannon Alpha-Diversity Alone':<42} | {time_shannon:<10.3f} | {auc_shannon:<18.3f} | {acc_shannon:<10.3f}")
    print(f"{'Simplicial Fractional Engine (Ours)':<42} | {time_simplex:<10.3f} | {auc_simplex:<18.3f} | {acc_simplex:<10.3f}")
    print("=" * 90)

if __name__ == '__main__':
    run_clinical_benchmark()
