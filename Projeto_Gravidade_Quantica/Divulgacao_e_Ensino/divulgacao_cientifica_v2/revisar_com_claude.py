#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
revisar_com_claude.py
---------------------
Script autônomo para solicitar ao Claude Code CLI (em modo de máximo raciocínio / pipe stdin)
uma revisão crítica profunda, auditoria adversarial e um banco de ideias criativas para a
suíte de divulgação científica v2.0 da Gravitação Quântica Simplicial em Delta_4 x Delta_2.

Protocolo IPC:
- Piped stdin (evita WinError 206 de limite de caracteres no Windows).
- Timeout configurável e monitoramento em tempo real.
- Salva o parecer completo em Markdown em UTF-8.

Autor: Reinaldo Maia Silva-Filho / Antigravity AI
Instituição: PPGEE/DES, Universidade Federal de Lavras (UFLA)
Apoio: CAPES Código 001
"""

import os
import sys
import argparse
import subprocess
import time
from pathlib import Path

DEFAULT_CLAUDE_CMD = r"C:\Users\monar\AppData\Roaming\npm\claude.cmd"
SCRIPT_DIR = Path(__file__).parent.resolve()

TEXTOS_MAP = {
    "1": {
        "nome": "Texto 1: Público Amplo e Entusiastas de Ciência",
        "arquivo": SCRIPT_DIR / "01_TEXTO_PUBLICO_AMPLO_NARRATIVO.md",
        "publico": "Público leigo, curiosos, entusiastas de ciência, estudantes de ensino médio e graduação, jornalistas científicos.",
        "foco": "Linguagem narrativa, quase zero equações, 4 grandes analogias físicas, 26 paradoxos resolvidos."
    },
    "2": {
        "nome": "Texto 2: Comunidade Científica Interdisciplinar",
        "arquivo": SCRIPT_DIR / "02_TEXTO_COMUNIDADE_CIENTIFICA_INTERDISCIPLINAR.md",
        "publico": "Cientistas da computação, cientistas de dados, engenheiros, estatísticos, biólogos computacionais e químicos.",
        "foco": "Geometria da informação (Fisher-Rao / Kullback-Leibler), eliminação de overfitting (26 parâmetros -> Tríade de Planck), colapso como obstáculo de Caffarelli C^{1,1}, regra de Born por bacias de atração, prova formal em Lean 4 (0 sorry)."
    },
    "3": {
        "nome": "Texto 3: Físicos e Matemáticos Gerais (Síntese v2.0)",
        "arquivo": SCRIPT_DIR / "03_TEXTO_FISICOS_E_MATEMATICOS_TECNICO.md",
        "publico": "Físicos teóricos de áreas afins (matéria condensada, astrofísica, física nuclear), matemáticos puros e aplicados, cosmólogos.",
        "foco": "Formas diferenciais de Dirac-Kähler, evasão de Nielsen-Ninomiya, Beta-Laplaciano fracionário (ds = 2 -> 4), funcional minimax L^infty no 3+1 de ADM, álgebra S_3 (Koide 2/3, Cabibbo), dupla cópia BCJ, scorecard comparativo e horizonte observacional (LISA, LiteBIRD)."
    }
}

def carregar_textos(selecao: str) -> dict:
    """Carrega os arquivos Markdown selecionados."""
    conteudos = {}
    chaves = ["1", "2", "3"] if selecao == "todos" else [selecao]
    for k in chaves:
        cfg = TEXTOS_MAP[k]
        path = cfg["arquivo"]
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        with open(path, "r", encoding="utf-8") as f:
            conteudos[k] = {
                "info": cfg,
                "texto": f.read()
            }
    return conteudos

def construir_prompt(conteudos: dict, modo: str) -> str:
    """Monta o prompt estruturado para o Claude Code."""
    prompt_parts = [
        "Você é o Revisor Sênior Internacional de Comunicação Científica e Físico Teórico Adversarial.",
        "Sua missão é auditar, revisar criticamente e gerar ideias inovadoras de divulgação e impacto para a suíte de divulgação científica v2.0 da Gravitação Quântica Simplicial em Delta_4 x Delta_2 (Autor: Reinaldo Maia Silva-Filho, UFLA / CAPES Código 001).",
        "",
        "=== DIRETRIZES EDITORIAIS E DE ENGENHARIA INEGOCIÁVEIS ===",
        "1. ZERO PLEONASMOS: Verifique rigorosamente se há o uso indevido de 'corpo material' ou 'sinal material'. A física e ontologia estritas exigem unicamente 'corpo', 'sinal', 'matéria', 'sistema físico'.",
        "2. ZERO PREGAÇÃO FILOSÓFICA: Foco puramente em princípios geométricos, mecanismos variacionais, teoria de EDPs e evidências observacionais.",
        "3. HONESTIDADE CIENTÍFICA: Distinção transparente entre retrodicções analíticas já calculadas e predições novas sujeitas a testes empíricos futuros (LISA, LiteBIRD, CMB-S4, MAGIS-100).",
        "",
        f"MODO DE OPERAÇÃO: {modo.upper()}",
        ""
    ]

    if modo in ["revisao", "completo"]:
        prompt_parts.extend([
            "=== PARTE 1: REVISÃO CRÍTICA E AUDITORIA ADVERSARIAL ===",
            "Para cada um dos textos fornecidos abaixo, avalie:",
            "a) Calibração do Tom e Linguagem: O texto fala com a língua exata de seu público-alvo?",
            "b) Eficácia Pedagógica das Analogias: As analogias mecânicas (redemoinho, trem minimax, folha elástica de Caffarelli, correia de Dirac) são cristalinas ou geram potenciais mal-entendidos?",
            "c) Solidez Conceitual: Há algum salto lógico, obscuridade ou imprecisão física?",
            "d) Verificação Anti-Pleonasmo e Higiene Textual: Algum deslize na terminologia?",
            "e) Avaliação do Impacto: Qual a probabilidade de convencer um cético e quais os contra-argumentos que um leitor crítico levantará?",
            ""
        ])

    if modo in ["ideias", "completo"]:
        prompt_parts.extend([
            "=== PARTE 2: BANCO DE IDEIAS CRIATIVAS E DISSEMINAÇÃO ===",
            "Apresente propostas concretas e viáveis de alto impacto:",
            "a) Recursos Visuais e Infográficos: Sugira 3 a 5 conceitos detalhados de diagramas visuais (com descrição da cena, elementos e layout) que tornariam os conceitos imediatamente compreensíveis.",
            "b) Roteiros para Vídeos Curtos (1 a 3 minutos): Desenvolva 2 roteiros dinâmicos (estilo Veritasium / Kurzgesagt / 3Blue1Brown) explicando o 'Big Bounce sem singularidades' e o 'Colapso como descolamento de Caffarelli'.",
            "c) Estratégia de Disseminação Digital: Como publicar e viralizar essas ideias em comunidades especializadas (Hacker News, r/Physics, r/MachineLearning, Physics Forums, Twitter/X acadêmico, LinkedIn)?",
            "d) Experimentos Didáticos e Analogias Adicionais: Que outras analogias ou demonstrações de laboratório/computacionais interativas (widgets, simulações em Python/Streamlit) poderiam ser criadas?",
            ""
        ])

    prompt_parts.extend([
        "=== TEXTOS DA SUÍTE PARA ANÁLISE ===",
        ""
    ])

    for k, data in conteudos.items():
        info = data["info"]
        prompt_parts.append(f"--- INÍCIO DE {info['nome']} ---")
        prompt_parts.append(f"Público-Alvo: {info['publico']}")
        prompt_parts.append(f"Foco do Documento: {info['foco']}")
        prompt_parts.append("")
        prompt_parts.append(data["texto"])
        prompt_parts.append(f"--- FIM DE {info['nome']} ---")
        prompt_parts.append("")

    prompt_parts.append("Forneça seu relatório em português formal, altamente estruturado, objetivo e diretamente acionável.")
    return "\n".join(prompt_parts)

def executar_claude(prompt: str, claude_cmd: str, timeout: int = 600) -> str:
    """Executa o Claude CLI via pipe stdin e captura a resposta."""
    print(f"[*] Iniciando Claude CLI em modo IPC (-p)...")
    print(f"[*] Binário: {claude_cmd}")
    print(f"[*] Tamanho do prompt: {len(prompt)} caracteres (~{len(prompt)//4} tokens)")

    start_time = time.time()
    try:
        proc = subprocess.Popen(
            [claude_cmd, "-p"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
    except FileNotFoundError:
        print(f"[ERRO] Comando claude não encontrado em: {claude_cmd}")
        sys.exit(1)

    print("[*] Enviando payload via stdin pipe...")
    try:
        stdout, stderr = proc.communicate(input=prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        print(f"[ERRO] Tempo limite de {timeout}s excedido!")
        return f"# ERRO: Timeout após {timeout}s\n\nSaída parcial:\n{stdout}\n\nStderr:\n{stderr}"

    elapsed = time.time() - start_time
    print(f"[*] Processo concluído em {elapsed:.2f} segundos com código {proc.returncode}.")

    if proc.returncode != 0:
        print(f"[AVISO] Código de saída diferente de zero: {proc.returncode}")
        if stderr:
            print(f"[STDERR]: {stderr[:500]}")

    return stdout

def main():
    parser = argparse.ArgumentParser(description="Revisão e Geração de Ideias com Claude Code CLI")
    parser.add_argument("--texto", choices=["1", "2", "3", "todos"], default="todos",
                        help="Texto a ser analisado (1, 2, 3 ou todos; padrão: todos)")
    parser.add_argument("--modo", choices=["ideias", "revisao", "completo"], default="completo",
                        help="Modo de operação: 'ideias', 'revisao' ou 'completo' (padrão: completo)")
    parser.add_argument("--output", type=str, default=str(SCRIPT_DIR / "FEEDBACK_E_IDEIAS_CLAUDE.md"),
                        help="Arquivo de saída em Markdown (padrão: divulgacao_cientifica_v2/FEEDBACK_E_IDEIAS_CLAUDE.md)")
    parser.add_argument("--claude-cmd", type=str, default=DEFAULT_CLAUDE_CMD,
                        help="Caminho para o executável claude.cmd")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Tempo limite em segundos para execução (padrão: 600s)")

    args = parser.parse_args()

    print("================================================================")
    print("  REVISÃO E BANCO DE IDEIAS COM CLAUDE CODE CLI (v2.0)")
    print("================================================================")
    print(f"Seleção de Textos : {args.texto}")
    print(f"Modo de Operação  : {args.modo}")
    print(f"Destino do Laudo  : {args.output}")
    print("----------------------------------------------------------------")

    conteudos = carregar_textos(args.texto)
    for k, v in conteudos.items():
        print(f" -> Carregado: {v['info']['nome']} ({len(v['texto'])} caracteres)")

    prompt = construir_prompt(conteudos, args.modo)

    resposta = executar_claude(prompt, args.claude_cmd, args.timeout)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(resposta)

    print("----------------------------------------------------------------")
    print(f"[SUCESSO] Parecer do Claude salvo com sucesso em:")
    print(f"  --> {output_path.resolve()}")
    print(f"Tamanho da resposta: {len(resposta)} caracteres.")
    print("================================================================")

if __name__ == "__main__":
    main()
