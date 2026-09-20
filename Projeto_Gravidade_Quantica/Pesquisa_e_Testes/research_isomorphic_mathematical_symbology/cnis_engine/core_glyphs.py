"""
CNIS Core Geometric AST and Parametric Combinator Engine
========================================================
Single source of truth for all mathematical glyphs.
Compiles deterministically to both SVG and Typst CeTZ.
Includes algebraic combinators for sequential composition (o) and parallel tensor (||).
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional, Union
import math
import json

# =========================================================================
# 1. GEOMETRIC PRIMITIVES (Single Source of Truth)
# =========================================================================

@dataclass
class Port:
    id: str
    label: str
    kind: str  # 'input', 'output', 'bidirectional'
    x: float
    y: float
    normal: Tuple[float, float]  # Unit normal vector pointing outward
    port_type: str = "T"

@dataclass
class VisualChannel:
    stroke_width: float = 2.0     # Channel 1: Tensorial weight / form degree
    hue: float = 210.0            # Channel 2: Chromatic hue (degrees in HSL)
    depth_layer: int = 0          # Channel 3: Depth layer z in {0, 1} for over/under crossings
    fill_opacity: float = 0.15

# Primitive Shape AST nodes
@dataclass
class GeomCircle:
    cx: float
    cy: float
    r: float
    stroke: Optional[str] = None
    fill: Optional[str] = None
    stroke_width: Optional[float] = None
    fill_opacity: Optional[float] = None

@dataclass
class GeomRect:
    x: float
    y: float
    w: float
    h: float
    rx: float = 0.0
    stroke: Optional[str] = None
    fill: Optional[str] = None
    stroke_width: Optional[float] = None
    fill_opacity: Optional[float] = None

@dataclass
class GeomLine:
    x1: float
    y1: float
    x2: float
    y2: float
    stroke: Optional[str] = None
    stroke_width: Optional[float] = None
    arrow_end: bool = False

@dataclass
class GeomArc:
    cx: float
    cy: float
    r: float
    start_deg: float
    stop_deg: float
    stroke: Optional[str] = None
    stroke_width: Optional[float] = None
    arrow_end: bool = False

@dataclass
class GeomCubicBezier:
    p0: Tuple[float, float]
    p1: Tuple[float, float]
    p2: Tuple[float, float]
    p3: Tuple[float, float]
    stroke: Optional[str] = None
    stroke_width: Optional[float] = None

@dataclass
class GeomAperture:
    """Real topological genus hole / Betti aperture."""
    cx: float
    cy: float
    r: float
    betti_label: str = "b_1"

@dataclass
class GeomText:
    x: float
    y: float
    text: str
    size: float = 12.0
    weight: str = "normal"
    fill: Optional[str] = None
    anchor: str = "middle"

GeomElement = Union[GeomCircle, GeomRect, GeomLine, GeomArc, GeomCubicBezier, GeomAperture, GeomText]

# =========================================================================
# 2. PARAMETRIC GLYPH DEFINITION
# =========================================================================

@dataclass
class ParametricGlyph:
    name: str
    symbol_latex: str
    category: str
    description: str
    autological_property: str
    channels: VisualChannel = field(default_factory=VisualChannel)
    ports: List[Port] = field(default_factory=list)
    elements: List[GeomElement] = field(default_factory=list)
    view_box: Tuple[float, float, float, float] = (-50, -50, 100, 100)

    # ---------------------------------------------------------------------
    # Algebraic Combinators: Sequential Composition (o) and Tensor (||)
    # ---------------------------------------------------------------------
    def compose_sequential(self, other: 'ParametricGlyph', glue_port_self: str, glue_port_other: str) -> 'ParametricGlyph':
        """Algebraic Combinator: Sequential composition (f o g) by port fusion."""
        new_name = f"{self.name}_circ_{other.name}"
        p_self = next((p for p in self.ports if p.id == glue_port_self), None)
        p_other = next((p for p in other.ports if p.id == glue_port_other), None)
        
        offset_y = 60.0
        shifted_other_elements = []
        for elem in other.elements:
            shifted_other_elements.append(self._shift_element(elem, 0.0, offset_y))
            
        combined_elements = list(self.elements) + shifted_other_elements
        # Add fusion bridge wire
        if p_self and p_other:
            combined_elements.append(
                GeomLine(p_self.x, p_self.y, p_other.x, p_other.y + offset_y, stroke="#d2640a", stroke_width=2.5)
            )
            
        remaining_ports = [p for p in self.ports if p.id != glue_port_self] + [
            Port(p.id, p.label, p.kind, p.x, p.y + offset_y, p.normal, p.port_type)
            for p in other.ports if p.id != glue_port_other
        ]
        
        return ParametricGlyph(
            name=new_name,
            symbol_latex=f"{self.symbol_latex} \\circ {other.symbol_latex}",
            category=self.category,
            description=f"Sequential composition of {self.name} and {other.name}",
            autological_property="Constructed via exact port fusion and functorial wire composition.",
            channels=self.channels,
            ports=remaining_ports,
            elements=combined_elements,
            view_box=(-60, -60, 120, 120 + offset_y)
        )

    def tensor_parallel(self, other: 'ParametricGlyph', separation_x: float = 70.0) -> 'ParametricGlyph':
        """Algebraic Combinator: Parallel tensor product (f || g)."""
        new_name = f"{self.name}_tensor_{other.name}"
        shift_x = separation_x
        shifted_other_elements = [self._shift_element(e, shift_x, 0.0) for e in other.elements]
        
        combined_ports = list(self.ports) + [
            Port(p.id, p.label, p.kind, p.x + shift_x, p.y, p.normal, p.port_type)
            for p in other.ports
        ]
        
        return ParametricGlyph(
            name=new_name,
            symbol_latex=f"{self.symbol_latex} \\otimes {other.symbol_latex}",
            category=self.category,
            description=f"Parallel monoidal tensor product of {self.name} and {other.name}",
            autological_property="Monoidal juxtaposition preserving independent strand topologies.",
            channels=self.channels,
            ports=combined_ports,
            elements=list(self.elements) + shifted_other_elements,
            view_box=(-50, -50, 100 + shift_x, 100)
        )

    @staticmethod
    def _shift_element(elem: GeomElement, dx: float, dy: float) -> GeomElement:
        if isinstance(elem, GeomCircle):
            return GeomCircle(elem.cx + dx, elem.cy + dy, elem.r, elem.stroke, elem.fill, elem.stroke_width, elem.fill_opacity)
        elif isinstance(elem, GeomRect):
            return GeomRect(elem.x + dx, elem.y + dy, elem.w, elem.h, elem.rx, elem.stroke, elem.fill, elem.stroke_width, elem.fill_opacity)
        elif isinstance(elem, GeomLine):
            return GeomLine(elem.x1 + dx, elem.y1 + dy, elem.x2 + dx, elem.y2 + dy, elem.stroke, elem.stroke_width, elem.arrow_end)
        elif isinstance(elem, GeomArc):
            return GeomArc(elem.cx + dx, elem.cy + dy, elem.r, elem.start_deg, elem.stop_deg, elem.stroke, elem.stroke_width, elem.arrow_end)
        elif isinstance(elem, GeomCubicBezier):
            p0 = (elem.p0[0] + dx, elem.p0[1] + dy)
            p1 = (elem.p1[0] + dx, elem.p1[1] + dy)
            p2 = (elem.p2[0] + dx, elem.p2[1] + dy)
            p3 = (elem.p3[0] + dx, elem.p3[1] + dy)
            return GeomCubicBezier(p0, p1, p2, p3, elem.stroke, elem.stroke_width)
        elif isinstance(elem, GeomAperture):
            return GeomAperture(elem.cx + dx, elem.cy + dy, elem.r, elem.betti_label)
        elif isinstance(elem, GeomText):
            return GeomText(elem.x + dx, elem.y + dy, elem.text, elem.size, elem.weight, elem.fill, elem.anchor)
        return elem

    # ---------------------------------------------------------------------
    # Deterministic Compilation: SVG Renderer
    # ---------------------------------------------------------------------
    def to_svg(self, width: int = 200, height: int = 200) -> str:
        vb_x, vb_y, vb_w, vb_h = self.view_box
        hsl_color = f"hsl({self.channels.hue}, 75%, 45%)"
        hsl_fill = f"hsl({self.channels.hue}, 85%, 60%)"
        
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x} {vb_y} {vb_w} {vb_h}" width="{width}" height="{height}" class="cnis-glyph" data-glyph="{self.name}">',
            '  <defs>',
            '    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            '      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#c01420"/>',
            '    </marker>',
            '    <filter id="depth-shadow" x="-20%" y="-20%" width="140%" height="140%">',
            '      <feDropShadow dx="2" dy="3" stdDeviation="2" flood-color="#000" flood-opacity="0.4"/>',
            '    </filter>',
            '  </defs>'
        ]
        
        for elem in self.elements:
            if isinstance(elem, GeomCircle):
                stroke = elem.stroke or hsl_color
                sw = elem.stroke_width if elem.stroke_width is not None else self.channels.stroke_width
                fill = elem.fill or hsl_fill
                fo = elem.fill_opacity if elem.fill_opacity is not None else self.channels.fill_opacity
                svg_parts.append(f'  <circle cx="{elem.cx}" cy="{elem.cy}" r="{elem.r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" fill-opacity="{fo}"/>')
            elif isinstance(elem, GeomRect):
                stroke = elem.stroke or hsl_color
                sw = elem.stroke_width if elem.stroke_width is not None else self.channels.stroke_width
                fill = elem.fill or hsl_fill
                fo = elem.fill_opacity if elem.fill_opacity is not None else self.channels.fill_opacity
                svg_parts.append(f'  <rect x="{elem.x}" y="{elem.y}" width="{elem.w}" height="{elem.h}" rx="{elem.rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" fill-opacity="{fo}"/>')
            elif isinstance(elem, GeomLine):
                stroke = elem.stroke or hsl_color
                sw = elem.stroke_width if elem.stroke_width is not None else self.channels.stroke_width
                marker = ' marker-end="url(#arrow)"' if elem.arrow_end else ''
                svg_parts.append(f'  <line x1="{elem.x1}" y1="{elem.y1}" x2="{elem.x2}" y2="{elem.y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{marker}/>')
            elif isinstance(elem, GeomArc):
                stroke = elem.stroke or hsl_color
                sw = elem.stroke_width if elem.stroke_width is not None else self.channels.stroke_width
                start_rad = math.radians(elem.start_deg)
                stop_rad = math.radians(elem.stop_deg)
                x1 = elem.cx + elem.r * math.cos(start_rad)
                y1 = elem.cy - elem.r * math.sin(start_rad)
                x2 = elem.cx + elem.r * math.cos(stop_rad)
                y2 = elem.cy - elem.r * math.sin(stop_rad)
                marker = ' marker-end="url(#arrow)"' if elem.arrow_end else ''
                svg_parts.append(f'  <path d="M {x1} {y1} A {elem.r} {elem.r} 0 0 0 {x2} {y2}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{marker}/>')
            elif isinstance(elem, GeomCubicBezier):
                stroke = elem.stroke or hsl_color
                sw = elem.stroke_width if elem.stroke_width is not None else self.channels.stroke_width
                svg_parts.append(f'  <path d="M {elem.p0[0]} {elem.p0[1]} C {elem.p1[0]} {elem.p1[1]}, {elem.p2[0]} {elem.p2[1]}, {elem.p3[0]} {elem.p3[1]}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>')
            elif isinstance(elem, GeomAperture):
                svg_parts.append(f'  <circle cx="{elem.cx}" cy="{elem.cy}" r="{elem.r}" fill="#ffffff" stroke="#c01420" stroke-width="2.5"/>')
                svg_parts.append(f'  <text x="{elem.cx}" y="{elem.cy + 4}" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#c01420" text-anchor="middle">{elem.betti_label}</text>')
            elif isinstance(elem, GeomText):
                fill_txt = elem.fill or hsl_color
                svg_parts.append(f'  <text x="{elem.x}" y="{elem.y}" font-family="system-ui, sans-serif" font-size="{elem.size}" font-weight="{elem.weight}" fill="{fill_txt}" text-anchor="{elem.anchor}">{elem.text}</text>')

        # Render Ports
        for port in self.ports:
            p_fill = "#0a2350" if port.kind == "input" else ("#a0141e" if port.kind == "output" else "#006e82")
            svg_parts.append(f'  <circle cx="{port.x}" cy="{port.y}" r="3.5" fill="{p_fill}" stroke="#ffffff" stroke-width="1.2"/>')

        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)

    # ---------------------------------------------------------------------
    # Deterministic Compilation: Typst CeTZ Renderer
    # ---------------------------------------------------------------------
    def to_typst_cetz(self) -> str:
        c = self.channels
        hue_deg = c.hue
        stroke_pt = c.stroke_width
        
        typst_lines = [
            f"// CNIS Autological Glyph: {self.name} ({self.symbol_latex})",
            f"// Category: {self.category}",
            f"// Autological Property: {self.autological_property}",
            f"#let draw_{self.name}(scale: 1.0) = cetz.canvas({{",
            f"  import cetz.draw: *",
            f"  let main-stroke = (paint: color.hsl({hue_deg}deg, 75%, 45%), thickness: {stroke_pt}pt)",
            f"  let fill-paint = color.hsl({hue_deg}deg, 85%, 60%, {c.fill_opacity * 100}%)",
            ""
        ]
        
        for elem in self.elements:
            if isinstance(elem, GeomCircle):
                typst_lines.append(f"  circle(({elem.cx * 0.05} * scale, {-elem.cy * 0.05} * scale), radius: {elem.r * 0.05} * scale, fill: fill-paint, stroke: main-stroke)")
            elif isinstance(elem, GeomRect):
                x1, y1 = elem.x * 0.05, -elem.y * 0.05
                x2, y2 = (elem.x + elem.w) * 0.05, -(elem.y + elem.h) * 0.05
                typst_lines.append(f"  rect(({x1} * scale, {y1} * scale), ({x2} * scale, {y2} * scale), radius: 3pt, fill: fill-paint, stroke: main-stroke)")
            elif isinstance(elem, GeomLine):
                x1, y1 = elem.x1 * 0.05, -elem.y1 * 0.05
                x2, y2 = elem.x2 * 0.05, -elem.y2 * 0.05
                mark_str = ', mark: (end: ">")' if elem.arrow_end else ''
                typst_lines.append(f"  line(({x1} * scale, {y1} * scale), ({x2} * scale, {y2} * scale), stroke: main-stroke{mark_str})")
            elif isinstance(elem, GeomArc):
                x, y = elem.cx * 0.05, -elem.cy * 0.05
                r = elem.r * 0.05
                mark_str = ', mark: (end: ">")' if elem.arrow_end else ''
                typst_lines.append(f"  arc(({x} * scale, {y} * scale), start: {elem.start_deg}deg, stop: {elem.stop_deg}deg, radius: {r} * scale, stroke: (paint: rgb(192, 20, 32), thickness: 2pt){mark_str})")
            elif isinstance(elem, GeomCubicBezier):
                p0 = f"({elem.p0[0]*0.05} * scale, {-elem.p0[1]*0.05} * scale)"
                p1 = f"({elem.p1[0]*0.05} * scale, {-elem.p1[1]*0.05} * scale)"
                p2 = f"({elem.p2[0]*0.05} * scale, {-elem.p2[1]*0.05} * scale)"
                p3 = f"({elem.p3[0]*0.05} * scale, {-elem.p3[1]*0.05} * scale)"
                typst_lines.append(f"  bezier({p0}, {p3}, {p1}, {p2}, stroke: main-stroke)")
            elif isinstance(elem, GeomAperture):
                x, y = elem.cx * 0.05, -elem.cy * 0.05
                r = elem.r * 0.05
                typst_lines.append(f"  circle(({x} * scale, {y} * scale), radius: {r} * scale, fill: white, stroke: 2pt + rgb(192, 20, 32))")
                typst_lines.append(f"  content(({x} * scale, {y} * scale), text(fill: rgb(192, 20, 32), weight: \"bold\", [${elem.betti_label}$]))")
            elif isinstance(elem, GeomText):
                x, y = elem.x * 0.05, -elem.y * 0.05
                typst_lines.append(f"  content(({x} * scale, {y} * scale), text(weight: \"bold\", [{elem.text}]))")

        typst_lines.append("})")
        return "\n".join(typst_lines)


# =========================================================================
# 3. CANONICAL GLYPH REGISTRY (Built from Pure Geometric AST)
# =========================================================================

class GlyphRegistry:
    @staticmethod
    def create_exterior_derivative(k: int = 1) -> ParametricGlyph:
        return ParametricGlyph(
            name="exterior_derivative",
            symbol_latex=r"\diff",
            category="Differential Geometry",
            description="Radial outward expansion ring mapping form grade k to k+1 with Stokes circulation boundary.",
            autological_property="The expanding concentric boundary geometry directly embodies the Stokes exactness boundary d^2 = 0.",
            channels=VisualChannel(stroke_width=2.5, hue=195.0, fill_opacity=0.2),
            elements=[
                GeomCircle(0, 0, 18.0),
                GeomCircle(0, 0, 34.0, fill_opacity=0.0),
                GeomText(0, 4, f"Ω^{k}", size=11, weight="bold", fill="#0a2350"),
                GeomLine(0, -18, 0, -34, stroke="#c01420", stroke_width=1.8, arrow_end=True),
                GeomLine(0, 18, 0, 34, stroke="#c01420", stroke_width=1.8, arrow_end=True),
                GeomLine(-18, 0, -34, 0, stroke="#c01420", stroke_width=1.8, arrow_end=True),
                GeomLine(18, 0, 34, 0, stroke="#c01420", stroke_width=1.8, arrow_end=True)
            ],
            ports=[
                Port("in_form", f"Ω^{k}", "input", 0, 18, (0, -1)),
                Port("out_form", f"Ω^{k+1}", "output", 0, 34, (0, 1))
            ]
        )

    @staticmethod
    def create_fourier_transform() -> ParametricGlyph:
        return ParametricGlyph(
            name="fourier_transform",
            symbol_latex=r"\mathcal{F}^\alpha",
            category="Harmonic Analysis",
            description="Metaplectic symplectic rotation in phase space (x <-> p) where F^2 = Parity and F^4 = Id.",
            autological_property="The glyph is an exact 90-degree continuous rotation frame mapping coordinate axes to momentum axes.",
            channels=VisualChannel(stroke_width=2.2, hue=350.0, fill_opacity=0.15),
            elements=[
                GeomLine(-38, 0, 38, 0, stroke="#8b949e", stroke_width=1.2),
                GeomLine(0, -38, 0, 38, stroke="#8b949e", stroke_width=1.2),
                GeomArc(0, 0, 26.0, 0, 90, stroke="#c01420", stroke_width=2.2, arrow_end=True),
                GeomText(34, 14, "x", size=10, weight="bold", fill="#0a2350"),
                GeomText(12, -32, "p", size=10, weight="bold", fill="#0a2350"),
                GeomCircle(24, 0, 5.0, stroke="#006e82", fill="#006e82", fill_opacity=0.6),
                GeomCircle(0, -24, 5.0, stroke="#c01420", fill="#c01420", fill_opacity=0.6),
                GeomText(16, -14, "π/2", size=9, weight="bold", fill="#c01420")
            ],
            ports=[
                Port("in_pos", "L²(x)", "input", 24, 0, (1, 0)),
                Port("out_mom", "L²(p)", "output", 0, -24, (0, -1))
            ]
        )

    @staticmethod
    def create_cohomology(betti: int = 1, k: int = 1) -> ParametricGlyph:
        return ParametricGlyph(
            name="cohomology",
            symbol_latex=rf"H^{k}(X)",
            category="Algebraic Topology",
            description="Cochain ladder where non-exactness manifests as a physical topological aperture of genus b_k.",
            autological_property="The symbol contains real topological holes matching the Betti number dim(ker d^k / im d^{k-1}).",
            channels=VisualChannel(stroke_width=2.5, hue=220.0, fill_opacity=0.1),
            elements=[
                GeomLine(-25, -38, -25, 38),
                GeomLine(25, -38, 25, 38),
                GeomLine(-25, 24, 25, 24),
                GeomLine(-25, -24, 25, -24),
                GeomLine(-25, 0, -12, 0),
                GeomLine(12, 0, 25, 0),
                GeomAperture(0, 0, 12.0, f"b_{k}"),
                GeomText(36, -20, f"Ω^{k+1}", size=9, weight="bold", fill="#0a2350"),
                GeomText(36, 4, f"Ω^{k}", size=9, weight="bold", fill="#c01420"),
                GeomText(36, 28, f"Ω^{k-1}", size=9, weight="bold", fill="#0a2350")
            ],
            ports=[
                Port("in_cochain", f"C^{k}", "input", 0, 38, (0, 1)),
                Port("out_cochain", f"H^{k}", "output", 0, -38, (0, -1))
            ]
        )

    @staticmethod
    def create_adjunction_snake() -> ParametricGlyph:
        return ParametricGlyph(
            name="category_adjunction",
            symbol_latex=r"F \dashv G",
            category="Category Theory",
            description="Adjunction unit-counit string diagram where triangle identity is a literal continuous snake removal.",
            autological_property="The zigzag curvature satisfies the topological snake move (epsilon F) o (F eta) = id_F.",
            channels=VisualChannel(stroke_width=2.8, hue=215.0, fill_opacity=0.0),
            elements=[
                GeomCubicBezier((-28, 32), (-28, -10), (0, -10), (0, 4), stroke="#58a6ff", stroke_width=2.8),
                GeomCubicBezier((0, 4), (0, 18), (28, 18), (28, -32), stroke="#58a6ff", stroke_width=2.8),
                GeomText(-14, -14, "ε", size=12, weight="bold", fill="#c01420"),
                GeomText(14, 24, "η", size=12, weight="bold", fill="#006e82"),
                GeomText(-28, 44, "F", size=10, weight="bold", fill="#0a2350"),
                GeomText(28, -40, "F", size=10, weight="bold", fill="#0a2350")
            ],
            ports=[
                Port("in_functor", "F", "input", -28, 32, (0, 1)),
                Port("out_functor", "F", "output", 28, -32, (0, -1))
            ]
        )

    @staticmethod
    def create_tensor_contraction() -> ParametricGlyph:
        return ParametricGlyph(
            name="tensor_contraction",
            symbol_latex=r"\odot",
            category="Multilinear Algebra",
            description="Direct port-to-port wire fusion eliminating index summation clutter.",
            autological_property="Contraction is physical topological wire fusion preserving trace and conservation invariants.",
            channels=VisualChannel(stroke_width=2.4, hue=160.0, fill_opacity=0.2),
            elements=[
                GeomRect(-28, -38, 56, 20, rx=4.0),
                GeomRect(-28, 18, 56, 20, rx=4.0),
                GeomText(0, -25, "T", size=11, weight="bold", fill="#0a2350"),
                GeomText(0, 31, "S", size=11, weight="bold", fill="#006e82"),
                GeomCubicBezier((14, -18), (14, 0), (-14, 0), (-14, 18), stroke="#d2640a", stroke_width=2.5),
                GeomCircle(0, 0, 4.5, stroke="#ffffff", fill="#d2640a", fill_opacity=1.0)
            ],
            ports=[
                Port("in_upper_1", "i₁", "input", -14, -38, (0, -1)),
                Port("in_upper_2", "i₂", "input", 14, -38, (0, -1)),
                Port("out_free_1", "j₁", "output", -14, -18, (0, 1)),
                Port("out_free_2", "l₁", "output", 14, 38, (0, 1))
            ]
        )

    @staticmethod
    def create_braided_crossing() -> ParametricGlyph:
        return ParametricGlyph(
            name="braided_crossing",
            symbol_latex=r"\beta_{X,Y}",
            category="Braided Monoidal Categories",
            description="Non-symmetric strand braiding with multi-channel over/under crossing depth layer.",
            autological_property="Over/under strand routing resolves the planarity obstruction, faithfully encoding B_n.",
            channels=VisualChannel(stroke_width=3.0, hue=275.0, depth_layer=1, fill_opacity=0.0),
            elements=[
                GeomLine(-26, 32, 26, -32, stroke="#bc8cff", stroke_width=3.0),  # Over-strand
                GeomLine(26, 32, 8, 8, stroke="#bc8cff", stroke_width=3.0),      # Under-strand (upper segment)
                GeomLine(-8, -8, -26, -32, stroke="#bc8cff", stroke_width=3.0),  # Under-strand (lower segment)
                GeomText(-26, 42, "X", size=10, weight="bold", fill="#6e1e8c"),
                GeomText(26, 42, "Y", size=10, weight="bold", fill="#6e1e8c"),
                GeomText(-26, -40, "Y", size=10, weight="bold", fill="#6e1e8c"),
                GeomText(26, -40, "X", size=10, weight="bold", fill="#6e1e8c")
            ],
            ports=[
                Port("in_1", "X", "input", -26, 32, (0, 1)),
                Port("in_2", "Y", "input", 26, 32, (0, 1)),
                Port("out_1", "Y", "output", -26, -32, (0, -1)),
                Port("out_2", "X", "output", 26, -32, (0, -1))
            ]
        )

    @staticmethod
    def create_clifford_fusion() -> ParametricGlyph:
        return ParametricGlyph(
            name="clifford_fusion",
            symbol_latex=r"\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}",
            category="Clifford Algebra & Spin Geometry",
            description="Anticommutative 180-degree strand swap collapsing into Minkowski metric projector.",
            autological_property="The symmetric sum of crossed paths cancels torsion and projects to the scalar metric channel.",
            channels=VisualChannel(stroke_width=2.8, hue=210.0, depth_layer=1, fill_opacity=0.15),
            elements=[
                GeomLine(-24, 30, 0, 0, stroke="#0a2350", stroke_width=2.5),
                GeomLine(24, 30, 0, 0, stroke="#0a2350", stroke_width=2.5),
                GeomCircle(0, 0, 6.0, stroke="#ffffff", fill="#d2640a", fill_opacity=1.0),
                GeomLine(0, 0, 0, -32, stroke="#d2640a", stroke_width=3.0, arrow_end=True),
                GeomText(0, -4, "η", size=10, weight="bold", fill="#ffffff"),
                GeomText(-26, 40, "γ^μ", size=10, weight="bold", fill="#0a2350"),
                GeomText(26, 40, "γ^ν", size=10, weight="bold", fill="#0a2350"),
                GeomText(0, -42, "2η^{μν}·id", size=10, weight="bold", fill="#d2640a")
            ],
            ports=[
                Port("in_mu", "γ^μ", "input", -24, 30, (0, 1)),
                Port("in_nu", "γ^ν", "input", 24, 30, (0, 1)),
                Port("out_metric", "2η^{μν}", "output", 0, -32, (0, -1))
            ]
        )

    @staticmethod
    def create_dirac_spinor() -> ParametricGlyph:
        return ParametricGlyph(
            name="dirac_spinor",
            symbol_latex=r"\Psi = \psi_L \oplus \psi_R",
            category="Relativistic Quantum Mechanics",
            description="Bipartite Weyl chirality bundle with invariant mass bridge coupling.",
            autological_property="Parallel left/right Weyl channels coupled by dynamic rest-mass cross-talk.",
            channels=VisualChannel(stroke_width=3.0, hue=195.0, fill_opacity=0.1),
            elements=[
                GeomLine(-20, -35, -20, 35, stroke="#006e82", stroke_width=3.0),
                GeomLine(20, -35, 20, 35, stroke="#c01420", stroke_width=3.0),
                GeomLine(-20, 0, 20, 0, stroke="#d2640a", stroke_width=2.4),
                GeomCircle(0, 0, 4.5, stroke="#ffffff", fill="#d2640a", fill_opacity=1.0),
                GeomText(-20, 44, "ψ_L", size=11, weight="bold", fill="#006e82"),
                GeomText(20, 44, "ψ_R", size=11, weight="bold", fill="#c01420"),
                GeomText(0, -8, "m", size=11, weight="bold", fill="#d2640a")
            ],
            ports=[
                Port("in_L", "ψ_L", "input", -20, -35, (0, -1)),
                Port("in_R", "ψ_R", "input", 20, -35, (0, -1)),
                Port("out_L", "ψ_L", "output", -20, 35, (0, 1)),
                Port("out_R", "ψ_R", "output", 20, 35, (0, 1))
            ]
        )

    @staticmethod
    def create_gauge_curvature_loop() -> ParametricGlyph:
        return ParametricGlyph(
            name="gauge_curvature_loop",
            symbol_latex=r"[D_\mu, D_\nu] = +ie F_{\mu\nu}",
            category="Gauge Field Theory",
            description="Non-Abelian holonomy loop generating Landé factor g=2.",
            autological_property="Closed curvature loop around spinor line producing exact magnetic moment coupling.",
            channels=VisualChannel(stroke_width=2.5, hue=350.0, fill_opacity=0.15),
            elements=[
                GeomLine(-38, 0, 38, 0, stroke="#0a2350", stroke_width=2.8),
                GeomArc(0, 0, 22.0, 180, 0, stroke="#c01420", stroke_width=2.2, arrow_end=True),
                GeomCircle(0, 12, 5.0, stroke="#ffffff", fill="#d2640a", fill_opacity=1.0),
                GeomText(0, 14, "σ", size=8, weight="bold", fill="#ffffff"),
                GeomText(-36, -10, "Ψ", size=10, weight="bold", fill="#0a2350"),
                GeomText(36, -10, "Ψ", size=10, weight="bold", fill="#0a2350"),
                GeomText(0, 32, "F_{μν}", size=9, weight="bold", fill="#c01420")
            ],
            ports=[
                Port("in_spinor", "Ψ", "input", -38, 0, (-1, 0)),
                Port("out_spinor", "Ψ", "output", 38, 0, (1, 0))
            ]
        )

    @staticmethod
    def create_gordon_current_split() -> ParametricGlyph:
        return ParametricGlyph(
            name="gordon_current_split",
            symbol_latex=r"J^\mu = J^\mu_{\text{conv}} + J^\mu_{\text{spin}}",
            category="Relativistic Electrodynamics",
            description="Algebraic Gordon decomposition of conserved current into convection and spin vortex.",
            autological_property="Bifurcation into longitudinal transport line and closed divergence-free vortex.",
            channels=VisualChannel(stroke_width=2.6, hue=160.0, fill_opacity=0.2),
            elements=[
                GeomLine(-36, 0, -10, 0, stroke="#0a2350", stroke_width=2.8, arrow_end=True),
                GeomCircle(-10, 0, 4.0, stroke="#ffffff", fill="#d2640a", fill_opacity=1.0),
                GeomLine(-10, 0, 25, 18, stroke="#006e82", stroke_width=2.2, arrow_end=True),
                GeomLine(-10, 0, 25, -18, stroke="#c01420", stroke_width=2.2, arrow_end=True),
                GeomArc(12, -18, 6.0, -90, 270, stroke="#c01420", stroke_width=1.5, arrow_end=True),
                GeomText(-30, 10, "J^μ", size=10, weight="bold", fill="#0a2350"),
                GeomText(28, 24, "J^μ_{conv}", size=9, weight="bold", fill="#006e82"),
                GeomText(28, -26, "J^μ_{spin}", size=9, weight="bold", fill="#c01420")
            ],
            ports=[
                Port("in_total", "J^μ", "input", -36, 0, (-1, 0)),
                Port("out_conv", "J^μ_{conv}", "output", 25, 18, (1, 0)),
                Port("out_spin", "J^μ_{spin}", "output", 25, -18, (1, 0))
            ]
        )

    @staticmethod
    def create_riemann_holonomy() -> ParametricGlyph:
        return ParametricGlyph(
            name="riemann_holonomy",
            symbol_latex=r"[\nabla_\mu, \nabla_\nu] V^\rho = R^\rho{}_{\sigma\mu\nu} V^\sigma",
            category="Differential Geometry & General Relativity",
            description="Quadrilateral loop holonomy commutator defect measuring spacetime curvature.",
            autological_property="Closed quadrilateral boundary integral yielding an angular rotation defect vector.",
            channels=VisualChannel(stroke_width=2.8, hue=210.0, fill_opacity=0.15),
            elements=[
                GeomRect(-24, -18, 48, 36, rx=4.0, stroke="#0a2350", stroke_width=2.4),
                GeomCircle(0, 0, 10.0, stroke="#0a2350", fill="#d2640a", fill_opacity=1.0),
                GeomText(0, 3, "R", size=11, weight="bold", fill="#0a2350"),
                GeomLine(-24, -18, -12, -6, stroke="#c01420", stroke_width=2.2, arrow_end=True),
                GeomLine(-24, -18, -10, -14, stroke="#006e82", stroke_width=2.2, arrow_end=True),
                GeomText(-26, 26, "Δx^μ", size=9, weight="bold", fill="#0a2350"),
                GeomText(26, -26, "Δx^ν", size=9, weight="bold", fill="#0a2350")
            ],
            ports=[
                Port("in_vec", "V_in", "input", -24, -18, (-1, -1)),
                Port("out_vec", "V_out", "output", -10, -14, (1, 1))
            ]
        )

    @staticmethod
    def create_einstein_tensor_gate() -> ParametricGlyph:
        return ParametricGlyph(
            name="einstein_tensor_gate",
            symbol_latex=r"G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu}",
            category="General Relativity",
            description="Trace-reversal gate ensuring exact divergence cancellation via contracted Bianchi identity.",
            autological_property="Port-to-port subtraction node enforcing zero boundary flux divergence ∇^μ G_{μν} ≡ 0.",
            channels=VisualChannel(stroke_width=3.0, hue=350.0, fill_opacity=0.2),
            elements=[
                GeomRect(-28, -20, 56, 40, rx=6.0, stroke="#c01420", fill="#c01420", fill_opacity=0.1, stroke_width=2.5),
                GeomText(0, 8, "G_{μν}", size=13, weight="bold", fill="#c01420"),
                GeomText(0, -10, "∇^μ G_{μν} ≡ 0", size=9, weight="bold", fill="#0a2350")
            ],
            ports=[
                Port("in_ricci", "R_{μν}", "input", -28, 0, (-1, 0)),
                Port("out_einstein", "G_{μν}", "output", 28, 0, (1, 0))
            ]
        )

    @staticmethod
    def create_einstein_functorial_coupling() -> ParametricGlyph:
        return ParametricGlyph(
            name="einstein_functorial_coupling",
            symbol_latex=r"\Phi_{\mathrm{EH}} : \mathbf{G} \overset{\kappa}{\Longleftrightarrow} \mathbf{T}",
            category="General Relativity & Field Theory",
            description="Functorial bridge wire coupling spacetime geometry variety to stress-energy fiber bundle.",
            autological_property="Bi-directional information channel where matter curves geometry and geometry guides matter.",
            channels=VisualChannel(stroke_width=3.2, hue=35.0, fill_opacity=0.15),
            elements=[
                GeomRect(-42, 12, 84, 24, rx=4.0, stroke="#006e82", fill="#006e82", fill_opacity=0.1, stroke_width=2.0),
                GeomText(0, 24, "Geometry G", size=10, weight="bold", fill="#006e82"),
                GeomLine(0, 12, 0, -12, stroke="#d2640a", stroke_width=3.5, arrow_end=True),
                GeomCircle(0, 0, 6.0, stroke="#ffffff", fill="#d2640a", fill_opacity=1.0),
                GeomText(0, 2, "κ", size=9, weight="bold", fill="#ffffff"),
                GeomRect(-42, -36, 84, 24, rx=4.0, stroke="#c01420", fill="#c01420", fill_opacity=0.1, stroke_width=2.0),
                GeomText(0, -24, "Matter T", size=10, weight="bold", fill="#c01420")
            ],
            ports=[
                Port("port_geom", "G", "bidirectional", 0, 36, (0, 1)),
                Port("port_matter", "T", "bidirectional", 0, -36, (0, -1))
            ]
        )

    @classmethod
    def get_standard_suite(cls) -> Dict[str, ParametricGlyph]:
        return {
            "exterior_derivative": cls.create_exterior_derivative(),
            "fourier_transform": cls.create_fourier_transform(),
            "cohomology": cls.create_cohomology(),
            "category_adjunction": cls.create_adjunction_snake(),
            "tensor_contraction": cls.create_tensor_contraction(),
            "braided_crossing": cls.create_braided_crossing(),
            "clifford_fusion": cls.create_clifford_fusion(),
            "dirac_spinor": cls.create_dirac_spinor(),
            "gauge_curvature_loop": cls.create_gauge_curvature_loop(),
            "gordon_current_split": cls.create_gordon_current_split(),
            "riemann_holonomy": cls.create_riemann_holonomy(),
            "einstein_tensor_gate": cls.create_einstein_tensor_gate(),
            "einstein_functorial_coupling": cls.create_einstein_functorial_coupling()
        }


