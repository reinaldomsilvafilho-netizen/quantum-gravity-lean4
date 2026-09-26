# Protocolo de organização e versões

Regra central: **cada documento tem uma única cópia viva**. Versões antigas existem só como *tags* do git e como versões no Zenodo, nunca como arquivos com nome `_final`, `_v2`, `.bak`, `(1)` ou `backup`.

## 1. Estrutura de pastas

```
resilient-turing/                     # repositório git (origin: quantum-gravity-lean4)
├── CLAUDE.md                         # hand-off compacto para qualquer modelo
├── README.md                         # estado público
├── Projeto_Gravidade_Quantica/
│   ├── AGENT_PROTOCOL.md             # economia de tokens e roteamento de modelos
│   ├── ORGANIZACAO_E_VERSOES.md      # este arquivo
│   ├── build_pdfs_safe.py            # build de tudo
│   ├── unified_quantum_gravity_book/ # o livro (fonte da verdade)
│   │   ├── chapNN_*.tex, master_*.tex, DICTIONARY_*.tex, declarations_chapter.tex
│   │   ├── WORKPLAN.md, CHANGELOG.md
│   │   ├── verify_chapNN_numerical.py
│   │   └── audit/                    # ledgers, verify/, scripts/ (histórico da auditoria)
│   ├── submission_package_jhep_scipost/   # artigo Simplicial QG (1 pasta = 1 obra)
│   ├── Manuscritos_Avulsos/<obra>/        # 1 pasta por artigo avulso: .tex, CORRECTIONS, scripts, lean
│   ├── formal_proofs_book/, formal_proofs_lean4/   # Lean
│   ├── releases/AAAA-MM-DD/          # pacote de cada publicação (PDFs + notas); fora do git
│   └── _arquivo/AAAA-MM-DD_<motivo>/ # material superado; fora do git
├── Outros_Projetos/                  # projetos fora da gravitação quântica
└── Scripts_Utilitarios/              # scripts de manutenção pontuais
```

Regras:
- **Uma obra, uma pasta.** O `.tex`, a nota de correções, os scripts de checagem e o Lean da obra ficam juntos.
- **Nada solto na raiz**, exceto os quatro documentos de topo: README, CLAUDE, AGENT_PROTOCOL e este protocolo.
- **Nomes de arquivo:** `snake_case`, ASCII, sem espaços. Datas no formato ISO (`AAAA-MM-DD`).
- **Artefatos de compilação** (`.aux`, `.log`, `.out`, `.toc`, `__pycache__`): descartáveis, nunca versionados, e podem ser apagados a qualquer momento.

## 2. Versões (versionamento semântico para documentos)

Cada obra tem número `MAJOR.MINOR.PATCH`:

| Parte | Quando sobe | Exemplo |
|---|---|---|
| MAJOR | Uma afirmação principal muda, é retirada ou vira conjectura; reorganização de capítulos | Yang–Mills: gap incondicional → condicional |
| MINOR | Resultado novo verificado, seção nova, conjectura resolvida | Dixon contínuo provado |
| PATCH | Tipografia, referências, números sem efeito nas conclusões | DOI corrigido |

Cada versão publicada tem três registros coerentes entre si:
1. uma entrada no `CHANGELOG.md` da obra, em ordem cronológica inversa, com a data;
2. uma *tag* do git no formato `<obra>-vMAJOR.MINOR.PATCH` (ex.: `book-v2.3.0`, `ym-v3.0.0`, `sqg-v2.0.0`, `fermions-v3.0.0`);
3. uma nova versão no Zenodo **do mesmo registro**, para o DOI de conceito continuar valendo, com a nota de versão.

Para recuperar uma versão antiga: `git checkout <tag>` ou baixar a versão correspondente no Zenodo. Não se guarda cópia.

## 3. Git

- **`main`** é sempre compilável e só recebe o que passou pelos portões do *Guia do Projeto*.
- **Ramos de trabalho:**
  - `fix/F-xx` para correções;
  - `research/<conjectura>` para pesquisa;
  - `tool/<gemini|outro>-AAAA-MM-DD` para trabalho de outros modelos.

  Cada ramo vai para `main` depois da auditoria.
- **Mensagens de commit:** `tipo: resumo`, com os tipos:
  - `fix` para correção matemática ou de texto;
  - `feat` para resultado novo;
  - `audit` para relatório ou script de verificação;
  - `docs` para README, protocolos e notas;
  - `build` para compilação e scripts de build;
  - `chore` para organização.
- **O que vai para o git:** fontes `.tex`, `.md` de protocolo e notas, scripts `.py`, Lean, figuras usadas pelos `.tex`.
- **O que não vai para o git:** PDFs de saída, artefatos de compilação, zips, backups, downloads de artigos, `_arquivo/`, `releases/`.
- **Como adicionar arquivos:** o `.gitignore` bloqueia `*.md` e `*.pdf` por padrão; adicione com `git add -f` só o que é fonte ou nota.

## 4. Trabalho feito fora do Claude (Gemini ou outros)

- Trabalhar num ramo `tool/…` ou numa cópia em `_staging/<ferramenta>-AAAA-MM-DD/`, nunca direto nos arquivos canônicos.
- Nada entra em `main` nem no Zenodo sem passar pela auditoria: verificador cego e reverificação.
- Relatórios que esses modelos produzirem com "PASSED", "CERTIFIED" ou "FINAL" não valem como evidência. Vão para `_arquivo/`.

## 5. Arquivo morto

- Material superado vai para `_arquivo/AAAA-MM-DD_<motivo>/`, mantendo o caminho relativo original.
- Cada movimentação gera um `MANIFESTO.tsv` com as colunas origem → destino. É o registro para desfazer.
- **Apagar de vez** só depois de 6 meses e só o que já estiver no git ou no Zenodo.

## 6. Rotina de limpeza

- **A cada publicação:** mover PDFs e notas para `releases/AAAA-MM-DD/`, criar a *tag* e conferir se sobrou alguma cópia com nome de versão.
- **Mensalmente:** listar arquivos com `_final`, `_v[0-9]`, `.bak`, `backup`, `(1)` ou `copy` no nome e arquivá-los.
- **Nunca:** editar um arquivo dentro de `_arquivo/` ou de `releases/`.
