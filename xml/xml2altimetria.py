import xml.etree.ElementTree as ET

class Svg(object):
    """
    Clase para generar archivos SVG
    """
    def __init__(self):
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")
        self.raiz.attrib['width'] = "1000"
        self.raiz.attrib['height'] = "500"
        self.raiz.attrib['viewBox'] = "0 0 1000 500"
        ET.SubElement(self.raiz, 'rect', x="0", y="0", width="1000", height="500", fill="white")

    def addRect(self, x, y, width, height, fill, stroke_width, stroke):
        ET.SubElement(self.raiz, 'rect',
                      x=str(x), y=str(y),
                      width=str(width), height=str(height),
                      fill=fill,
                      **{'stroke-width': str(stroke_width)},
                      stroke=stroke)

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


class ProcesadorAltimetria(object):
    """
    Clase para procesar las rutas del XML y generar los SVG de altimetria
    """
    def __init__(self, archivoXML):
        self.__archivoXML = archivoXML
        self.__ns = {'ns': 'http://www.uniovi.es'}
        self.__nombres_svg = [
            "altimetria_medulas.svg",
            "altimetria_catedral.svg",
            "altimetria_camino.svg"
        ]

    def procesar(self):
        try:
            arbolXML = ET.parse(self.__archivoXML)
            raizXML = arbolXML.getroot()

            # XPath para obtener todas las rutas
            rutas = raizXML.findall('ns:ruta', self.__ns)

            for i, ruta in enumerate(rutas):
                self.__procesarAltimetria(ruta, self.__nombres_svg[i])

        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo {self.__archivoXML}")
        except AttributeError as e:
            print(f"Error de estructura XML: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def __procesarAltimetria(self, ruta, nombreSVG):
        # XPath para obtener el nombre de la ruta
        nombre_ruta = ruta.find('ns:nombre', self.__ns).text

        # XPath para obtener la altitud inicial
        coordenadasInicio = ruta.find('ns:coordenadasInicio', self.__ns)
        alt_inicial = float(coordenadasInicio.find('ns:altitud', self.__ns).text)

        puntos_grafica = []
        distancia_acumulada = 0.0
        puntos_grafica.append((distancia_acumulada, alt_inicial))
        nombres_hitos = ["Inicio"]

        # XPath para obtener los hitos
        hitos = ruta.findall('ns:hitos/ns:hito', self.__ns)
        for hito in hitos:
            dist = float(hito.find('ns:distanciaAnterior', self.__ns).text)
            coordenadasHito = hito.find('ns:coordenadasHito', self.__ns)
            alt = float(coordenadasHito.find('ns:altitud', self.__ns).text)
            nombre_hito = hito.find('ns:nombreHito', self.__ns).text

            distancia_acumulada += dist
            puntos_grafica.append((distancia_acumulada, alt))
            nombres_hitos.append(nombre_hito)

        ancho_canvas = 1000
        alto_canvas = 500
        margen_x = 80
        margen_y = 60

        max_dist = puntos_grafica[-1][0]
        altitudes = [p[1] for p in puntos_grafica]
        min_alt = min(altitudes)
        max_alt = max(altitudes)
        diff_alt = max_alt - min_alt if max_alt != min_alt else 1

        scale_x = (ancho_canvas - 2 * margen_x) / max_dist
        scale_y = (alto_canvas - 2 * margen_y) / diff_alt

        print(f"Ruta: {nombre_ruta}")
        print(f"Distancia total: {max_dist:.2f}m. Altitud Min: {min_alt:.2f}m, Max: {max_alt:.2f}m")

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

        miSVG.addText(f"Altimetria: {nombre_ruta}",
                      margen_x, margen_y - 20, "Arial", 20, "darkblue")

        miSVG.addPolyline(polygon_string, "none", 0, "lightgrey")
        miSVG.addPolyline(polyline_string, "blue", 3, "none")

        miSVG.addLine(margen_x, suelo_y, ancho_canvas - margen_x, suelo_y, "black", 2)
        miSVG.addLine(margen_x, margen_y, margen_x, suelo_y, "black", 2)

        num_marcas = 5
        for i in range(num_marcas + 1):
            dist_marca = (max_dist / num_marcas) * i
            px = margen_x + (dist_marca * scale_x)
            miSVG.addLine(px, suelo_y, px, suelo_y + 5, "black", 1)
            miSVG.addText(f"{dist_marca:.0f}m", px - 15, suelo_y + 20, "Arial", 10)

        num_marcas_alt = 5
        for i in range(num_marcas_alt + 1):
            alt_marca = min_alt + (diff_alt / num_marcas_alt) * i
            py = (alto_canvas - margen_y) - ((alt_marca - min_alt) * scale_y)
            miSVG.addLine(margen_x - 5, py, margen_x, py, "black", 1)
            miSVG.addText(f"{alt_marca:.0f}m", 5, py + 5, "Arial", 10)

        for i, (px, py) in enumerate(coords_svg):
            miSVG.addCircle(px, py, 4, "red")
            if i < len(nombres_hitos):
                miSVG.addText(nombres_hitos[i], px + 5, py - 10, "Arial", 9, "red")

        miSVG.escribir(nombreSVG)
        print(f"Creado el archivo: {nombreSVG}")


if __name__ == "__main__":
    procesador = ProcesadorAltimetria("rutas.xml")
    procesador.procesar()