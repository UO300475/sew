class Noticias {
    #busqueda;
    #apiKey;
    #url;

    constructor(busqueda) {
        this.#busqueda = busqueda;
        this.#apiKey = "DSO8O61U6KtIvkgYat3ODK8ImPo8kNHvkeQoRBBS";
        this.#url = "https://api.thenewsapi.com/v1/news/all";
    }

    buscar() {
        const urlPeticion = `${this.#url}?api_token=${this.#apiKey}&search=${this.#busqueda}&language=es&limit=3`;

        // Llamada a fetch(). Esto devuelve un objeto Promise
        fetch(urlPeticion)
            .then(response => {
                // Verificamos si la respuesta de la red es correcta
                if (!response.ok) {
                    throw new Error("Error de red al intentar cargar las noticias");
                }
                // response.json() devuelve una nueva Promesa que se resuelve con el objeto JSON
                return response.json(); 
            })
            .then(json => {
                // Aquí ya tenemos la información procesada del objeto JSON
                // Llamamos al método encargado de pintarlo en el HTML
                this.procesarInformacion(json);
            })
            .catch(error => {
                // Manejo de errores de la Promesa
                console.error("Hubo un problema con la operación fetch:", error);
                $("main").append("<p class='error'>No se han podido cargar las noticias.</p>");
            });
    }

    procesarInformacion(json) {
        // Seleccionamos el main
        const $main = $("main");

        // Creamos la sección contenedora
        const $seccion = $("<section></section>");
        $seccion.append("<h2>Últimas noticias de MotoGP</h2>");

        // Obtenemos el array de noticias (en TheNewsApi está bajo la clave 'data')
        const items = json.data;

        // Iteramos por cada noticia
        items.forEach(noticia => {
            const titulo = noticia.title;
            const descripcion = noticia.description;
            const url = noticia.url;
            const fuente = noticia.source;

            const $h3 = $("<h3></h3>").text(titulo);

            const $pDesc = $("<p></p>").text(descripcion);
            
            const $pMeta = $("<p></p>").html(`Fuente: <strong>${fuente}</strong> - `);
            const $a = $("<a></a>").attr("href", url).attr("target", "_blank").text("Leer más");
            
            $pMeta.append($a);

            $seccion.append($h3);
            $seccion.append($pDesc);
            $seccion.append($pMeta);
        });

        $main.append($seccion);
    }
}