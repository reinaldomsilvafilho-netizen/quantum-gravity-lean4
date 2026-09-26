# Cap. 4: ledger de afirmações (auditoria 2026-09-24)

| ID | Enunciado | Tipo | Veredito | Ação |
|---|---|---|---|---|
| C04-P2.3 | Simétrico e semidefinido positivo | CL | correto (prova completa) | — |
| C04-D2.4/T2.5 | Laplaciano espectral; "coincide com a forma integral para s∈(0,1)"; "s=2 exige clamped $H_0^2$"; barreira de Friedrichs | NE | **falso**: espectral ≠ integral restrito em domínio limitado; o quadrado de $-\Delta_D$ impõe condições de **Navier** ($u=\Delta u=0$), não clamped; o trecho da "barreira" não tem conteúdo matemático; e nada disso é o operador de núcleo Beta do capítulo | substituído por dois Remarks corretos (limitação; Navier vs clamped) |
| C04-T2.6 | Símbolo fechado + limite "Gram $A_{m-1}$" $\frac{1}{2m\alpha}$ | NE | **falso** (herdado do cap. 3) | substituído por símbolo integral + $\mathbf M_2$ (cap. 3, Thm 7.2) |
| C04-T3.1 | Conservação de massa e energia (NLSE) | CL | correto (operador limitado e autoadjunto) | — |
| C04-T3.2 | Instabilidade modulacional | NP | fórmula correta (conferida); faltava a prova e a observação de que o símbolo é limitado | prova adicionada; condição de não vazio; "todo k instável" se $4M\kappa p\rho^p/\hbar^2>\sup\sigma$ |
| C04-T3.3 | Sólitons com simetria $S_m$ e decaimento algébrico | NE | sem prova; a simetria linear é $S_{m-1}\times\mathbb Z_2$ (a troca com $y_m$ é afim); com suporte compacto, o decaimento esperado é exponencial | rebaixado a Conjectura + Remark |
| C04-T4.2 | Propagador Mittag-Leffler | CL | correto | — |
| C04-T4.3 | MSD $=\frac{K}{m\alpha\Gamma(\beta+1)}A\,t^\beta$ | NP | **coeficiente falso** (herdado); a estrutura da prova está certa e o resultado é exato para todo t | corrigido: $\frac{K}{\alpha^2\Gamma(\beta+1)}\mathbf M_2(\alpha)t^\beta$ |
| C04-R4.4 | "Antes não havia Green fechado" | HE | excesso (CTRW/Mittag-Leffler são padrão) | corrigido |
