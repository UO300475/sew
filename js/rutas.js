class Rutas {

    constructor() {}

    leerRutasXML() {
        $.ajax({
            url: 'xml/rutas.xml',
            method: 'GET',
            dataType: 'xml',
            success: (xml) => {
                this.#procesarXML(xml);
            },
            error: () => {
                console.error("ERROR: No se pudo cargar el archivo rutas.xml");
            }
        });
    }

    #procesarXML(xml) {
        const main = document.querySelector("main section");
        const rutas = $(xml).find("ruta");

        const nombresSVG = [
            "xml/altimetria_medulas.svg",
            "xml/altimetria_catedral.svg",
            "xml/altimetria_camino.svg"
        ];

        const nombresKML = [
            "xml/planimetria_medulas.kml",
            "xml/planimetria_catedral.kml",
            "xml/planimetria_camino.kml"
        ];

        rutas.each((indice, ruta) => {
            const nombre = $(ruta).find("nombre").first().text();
            const tipo = $(ruta).find("tipo").first().text();
            const transporte = $(ruta).find("transporte").first().text();
            const duracion = $(ruta).find("duracion").first().text();
            const agencia = $(ruta).find("agencia").first().text();
            const descripcion = $(ruta).find("descripcion").first().text();
            const personas = $(ruta).find("personas").first().text();
            const lugarInicio = $(ruta).find("lugarInicio").first().text();
            const recomendacion = $(ruta).find("recomendacion").first().text();
            const fechaInicio = $(ruta).find("fechaInicio").first().text();
            const horaInicio = $(ruta).find("horaInicio").first().text();

            const article = document.createElement("article");

            const h3 = document.createElement("h3");
            h3.textContent = nombre;
            article.appendChild(h3);

            const pDesc = document.createElement("p");
            pDesc.textContent = descripcion;
            article.appendChild(pDesc);

            const ul = document.createElement("ul");
            const datos = [
                `Tipo: ${tipo}`,
                `Transporte: ${transporte}`,
                `Duracion: ${duracion}`,
                `Agencia: ${agencia}`,
                `Personas: ${personas}`,
                `Lugar de inicio: ${lugarInicio}`,
                `Recomendacion: ${recomendacion}/10`,
                `Fecha de inicio: ${fechaInicio}`,
                `Hora de inicio: ${horaInicio}`
            ];

            datos.forEach(dato => {
                const li = document.createElement("li");
                li.textContent = dato;
                ul.appendChild(li);
            });

            article.appendChild(ul);

            const h4Hitos = document.createElement("h4");
            h4Hitos.textContent = "Hitos de la ruta";
            article.appendChild(h4Hitos);

            $(ruta).find("hito").each((i, hito) => {
                const nombreHito = $(hito).find("nombreHito").first().text();
                const descripcionHito = $(hito).find("descripcionHito").first().text();
                const distancia = $(hito).find("distanciaAnterior").first().text();
                const unidad = $(hito).find("distanciaAnterior").attr("unidad");

                const sectionHito = document.createElement("section");

                const h5 = document.createElement("h5");
                h5.textContent = nombreHito;
                sectionHito.appendChild(h5);

                const pHito = document.createElement("p");
                pHito.textContent = descripcionHito;
                sectionHito.appendChild(pHito);

                const pDist = document.createElement("p");
                pDist.textContent = `Distancia desde el hito anterior: ${distancia} ${unidad}`;
                sectionHito.appendChild(pDist);

                article.appendChild(sectionHito);
            });

            const h4Refs = document.createElement("h4");
            h4Refs.textContent = "Referencias";
            article.appendChild(h4Refs);

            const ulRefs = document.createElement("ul");
            $(ruta).find("referencia").each((i, ref) => {
                const url = $(ref).attr("url");
                const texto = $(ref).text();
                const li = document.createElement("li");
                const a = document.createElement("a");
                a.href = url;
                a.textContent = texto;
                a.title = texto;
                li.appendChild(a);
                ulRefs.appendChild(li);
            });
            article.appendChild(ulRefs);

            main.appendChild(article);

            const coordInicio = $(ruta).find("coordenadasInicio").first();
            const lat = parseFloat($(coordInicio).find("latitud").first().text());
            const lon = parseFloat($(coordInicio).find("longitud").first().text());

            const cargadorSVG = new CargadorSVG(nombresSVG[indice]);
            cargadorSVG.cargar(article);

            const cargadorKML = new CargadorKML(nombresKML[indice], lat, lon);
            cargadorKML.cargar(article);
        });
    }
}

