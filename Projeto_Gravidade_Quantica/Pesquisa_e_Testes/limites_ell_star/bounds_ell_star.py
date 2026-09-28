#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bounds_ell_star.py
===================

Coleta os limites experimentais atuais que restringem a escala livre
ell_star = 1/M_star de um modelo-brinquedo de gravidade quantica com dois
ramos:

  (I)  Isotropico:      omega^2 = k^2 (1 + ell_star^2 k^2)
       -> potencial estatico V(r) = -(GMm/r)(1 - exp(-r/ell_star))
          (Yukawa com forca alpha = -1 e alcance lambda = ell_star,
          equivalente a um ghost de spin-2 tipo Stelle de massa 1/ell_star).

  (II) Anisotropico (Horava-Lifshitz, z=3):
       omega^2 = k^2 + k^6 / M_star^4
       (sem desvio estatico de Newton em ordem dominante).

  (III) Hipotese opcional de universalidade: se o mesmo operador atua em
        fotons, ha violacao quadratica de Lorentz (n=2) para o ramo I e
        quartica (n=4) para o ramo II, com atraso de tempo proporcional a
        (E/M_star)^2 e (E/M_star)^4, respectivamente.

Este script:
  1. Codifica cada limite experimental com sua fonte (DOI, tabela/pagina).
  2. Converte cada limite para ell_star [m] e M_star [eV, GeV], usando duas
     rotas de calculo independentes (cross-check).
  3. Inclui um controle negativo: uma conversao mutada (potencia errada de
     E, ou fator de 2*pi errado) deve DIVERGIR do resultado correto -- o
     teste verifica isso explicitamente.
  4. Produz um grafico de exclusao fig_bounds_ell_star.pdf.

Convencao de unidades: hbar = c = 1 nas formulas de fisica de particulas;
todas as conversoes explicitas usam
    hbar*c = 197.327 MeV*fm = 1.97327e-7 eV*m
Nunca se usa G, apenas hbar*c, pois ell_star e M_star sao definidos via
hbar = c = 1 (ell_star = 1/M_star nessas unidades).

Nenhum numero e inventado: todo valor vem de uma fonte citada abaixo.
Onde a literatura nao fornece um numero diretamente comparavel, o campo
'nota' diz explicitamente "not found" ou explica a limitacao.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field
from typing import Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ---------------------------------------------------------------------------
# 1. Constantes fisicas e conversao de unidades
# ---------------------------------------------------------------------------

# hbar*c em eV*m (CODATA / PDG: hbar*c = 197.3269804 MeV*fm)
HBARC_MeV_fm = 197.3269804  # MeV * fm  (valor do PDG, consistente com o
                             # "197.327 MeV*fm" citado no enunciado)
HBARC_eV_m = HBARC_MeV_fm * 1.0e6 * 1.0e-15  # (MeV->eV) * (fm->m)
assert abs(HBARC_eV_m - 1.97327e-7) / 1.97327e-7 < 1e-5, "hbar*c fora do esperado"

EV_PER_GEV = 1.0e9

# Comprimento de Planck (CODATA 2018): 1.616255e-35 m.
# O enunciado pede eixo comecando em 1.6e-35 m; usamos o valor CODATA
# completo para a linha vertical marcada no grafico.
PLANCK_LENGTH_M = 1.616255e-35
PLANCK_LENGTH_AXIS_M = 1.6e-35  # extremo do eixo, conforme instrucao


# ---------------------------------------------------------------------------
# 2. Rotas de conversao (independentes, para permitir cross-check)
# ---------------------------------------------------------------------------

def mass_eV_to_length_m(mass_eV: float) -> float:
    """M_star [eV] -> ell_star [m], rota 1: ell_star = hbar*c / M_star."""
    return HBARC_eV_m / mass_eV


def length_m_to_mass_eV(length_m: float) -> float:
    """ell_star [m] -> M_star [eV], rota 1: M_star = hbar*c / ell_star."""
    return HBARC_eV_m / length_m


def length_m_to_mass_eV_route2(length_m: float) -> float:
    """
    Rota 2 (independente) para o mesmo numero: passa por comprimento em
    femtometros e massa em MeV antes de converter para eV, usando hbar*c em
    MeV*fm diretamente (evita reaproveitar a constante HBARC_eV_m ja
    convertida). Serve de cross-check numerico da rota 1.
    """
    length_fm = length_m * 1.0e15  # m -> fm
    mass_MeV = HBARC_MeV_fm / length_fm
    mass_eV = mass_MeV * 1.0e6
    return mass_eV


