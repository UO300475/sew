class Memoria{

    #tablero_bloqueado
    #primera_carta
    #segunda_carta
    #cronometro

    constructor(){
        this.#tablero_bloqueado = true;
        this.#primera_carta = null;
        this.#segunda_carta = null;

        this.barajarCartas();

        this.crarFuncionCartas();
        
        this.#tablero_bloqueado = false;

        this.#cronometro = new Cronometro();
        this.#cronometro.arrancar();
    }

    crarFuncionCartas(){
        const cartas = document.querySelectorAll("main article");

        cartas.forEach(carta => {
            carta.addEventListener("click", (event) => {
                this.voltearCarta(event.currentTarget);
            });
        });
    }

    barajarCartas(){
        const contenedor = document.querySelector("main");
        const cartas = contenedor.querySelectorAll("article");
        const listaCartas = Array.from(cartas);
        for (let i = listaCartas.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1)); 
            [listaCartas[i], listaCartas[j]] = [listaCartas[j], listaCartas[i]];
        }
        listaCartas.forEach(carta => contenedor.appendChild(carta));
    }

    reiniciarAtributos(){
        this.#tablero_bloqueado = false;
        this.#primera_carta = null;
        this.#segunda_carta = null;
    }

    deshabilitarCartas(){
        this.#primera_carta.dataset.estado = "revelada";
        this.#segunda_carta.dataset.estado = "revelada";
        this.comprobarJuego()
        this.reiniciarAtributos();
    }

    comprobarJuego(){
        const cartas = document.querySelectorAll("main article");
        const todasVolteadas = Array.from(cartas).every(carta => carta.getAttribute("data-estado") === "revelada");
        if(todasVolteadas){
            this.#cronometro.parar();
            setTimeout(function(){alert("¡¡Enorabuena!! ¡Has ganado el juego!")})
        }
    }

    voltearCarta(carta){
        
        // 1. Comprobaciones iniciales
        if (
            carta.getAttribute("data-estado") === "revelada" || // Ya deshabilitada
            carta.getAttribute("data-estado") === "volteada" || // Ya volteada
            this.#tablero_bloqueado                 // Tablero bloqueado
        ) {
            return; // No hacemos nada
        }

        // 2. Voltear la carta
        carta.dataset.estado = "volteada";

        //3. Logica principal  
        if (!this.#primera_carta) {
            // Caso a) Primera carta
            this.#primera_carta = carta;
            return;
        }        
        // Caso b) Segunda carta
        this.#segunda_carta = carta;
        this.#tablero_bloqueado = true; // Bloqueamos mientras comprobamos

        // Invocamos a comprobarPareja
        this.comprobarPareja();

    }

    cubrirCartas(){
        this.#tablero_bloqueado = true;
        
        setTimeout(function() {
            // Quita el atributo data-estado de las dos cartas
            this.#primera_carta.removeAttribute("data-estado");
            this.#segunda_carta.removeAttribute("data-estado");
                
            // Reinicia atributos para la siguiente jugada
            this.reiniciarAtributos();
            }.bind(this), 1500);
    }

    comprobarPareja(){
        
        const imgPrimera = this.#primera_carta.children[1].getAttribute("src");
        const imgSegunda = this.#segunda_carta.children[1].getAttribute("src");

        const esPareja = imgPrimera == imgSegunda;

        esPareja ? this.deshabilitarCartas() : this.cubrirCartas();
    }
}