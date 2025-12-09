class Cronometro{
    
    #tiempo
    #inicio
    #corriendo

    constructor(){
        this.#tiempo = 0;

        const botones = document.querySelectorAll("main button");

        if (botones.length == 3){
            botones[0].addEventListener("click", (event) => {
                this.arrancar();
            })
            botones[1].addEventListener("click", (event) => {
                this.parar();
            })
            botones[2].addEventListener("click", (event) => {
                this.restart();
            })
        }

    }

    
    arrancar() {
        if (!this.#corriendo) {
            try {
            // Intentamos usar Temporal si está disponible
                this.#inicio = Temporal.Now.instant() - this.#tiempo; // Obtenemos el instante actual
            } catch (error) {
                // Si Temporal no está disponible, usamos Date
                    this.#inicio = new Date() - this.#tiempo;
            }
            this.#corriendo = setInterval(this.actualizar.bind(this), 100);
        }

    }

    actualizar(){
        let ahora;
        try {
            ahora = Temporal.Now.instant();
            // Calculamos la diferencia en milisegundos
            this.#tiempo = ahora - this.#inicio;
        } catch (error) {
            ahora = new Date();
            this.#tiempo = ahora - this.#inicio;
        }
        this.mostrar();
    }

    mostrar(){
        this.minutos = parseInt(this.#tiempo / 60000);
        this.segundos = parseInt((this.#tiempo % 60000) / 1000);
        this.decimas = parseInt((this.#tiempo % 1000) / 100);

        
        var stringMinutos = this.minutos < 10 ? "0" + this.minutos : this.minutos;
        var stringSegundos = this.segundos < 10 ? "0" + this.segundos : this.segundos;

        var stringCronometro = stringMinutos + ":" +
                                stringSegundos + "." +
                                this.decimas;

        document.querySelector("main p").textContent = stringCronometro;
    }

    parar(){
        clearInterval(this.#corriendo);
        this.#corriendo = null;
    }

    restart(){
        clearInterval(this.#corriendo);
        this.#corriendo = null;
        this.#tiempo = 0;
        this.#inicio = null;
        this.mostrar();
    }
}