"""
CNIS - Interactive HTML & SVG Glyph Gallery Generator
=====================================================
Builds a rich interactive visual catalog allowing mathematicians to inspect,
parameterize, and export computer-native autological glyphs in real-time.
"""

import os
from core_glyphs import GlyphRegistry

def generate_interactive_gallery(output_path: str):
    suite = GlyphRegistry.get_standard_suite()
    
    glyph_cards_html = []
    for key, glyph in suite.items():
        svg_code = glyph.to_svg(width=220, height=220)
        ports_info = "".join([
            f'<span class="port-tag port-{p.kind}">{p.label} ({p.kind})</span> '
            for p in glyph.ports
        ])
        
        glyph_cards_html.append(f"""
        <div class="glyph-card" id="card-{glyph.name}">
            <div class="glyph-header">
                <h3>{glyph.name.replace('_', ' ').title()}</h3>
                <span class="latex-badge">{glyph.symbol_latex}</span>
            </div>
            <div class="glyph-category">{glyph.category}</div>
            <div class="svg-container">
                {svg_code}
            </div>
            <div class="glyph-body">
                <p class="desc">{glyph.description}</p>
                <div class="autological-box">
                    <strong>💡 Autological Property:</strong><br>
                    {glyph.autological_property}
                </div>
                <div class="ports-container">
                    <strong>Multilinear Ports:</strong><br>
                    {ports_info if ports_info else '<span class="text-muted">Closed operator</span>'}
                </div>
            </div>
            <div class="glyph-footer">
                <button onclick="copySVG('{glyph.name}')" class="btn btn-primary">Copy SVG</button>
                <button onclick="inspectPorts('{glyph.name}')" class="btn btn-secondary">Inspect Ports</button>
            </div>
        </div>
        """)
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CNIS - Computer-Native Isomorphic Mathematical Symbology Gallery</title>
    <style>
        :root {{
            --bg: #0d1117;
            --card-bg: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --text-bright: #f0f6fc;
            --accent: #58a6ff;
            --accent-red: #f85149;
            --accent-teal: #39d353;
            --accent-purple: #bc8cff;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 24px;
        }}
        .header {{
            max-width: 1200px;
            margin: 0 auto 32px auto;
            text-align: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 24px;
        }}
        .header h1 {{
            color: var(--text-bright);
            font-size: 2.2rem;
            margin-bottom: 8px;
        }}
        .header p {{
            font-size: 1.1rem;
            color: #8b949e;
            max-width: 800px;
            margin: 0 auto;
        }}
        .badge-bar {{
            margin-top: 16px;
            display: flex;
            justify-content: center;
            gap: 12px;
        }}
        .badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: bold;
            background: rgba(88, 166, 255, 0.15);
            color: var(--accent);
            border: 1px solid rgba(88, 166, 255, 0.3);
        }}
        .gallery-grid {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
        }}
        .glyph-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .glyph-card:hover {{
            transform: translateY(-3px);
            border-color: var(--accent);
        }}
        .glyph-header {{
            padding: 16px 20px 8px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .glyph-header h3 {{
            margin: 0;
            color: var(--text-bright);
            font-size: 1.25rem;
        }}
        .latex-badge {{
            background: #21262d;
            border: 1px solid var(--border);
            padding: 2px 8px;
            border-radius: 4px;
            font-family: monospace;
            color: var(--accent);
            font-size: 0.95rem;
        }}
        .glyph-category {{
            padding: 0 20px 12px 20px;
            font-size: 0.85rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .svg-container {{
            background: #090d13;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
        }}
        .svg-container svg {{
            background: #ffffff;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .glyph-body {{
            padding: 16px 20px;
            flex-grow: 1;
        }}
        .desc {{
            margin-top: 0;
            font-size: 0.95rem;
            line-height: 1.5;
            color: #8b949e;
        }}
        .autological-box {{
            background: rgba(57, 211, 83, 0.08);
            border-left: 3px solid var(--accent-teal);
            padding: 10px 14px;
            border-radius: 0 4px 4px 0;
            font-size: 0.88rem;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        .ports-container {{
            font-size: 0.88rem;
            margin-top: 8px;
        }}
        .port-tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 4px;
        }}
        .port-input {{
            background: rgba(88, 166, 255, 0.2);
            color: #58a6ff;
            border: 1px solid rgba(88, 166, 255, 0.4);
        }}
        .port-output {{
            background: rgba(248, 81, 73, 0.2);
            color: #f85149;
            border: 1px solid rgba(248, 81, 73, 0.4);
        }}
        .glyph-footer {{
            padding: 12px 20px;
            background: #0d1117;
            border-top: 1px solid var(--border);
            display: flex;
            gap: 10px;
        }}
        .btn {{
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.15s ease;
        }}
        .btn-primary {{
            background: #238636;
            color: #ffffff;
        }}
        .btn-primary:hover {{
            background: #2ea043;
        }}
        .btn-secondary {{
            background: #21262d;
            color: #c9d1d9;
            border-color: var(--border);
        }}
        .btn-secondary:hover {{
            background: #30363d;
        }}
        #toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #238636;
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            display: none;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📐 CNIS: Computer-Native Isomorphic Symbology</h1>
        <p>Canonical Open Vector Glyph Standard (SVG / Typst / Lean 4) where visual geometry and topology are strictly isomorphic to algebraic semantics.</p>
        <div class="badge-bar">
            <span class="badge">Joyal-Street Coherent</span>
            <span class="badge">Lean 4 AST Native</span>
            <span class="badge">Multi-Channel Visual Orthogonality</span>
            <span class="badge">Pareto-Optimal NOI</span>
        </div>
    </div>

    <div class="gallery-grid">
        {"".join(glyph_cards_html)}
    </div>

    <div id="toast">SVG Copied to clipboard!</div>

    <script>
        function copySVG(glyphName) {{
            const card = document.getElementById('card-' + glyphName);
            const svg = card.querySelector('svg').outerHTML;
            navigator.clipboard.writeText(svg).then(() => {{
                showToast('SVG code for ' + glyphName + ' copied!');
            }});
        }}
        function inspectPorts(glyphName) {{
            alert('Inspecting multi-channel topological ports for: ' + glyphName);
        }}
        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => {{ t.style.display = 'none'; }}, 2500);
        }}
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated Interactive Glyph Gallery at {output_path}")

if __name__ == "__main__":
    generate_interactive_gallery("interactive_glyph_gallery.html")
