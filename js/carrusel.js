class Carrusel{
    #busqueda
    #actual
    #maximo
    #fotografias
    
    constructor(busqueda){
        this.#busqueda = busqueda;
        this.#actual = 0;
        this.#maximo = 5;
        this.#fotografias = [];
    }

    
    getFotografias() {
        const url = "https://www.flickr.com/services/feeds/photos_public.gne?jsoncallback=?";
        
        $.ajax({
            dataType: "json",
            url: url,
            method: "GET",      
            data: {
                tags: this.#busqueda,
                tagmode: "any",
                format: "json"
            },
            success: (data) => {
                this.#fotografias = []; // limpiar las que habia
                for (let i = 0; i < this.#maximo && i < data.items.length; i++) {
                    let url = data.items[i].media.m.replace("_m", "_z"); // ponemos a 640px
                    this.#fotografias.push({
                        url: url,
                        titulo: data.items[i].title
                    });
                }

                this.mostrarFotografias();
            },
            error: () => {
                console.error("No se pudo cargar el JSON de Flickr");
            }
        });
    }

    procesarJSONFotografias(json) {
        this.#fotografias = []; // limpiar las que habia

        json.items.slice(0, this.#maximo).forEach(item => {
            // Sustituimos el sufijo "_m" por "_z" para obtener 640px
            const url640 = item.media.m.replace("_m.", "_z.");
            this.#fotografias.push({
                titulo: item.title,
                url: url640
            });
        });
   }

   mostrarFotografias() {
        if(this.#fotografias.length === 0) return;

        const articulo = document.createElement("article");

        const h2 = document.createElement("h2");
        h2.textContent = "Imágenes del circuito Autódromo Internacional do Algarve ";

        const imagen = document.createElement("img");
        imagen.src = this.#fotografias[0].url;
        imagen.alt = this.#fotografias[0].titulo;

        articulo.appendChild(h2);
        articulo.appendChild(imagen);

        document.querySelector("main").appendChild(articulo);

        setInterval(this.cambiarFotografia.bind(this), 3000);
    }

    cambiarFotografia() {
        this.#actual++; // avanzar al siguiente índice

        if(this.#actual >= this.#maximo) this.#actual = 0; // reiniciar al llegar al final

        const $img = $("main article img");
        if($img.length > 0) {
            $img.attr("src", this.#fotografias[this.#actual].url);
            $img.attr("alt", this.#fotografias[this.#actual].titulo);
        }
    }

}