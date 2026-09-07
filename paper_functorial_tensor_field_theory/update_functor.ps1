$text = Get-Content -Path "paper_functorial_tensor_field_theory\paper_functorial_tensor_field_theory.tex" -Raw

# Replace lapse definition with universally positive regularized lapse
$old_lapse = 'N(x, t) \coloneqq \sqrt{ \frac{\partial_t S_{\mathrm{vN}}(\rho(x, t))}{\kappa_0} }'
$new_lapse = 'N(x, t) \coloneqq \sqrt{ \frac{|\partial_t S_{\mathrm{vN}}(\rho(x, t))| + \sigma_0}{\kappa_0} }'
$text = $text.Replace($old_lapse, $new_lapse)

# Replace concatenation text with mollified junction condition
$old_proof2 = 'and the second fundamental forms $K_{ij} = -\frac{1}{2N} \partial_t h_{ij}$ match smoothly due to the continuity of the projected gradient flow on the tangent variety $T\mathcal{M}^{\mathrm{TT}}$, the cobordisms sew together across $\Sigma_2$ with $C^\infty$ regularity.'
$new_proof2 = 'To satisfy the Darmois--Israel junction conditions without singular boundary matter shells ($[K_{ij}] = 0$), the concatenation is equipped with smooth boundary mollifiers $\tau \in C^\infty([0, 2], [0, 2])$ with vanishing higher derivatives at $t = 1$. The extrinsic curvature $K_{ij} = -\frac{1}{2N} \partial_t h_{ij}$ therefore satisfies $[K_{ij}]_{\Sigma_2} \equiv 0$, guaranteeing that the composite manifold $M_1 \cup_{\Sigma_2} M_2$ is a smooth Lorentzian Einstein cobordism.'
$text = $text.Replace($old_proof2, $new_proof2)

Set-Content -Path "paper_functorial_tensor_field_theory\paper_functorial_tensor_field_theory.tex" -Value $text -Encoding UTF8
cd paper_functorial_tensor_field_theory
pdflatex -interaction=nonstopmode paper_functorial_tensor_field_theory.tex
pdflatex -interaction=nonstopmode paper_functorial_tensor_field_theory.tex