def yukawa_lambda_to_ell_star(lambda_m: float) -> float:
    """
    Ramo I -- identificacao direta do alcance de Yukawa lambda com ell_star:
    V(r) = -(GMm/r)(1 - exp(-r/ell_star)) e uma Yukawa com alpha=-1 e
    alcance lambda = ell_star (mesma escala do ghost massivo 1/ell_star).
    """
    return lambda_m


def dispersion_A4_to_ell_star_route1(A4_eV_minus2: float) -> float:
    """
    Ramo I, dispersao do graviton: omega^2 = k^2 + ell_star^2 k^4, ou seja,
    em unidades hbar=c=1, E^2 = p^2 + A_4 p^4 com A_4 = ell_star^2
    (unidades eV^-2, exatamente como tabulado pela LVK).

    Rota 1: eleva a raiz quadrada em unidades naturais (eV^-1) e so depois
    converte para metros multiplicando por hbar*c.
    """
    ell_star_natural_eVinv = math.sqrt(A4_eV_minus2)  # eV^-1
    return ell_star_natural_eVinv * HBARC_eV_m


def dispersion_A4_to_ell_star_route2(A4_eV_minus2: float) -> float:
    """
    Rota 2 (independente): primeiro converte o coeficiente A_4 [eV^-2] para
    m^2 multiplicando por (hbar*c)^2, e so depois tira a raiz quadrada.
    Mesma fisica, ordem de operacoes diferente -> cross-check numerico.
    """
    A4_m2 = A4_eV_minus2 * (HBARC_eV_m ** 2)  # eV^-2 -> m^2
    return math.sqrt(A4_m2)


def photon_liv_EQG_to_ell_star(E_QG_eV: float) -> float:
    """
    Ramo III (universalidade de fotons): identifica M_star com a escala de
    LIV fotonica E_QG,n extraida de GRBs, e converte para ell_star=1/M_star.
    """
    return mass_eV_to_length_m(E_QG_eV)


def gw_speed_bound_to_ell_star_branchI(delta_v_over_c: float, f_Hz: float) -> float:
    """
    Ramo I, cross-check fraco via velocidade de grupo do GW170817:
    omega^2 = k^2(1+ell_star^2 k^2)  =>  v_g/c - 1 ~ ell_star^2 k^2
    (k = 2*pi*f/c convertido para unidades naturais eV via k[eV] = 2*pi*f*hbar).
    ell_star < sqrt(delta_v_over_c) / k
    """
    hbar_eVs = 6.582119569e-16  # eV*s (CODATA)
    k_eV = 2.0 * math.pi * f_Hz * hbar_eVs  # p = hbar*omega, unidades eV
    ell_star_natural = math.sqrt(delta_v_over_c) / k_eV  # eV^-1
    return ell_star_natural * HBARC_eV_m


def gw_speed_bound_to_ell_star_branchII(delta_v_over_c: float, f_Hz: float) -> float:
    """
    Ramo II, cross-check fraco via velocidade de grupo do GW170817:
    omega^2 = k^2 + k^6/M_star^4 => v_g/c - 1 ~ 2*(k/M_star)^4
    (fator de ordem 1 tomado como 2, ver derivacao no README; usado apenas
    como estimativa de ordem de grandeza, nao como limite competitivo).
    M_star > k / (delta_v_over_c/2)^(1/4)
    """
    hbar_eVs = 6.582119569e-16
    k_eV = 2.0 * math.pi * f_Hz * hbar_eVs
    M_star_eV = k_eV / (delta_v_over_c / 2.0) ** 0.25
    return mass_eV_to_length_m(M_star_eV)


# ---------------------------------------------------------------------------
# 3. Controle negativo (mutacoes que DEVEM divergir do resultado correto)
# ---------------------------------------------------------------------------

def dispersion_A4_to_ell_star_MUTATED_wrong_power(A4_eV_minus2: float) -> float:
    """
    Mutacao proposital: usa ell_star = A_4 (potencia 1) em vez de
    ell_star = sqrt(A_4) (potencia 1/2). Formula fisicamente errada.
    """
    return A4_eV_minus2 * HBARC_eV_m  # ERRADO DE PROPOSITO


