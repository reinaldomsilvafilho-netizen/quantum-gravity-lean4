"""
CNIS - Typst / CeTZ Vector Code Exporter (Unified Compiler)
==========================================================
Deterministically compiles ParametricGlyph Geometric AST to native Typst / CeTZ scripts.
"""

from typing import Dict, Any
from core_glyphs import ParametricGlyph, GlyphRegistry

class TypstExporter:
    """Exports CNIS Parametric Glyphs to native Typst / CeTZ format via Geometric AST compilation."""
    
    @staticmethod
    def export_glyph(glyph: ParametricGlyph) -> str:
        """Deterministically compile a glyph's Geometric AST to CeTZ code."""
        return glyph.to_typst_cetz()

    @classmethod
    def export_all_to_file(cls, filepath: str):
        suite = GlyphRegistry.get_standard_suite()
        all_code = [
            "// ========================================================",
            "// CNIS Standard Autological Mathematical Glyphs for Typst",
            "// Compiled deterministically from Unified Geometric AST v1.0",
            "// ========================================================",
            "#import \"@preview/cetz:0.2.2\"\n"
        ]
        for name, glyph in suite.items():
            all_code.append(cls.export_glyph(glyph))
            all_code.append("\n")
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(all_code))

if __name__ == "__main__":
    TypstExporter.export_all_to_file("typst_glyphs.typ")
    print("Exported all 6 canonical glyphs deterministically to typst_glyphs.typ")
