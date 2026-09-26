# Protocolo de verificação independente (regra dos quatro olhos)

Objetivo: dar a cada afirmação do livro um veredito de alguém que **não** escreveu a correção. Um achado F-xx só passa a `verificado` no WORKPLAN com CONFIRMA na camada 1 (cega) **e** na camada 2 (dirigida). Quem corrige nunca verifica a própria correção.

## Quem pode ser verificador
- Sessão ou subagente de LLM com **contexto limpo** (sem acesso a esta conversa, aos ledgers `audit/chXX_claims.md` nem ao WORKPLAN durante a camada 1).
- Outro modelo (ex.: Gemini/Antigravity), para itens de severidade C/A.
- Revisor humano da área, para os itens marcados como prioritários.

## Camada 1: reauditoria cega (um capítulo por verificador)

**Entrada permitida:** só o arquivo `chapXX_*.tex` e, se o capítulo citar outro capítulo do livro, o `.tex` citado. **Proibido ler** `audit/chXX_claims.md`, `WORKPLAN.md`, `CHANGELOG.md`, `audit/baseline_v2.2/`, `audit/_chXX_*.tex`.

**Tarefa:** para cada `theorem`, `proposition`, `lemma`, `corollary`, `conjecture`, `remark` com conteúdo matemático, e para cada afirmação numérica ou física do abstract, da introdução e da conclusão:
1. Enunciado resumido (1 linha) e rótulo/número.
2. Tipo declarado no texto (provado aqui / clássico citado / conjectura / heurística) e se esse rótulo é **honesto**. Um teorema sem prova é problema. Uma conjectura que tem prova simples também deve ser apontada.
3. Checagem da prova, linha a linha: hipóteses usadas, passos que não seguem, casos de fronteira, sinais, fatores, dimensões.
4. **Tentativa ativa de contraexemplo** antes de confirmar: casos degenerados (k=2, n=1, curvatura 0, obstáculo convexo etc.) e verificação numérica rápida em Python quando possível (salvar em `audit/verify/scripts/chXX_*.py`).
5. Citações: o resultado citado diz mesmo isso? (Não é preciso resolver DOIs; basta apontar dúvidas.)
6. Veredito: **CONFIRMA** / **PROBLEMA** (dizer qual, com evidência reproduzível) / **INCERTO** (dizer o que faltaria).

Também verificar se o abstract, a introdução e a conclusão afirmam só o que o corpo prova.

**Saída:** `audit/verify/chXX_blind.md`, com uma tabela `| Item | Enunciado | Rótulo honesto? | Veredito | Evidência/observação |` seguida de um resumo com os PROBLEMAS por gravidade (A: erro matemático/físico; M: lacuna ou rótulo errado; B: redação/citação).

**Restrições:** não editar nenhum arquivo fora de `audit/verify/`. Não "corrigir" o capítulo. Ser cético: o autor anterior do texto (humano ou IA) errou muitas vezes neste livro.

## Camada 2: verificação dirigida dos F-xx (depois da camada 1)

**Entrada:** a linha do F-xx no WORKPLAN, o trecho antes (`audit/baseline_v2.2/`), o trecho atual e o script de evidência citado.

**Tarefa:**
1. Rodar o script de evidência e conferir que ele sustenta o achado.
2. **Teste de mutação:** alterar a fórmula corrigida (sinal, fator 2, expoente) no script e confirmar que o teste falha. Script sem controle negativo não conta como evidência.
3. Julgar se a correção resolve o problema **e** não exagera no sentido oposto (ex.: rebaixar a conjectura algo que tem prova simples, ou remover conteúdo correto).
4. Veredito CONFIRMA / PROBLEMA / INCERTO.

**Saída:** `audit/verify/F-xx.md` (ou uma tabela em `audit/verify/findings.md`).

## Consolidação
- Quem consolida só copia os vereditos para o WORKPLAN. Se o consolidador foi o autor da correção, ele **não** decide as divergências: cada PROBLEMA vira um novo F-xx e a correção vai para outra sessão.
- Status no WORKPLAN: `verificado (camada 1: <quem>, camada 2: <quem>, data)`.

## Prioridade
1. Caps. 7, 9, 10, 11 (mais conteúdo novo; F-33, F-35, F-36, F-07/17/32).
2. Cap. 8 (F-13, F-14, F-34), caps. 12–13 (F-03…F-12, F-22, F-27).
3. Caps. 2, 3, 5; depois 1, 4, 6.

Itens sugeridos para revisor humano: princípio de contato (cap. 7); finitude de classes sob limite de comprimento (cap. 9); contraexemplo de generalização (cap. 10); atribuição FGHMV e SLD/BKM (cap. 11); ordens de grandeza (cap. 13).