def gw_speed_bound_to_ell_star_branchI_MUTATED_missing_2pi(
    delta_v_over_c: float, f_Hz: float
) -> float:
    """
    Mutacao proposital: omite o fator 2*pi na conversao de frequencia f
    [Hz] para numero de onda angular k, usando k[eV] = f*hbar em vez de
    k[eV] = 2*pi*f*hbar. Formula fisicamente errada.
    """
    hbar_eVs = 6.582119569e-16
    k_eV_wrong = f_Hz * hbar_eVs  # falta o 2*pi
    ell_star_natural = math.sqrt(delta_v_over_c) / k_eV_wrong
    return ell_star_natural * HBARC_eV_m


def run_negative_controls() -> None:
    """
    Verifica que as formulas mutadas (fisicamente erradas) produzem um
    resultado detectavelmente DIFERENTE do resultado correto. Se a mutacao
    coincidisse com o resultado correto, o teste de controle negativo teria
    falhado em capturar o erro -- este assert garante que isso NAO acontece.
    """
    A4_test = 3.0e3  # eV^-2, ordem de grandeza do bound GWTC-3 A_4

    correct = dispersion_A4_to_ell_star_route1(A4_test)
    mutated = dispersion_A4_to_ell_star_MUTATED_wrong_power(A4_test)
    rel_diff = abs(correct - mutated) / correct
    assert rel_diff > 0.5, (
        "CONTROLE NEGATIVO FALHOU: a formula mutada (potencia errada) "
        "deveria divergir fortemente do resultado correto, mas nao divergiu."
    )
    print(f"[controle negativo 1] potencia errada em A_4: "
          f"correto={correct:.3e} m, mutado={mutated:.3e} m, "
          f"diferenca relativa={rel_diff:.3e} (OK, mutacao detectada)")

    dv = 3.0e-15
    f = 100.0
    correct2 = gw_speed_bound_to_ell_star_branchI(dv, f)
    mutated2 = gw_speed_bound_to_ell_star_branchI_MUTATED_missing_2pi(dv, f)
    rel_diff2 = abs(correct2 - mutated2) / correct2
    assert rel_diff2 > 0.5, (
        "CONTROLE NEGATIVO FALHOU: a formula mutada (2*pi ausente) "
        "deveria divergir fortemente do resultado correto, mas nao divergiu."
    )
    print(f"[controle negativo 2] fator 2*pi ausente: "
          f"correto={correct2:.3e} m, mutado={mutated2:.3e} m, "
          f"diferenca relativa={rel_diff2:.3e} (OK, mutacao detectada)")


def run_cross_checks() -> None:
    """Confere que as duas rotas independentes de conversao concordam."""
    # Yukawa lambda <-> M_star, ida e volta (rota massa <-> rota comprimento)
    lam = 38.6e-6  # m (Lee et al. 2020)
    M = length_m_to_mass_eV(lam)
    M2 = length_m_to_mass_eV_route2(lam)
    rel = abs(M - M2) / M
    assert rel < 1e-9, f"Cross-check de massa (rota 1 vs rota 2) falhou: {rel}"
    lam_back = mass_eV_to_length_m(M)
    rel2 = abs(lam_back - lam) / lam
    assert rel2 < 1e-9, f"Cross-check ida-e-volta comprimento->massa->comprimento falhou: {rel2}"
    print(f"[cross-check 1] Yukawa lambda={lam:.4e} m -> M_star rota1={M:.6e} eV, "
          f"rota2={M2:.6e} eV (diff rel={rel:.2e}); volta -> {lam_back:.4e} m (OK)")

    # A_4 (GWTC-3) por duas rotas de calculo diferentes
    A4 = 3.0e3  # eV^-2
    r1 = dispersion_A4_to_ell_star_route1(A4)
    r2 = dispersion_A4_to_ell_star_route2(A4)
    rel3 = abs(r1 - r2) / r1
    assert rel3 < 1e-9, f"Cross-check de A_4 (rota 1 vs rota 2) falhou: {rel3}"
    print(f"[cross-check 2] A_4={A4:.3e} eV^-2 -> ell_star rota1={r1:.6e} m, "
          f"rota2={r2:.6e} m (diff rel={rel3:.2e}) (OK)")


# ---------------------------------------------------------------------------
# 4. Base de dados dos limites experimentais (com fonte)
# ---------------------------------------------------------------------------

