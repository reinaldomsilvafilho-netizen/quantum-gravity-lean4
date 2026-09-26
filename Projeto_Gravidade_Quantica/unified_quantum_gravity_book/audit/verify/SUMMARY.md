# Verificação independente: consolidação da camada 1 (2026-09-24)

Verificadores: subagentes Claude com contexto limpo (mesmo modelo do corretor, contextos independentes), protocolo `PROTOCOL.md`. Relatórios completos: `chXX_blind.md`; scripts em `scripts/` (todos com controles negativos).

| Cap. | Itens | A | M | B | INCERTO | Achado novo |
|---|---|---|---|---|---|---|
| 7 | ~50 | 0 | 4 | 8 | 1 | F-37 |
| 9 | 30 | 0 | 6 | 7 | 0 | F-38 |
| 10 | 24 | 0 | 3 | 8 | 0 | F-39 |
| 11 | 37 | 0 | 2 | 10 | 1 | F-40 |

Nenhum erro de gravidade A nos quatro capítulos. Todos os teoremas e proposições com prova foram confirmados, às vezes com hipóteses que precisam ser acrescentadas. Os problemas M concentram-se em enunciados de conjecturas, afirmações de abstract/conclusão e hipóteses omitidas.

## Problemas M (resumo; detalhes nos relatórios)

**Cap. 7 (F-37):** (1) pipeline: perfis de grau r−2 não dão $C^r$ (mínimo 2r−3); (2) abstract: "só obstáculos que curvam para Ω restringem" é falso globalmente (um disco entre p e q eleva κ*); vale só no ponto de contato; (3) princípio de contato provado para $C^2$ mas aplicado a minimizadores $C^{1,1}$ (extensão curta, não escrita); (4) título "up to Dimension 12" sem suporte.

**Cap. 9 (F-38):** (1) "mapping classes não agem por conjugação" falso para ρ específica (par livre em SU(2) em que σ₁ é realizado por conjugação); vale só para ρ genérica; (2) hipóteses insuficientes para π₁ ≅ F_m (obstáculo sem interior, obstáculo anular, anel com fenda); (3) ∫|κ| ≥ ∫|θ'| − π é **verdadeira** (prova curta) e o texto diz "não sabemos"; (4) Remark sobre teardrop nulo-homotópico afirma sem prova o que a conclusão lista como aberto; (5) "CAD dá algoritmo" para n ≥ 3 é falso em geral (Novikov–Boone para n ≥ 5); (6) checagem em grade não garante cota superior (Bézier quase cuspidal: 3,7e3 na grade vs 1,19e6).

**Cap. 10 (F-39):** (1) κ*_info sem limite de comprimento é ainda mais degenerado: κ* = 0 mesmo quando nenhuma geodésica evita o obstáculo (arcos grandes); a conclusão "mede quanto o obstáculo força a curvar" é falsa em Θ ilimitado; (2) Conj. 3.1: primeira metade trivial (λ_min ≥ λ₀) e restrição a Stiefel pode tornar Σ* inalcançável; (3) §4 atribui ao cap. 7 curvatura constante com obstáculo ativo (só provado sem obstáculo). Positivo: o contraexemplo da Prop. 2.2 é mais forte do que o texto diz (gap ≥ 1/2 analiticamente).

**Cap. 11 (F-40):** (1) Conj. cMERA: a métrica escrita é de $H^d$ (fatia espacial), não AdS$_{d+1}$; $c_2 = L^2/z_0^2$; (2) Conj. RT via MCF: "todo corte admissível converge a um minimizador" é falso (par de geodésicas não minimizante para dois intervalos é estacionário); mesmo defeito na Conj. 5.2 do cap. 12.

## Problemas B recorrentes (todos os capítulos)
- O texto publicado remete a `audit/scripts/…`, inacessível ao leitor (caps. 7, 9, 10, 11): mover para uma seção "Reproducibility" com link ao repositório, ou remover.
- Itens de bibliografia sem citação; citações faltando (Fenchel; Petz; Bisognano–Wichmann; FLM; Miyaji et al. 2015; Hayden et al.); atribuições a ajustar (Miyaji et al. em vez de Nozaki–Ryu–Takayanagi para a métrica de estados localmente excitados; prefator de Immirzi não é de Rovelli–Smolin 1995; restrições de Faulkner et al. 2017).

## Próximos passos
1. Correção dos F-37…F-40 por **uma sessão diferente** da que escreveu as versões atuais.
2. Camada 2 (dirigida) dos F-xx antigos.
3. Camada 1 para caps. 8, 12, 13, depois 2, 3, 5, 1, 4, 6.
4. Itens prioritários para outro modelo / revisor humano: ver `PROTOCOL.md`.
