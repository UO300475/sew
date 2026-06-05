import xml.etree.ElementTree as ET

class Kml(object):
    """
    Clase para generar archivos KML
    """
    def __init__(self):
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz, 'Document')

    def addPlacemark(self, nombre, descripcion, long, lat, alt, modoAltitud):
        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        ET.SubElement(pm, 'description').text = descripcion
        punto = ET.SubElement(pm, 'Point')
        ET.SubElement(punto, 'coordinates').text = '{},{},{}'.format(long, lat, alt)
        ET.SubElement(punto, 'altitudeMode').text = modoAltitud

    def addLineString(self, nombre, extrude, tesela, listaCoordenadas, modoAltitud, color, ancho):
        ET.SubElement(self.doc, 'name').text = nombre
        pm = ET.SubElement(self.doc, 'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls, 'extrude').text = extrude
        ET.SubElement(ls, 'tessellation').text = tesela
        ET.SubElement(ls, 'coordinates').text = listaCoordenadas
        ET.SubElement(ls, 'altitudeMode').text = modoAltitud

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement(linea, 'color').text = color
        ET.SubElement(linea, 'width').text = ancho

    def escribir(self, nombreArchivoKML):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)


class ProcesadorRutas(object):
    """
    Clase para procesar las rutas del archivo XML y generar los KML
    """
    def __init__(self, archivoXML):
        self.__archivoXML = archivoXML
        self.__ns = {'ns': 'http://www.uniovi.es'}
        self.__nombres_kml = [
            "planimetria_medulas.kml",
            "planimetria_catedral.kml",
            "planimetria_camino.kml"
        ]

    def procesar(self):
        try:
            arbolXML = ET.parse(self.__archivoXML)
            raizXML = arbolXML.getroot()

            # XPath para obtener todas las rutas
            rutas = raizXML.findall('ns:ruta', self.__ns)

            for i, ruta in enumerate(rutas):
                nuevoKML = Kml()
                nombre_ruta = self.__procesarRuta(ruta, nuevoKML)
                nuevoKML.escribir(self.__nombres_kml[i])
                print(f"Archivo '{self.__nombres_kml[i]}' creado para la ruta: {nombre_ruta}")

        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo {self.__archivoXML}")
        except AttributeError as e:
            print(f"Error de estructura XML: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def __procesarRuta(self, ruta, nuevoKML):
        # XPath para obtener los datos de la ruta
        nombre_ruta = ruta.find('ns:nombre', self.__ns).text
        descripcion = ruta.find('ns:descripcion', self.__ns).text

        # XPath para obtener las coordenadas de inicio
        coordenadasInicio = ruta.find('ns:coordenadasInicio', self.__ns)
        orig_lon = coordenadasInicio.find('ns:longitud', self.__ns).text
        orig_lat = coordenadasInicio.find('ns:latitud', self.__ns).text
        orig_alt = coordenadasInicio.find('ns:altitud', self.__ns).text

        nuevoKML.addPlacemark(
            f"Inicio: {nombre_ruta}",
            descripcion,
            orig_lon, orig_lat, orig_alt,
            'relativeToGround'
        )

        lista_coords = [f"{orig_lon},{orig_lat},{orig_alt}"]

        # XPath para obtener los hitos de la ruta
        hitos = ruta.findall('ns:hitos/ns:hito', self.__ns)

        for hito in hitos:
            coordenadasHito = hito.find('ns:coordenadasHito', self.__ns)
            lon = coordenadasHito.find('ns:longitud', self.__ns).text
            lat = coordenadasHito.find('ns:latitud', self.__ns).text
            alt = coordenadasHito.find('ns:altitud', self.__ns).text
            nombre_hito = hito.find('ns:nombreHito', self.__ns).text

            nuevoKML.addPlacemark(
                nombre_hito,
                hito.find('ns:descripcionHito', self.__ns).text,
                lon, lat, alt,
                'relativeToGround'
            )

            lista_coords.append(f"{lon},{lat},{alt}")

        string_coordenadas = "\n".join(lista_coords)

        nuevoKML.addLineString(
            nombre_ruta,
            "1", "1",
            string_coordenadas,
            'relativeToGround',
            "#ff0000ff", "5"
        )

        return nombre_ruta


if __name__ == "__main__":
    procesador = ProcesadorRutas("rutas.xml")
    procesador.procesar()