class CargadorSVG {

    #urlSVG
    #seccion

    constructor(urlSVG) {
        this.#urlSVG = urlSVG;
    }

    cargar(contenedorPadre) {
        this.#seccion = document.createElement('article');

        const h4 = document.createElement('h4');
        h4.textContent = 'Altimetria de la ruta';
        this.#seccion.appendChild(h4);

        contenedorPadre.appendChild(this.#seccion);

        fetch(this.#urlSVG)
            .then(r => r.text())
            .then(texto => this.#insertarSVG(texto))
            .catch(() => {
                const p = document.createElement('p');
                p.textContent = 'No se pudo cargar la altimetria.';
                this.#seccion.appendChild(p);
            });
    }

    #insertarSVG(contenidoTexto) {
        const parser = new DOMParser();
        const docSVG = parser.parseFromString(contenidoTexto, 'image/svg+xml');
        const svg = docSVG.documentElement;

        if (svg.getAttribute('version') === '2.0') {
            svg.setAttribute('version', '1.1');
        }

        this.#seccion.appendChild(svg);
    }
}

class CargadorKML {

    #urlKML
    #mapa
    #divMapa
    #seccion
    #lat
    #lon

    constructor(urlKML, lat, lon) {
        this.#urlKML = urlKML;
        this.#lat = isNaN(lat) ? 42.5987 : lat;
        this.#lon = isNaN(lon) ? -5.5671 : lon;
    }

    cargar(contenedorPadre) {
        this.#seccion = document.createElement('article');

        const h4 = document.createElement('h4');
        h4.textContent = 'Planimetria de la ruta';
        this.#seccion.appendChild(h4);

        this.#divMapa = document.createElement('div');
        this.#divMapa.setAttribute('data-mapa', 'ruta');
        this.#seccion.appendChild(this.#divMapa);

        contenedorPadre.appendChild(this.#seccion);

        mapboxgl.accessToken = 'pk.eyJ1IjoidW8zMDA0NzUiLCJhIjoiY21qZ2Exdm1mMHp3bDNjc2xxaDNjeTNvNCJ9.2o13ht2X6rIc0NYLcYiYSA';
        this.#mapa = new mapboxgl.Map({
            container: this.#divMapa,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [this.#lon, this.#lat],
            zoom: 9
        });

        Promise.all([
            fetch(this.#urlKML).then(r => r.text()),
            new Promise(resolve => {
                if (this.#mapa.isStyleLoaded()) resolve();
                else this.#mapa.once('load', resolve);
            })
        ]).then(([textoKML]) => {
            this.#procesarKML(textoKML);
        }).catch(error => {
            console.error("Error al cargar KML:", error);
        });
    }

    #procesarKML(textoKML) {
        const textoLimpio = textoKML.replace(/xmlns="[^"]*"/g, '');
        const parser = new DOMParser();
        const xml = parser.parseFromString(textoLimpio, "text/xml");

        const coordenadas = [];
        xml.querySelectorAll('LineString coordinates').forEach(linea => {
            linea.textContent.trim().split(/\s+/).forEach(par => {
                const partes = par.split(',');
                const lon = parseFloat(partes[0]);
                const lat = parseFloat(partes[1]);
                if (!isNaN(lon) && !isNaN(lat)) coordenadas.push([lon, lat]);
            });
        });

        xml.querySelectorAll('Placemark').forEach(pm => {
            const punto = pm.querySelector('Point coordinates');
            if (!punto) return;
            const partes = punto.textContent.trim().split(',');
            const lon = parseFloat(partes[0]);
            const lat = parseFloat(partes[1]);
            const nombre = pm.querySelector('name') ? pm.querySelector('name').textContent : '';
            if (!isNaN(lon) && !isNaN(lat)) {
                new mapboxgl.Marker()
                    .setLngLat([lon, lat])
                    .setPopup(new mapboxgl.Popup().setText(nombre))
                    .addTo(this.#mapa);
            }
        });

        if (coordenadas.length === 0) return;

        this.#mapa.setCenter(coordenadas[0]);
        this.#mapa.setZoom(10);

        this.#mapa.addSource('ruta', {
            type: 'geojson',
            data: {
                type: 'Feature',
                geometry: { type: 'LineString', coordinates: coordenadas }
            }
        });

        this.#mapa.addLayer({
            id: 'tramo-ruta',
            type: 'line',
            source: 'ruta',
            layout: { 'line-join': 'round', 'line-cap': 'round' },
            paint: { 'line-color': '#cc0000', 'line-width': 4 }
        });
    }
}