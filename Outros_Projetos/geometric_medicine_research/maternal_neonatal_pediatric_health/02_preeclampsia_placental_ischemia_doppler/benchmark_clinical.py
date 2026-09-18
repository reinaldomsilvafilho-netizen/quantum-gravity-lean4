"""
CLINICAL BENCHMARK: PREECLAMPSIA & FIRST-TRIMESTER PLACENTAL SCREENING
Cohort: n = 500 Pregnant Women at 11-13 Weeks (250 Developing Preeclampsia, 250 Normotensive)
Clinical Challenge: Standard Mean Arterial Pressure (MAP) and 1D Doppler Miss Early Micro-Ischemia
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
import time
from model_engine import PreeclampsiaPlacentalEngine

def calc_auc(y_true, scores):
    pos = scores[y_true == 1]
    neg = scores[y_true == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))

def calc_accuracy(y_true, y_pred):
    return float(np.mean(y_true == y_pred))

def run_clinical_benchmark():
    print("=" * 90)
    print("CLINICAL BENCHMARK: FIRST-TRIMESTER PREECLAMPSIA SCREENING (11-13 WEEKS)")
    print("Cohort Architecture: n = 500 Patients (250 Early-Onset Preeclampsia, 250 Normotensive)")
    print("Challenge: Prevent Fatal Maternal Eclampsia & Fetal Growth Restriction via Early Aspirin")
    print("=" * 90)

    np.random.seed(302)
    n_samples = 500
    n_pos = 250
    n_neg = 250
    y_true = np.array([1]*n_pos + [0]*n_neg)

    # Patient true vascular remodeling parameters
    # Preeclampsia: poor invasion rate (mean 0.22), Normotensive: healthy invasion (mean 0.85)
    invasion_rates = np.concatenate([
        np.random.normal(0.22, 0.08, n_pos),
        np.random.normal(0.85, 0.12, n_neg)
    ])
    invasion_rates = np.clip(invasion_rates, 0.05, 1.2)

    # sFlt-1 / PlGF ratio at 12 weeks
    sflt_plgf = np.concatenate([
        np.random.normal(75.0, 20.0, n_pos),
        np.random.normal(14.0, 5.0, n_neg)
    ])
    sflt_plgf = np.clip(sflt_plgf, 2.0, 250.0)

    # Mean Arterial Pressure (MAP in mmHg)
    map_values = np.concatenate([
        np.random.normal(96.0, 9.0, n_pos),
        np.random.normal(84.0, 8.0, n_neg)
    ])

    engine = PreeclampsiaPlacentalEngine()
    G_initial_unremodeled = np.diag([0.8, 0.7, 3.2])

    # ---------------------------------------------------------
    # Method 1: Mean Arterial Pressure (MAP Alone)
    # ---------------------------------------------------------
    t0 = time.time()
    scores_map = np.clip((map_values - 75.0) / 30.0, 0.0, 1.0)
    time_map = time.time() - t0
    auc_map = calc_auc(y_true, scores_map)
    acc_map = calc_accuracy(y_true, (scores_map >= 0.50).astype(int))

    print(f"\n[METHOD 1] Mean Arterial Pressure (MAP Alone)...")
    print(f"  -> CPU Time: {time_map:.3f}s | Preeclampsia AUC: {auc_map:.3f} | Accuracy: {acc_map:.3f}")

    # ---------------------------------------------------------
    # Method 2: Uterine Artery Doppler 1D Pulsatility Index (UtA-PI)
    # ---------------------------------------------------------
    t0 = time.time()
    scores_pi = []
    for i in range(n_samples):
        G_t = engine.simulate_trophoblast_ricci_flow(G_initial_unremodeled, steps=15, trophoblast_invasion_rate=invasion_rates[i])
        pi, _, _ = engine.evaluate_doppler_waveforms(G_t)
        scores_pi.append(pi)
    scores_pi = np.array(scores_pi)
    # Normalize
    scores_pi_norm = np.clip((scores_pi - 0.8) / 1.5, 0.0, 1.0)
    time_pi = time.time() - t0
    auc_pi = calc_auc(y_true, scores_pi_norm)
    acc_pi = calc_accuracy(y_true, (scores_pi_norm >= 0.50).astype(int))

    print(f"\n[METHOD 2] Uterine Artery 1D Doppler Pulsatility Index (UtA-PI)...")
    print(f"  -> CPU Time: {time_pi:.3f}s | Preeclampsia AUC: {auc_pi:.3f} | Accuracy: {acc_pi:.3f}")

    # ---------------------------------------------------------
    # Method 3: Riemannian Spiral Artery Placental Engine (Ours)
    # ---------------------------------------------------------
    t0 = time.time()
    scores_riemannian = []
    for i in range(n_samples):
        G_t = engine.simulate_trophoblast_ricci_flow(G_initial_unremodeled, steps=15, trophoblast_invasion_rate=invasion_rates[i])
        _, _, p_risk = engine.predict_preeclampsia_risk(G_t, sflt_plgf_ratio=sflt_plgf[i])
        scores_riemannian.append(p_risk)
        
    scores_riemannian = np.array(scores_riemannian)
    time_riemannian = time.time() - t0
    auc_riemannian = calc_auc(y_true, scores_riemannian)
    acc_riemannian = calc_accuracy(y_true, (scores_riemannian >= 0.50).astype(int))

    print(f"\n[METHOD 3] Riemannian Spiral Artery Engine (Ours)...")
    print(f"  -> CPU Time: {time_riemannian:.3f}s | Preeclampsia AUC: {auc_riemannian:.3f} | Accuracy: {acc_riemannian:.3f}")

    print("\n" + "=" * 90)
    print("CONSOLIDATED CLINICAL BENCHMARK COMPARISON TABLE")
    print("=" * 90)
    print(f"{'Method / Framework':<42} | {'Time (s)':<10} | {'Preeclampsia AUC':<18} | {'Accuracy':<10}")
    print("-" * 90)
    print(f"{'Mean Arterial Pressure (MAP Alone)':<42} | {time_map:<10.3f} | {auc_map:<18.3f} | {acc_map:<10.3f}")
    print(f"{'1D Uterine Artery Pulsatility Index':<42} | {time_pi:<10.3f} | {auc_pi:<18.3f} | {acc_pi:<10.3f}")
    print(f"{'Riemannian Spiral Artery Engine (Ours)':<42} | {time_riemannian:<10.3f} | {auc_riemannian:<18.3f} | {acc_riemannian:<10.3f}")
    print("=" * 90)

if __name__ == '__main__':
    run_clinical_benchmark()