@dataclass
class Bound:
    label: str
    branch: str            # "I" ou "II"
    observable: str        # "yukawa", "dispersion_A4", "gw_speed", "photon_liv_n2", "photon_liv_n4"
    raw_value: float
    raw_units: str
    ell_star_bound_m: float = field(init=False)
    M_star_bound_eV: float = field(init=False)
    source: str = ""
    table_page: str = ""
    doi: str = ""
    note: str = ""

    def __post_init__(self):
        pass  # preenchido externamente apos a conversao, ver main()


bounds: list[Bound] = []

# --- Ramo I: desvios de Yukawa em curto alcance (balanca de torcao) -------

b = Bound(
    label="Eot-Wash (Lee et al. 2020)",
    branch="I",
    observable="yukawa",
    raw_value=38.6e-6,
    raw_units="m (lambda, 95% CL, |alpha|=1)",
    source="Lee, Adelberger, Cook, Fleischer, Heckel, PRL 124, 101101 (2020)",
    table_page="Abstract (limite headline); dados de alpha(lambda) na Fig. 3",
    doi="10.1103/PhysRevLett.124.101101",
    note="Verificado via Crossref: PRL 124, 101101, publicado 2020-03-10.",
)
bounds.append(b)

b = Bound(
    label="HUST torsion pendulum (Tan et al. 2020)",
    branch="I",
    observable="yukawa",
    raw_value=48e-6,
    raw_units="m (lambda, 95% CL, |alpha|=1)",
    source="Tan, Du, Dong, Yang et al., PRL 124, 051301 (2020)",
    table_page="Abstract (limite headline); curva alpha(lambda) na Fig. 4",
    doi="10.1103/PhysRevLett.124.051301",
    note="Verificado via Crossref: PRL 124, 051301, publicado 2020-02-05. "
         "Nao localizamos uma versao arXiv indexada para este artigo.",
)
bounds.append(b)

# --- Ramo I: dispersao modificada do graviton via LIGO/Virgo/KAGRA --------

b = Bound(
    label="LVK GWTC-3 modified dispersion (A_4, 43 eventos)",
    branch="I",
    observable="dispersion_A4",
    raw_value=0.30e4,  # eV^-2, ramo A>0 (nosso modelo tem A_4=+ell_star^2>0)
    raw_units="eV^-2 (|A_4|, 90% credible, A>0)",
    source="LIGO-Virgo-KAGRA Collaboration, 'Tests of general relativity with GWTC-3', "
           "Phys. Rev. D 112, 084080 (2025) [arXiv:2112.06861]",
    table_page="Tabela VII, coluna |A_4| (unidades [10^4] eV^2-alpha), pagina 24 do PDF do arXiv",
    doi="10.1103/PhysRevD.112.084080",
    note="Tabela VII lista alpha ate 4 apenas; nao ha entrada para alpha=6 "
         "(ramo II), ver nota correspondente abaixo.",
)
bounds.append(b)

# --- Cross-check fraco: velocidade de propagacao GW170817 -----------------

b = Bound(
    label="GW170817 speed bound (ramo I, cross-check fraco)",
    branch="I",
    observable="gw_speed",
    raw_value=3e-15,  # |delta v / c|, sub-luminal
    raw_units="adimensional, f~100 Hz",
    source="Abbott et al. (LIGO-Virgo + Fermi-GBM + INTEGRAL), "
           "'Gravitational Waves and Gamma-Rays from a Binary Neutron Star Merger: "
           "GW170817 and GRB 170817A', ApJL 848, L13 (2017)",
    table_page="Eq. (obtida de -3e-15 < (v_GW-c)/c < +7e-16), Secao 'Constraints', p.4",
    doi="10.3847/2041-8213/aa920c",
    note="Bound MUITO mais fraco que os anteriores para o ramo I (a frequencia "
         "de LIGO e extremamente baixa em unidades naturais); incluido apenas "
         "como cross-check de ordem de grandeza pedido no enunciado.",
)
bounds.append(b)

b = Bound(
    label="GW170817 speed bound (ramo II, proxy fraco)",
    branch="II",
    observable="gw_speed",
    raw_value=3e-15,
    raw_units="adimensional, f~100 Hz",
    source="Abbott et al., ApJL 848, L13 (2017) (mesmo dado acima, "
           "reinterpretado para o ramo II via omega^2=k^2+k^6/M_star^4)",
    table_page="idem",
    doi="10.3847/2041-8213/aa920c",
    note="Bound extremamente fraco (ell_star ~ 10^2 m); nao competitivo. "
         "Nao existe, ate onde verificamos, um limite direto de LVK para "
         "alpha=6 na parametrizacao de dispersao (Tabela VII de GWTC-3 para "
         "em alpha<=4 apenas) -- registrado como 'not found'.",
)
bounds.append(b)

