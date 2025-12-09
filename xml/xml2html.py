import xml.etree.ElementTree as ET

class Html(object):
    """
    Clase para generar documentos HTML 5 válidos a partir de datos procesados.
    Adaptada al estilo de MotoGP Desktop.
    @version 1.1
    """
    def __init__(self, titulo, archivo_css):
        """
        Inicializa la estructura básica del HTML
        """
        self.titulo = titulo
        self.archivo_css = archivo_css
        self.contenido = []
        
        # Cabecera HTML5 estándar con metadatos del ejemplo
        self.contenido.append('<!DOCTYPE HTML>')
        self.contenido.append('<html lang="es">')
        self.contenido.append('<head>')
        self.contenido.append('    <!-- Datos que describen el documento -->')
        self.contenido.append('    <meta charset="UTF-8" />')
        self.contenido.append('    <meta name="author" content="Guillermo Gil Naves" />')
        self.contenido.append('    <meta name="description" content="Información del circuito proyecto MotoGp-Desktop" />')
        self.contenido.append('    <meta name="keywords" content="circuito, motogp, carrera, datos" />')
        self.contenido.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
        
        self.contenido.append(f'    <title>{self.titulo}</title>')
        self.contenido.append('    <link rel="stylesheet" type="text/css" href= "../estilo/estilo.css" />')
        self.contenido.append('    <link rel="stylesheet" type="text/css" href= "../estilo/layout.css" />')
        self.contenido.append('    <link rel="icon" href="../multimedia/favicon.ico" />')
        self.contenido.append('</head>')
        self.contenido.append('<body>')
        
    def add_body_start(self):
        self.contenido.append('    <main>')

    def add_header(self, nivel, texto):
        self.contenido.append(f'            <h{nivel}>{texto}</h{nivel}>')

    def add_paragraph(self, texto):
        self.contenido.append(f'            <p>{texto}</p>')

    def add_list_item(self, etiqueta, valor, unidad=""):
        texto_unidad = f" {unidad}" if unidad else ""
        self.contenido.append(f'                <li>{etiqueta}: {valor}{texto_unidad}</li>')

    def start_section(self):
        self.contenido.append('        <section>')
    
    def end_section(self):
        self.contenido.append('        </section>')

    def start_ul(self):
        self.contenido.append('            <ul>')

    def end_ul(self):
        self.contenido.append('            </ul>')

    def add_link(self, url, texto):
        self.contenido.append(f'                <li><a href="{url}" title="{texto}">{texto}</a></li>')

    def add_image(self, src, alt, titulo=""):
        # Adaptado para parecerse al ejemplo, aunque el XML no trae distintas resoluciones
        # Usamos <figure> o <img> directamente según convenga.
        self.contenido.append('            <figure>')
        self.contenido.append(f'                <img src="{src}" alt="{alt}" title="{titulo}" />')
        if titulo:
             self.contenido.append(f'                <figcaption>{titulo}</figcaption>')
        self.contenido.append('            </figure>')

    def add_video(self, src, titulo=""):
        self.contenido.append('            <section>') # Contenedor interno si se desea
        if titulo:
             self.contenido.append(f'                <h3>{titulo}</h3>')
        self.contenido.append('                <video controls preload="auto">')
        self.contenido.append(f'                    <source src="{src}" type="video/mp4" />')
        self.contenido.append('                    Tu navegador no soporta la etiqueta de video.')
        self.contenido.append('                </video>')
        self.contenido.append('            </section>')

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
    nombre_xml = "circuitoEsquema.xml"
    nombre_html = "InfoCircuito.html"
    
    try:
        arbol = ET.parse(nombre_xml)
        raiz = arbol.getroot()
    except Exception as e:
        print(f"Error abriendo XML: {e}")
        return

    # Definición del Namespace
    ns = {'ns': 'http://www.uniovi.es'} 
    # Fallback si no tiene namespace correcto
    if raiz.find('ns:nombre', ns) is None:
        ns = {'ns': 'http://www.uniovi.es/'}

    # Instancia de la clase Html
    doc_html = Html("Información del Circuito", "estilo.css")
    
    # Generar cabecera body (Nav, Breadcrumbs)
    doc_html.add_body_start()

    # --- SECCIÓN 1: DATOS GENERALES ---
    doc_html.start_section()
    
    nombre = raiz.find('ns:nombre', ns).text
    doc_html.add_header(2, nombre) # H2 como en el ejemplo del piloto
    
    # Descripción construida
    localidad = raiz.find('ns:ubicacion/ns:localidad', ns)
    pais = raiz.find('ns:ubicacion/ns:pais', ns)
    if localidad is None: localidad = raiz.find('ns:localidad', ns) # Fallback
    if pais is None: pais = raiz.find('ns:pais', ns) # Fallback

    descripcion = f"Información sobre el circuito {nombre}, situado en {localidad.text if localidad is not None else ''} ({pais.text if pais is not None else ''})."
    doc_html.add_paragraph(descripcion)

    doc_html.start_ul()
    
    # Extracción de datos con xPath
    longitud = raiz.find('ns:dimensiones/ns:longitud', ns)
    anchura = raiz.find('ns:dimensiones/ns:anchuraMedia', ns)
    # Fallback estructura plana
    if longitud is None: longitud = raiz.find('ns:longitud', ns)
    if anchura is None: anchura = raiz.find('ns:anchura', ns)

    if longitud is not None:
        doc_html.add_list_item("Longitud", longitud.text, longitud.get('unidad'))
    if anchura is not None:
        doc_html.add_list_item("Anchura media", anchura.text, anchura.get('unidad'))

    fecha = raiz.find('ns:fechaCarrera', ns) or raiz.find('ns:fecha', ns)
    hora = raiz.find('ns:horaInicio', ns)
    vueltas = raiz.find('ns:vueltas', ns)

    if fecha is not None: doc_html.add_list_item("Fecha carrera", fecha.text)
    if hora is not None: doc_html.add_list_item("Hora inicio", hora.text)
    if vueltas is not None: doc_html.add_list_item("Numero de vueltas", vueltas.text)
    
    doc_html.end_ul()
    
    # Galería de imágenes (dentro de la primera sección o separada)
    fotos = raiz.findall('ns:galeriaFotos/ns:foto', ns)
    for foto in fotos:
        src = foto.get('archivo') or foto.get('src')
        titulo = foto.get('titulo')
        if src:
            doc_html.add_image(src, f"Imagen del circuito {nombre}", titulo)
            
    doc_html.end_section()

    # --- SECCIÓN 2: REFERENCIAS ---
    doc_html.start_section()
    doc_html.add_header(2, "Referencias")
    doc_html.add_paragraph(f"Otras páginas donde encontrar información sobre {nombre}")
    
    # Estructura del ejemplo: nav > aside > ul
    # Lo simularé con start_ul para mantener simplicidad de la clase, 
    # pero el HTML final tendrá la lista.
    doc_html.start_ul()
    referencias = raiz.findall('ns:referencias/ns:referencia', ns) or raiz.findall('ns:referencias/ns:ref', ns)
    for ref in referencias:
        url = ref.get('url')
        texto = ref.text
        doc_html.add_link(url, texto)
    doc_html.end_ul()
    doc_html.end_section()

    # --- SECCIÓN 3: VIDEOS ---
    videos = raiz.findall('ns:galeriaVideos/ns:video', ns)
    if videos:
        doc_html.start_section()
        doc_html.add_header(2, "Videos")
        for video in videos:
            src = video.get('archivo') or video.get('src')
            titulo = video.get('titulo')
            if src:
                doc_html.add_video(src, titulo)
        doc_html.end_section()

    # Escribir archivo
    doc_html.escribir(nombre_html)

if __name__ == "__main__":
    main()