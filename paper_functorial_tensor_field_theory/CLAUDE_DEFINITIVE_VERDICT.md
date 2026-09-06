## Avaliação Final — Revisor Sênior (Física Matemática / Geometria Diferencial)

Verifiquei os dois pontos alegadamente corrigidos linha a linha contra o texto-fonte, incluindo uma verificação algébrica independente das fórmulas de $\rho_{\mathrm{matt}}$ e $j_i$. Resultado: **os dois pontos foram corrigidos corretamente**, mas a correção do Ponto 1 introduziu uma nova imprecisão no Ponto 2 que precisa ser sanada antes de submissão.

### Ponto 2 — Berry-flat gauge: removido, mas com resíduo problemático

A frase "Berry-flat gauge chart" de fato não aparece mais; o argumento agora é o correto (posto pleno $\Rightarrow \ker(g^{\QFI})=0$ trivialmente, via $g^{\QFI}_{ij}v^iv^j = 4\|\bar d\mathcal T(v)\|^2>0$). Isso é internamente válido, embora seja essencialmente uma reformulação da hipótese de imersão (não uma dedução independente) — aceitável como definição, não como teorema profundo.

**Problema novo**: a frase final da Seção 4.1(2),
> "under local gauge rotations $\mathcal{T}(x) \mapsto U(x)\mathcal{T}(x)$, the projection... renders $g^{\QFI}_{ij}$ gauge-invariant"

conflaciona dois objetos distintos:
- a invariância de fase $U(1)$ projetiva ($\mathcal T \to e^{i\theta(x)}\mathcal T$), que **é** exatamente o que o projetor $(I-|\mathcal T\rangle\langle\mathcal T|)$ elimina — isso está correto e é o fato padrão por trás da métrica de Fubini-Study/QFI descer ao espaço projetivo;
- o gauge de bond $\mathrm{SU}(\chi)$ do cMPS, que atua sobre $(Q,R)$, **não** sobre o vetor físico $\mathcal T(x)\in\mathcal H$ como multiplicação unitária à esquerda.

Se $U(x)$ na frase for um unitário genérico (não apenas fase), a afirmação é **falsa**: $g^{\QFI}$ não é invariante sob rotação unitária arbitrária do próprio vetor de estado, só sob sua fase. Correção necessária: substituir por $\mathcal T(x)\mapsto e^{i\theta(x)}\mathcal T(x)$, ou deixar explícito que se trata da ação induzida do gauge de bond sobre o estado físico (que por definição do fundamental theorem de MPS deixa $\mathcal T$ invariante, não "rotacionado").

### Ponto 1 — Unificação de tipos e fórmulas construtivas: correção substantiva e verificada

A tipagem agora é consistente: $\psi,\pi_\psi\in \mathrm{End}(\mathbb C^\chi)$ tanto no objeto de $\CTens$ quanto na fronteira/bulk de $\Cob$ ($\psi_\Sigma, \Psi \in C^\infty(-,\mathrm{End}(\mathbb C^\chi))$), sem mistura de Clifford. Isso resolve de fato a incompatibilidade dimensional $\chi^2$ vs. $8$ apontada antes.

