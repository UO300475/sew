class Noticias {

    #busqueda
    #url
    #apiKey

    constructor(busqueda) {
        this.#busqueda = busqueda;
        this.#url = "https://api.thenewsapi.com/v1/news/top";
        this.#apiKey = "DSO8O61U6KtIvkgYat3ODK8ImPo8kNHvkeQoRBBS";
    }

    buscar() {
        const urlPeticion = `${this.#url}?api_token=${this.#apiKey}&search=${this.#busqueda}&language=es&limit=5`;

        fetch(urlPeticion)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error de red al intentar cargar las noticias");
                }
                return response.json();
            })
            .then(json => {
                this.procesarInformacion(json);
            })
            .catch(error => {
                console.error("Hubo un problema con la operacion fetch:", error);
                $("main").append("<p>No se han podido cargar las noticias.</p>");
            });
    }

    procesarInformacion(json) {
        const items = json.data;

        if (!items || items.length === 0) {
            $("main").append("<section><h2>No hay noticias disponibles</h2></section>");
            return;
        }

        const $seccion = $("<section></section>");
        $seccion.append("<h2>Ultimas noticias sobre Leon</h2>");

        items.forEach(noticia => {
            const titulo = noticia.title;
            const descripcion = noticia.description;
            const url = noticia.url;
            const fuente = noticia.source;

            const $h3 = $("<h3></h3>").text(titulo);
            const $pDesc = $("<p></p>").text(descripcion);
            const $pMeta = $("<p></p>").html(`Fuente: <strong>${fuente}</strong> - `);
            const $a = $("<a></a>").attr("href", url).attr("target", "_blank").text("Leer mas");

            $pMeta.append($a);

            $seccion.append($h3);
            $seccion.append($pDesc);
            $seccion.append($pMeta);
        });
        
        // IMPORTANTE: Insertar debajo del carrusel
        $("main article").last().after($seccion);
    }
}