# --- Ramo III (universalidade fotonica), usado como proxy para ambos ramos

b = Bound(
    label="LHAASO GRB 221009A, LIV quadratica n=2 (proxy ramo I)",
    branch="I",
    observable="photon_liv_n2",
    raw_value=6.9e11 * EV_PER_GEV,  # eV
    raw_units="eV (E_QG,2, 95% CL, sub-luminal)",
    source="LHAASO Collaboration, 'Stringent Tests of Lorentz Invariance Violation "
           "from LHAASO Observations of GRB 221009A', PRL 133, 071501 (2024) "
           "[arXiv:2402.06009]",
    table_page="Tabela I, linha E_QG,2 [10^11 GeV], pagina 6 do PDF do arXiv",
    doi="10.1103/PhysRevLett.133.071501",
    note="Valido SOMENTE sob a hipotese opcional de universalidade "
         "(mesmo operador atua em fotons). Bound MUITO mais forte que os "
         "de laboratorio porque sonda diretamente perto da escala de Planck.",
)
bounds.append(b)

b = Bound(
    label="Fermi-LAT GRBs, LIV quadratica n=2 (proxy ramo I, cross-check)",
    branch="I",
    observable="photon_liv_n2",
    raw_value=1.3e11 * EV_PER_GEV,  # eV
    raw_units="eV (E_QG,2, 95% CL, sub-luminal)",
    source="Vasileiou, Jacholkowska, Piron et al., 'Constraints on Lorentz "
           "Invariance Violation from Fermi-Large Area Telescope Observations "
           "of Gamma-Ray Bursts', Phys. Rev. D 87, 122001 (2013) [arXiv:1305.3463]",
    table_page="Resultados para GRB 090510 (texto principal / Tabela de resultados)",
    doi="10.1103/PhysRevD.87.122001",
    note="Mais fraco que o limite LHAASO 2024 (fator ~5), usado como cross-check "
         "independente do mesmo tipo de observavel.",
)
bounds.append(b)

b = Bound(
    label="Crab Nebula spectrum, LIV quartica n=4 (proxy ramo II, mecanismo distinto)",
    branch="II",
    observable="photon_liv_n4",
    raw_value=1.4e12 * EV_PER_GEV,  # eV, canal sub-luminal (supressao de chuveiro)
    raw_units="eV (E_QG,4-like, canal sub-luminal)",
    source="Satunin et al., 'New constraints on Lorentz Invariance violation "
           "from Crab Nebula spectrum beyond 100 TeV', Eur. Phys. J. C 79, 1011 (2019) "
           "[arXiv:1906.08221]",
    table_page="Resultados finais, canais de splitting/decay/shower (texto principal)",
    doi="10.1140/epjc/s10052-019-7520-y",
    note="CAVEAT IMPORTANTE: este limite vem de limiares de producao de pares / "
         "splitting de fotons em QED-LIV, NAO do atraso temporal (E/M_star)^4 "
         "assumido no enunciado. Mecanismo fisico diferente; ordem de grandeza "
         "apenas ilustrativa. Nao encontramos um limite n=4 dedicado de tempo-de-voo "
         "de GRBs com significancia estatistica robusta -- registrado como "
         "'not found' para o observavel exato pedido.",
)
bounds.append(b)


# ---------------------------------------------------------------------------
# 5. Preenche as conversoes
# ---------------------------------------------------------------------------

def fill_conversions(b: Bound) -> None:
    if b.observable == "yukawa":
        ell = yukawa_lambda_to_ell_star(b.raw_value)
        M = length_m_to_mass_eV(ell)
    elif b.observable == "dispersion_A4":
        ell = dispersion_A4_to_ell_star_route1(b.raw_value)
        ell_check = dispersion_A4_to_ell_star_route2(b.raw_value)
        assert abs(ell - ell_check) / ell < 1e-9
        M = length_m_to_mass_eV(ell)
    elif b.observable == "gw_speed":
        if b.branch == "I":
            ell = gw_speed_bound_to_ell_star_branchI(b.raw_value, 100.0)
        else:
            ell = gw_speed_bound_to_ell_star_branchII(b.raw_value, 100.0)
        M = length_m_to_mass_eV(ell)
    elif b.observable in ("photon_liv_n2", "photon_liv_n4"):
        ell = photon_liv_EQG_to_ell_star(b.raw_value)
        M = b.raw_value  # ja em eV
    else:
        raise ValueError(f"observavel desconhecido: {b.observable}")

    b.ell_star_bound_m = ell
    b.M_star_bound_eV = M


