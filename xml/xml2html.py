import xml.etree.ElementTree as ET

class Html(object):
    """
    Clase para generar documentos HTML5 validos a partir de datos procesados.
    Adaptada al estilo de Leon-Desktop.
    """
    def __init__(self, titulo):
        self.titulo = titulo
        self.contenido = []

        self.contenido.append('<!DOCTYPE HTML>')
        self.contenido.append('<html lang="es">')
        self.contenido.append('<head>')
        self.contenido.append('    <!-- Datos que describen el documento -->')
        self.contenido.append('    <meta charset="UTF-8" />')
        self.contenido.append('    <meta name="author" content="tu nombre aqui" />')
        self.contenido.append('    <meta name="description" content="Rutas turisticas de la provincia de Leon" />')
        self.contenido.append('    <meta name="keywords" content="Leon, rutas, turismo, senderismo" />')
        self.contenido.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
        self.contenido.append(f'    <title>{self.titulo}</title>')
        self.contenido.append('    <link rel="stylesheet" type="text/css" href="../estilo/estilo.css" />')
        self.contenido.append('    <link rel="stylesheet" type="text/css" href="../estilo/layout.css" />')
        self.contenido.append('    <link rel="icon" href="../multimedia/favicon.ico" />')
        self.contenido.append('</head>')
        self.contenido.append('<body>')
        self.contenido.append('    <main>')

    def add_header(self, nivel, texto):
        self.contenido.append(f'        <h{nivel}>{texto}</h{nivel}>')

    def add_paragraph(self, texto):
        self.contenido.append(f'        <p>{texto}</p>')

    def start_section(self):
        self.contenido.append('        <section>')

    def end_section(self):
        self.contenido.append('        </section>')

    def start_aside(self):
        self.contenido.append('        <aside>')

    def end_aside(self):
        self.contenido.append('        </aside>')

    def start_ul(self):
        self.contenido.append('            <ul>')

    def end_ul(self):
        self.contenido.append('            </ul>')

    def add_list_item(self, etiqueta, valor, unidad=""):
        texto_unidad = f" {unidad}" if unidad else ""
        self.contenido.append(f'                <li>{etiqueta}: {valor}{texto_unidad}')

    def add_link(self, url, texto):
        self.contenido.append(f'                <li><a href="{url}" title="{texto}">{texto}</a>')

    def add_image(self, src, alt, titulo=""):
        self.contenido.append('            <figure>')
        self.contenido.append(f'                <img src="{src}" alt="{alt}" title="{titulo}" />')
        if titulo:
            self.contenido.append(f'                <figcaption>{titulo}</figcaption>')
        self.contenido.append('            </figure>')

    def add_svg(self, src, nombre_ruta):
        self.contenido.append(f'            <img src="{src}" alt="Altimetria de la ruta {nombre_ruta}" />')

    def escribir(self, nombre_archivo):
        self.contenido.append('    </main>')
        self.contenido.append('</body>')
        self.contenido.append('</html>')

        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.contenido))
            print(f"Archivo HTML generado correctamente: {nombre_archivo}")
        except IOError as e:
            print(f"Error escribiendo el archivo: {e}")


def main():
    nombre_xml = "rutasEsquema.xml"
    nombre_html = "infoRutas.html"

    try:
        arbol = ET.parse(nombre_xml)
        raiz = arbol.getroot()
    except Exception as e:
        print(f"Error abriendo XML ({nombre_xml}): {e}")
        return

    ns = {'ns': 'http://www.uniovi.es'}

    doc_html = Html("Leon - Info Rutas")

    rutas = raiz.findall('ns:ruta', ns)

    for ruta in rutas:
        nombre = ruta.find('ns:nombre', ns).text
        tipo = ruta.find('ns:tipo', ns).text
        transporte = ruta.find('ns:transporte', ns).text
        duracion = ruta.find('ns:duracion', ns).text
        agencia = ruta.find('ns:agencia', ns).text
        descripcion = ruta.find('ns:descripcion', ns).text
        personas = ruta.find('ns:personas', ns).text
        lugar_inicio = ruta.find('ns:lugarInicio', ns).text
        direccion_inicio = ruta.find('ns:direccionInicio', ns).text
        recomendacion = ruta.find('ns:recomendacion', ns).text

        fecha_inicio = ruta.find('ns:fechaInicio', ns)
        hora_inicio = ruta.find('ns:horaInicio', ns)

        altimetria = ruta.find('ns:altimetria', ns).text

        # SECCION PRINCIPAL DE LA RUTA
        doc_html.start_section()
        doc_html.add_header(2, nombre)
        doc_html.add_paragraph(descripcion)

        doc_html.start_ul()
        doc_html.add_list_item("Tipo", tipo)
        doc_html.add_list_item("Transporte", transporte)
        doc_html.add_list_item("Duracion", duracion)
        doc_html.add_list_item("Agencia", agencia)
        doc_html.add_list_item("Personas", personas)
        doc_html.add_list_item("Lugar de inicio", lugar_inicio)
        doc_html.add_list_item("Direccion de inicio", direccion_inicio)
        doc_html.add_list_item("Recomendacion", f"{recomendacion}/10")
        if fecha_inicio is not None:
            doc_html.add_list_item("Fecha de inicio", fecha_inicio.text)
        if hora_inicio is not None:
            doc_html.add_list_item("Hora de inicio", hora_inicio.text)
        doc_html.end_ul()

        # HITOS DE LA RUTA
        doc_html.add_header(3, "Hitos de la ruta")
        hitos = ruta.findall('ns:hitos/ns:hito', ns)
        for hito in hitos:
            nombre_hito = hito.find('ns:nombreHito', ns).text
            descripcion_hito = hito.find('ns:descripcionHito', ns).text
            distancia = hito.find('ns:distanciaAnterior', ns).text
            unidad = hito.find('ns:distanciaAnterior', ns).get('unidad')

            doc_html.start_section()
            doc_html.add_header(4, nombre_hito)
            doc_html.add_paragraph(descripcion_hito)
            doc_html.add_paragraph(f"Distancia desde el hito anterior: {distancia} {unidad}")

            fotos = hito.findall('ns:galeriaFotos/ns:foto', ns)
            for foto in fotos:
                src = foto.get('archivo')
                titulo = foto.get('titulo')
                if src:
                    doc_html.add_image(f"../{src}", f"Imagen de {nombre_hito}", titulo)

            doc_html.end_section()

        # ALTIMETRIA
        doc_html.add_header(3, "Altimetria de la ruta")
        doc_html.add_svg(altimetria, nombre)

        doc_html.end_section()

        # REFERENCIAS
        doc_html.start_aside()
        doc_html.add_header(3, "Referencias")
        doc_html.start_ul()
        referencias = ruta.findall('ns:referencias/ns:referencia', ns)
        for ref in referencias:
            url = ref.get('url')
            texto = ref.text
            doc_html.add_link(url, texto)
        doc_html.end_ul()
        doc_html.end_aside()

    doc_html.escribir(nombre_html)

if __name__ == "__main__":
    main()