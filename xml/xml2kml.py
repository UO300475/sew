import xml.etree.ElementTree as ET

class Kml(object):
    def __init__(self):
        """
        Crea el elemento raíz y el espacio de nombres
        """
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz,'Document')

    def addPlacemark(self, nombre, descripcion, long, lat, alt, modoAltitud):
        """
        Añade un elemento <Placemark> con puntos <Point>
        """
        pm = ET.SubElement(self.doc,'Placemark')
        ET.SubElement(pm,'name').text = nombre
        ET.SubElement(pm,'description').text = descripcion
        punto = ET.SubElement(pm,'Point')
        ET.SubElement(punto,'coordinates').text = '{},{},{}'.format(long,lat,alt)
        ET.SubElement(punto,'altitudeMode').text = modoAltitud

    def addLineString(self, nombre, extrude, tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """
        ET.SubElement(self.doc,'name').text = nombre
        pm = ET.SubElement(self.doc,'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls,'extrude').text = extrude
        ET.SubElement(ls,'tessellation').text = tesela
        ET.SubElement(ls,'coordinates').text = listaCoordenadas
        ET.SubElement(ls,'altitudeMode').text = modoAltitud 

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        color_elem = ET.SubElement(linea, 'color')
        color_elem.text = color
        width_elem = ET.SubElement(linea, 'width')
        width_elem.text = ancho

    def escribir(self, nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)

def main():
    nombreKML = "circuito.kml"
    archivoXML = "circuitoEsquema.xml"

    print("Leyendo archivo XML:", archivoXML)
    
    try:
        arbolXML = ET.parse(archivoXML)
        raizXML = arbolXML.getroot()
        
        ns = {'ns': 'http://www.uniovi.es/'}

        nuevoKML = Kml()

        nombre_circuito = raizXML.find('ns:nombre', ns).text
        localidad = raizXML.find('ns:localidad', ns).text
        pais = raizXML.find('ns:pais', ns).text
        descripcion = f"Circuito situado en {localidad}, {pais}"

        origen = raizXML.find('ns:origen', ns)
        orig_lat = origen.find('ns:latitudGeo', ns).text
        orig_lon = origen.find('ns:longitudGeo', ns).text
        orig_alt = origen.find('ns:altitudGeo', ns).text

        nuevoKML.addPlacemark(f"Salida: {nombre_circuito}", 
                              descripcion, 
                              orig_lon, orig_lat, orig_alt, 
                              'relativeToGround')

        lista_coords = [f"{orig_lon},{orig_lat},{orig_alt}"]

        tramos = raizXML.findall('ns:tramos/ns:tramo', ns)
        
        for tramo in tramos:
            fin = tramo.find('ns:fin', ns)
            lon = fin.find('ns:longitudGeo', ns).text
            lat = fin.find('ns:latitudGeo', ns).text
            alt = fin.find('ns:altitudGeo', ns).text
            
            lista_coords.append(f"{lon},{lat},{alt}")

        string_coordenadas = "\n".join(lista_coords)

        nuevoKML.addLineString(nombre_circuito, 
                               "1", "1", 
                               string_coordenadas, 
                               'relativeToGround', 
                               '#ff0000ff', "5")

        nuevoKML.escribir(nombreKML)
        print(f"¡Éxito! Creado el archivo: {nombreKML} con {len(lista_coords)} puntos.")

    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo {archivoXML}")
    except ET.ParseError:
        print(f"Error: El archivo {archivoXML} no es un XML válido")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()