# ---------------------------------------------------------------------------
# 6. Grafico de exclusao
# ---------------------------------------------------------------------------

def make_plot(bounds: list[Bound], out_path: str) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 6.0))

    xmin, xmax = PLANCK_LENGTH_AXIS_M, 1e-3  # m, conforme enunciado

    branch_colors = {"I": "#2b6cb0", "II": "#c05621"}

    # ordena por bound (mais estringente/menor primeiro) para leitura vertical
    ordered = sorted(bounds, key=lambda b: b.ell_star_bound_m)

    y_positions = list(range(len(ordered)))
    labels = []

    for y, b in zip(y_positions, ordered):
        color = branch_colors[b.branch]
        # regiao excluida: ell_star > bound (ate a borda direita do grafico)
        left = b.ell_star_bound_m
        width = xmax - left
        if width > 0:
            rect = Rectangle(
                (left, y - 0.38), width, 0.76,
                facecolor=color, alpha=0.35, edgecolor=color, linewidth=1.2,
            )
            ax.add_patch(rect)
        ax.plot([b.ell_star_bound_m], [y], marker="|", color=color,
                 markersize=18, markeredgewidth=2.0)
        labels.append(f"{b.label} (ramo {b.branch})")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-0.7, len(ordered) - 0.3)

    ax.axvline(PLANCK_LENGTH_M, color="black", linestyle="--", linewidth=1.3)
    ax.text(PLANCK_LENGTH_M * 1.6, len(ordered) - 0.55,
             r"$\ell_P \approx 1.616\times10^{-35}\,$m",
             rotation=90, va="top", ha="left", fontsize=8)

    ax.set_xlabel(r"$\ell_\star$  [m]  (regiao sombreada = excluida por cada experimento)")
    ax.set_title(
        "Limites experimentais sobre a escala livre " r"$\ell_\star=1/M_\star$" "\n"
        "modelo-brinquete de gravidade quantica: ramo I (Yukawa/isotropico) "
        "vs ramo II (Horava z=3)",
        fontsize=10,
    )

    handles = [
        Rectangle((0, 0), 1, 1, facecolor=branch_colors["I"], alpha=0.35,
                  edgecolor=branch_colors["I"], label="Ramo I (isotropico)"),
        Rectangle((0, 0), 1, 1, facecolor=branch_colors["II"], alpha=0.35,
                  edgecolor=branch_colors["II"], label="Ramo II (Horava z=3)"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=8.5, framealpha=0.9)

    ax.grid(True, which="both", axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. Main
# ---------------------------------------------------------------------------

def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))

    print("=" * 78)
    print("Controles negativos (mutacoes devem DIVERGIR do resultado correto)")
    print("=" * 78)
    run_negative_controls()

    print()
    print("=" * 78)
    print("Cross-checks (duas rotas de conversao devem CONCORDAR)")
    print("=" * 78)
    run_cross_checks()

    print()
    print("=" * 78)
    print("Conversao de todos os limites da base de dados")
    print("=" * 78)
    for b in bounds:
        fill_conversions(b)
        M_GeV = b.M_star_bound_eV / EV_PER_GEV
        print(f"- {b.label} [ramo {b.branch}]")
        print(f"    bruto: {b.raw_value:.4e} {b.raw_units}")
        print(f"    ell_star < {b.ell_star_bound_m:.4e} m   "
              f"M_star > {b.M_star_bound_eV:.4e} eV = {M_GeV:.4e} GeV")
        print(f"    fonte: {b.source}")
        print(f"    DOI: {b.doi}")
        print()

    plot_path = os.path.join(here, "fig_bounds_ell_star.pdf")
    make_plot(bounds, plot_path)
    print(f"Grafico salvo em: {plot_path}")
    assert os.path.isfile(plot_path), "Falha ao gerar o grafico PDF"

    print()
    print("TODOS OS TESTES PASSARAM (controles negativos + cross-checks + grafico gerado).")


if __name__ == "__main__":
    main()