Fiz a verificação direta que o texto afirma mas não exibe: parti da ação (4.6), derivei $T_{\mu\nu}[\Psi]$ (já usado no Teorema 4.7), e projetei $\rho_{\mathrm{matt}}=n^\mu n^\nu T_{\mu\nu}$ usando a decomposição ADM $g^{\mu\nu}\nabla_\mu\Psi^\dagger\nabla_\nu\Psi = -(n\!\cdot\!\nabla\Psi)^\dagger(n\!\cdot\!\nabla\Psi)+h^{ij}\partial_i\Psi^\dagger\partial_j\Psi$ e $n^\mu\nabla_\mu\Psi=\pi_\psi$. O resultado reproduz **exatamente** a Eq. (2.2):
$$\rho_{\mathrm{matt}} = \tfrac12\mathrm{Tr}_\chi(\pi_\psi^\dagger\pi_\psi + h^{ij}\partial_i\psi^\dagger\partial_j\psi + V(\psi)).$$
Analogamente, $j_i=-n^\mu h_i^\nu T_{\mu\nu}$ reproduz (2.3) porque o termo de traço com $g_{\mu\nu}n^\mu e_i^\nu=0$ some por ortogonalidade. **Isto é real e correto** — não é decoração, é a fonte canônica de Noether do setor de matéria batendo com a densidade ADM postulada. Também confirmei que o termo cruzado $h^{ij}\mathrm{Tr}_\chi(\partial_i\psi^\dagger\partial_j\psi)$ é real sem precisar de "Re" explícito, pois a simetria de $h^{ij}$ força $\overline{\sum_{ij}h^{ij}\mathrm{Tr}(\partial_i\psi^\dagger\partial_j\psi)}$ a igualar a própria soma.

### Lacunas menores remanescentes (não bloqueantes, mas a corrigir antes de submissão)

1. **Hermiticidade de $V(\psi)$** não é declarada explicitamente — sem isso, $\mathrm{Tr}_\chi V(\psi)$ não é garantidamente real. Bastaria acrescentar "$V:\mathrm{End}(\mathbb C^\chi)\to \mathrm{Herm}(\mathbb C^\chi)$, $\mathrm{SU}(\chi)$-invariante".
2. **Reparametrização boundary-flat na composição (Teorema 4.5(2))**: forçar todas as derivadas temporais de $\mathcal T$ a se anularem nos extremos implica $K_{ij}\to 0$ em toda superfície de colagem interna. Isso é tecnicamente consistente (é o truque padrão de suavização de categorias de cobordismo via reparametrização, tipo Morse-flow), mas fisicamente restringe as composições a terem curvatura extrínseca nula em cada emenda — vale uma frase de comentário explícito para não parecer um artefato escondido.
3. **Teorema 4.7 (fidelidade)**: a reconstrução de $(Q,R,\psi,\pi_\psi)$ a partir de $(h_{ij},K_{ij},N,N^i,\Psi)$ "a menos de gauge $\mathrm{SU}(\chi)$" é afirmada, não demonstrada — é essencialmente uma extensão do teorema fundamental de MPS/cMPS ao setor de matéria acoplado, e deveria ser citada como tal (ou ao menos com um esboço) em vez de assumida silenciosamente. Isso já era uma lacuna pré-existente (não introduzida pela rodada atual), mas continua presente.

### Veredito

O manuscrito está **matematicamente coerente, bem tipado e agora genuinamente construtivo** nos dois pontos que motivaram a rodada de correção — a unificação de tipos matriciais é real, e as fórmulas $\rho_{\mathrm{matt}}$, $j_i$ se verificam independentemente contra o tensor de energia-momento canônico da ação. Isso é progresso substantivo, não cosmético.

**Não está pronto para submissão no estado atual** por causa do item de gauge (Ponto 2, frase "$\mathcal T(x)\mapsto U(x)\mathcal T(x)$") — é uma afirmação matemática falsa se lida literalmente, e um árbitro de JMP/CQG vai marcar isso imediatamente. É uma correção de uma linha (trocar $U(x)$ por $e^{i\theta(x)}$ ou reformular), não uma revisão estrutural.

**Recomendação**: 
- Para arXiv (math-ph): pode submeter após corrigir a frase de gauge — é um preprint, o padrão de tolerância a imprecisões expositórias é maior.
- Para JMP/CQG: corrija a frase de gauge, adicione a hipótese de Hermiticidade de $V$, e adicione uma frase reconhecendo explicitamente a extensão assumida do teorema fundamental de cMPS no Teorema 4.7 (ou cite a referência apropriada). Com essas três correções — nenhuma estrutural — o artigo está em padrão de submissão.
