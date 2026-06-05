class Carrusel {

    #busqueda
    #actual
    #maximo
    #fotografias

    constructor() {
        this.#actual = 0;
        this.#maximo = 5;
        this.#fotografias = [
            { url: "multimedia/mapa_leon.jpg", titulo: "Mapa de situacion de Leon" },
            { url: "multimedia/carrusel_catedral.jpg", titulo: "Catedral de Leon" },
            { url: "multimedia/carrusel_medulas.jpg", titulo: "Las Medulas de Leon" },
            { url: "multimedia/carrusel_lago_sanabria.jpg", titulo: "Lago de Sanabria" },
            { url: "multimedia/carrusel_barrio_humedo.jpg", titulo: "Barrio Humedo de Leon" }
        ];
    }

    mostrarFotografias() {
        if (this.#fotografias.length === 0) return;

        const article = document.createElement("article");

        const h2 = document.createElement("h2");
        h2.textContent = "Recursos turisticos de Leon";

        const img = document.createElement("img");
        img.src = this.#fotografias[0].url;
        img.alt = this.#fotografias[0].titulo;

        article.appendChild(h2);
        article.appendChild(img);

        document.querySelector("main").appendChild(article);

        setInterval(this.cambiarFotografia.bind(this), 3000);
    }

    cambiarFotografia() {
        this.#actual++;

        if (this.#actual >= this.#maximo) this.#actual = 0;

        const $img = $("main article img");
        if ($img.length > 0) {
            $img.attr("src", this.#fotografias[this.#actual].url);
            $img.attr("alt", this.#fotografias[this.#actual].titulo);
        }
    }
}