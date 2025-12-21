class Circuito {

    constructor() {
        this.comprobarApiFile();
    }

    comprobarApiFile() {  
        // Version 1.1 23/10/2021 
        if (!(window.File && window.FileReader && window.FileList && window.Blob)) 
        {  
            //El navegador no soporta el API File
            const main = document.querySelector("main");
            const seccion = document.createElement("section");
            const p = document.createElement("p");
            p.textContent = `¡¡¡ Este navegador NO soporta el API File y este programa puede no funcionar correctamente !!!`
            seccion.appendChild(p);
            main.appendChild(seccion);
        } 
    }

    async leerArchivoHTML() {

        const rutaFija = 'xml/InfoCircuito.html';
        try {
            const respuesta = await fetch(rutaFija);
            
            if (!respuesta.ok) throw new Error("No se encontró el archivo");

            const blob = await respuesta.blob();
            const archivo = new File([blob], "Infocircuito.html", { type: "text/html" });

            if (!archivo) return;
        
            const main = document.querySelector("main");
            const seccion = main.querySelectorAll("section")[0]; 

            const lector = new FileReader();
            
            lector.onload = () => {
                const cadenaHTML = lector.result;
                const parser = new DOMParser();
                const doc = parser.parseFromString(cadenaHTML, "text/html");
                const elementosLeidos = doc.body.children;
                const articuloContenido = document.createElement("article");
                Array.from(elementosLeidos).forEach(elemento => {
                    articuloContenido.appendChild(elemento);
                });
                seccion.appendChild(articuloContenido);
            };

            lector.readAsText(archivo);

        } catch (error) {
            console.error("Error al cargar el archivo:", error);
        }
    }
}

class CargadorSVG {
    leerArchivoSVG(files) {

        const archivo = files[0];
        if (!archivo) return;

        const lector = new FileReader();
        
        lector.onload = (evento) => {
            this.insertarSVG(evento.target.result);
            const cadenaHTML = lector.result;
            const parser = new DOMParser();
            const doc = parser.parseFromString(cadenaHTML, "image/svg");
            const elementosLeidos = doc.body.children;
            const articuloContenido = document.createElement("article");
            Array.from(elementosLeidos).forEach(elemento => {
                articuloContenido.appendChild(elemento);
            });
            seccion.appendChild(articuloContenido);
        };

        lector.readAsText(archivo);
    
    }

    insertarSVG(contenidoTexto){
        const main = document.querySelector("main");
        const secciones = main.querySelectorAll("section"); 
        const seccion = secciones[secciones.length - 2];
        const parser = new DOMParser();
        const doc = parser.parseFromString(contenidoTexto, "image/svg+xml");
        const elementoSVG = doc.documentElement;
        const articuloContenido = document.createElement("article");
        articuloContenido.innerHTML = '';
        articuloContenido.appendChild(elementoSVG);
        seccion.appendChild(articuloContenido);
    }
}

class CargadorKML {

    constructor() {
        mapboxgl.accessToken = 'pk.eyJ1IjoidW8zMDA0NzUiLCJhIjoiY21qZ2Exdm1mMHp3bDNjc2xxaDNjeTNvNCJ9.2o13ht2X6rIc0NYLcYiYSA';

        const section = document.querySelector("main section:last-of-type");

        this.contenedor = document.createElement("div");
        this.contenedor.style.width = "100%";
        this.contenedor.style.height = "400px";

        section.appendChild(this.contenedor);

        this.mapa = null;   // ❗ aún NO existe el mapa
    }

    leerArchivoKML(files) {
        const archivo = files[0];
        if (!archivo) return;

        const lector = new FileReader();
        lector.onload = e => this.procesarKML(e.target.result);
        lector.readAsText(archivo);
    }

    procesarKML(textoKML) {
        const parser = new DOMParser();
        const xml = parser.parseFromString(textoKML, "text/xml");

        const origen = xml.querySelector("Placemark Point coordinates");
        if (!origen) {
            alert("KML sin punto de origen");
            return;
        }

        const [lon, lat] = origen.textContent.trim().split(",").map(Number);

        const coordenadas = [];
        const puntos = xml.querySelectorAll("LineString coordinates");

        puntos.forEach(p => {
            p.textContent.trim().split(/\s+/).forEach(par => {
                const [lo, la] = par.split(",").map(Number);
                coordenadas.push([lo, la]);
            });
        });

        // 🔥 AQUÍ se crea el mapa
        this.crearMapa(lat, lon, coordenadas);
    }

    crearMapa(lat, lon, coordenadas) {

        // Crear mapa SOLO una vez
        if (!this.mapa) {
            this.mapa = new mapboxgl.Map({
                container: this.contenedor, // sin id
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [lon, lat],
                zoom: 14
            });

            this.mapa.on('load', () => {
                this.pintarCircuito(lat, lon, coordenadas);
            });

        } else {
            // Si el mapa ya existe, solo actualizar
            this.mapa.setCenter([lon, lat]);
            this.pintarCircuito(lat, lon, coordenadas);
        }
    }

    pintarCircuito(lat, lon, coordenadas) {

        new mapboxgl.Marker()
            .setLngLat([lon, lat])
            .addTo(this.mapa);

        if (this.mapa.getSource('circuito')) {
            this.mapa.removeLayer('tramos');
            this.mapa.removeSource('circuito');
        }

        this.mapa.addSource('circuito', {
            type: 'geojson',
            data: {
                type: 'Feature',
                geometry: {
                    type: 'LineString',
                    coordinates: coordenadas
                }
            }
        });

        this.mapa.addLayer({
            id: 'tramos',
            type: 'line',
            source: 'circuito',
            paint: {
                'line-color': '#ff0000',
                'line-width': 4
            }
        });
    }
}