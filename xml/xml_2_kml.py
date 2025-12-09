import sys
import os
import argparse
import xml.etree.ElementTree as ET
from typing import List, Tuple

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False


def parse_args():
    p = argparse.ArgumentParser(description='Convertir circuitoEsquema.xml a circuito.kml y planimetria.pdf')
    p.add_argument('--input', '-i', default='circuitoEsquema.xml', help='Archivo XML de entrada')
    p.add_argument('--bg-image', '-b', default=None, help='Imagen de fondo para la planimetría (opcional)')
    return p.parse_args()


# --- Plantilla KML ---
def prologoKML(archivo, nombre):
    archivo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    archivo.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    archivo.write('<Document>\n')
    archivo.write('<Placemark>\n')
    archivo.write('<name>{}</name>'.format(nombre))
    archivo.write('<LineString>\n')
    archivo.write('<extrude>1</extrude>\n')
    archivo.write('<tessellate>1</tessellate>\n')
    archivo.write('<coordinates>\n')


def epilogoKML(archivo):
    archivo.write('</coordinates>\n')
    archivo.write('<altitudeMode>relativeToGround</altitudeMode>\n')
    archivo.write('</LineString>\n')
    archivo.write("<Style id='lineaRoja'>\n")
    archivo.write('<LineStyle>\n')
    archivo.write('<color>#ff0000ff</color>\n')
    archivo.write('<width>5</width>\n')
    archivo.write('</LineStyle>\n')
    archivo.write('</Style>\n')
    archivo.write('</Placemark>\n')
    archivo.write('</Document>\n')
    archivo.write('</kml>\n')


# --- Extracción de coordenadas ---
def extract_origin(root: ET.Element) -> list[tuple[float, float, float]]:
    ns = {'ns': 'http://www.uniovi.es/'}
    coords = []
    origen_nodes = root.findall('.//ns:origen', ns)
    for o in origen_nodes:
        lon_el = o.find('ns:longitudGeo', ns)
        lat_el = o.find('ns:latitudGeo', ns)
        alt_el = o.find('ns:altitudGeo', ns)
        try:
            lon = float(lon_el.text.strip()) if lon_el is not None and lon_el.text else None
            lat = float(lat_el.text.strip()) if lat_el is not None and lat_el.text else None
            alt = float(alt_el.text.strip()) if alt_el is not None and alt_el.text else 0.0
            if lon is not None and lat is not None:
                coords.append((lon, lat, alt))
        except Exception:
            continue
    return coords


def extract_puntos_final(root: ET.Element):
    ns = {'ns': 'http://www.uniovi.es/'}
    coords = []
    tramo_nodes = root.findall('.//ns:tramos/ns:tramo', ns)
    for t in tramo_nodes:
        pf = t.find('ns:fin', ns)
        if pf is None:
            continue
        lon_el = pf.find('ns:longitudGeo', ns)
        lat_el = pf.find('ns:latitudGeo', ns)
        alt_el = pf.find('ns:altitudGeo', ns)
        try:
            lon = float(lon_el.text.strip()) if lon_el is not None and lon_el.text else None
            lat = float(lat_el.text.strip()) if lat_el is not None and lat_el.text else None
            alt = float(alt_el.text.strip()) if alt_el is not None and alt_el.text else 0.0
            if lon is not None and lat is not None:
                coords.append((lon, lat, alt))
        except Exception:
            continue
    return coords


# --- Generar KML ---
def write_kml(coords: List[Tuple[float, float, float]], output='circuito.kml', nombre='circuito'):
    with open(output, 'w', encoding='utf-8') as f:
        prologoKML(f, nombre)
        for lon, lat, alt in coords:
            f.write(f'          {lon},{lat},{alt}\n')  # línea por coordenada
        epilogoKML(f)
    print('KML generado:', output)


# --- Generar planimetría PDF ---
def generate_planimetria_pdf(coords: List[Tuple[float, float, float]], output_pdf='planimetria.pdf', bg_image: str = None):
    if not MATPLOTLIB_AVAILABLE:
        print('matplotlib no disponible: no se generará planimetria.pdf')
        return
    if not coords:
        print('No hay coordenadas para dibujar la planimetría')
        return

    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]

    with PdfPages(output_pdf) as pdf:
        fig, ax = plt.subplots(figsize=(8, 6))

        # Imagen de fondo opcional
        if bg_image and os.path.exists(bg_image):
            try:
                img = plt.imread(bg_image)
                ax.imshow(img, extent=[min(lons)-0.001, max(lons)+0.001, min(lats)-0.001, max(lats)+0.001])
            except Exception:
                print('No se pudo cargar la imagen de fondo:', bg_image)

        ax.plot(lons, lats, marker='o', color='red')
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_title('Planimetría del circuito')
        ax.grid(True)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

    print('PDF de planimetría generado:', output_pdf)


# --- Función principal ---
def main():
    args = parse_args()
    input_xml = args.input

    if not os.path.exists(input_xml):
        print('Error: no se encuentra el archivo de entrada:', input_xml, file=sys.stderr)
        sys.exit(2)

    try:
        tree = ET.parse(input_xml)
    except ET.ParseError as e:
        print('Error parseando XML:', e, file=sys.stderr)
        sys.exit(3)

    root = tree.getroot()

    coords: List[Tuple[float, float, float]] = []

    origen = extract_origin(root)
    if origen:
        coords.extend(origen)

    puntos = extract_puntos_final(root)
    coords.extend(puntos)

    if not coords:
        print('No se encontraron coordenadas en el XML.', file=sys.stderr)
        sys.exit(4)

    nombre_doc = os.path.splitext(os.path.basename(input_xml))[0]
    write_kml(coords, output='circuito.kml', nombre=nombre_doc)

    generate_planimetria_pdf(coords, output_pdf='planimetria.pdf', bg_image=args.bg_image)


if __name__ == '__main__':
    main()