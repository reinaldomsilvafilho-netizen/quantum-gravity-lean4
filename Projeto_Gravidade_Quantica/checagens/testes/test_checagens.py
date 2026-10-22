"""Testes das checagens: cada uma tem de REPROVAR o erro que motivou sua criação
(controle negativo) e APROVAR o caso limpo. Rodar: python checagens/testes/test_checagens.py"""
import pathlib
import shutil
import sys
import tempfile
import unittest

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import check_entrega  # noqa: E402
import lint_estilo  # noqa: E402

ROOT = AQUI.parent.parent


class Lint(unittest.TestCase):
    def test_ruim_reprova_cada_regra(self):
        cods = {c for c, *_ in lint_estilo.checar(AQUI / "ruim.tex", estrito=True)}
        self.assertEqual(cods, {"H1", "H2", "H3", "R1"})

    def test_bom_aprova(self):
        self.assertEqual(lint_estilo.checar(AQUI / "bom.tex", estrito=True), [])

    def test_erro_real_do_passado(self):
        # versão de 2026-10-07 do Beyond the Spectrum III, com "earlier versions" no texto
        p = ROOT / "_arquivo/backup_tex_2026-10-07/Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3_prerelease.tex"
        if not p.exists():
            self.skipTest("backup fora desta máquina")
        self.assertIn("H1", {c for c, *_ in lint_estilo.checar(p)})


class Entrega(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(dir=AQUI))
        self.real = self.dir / "cap.tex"
        self.real.write_text("texto velho\n", encoding="utf-8")
        self.h0 = check_entrega.sha256(self.real)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_falha_de_2026_10_17_copia_temporaria(self):
        # o agente edita a cópia temporária; o arquivo real fica igual
        tmp = pathlib.Path(tempfile.mkdtemp())
        copia = tmp / "cap.tex"
        shutil.copy(self.real, copia)
        copia.write_text("texto novo\n", encoding="utf-8")
        falhas, _ = check_entrega.conferir(self.real, self.h0, contem=["texto novo"], nao_contem=["texto velho"])
        self.assertTrue({"E3", "E4"} <= {c for c, _ in falhas})
        falhas_copia, _ = check_entrega.conferir(copia, self.h0, contem=["texto novo"])
        self.assertIn("E1", {c for c, _ in falhas_copia})
        shutil.rmtree(tmp)

    def test_entrega_certa_aprova(self):
        self.real.write_text("texto novo\n", encoding="utf-8")
        falhas, _ = check_entrega.conferir(self.real, self.h0, minutos=5, contem=["texto novo"], nao_contem=["texto velho"])
        self.assertEqual(falhas, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
