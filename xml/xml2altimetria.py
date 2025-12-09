import xml.etree.ElementTree as ET

class Svg(object):
    """
    Genera archivos SVG con rectángulos, círculos, líneas, polilíneas y texto
    @version 1.1 (Corregido: incluye addCircle y atributos estándar)
    """
    def __init__(self):
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")
        # Definimos el tamaño del lienzo (canvas)
        self.raiz.attrib['width'] = "1000"
        self.raiz.attrib['height'] = "500"
        self.raiz.attrib['viewBox'] = "0 0 1000 500"
        # Fondo blanco
        ET.SubElement(self.raiz, 'rect', x="0", y="0", width="1000", height="500", fill="white")

    def addRect(self, x, y, width, height, fill, stroke_width, stroke):
        ET.SubElement(self.raiz, 'rect',
                      x=str(x), y=str(y),
                      width=str(width), height=str(height),
                      fill=fill,
                      **{'stroke-width': str(stroke_width)},
                      stroke=stroke)

    # ESTE ES EL MÉTODO QUE FALTABA
    def addCircle(self, cx, cy, r, fill, stroke="none", stroke_width="0"):
        ET.SubElement(self.raiz, 'circle',
                      cx=str(cx), cy=str(cy),
                      r=str(r),
                      fill=fill,
                      stroke=stroke,
                      **{'stroke-width': str(stroke_width)})

    def addLine(self, x1, y1, x2, y2, stroke, stroke_width):
        ET.SubElement(self.raiz, 'line',
                      x1=str(x1), y1=str(y1),
                      x2=str(x2), y2=str(y2),
                      stroke=stroke,
                      **{'stroke-width': str(stroke_width)})

    def addPolyline(self, points, stroke, stroke_width, fill):
        ET.SubElement(self.raiz, 'polyline',
                      points=points,
                      stroke=stroke,
                      **{'stroke-width': str(stroke_width)},
                      fill=fill)

    def addText(self, texto, x, y, font_family, font_size, fill="black"):
        t = ET.SubElement(self.raiz, 'text',
                          x=str(x), y=str(y),
                          **{'font-family': font_family},
                          **{'font-size': str(font_size)},
                          fill=fill)
        t.text = texto

    def escribir(self, nombreArchivoSVG):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG, encoding='utf-8', xml_declaration=True)

def main():
    nombreSVG = "altimetria.svg"
    archivoXML = "circuitoEsquema.xml"
    
    print(f"Leyendo {archivoXML}...")

    try:
        arbolXML = ET.parse(archivoXML)
        raizXML = arbolXML.getroot()
        
        ns = {'ns': 'http://www.uniovi.es/'} 

        nombre_circuito = raizXML.find('ns:nombre', ns).text
        
        alt_inicial = float(raizXML.find('ns:origen/ns:altitudGeo', ns).text)
        
        puntos_grafica = [] 
        distancia_acumulada = 0.0
        
        puntos_grafica.append((distancia_acumulada, alt_inicial))

        tramos = raizXML.findall('ns:tramos/ns:tramo', ns)
        for tramo in tramos:
            dist = float(tramo.find('ns:distancia', ns).text)
            alt = float(tramo.find('ns:fin/ns:altitudGeo', ns).text)
            
            distancia_acumulada += dist
            puntos_grafica.append((distancia_acumulada, alt))

        ancho_canvas = 1000
        alto_canvas = 500
        margen_x = 50
        margen_y = 50
        
        max_dist = puntos_grafica[-1][0] 
        altitudes = [p[1] for p in puntos_grafica]
        min_alt = min(altitudes)
        max_alt = max(altitudes)
        diff_alt = max_alt - min_alt if max_alt != min_alt else 1
        
        scale_x = (ancho_canvas - 2 * margen_x) / max_dist
        scale_y = (alto_canvas - 2 * margen_y) / diff_alt

        print(f"Circuito: {nombre_circuito}")
        print(f"Puntos procesados: {len(puntos_grafica)}")

        coords_svg = []
        polyline_string = ""
        
        for dist, alt in puntos_grafica:
            px = margen_x + (dist * scale_x)
            py = (alto_canvas - margen_y) - ((alt - min_alt) * scale_y)
            coords_svg.append((px, py))
            polyline_string += f"{px},{py} "

        suelo_y = alto_canvas - margen_y
        polygon_string = polyline_string + f"{coords_svg[-1][0]},{suelo_y} {coords_svg[0][0]},{suelo_y} {coords_svg[0][0]},{coords_svg[0][1]}"

        miSVG = Svg()

        miSVG.addText(f"Altimetría: {nombre_circuito}", 
                      margen_x, margen_y - 20, "Arial", 24, "darkblue")

        miSVG.addPolyline(polygon_string, "none", 0, "lightgrey")

        miSVG.addPolyline(polyline_string, "red", 3, "none")

        miSVG.addLine(margen_x, suelo_y, ancho_canvas - margen_x, suelo_y, "black", 2) # X
        miSVG.addLine(margen_x, margen_y, margen_x, suelo_y, "black", 2) # Y

        for i in range(0, int(max_dist) + 1, 1000):
            px = margen_x + (i * scale_x)
            miSVG.addLine(px, suelo_y, px, suelo_y + 5, "black", 1)
            miSVG.addText(f"{i//1000}km", px - 10, suelo_y + 20, "Arial", 10)

        py_min = suelo_y 
        miSVG.addText(f"{min_alt:.1f}m", 5, py_min, "Arial", 10)
        
        py_max = (alto_canvas - margen_y) - ((max_alt - min_alt) * scale_y)
        miSVG.addLine(margen_x - 5, py_max, margen_x, py_max, "black", 1)
        miSVG.addText(f"{max_alt:.1f}m", 5, py_max + 5, "Arial", 10)

        miSVG.addText("Salida", coords_svg[0][0], coords_svg[0][1] - 10, "Arial", 10, "green")
        miSVG.addCircle(coords_svg[0][0], coords_svg[0][1], 4, "green")

        miSVG.escribir(nombreSVG)
        print(f"Creado el archivo: {nombreSVG}")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()