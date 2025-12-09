#!/usr/bin/env python3
"""
xml2altimetria.py

Genera altimetria.svg a partir de circuitoEsquema.xml (XPath + xml.etree.ElementTree obligatorio).

Uso:
    python xml2altimetria.py
    python xml2altimetria.py --input circuitoEsquema.xml --out altimetria.svg

Salida:
    - altimetria.svg
"""

import argparse
import math
import xml.etree.ElementTree as ET
from typing import List, Tuple, Optional

def parse_args():
    p = argparse.ArgumentParser(description="Generar altimetria.svg desde circuitoEsquema.xml")
    p.add_argument('--input', '-i', default='circuitoEsquema.xml', help='Archivo XML de entrada')
    p.add_argument('--out', '-o', default='altimetria.svg', help='Archivo SVG de salida')
    return p.parse_args()


def get_namespace(root_tag: str) -> Optional[str]:
    """Extrae la URI del namespace del tag de la forma '{namespace}tag'"""
    if root_tag.startswith("{"):
        end = root_tag.find("}")
        if end != -1:
            return root_tag[1:end]
    return None


def read_points_from_xml(xml_path: str) -> List[Tuple[float, float]]:
    """
    Lee el XML y devuelve una lista de (distancia_acumulada_m, altitud_m).
    Usa expresiones XPath con prefijo ns.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns_uri = get_namespace(root.tag) or ''
    ns = {'ns': ns_uri} if ns_uri else {}

    points: List[Tuple[float, float]] = []

    # 1) obtener el origen (si existe) -> tratamos como distancia 0
    origen_nodes = root.findall('.//ns:origen', ns) if ns else root.findall('.//origen')
    if origen_nodes:
        o = origen_nodes[0]
        alt_el = o.find('ns:altitudGeo', ns) if ns else o.find('altitudGeo')
        if alt_el is not None and alt_el.text:
            try:
                alt0 = float(alt_el.text.strip())
            except Exception:
                alt0 = 0.0
            points.append((0.0, alt0))

    # 2) recorrer tramos y sumar distancias; por cada tramo tomar altitud del fin
    tramo_nodes = root.findall('.//ns:tramos/ns:tramo', ns) if ns else root.findall('.//tramos/tramo')
    distancia_acum = 0.0
    for t in tramo_nodes:
        # distancia del tramo (en m)
        dist_el = t.find('ns:distancia', ns) if ns else t.find('distancia')
        try:
            d = float(dist_el.text.strip()) if dist_el is not None and dist_el.text else 0.0
        except Exception:
            d = 0.0
        distancia_acum += d

        # altitud del final del tramo
        fin = t.find('ns:fin', ns) if ns else t.find('fin')
        alt_el = fin.find('ns:altitudGeo', ns) if (fin is not None and ns) else (fin.find('altitudGeo') if fin is not None else None)
        try:
            alt = float(alt_el.text.strip()) if alt_el is not None and alt_el.text else 0.0
        except Exception:
            alt = 0.0

        points.append((distancia_acum, alt))

    return points


class SvgWriter:
    """
    Clase mínima para generar un SVG simple.
    No depende de bibliotecas externas.
    """
    def __init__(self, width: int = 1200, height: int = 400, margin: int = 50):
        self.width = width
        self.height = height
        self.margin = margin
        self.content: List[str] = []

    def header(self, title="Altimetría"):
        head = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
            f'<title>{title}</title>',
            f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="white" />'
        ]
        self.content.extend(head)

    def footer(self):
        self.content.append('</svg>')

    def add(self, s: str):
        self.content.append(s)

    def save(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.content))
        print(f"SVG guardado: {filename}")


def build_profile_svg(points: List[Tuple[float, float]], svg_path: str, width=1200, height=400, margin=60):
    """
    Construye un SVG con:
    - eje X: distancia (m)
    - eje Y: altitud (m)
    - polyline para el perfil y polígono rellenado para "suelo"
    - marcas y etiquetas (ticks)
    - textos verticales y horizontales
    """
    if not points:
        raise ValueError("No hay puntos para construir el perfil.")

    # Separar distancias y altitudes
    dists = [p[0] for p in points]
    alts = [p[1] for p in points]

    x_min, x_max = min(dists), max(dists)
    y_min, y_max = min(alts), max(alts)

    # Añadir un poco de margen vertical para estética
    y_pad = max(1.0, (y_max - y_min) * 0.08)
    y_min_plot = y_min - y_pad
    y_max_plot = y_max + y_pad

    svg = SvgWriter(width=width, height=height, margin=margin)
    svg.header(title="Altimetría del circuito")

    plot_w = width - 2 * margin
    plot_h = height - 2 * margin

    def map_x(d):
        if x_max == x_min:
            return margin + plot_w / 2
        return margin + ((d - x_min) / (x_max - x_min)) * plot_w

    def map_y(h):
        # invertimos: altitudes mayores -> menor y en SVG
        if y_max_plot == y_min_plot:
            return margin + plot_h / 2
        return margin + (1.0 - ((h - y_min_plot) / (y_max_plot - y_min_plot))) * plot_h

    # Dibujar ejes
    # Eje X (horizontal) en la parte inferior del área de plot
    x_axis_y = margin + plot_h + 0  # justo al final del plot
    svg.add(f'<line x1="{margin}" y1="{x_axis_y}" x2="{margin + plot_w}" y2="{x_axis_y}" stroke="black" stroke-width="1"/>')
    # Eje Y (vertical) en margen izquierdo
    svg.add(f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{margin + plot_h}" stroke="black" stroke-width="1"/>')

    # Grid y ticks - Y (altitud)
    # decidir paso de altitud (aprox 6-8 marcas)
    desired_ticks = 7
    raw_step = (y_max_plot - y_min_plot) / desired_ticks
    # normalizar paso a un valor "agradable"
    def nice_number(x):
        exp = math.floor(math.log10(x)) if x > 0 else 0
        frac = x / (10 ** exp)
        if frac < 1.5:
            nice = 1
        elif frac < 3:
            nice = 2
        elif frac < 7:
            nice = 5
        else:
            nice = 10
        return nice * (10 ** exp)

    y_step = nice_number(raw_step) if raw_step > 0 else 1.0
    y_start = math.floor(y_min_plot / y_step) * y_step
    y_end = math.ceil(y_max_plot / y_step) * y_step

    for y in frange(y_start, y_end + 0.0001, y_step):
        yy = map_y(y)
        # línea horizontal de grid ligera
        svg.add(f'<line x1="{margin}" y1="{yy}" x2="{margin + plot_w}" y2="{yy}" stroke="#e0e0e0" stroke-width="1"/>')
        # tick y label (a la izquierda)
        svg.add(f'<text x="{margin - 8}" y="{yy+3}" font-size="12" text-anchor="end">{format_number(y)}</text>')

    # Grid y ticks - X (distancia)
    # 5 marcas en X aproximadamente
    x_ticks = 6
    if x_max - x_min <= 0:
        x_step = 1
    else:
        x_step_raw = (x_max - x_min) / (x_ticks - 1)
        x_step = nice_number(x_step_raw)

    x_start = math.floor(x_min / x_step) * x_step
    x_end = math.ceil(x_max / x_step) * x_step
    for x in frange(x_start, x_end + 0.0001, x_step):
        xx = map_x(x)
        # línea vertical ligera
        svg.add(f'<line x1="{xx}" y1="{margin}" x2="{xx}" y2="{margin + plot_h}" stroke="#f0f0f0" stroke-width="1"/>')
        # tick label abajo
        svg.add(f'<text x="{xx}" y="{x_axis_y + 16}" font-size="12" text-anchor="middle">{format_number(x)} m</text>')

    # Construir puntos para polyline
    poly_points = []
    for d, h in points:
        x = map_x(d)
        y = map_y(h)
        poly_points.append(f'{x:.2f},{y:.2f}')

    poly_str = " ".join(poly_points)

    # También construir polígono cerrado para "relleno suelo"
    # Añadimos punto final en (x_max, bottom) y punto inicial (x_min, bottom)
    bottom_y = map_y(y_min_plot)  # coordenada y del "suelo"
    polygon_points = list(poly_points)  # copia de la cadena de puntos como strings
    # append final bottom and start bottom to close shape
    if polygon_points:
        last_x = map_x(x_max)
        first_x = map_x(x_min)
        polygon_points.append(f'{last_x:.2f},{bottom_y:.2f}')
        polygon_points.append(f'{first_x:.2f},{bottom_y:.2f}')
    polygon_str = " ".join(polygon_points)

    # Relleno del perfil (suelo)
    svg.add(f'<polygon points="{polygon_str}" fill="#d6eaf8" stroke="none" opacity="0.9"/>')

    # Dibujar la línea del perfil encima
    svg.add(f'<polyline points="{poly_str}" fill="none" stroke="#1f77b4" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')

    # Marcar puntos con círculos y etiquetas de altitud cada N puntos (por ej cada 5% o cada 10 puntos)
    n = len(points)
    label_every = max(1, n // 12)
    for idx, (d, h) in enumerate(points):
        x = map_x(d)
        y = map_y(h)
        svg.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" fill="#ff4500" />')
        if idx % label_every == 0 or idx == n-1 or idx == 0:
            # etiqueta horizontal
            svg.add(f'<text x="{x+6:.2f}" y="{y+4:.2f}" font-size="11" text-anchor="start">{format_number(h)} m</text>')

    # Título y anotaciones
    svg.add(f'<text x="{width/2:.1f}" y="{margin/2:.1f}" font-size="16" text-anchor="middle">Altimetría del circuito</text>')
    svg.add(f'<text x="{margin/2:.1f}" y="{height/2:.1f}" font-size="12" transform="rotate(-90 {margin/2:.1f},{height/2:.1f})" text-anchor="middle">Altitud (m)</text>')
    svg.add(f'<text x="{width - margin/1.5:.1f}" y="{height - margin/6:.1f}" font-size="12" text-anchor="end">Distancia (m)</text>')

    svg.footer()
    svg.save(svg_path)


def frange(start, stop, step):
    """Generador de punto flotante como range."""
    x = start
    # evitar problemas con precisión acumulada usando contador
    if step == 0:
        return
    count = 0
    # prevenir loop infinito:
    max_iters = int(abs((stop - start) / step)) + 5
    while (step > 0 and x <= stop + 1e-9) or (step < 0 and x >= stop - 1e-9):
        if count > max_iters:
            break
        yield x
        x += step
        count += 1


def format_number(x: float) -> str:
    """Formatea números: si es entero muestra sin decimales, si no con 1 decimal razonable."""
    if abs(x - round(x)) < 1e-6:
        return f"{int(round(x))}"
    else:
        return f"{x:.1f}"


def main():
    args = parse_args()
    try:
        points = read_points_from_xml(args.input)
    except ET.ParseError as e:
        print("Error parseando XML:", e)
        return
    except FileNotFoundError:
        print("No se encuentra el archivo:", args.input)
        return

    if not points:
        print("No se han encontrado puntos de altitud en el XML.")
        return

    # Si el primer punto tiene distancia > 0 (no hay origen), opcionalmente insertamos punto 0 con la alt de primer fin
    if points[0][0] != 0.0:
        # insertar un punto inicial en 0 con la altitud del primer punto
        alt0 = points[0][1]
        points.insert(0, (0.0, alt0))

    svg_out = args.out
    build_profile_svg(points, svg_out)

if __name__ == "__main__":
    main()
