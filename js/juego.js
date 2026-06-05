class Juego {

    #preguntas
    #puntuacion

    constructor() {
        this.#puntuacion = 0;
        this.#preguntas = [
            {
                pregunta: "¿Como se conoce popularmente a la Catedral de Leon?",
                opciones: ["La Bella Leonina", "La Pulchra Leonina", "La Magna Leonina", "La Domus Leonina", "La Gloria Leonina"],
                correcta: 1
            },
            {
                pregunta: "¿Que indicacion tiene la Cecina de Leon?",
                opciones: ["Denominacion de Origen", "Marca de Garantia", "Indicacion Geografica Protegida", "Especialidad Tradicional Garantizada", "Producto Artesanal Certificado"],
                correcta: 2
            },
            {
                pregunta: "¿Con que se elabora el Botillo del Bierzo?",
                opciones: ["Carne de vacuno curada", "Costillas, rabo y huesos de cerdo adobados y ahumados", "Sangre de cerdo con arroz y especias", "Pimientos rojos asados", "Garbanzos con verduras y carnes"],
                correcta: 1
            },
            {
                pregunta: "¿Que nota tiene la Ruta de la Catedral de Leon?",
                opciones: ["7", "8", "9", "6", "10"],
                correcta: 4
            },
            {
                pregunta: "¿Cual es el medio de transporte de la Ruta de las Medulas?",
                opciones: ["Bicicleta", "Caballo", "A pie", "Coche", "Bus turistico"],
                correcta: 2
            },
            {
                pregunta: "¿Que agencia gestiona la Ruta de la Catedral de Leon?",
                opciones: ["Sin agencia", "Turismo del Bierzo", "Turismo Castilla y Leon", "Turismo de Leon", "Guias de Leon"],
                correcta: 3
            },
            {
                pregunta: "¿Cuanto dura la Ruta del Camino de Santiago por Leon?",
                opciones: ["2 horas", "3 horas", "4 horas", "5 horas", "6 horas"],
                correcta: 4
            },
            {
                pregunta: "¿Donde comienza la Ruta de las Medulas?",
                opciones: ["Plaza del Ayuntamiento", "Plaza de Regla", "Plaza de las Medulas", "Plaza Mayor", "Plaza de San Marcos"],
                correcta: 2
            },
            {
                pregunta: "¿Que queso tipico de Leon tiene Indicacion Geografica Protegida?",
                opciones: ["Queso de Burgos", "Queso Manchego", "Queso de Valdeon", "Queso de Cabrales", "Queso de Idiazabal"],
                correcta: 2
            },
            {
                pregunta: "¿Cuantas proteinas tiene la Cecina de Leon por racion?",
                opciones: ["20g", "25g", "32g", "40g", "45g"],
                correcta: 2
            }
        ];
    }

    mostrar() {
        const main = document.querySelector("main");

        const h2 = document.createElement("h2");
        h2.textContent = "Juego sobre Leon";
        main.appendChild(h2);

        const section = document.createElement("section");

        const h3 = document.createElement("h3");
        h3.textContent = "Preguntas sobre los recursos turisticos de Leon";
        section.appendChild(h3);

        this.#preguntas.forEach((pregunta, indicePregunta) => {
            const article = document.createElement("article");

            const h3 = document.createElement("h3");
            h3.textContent = `Pregunta ${indicePregunta + 1}`;
            article.appendChild(h3);

            const p = document.createElement("p");
            p.textContent = pregunta.pregunta;
            article.appendChild(p);

            const ol = document.createElement("ol");

            pregunta.opciones.forEach((opcion, indiceOpcion) => {
                const li = document.createElement("li");

                const label = document.createElement("label");

                const input = document.createElement("input");
                input.type = "radio";
                input.name = `pregunta${indicePregunta}`;
                input.value = indiceOpcion;

                label.appendChild(input);
                label.appendChild(document.createTextNode(opcion));
                li.appendChild(label);
                ol.appendChild(li);
            });

            article.appendChild(ol);
            section.appendChild(article);
        });

        const boton = document.createElement("button");
        boton.textContent = "Enviar respuestas";
        boton.addEventListener("click", () => {
            this.comprobarRespuestas();
        });

        section.appendChild(boton);
        main.appendChild(section);
    }

    comprobarRespuestas() {
        const todasRespondidas = this.#preguntas.every((pregunta, indice) => {
            return document.querySelector(`input[name="pregunta${indice}"]:checked`) !== null;
        });

        if (!todasRespondidas) {
            alert("Debes responder todas las preguntas antes de enviar");
            return;
        }

        this.#puntuacion = 0;

        this.#preguntas.forEach((pregunta, indice) => {
            const respuesta = document.querySelector(`input[name="pregunta${indice}"]:checked`);
            if (parseInt(respuesta.value) === pregunta.correcta) {
                this.#puntuacion++;
            }
        });

        this.mostrarResultado();
    }

    mostrarResultado() {
        const main = document.querySelector("main");
        const section = main.querySelector("section");
        main.removeChild(section);

        const sectionResultado = document.createElement("section");

        const h3 = document.createElement("h3");
        h3.textContent = "Resultado final";
        sectionResultado.appendChild(h3);

        const p = document.createElement("p");
        p.textContent = `Has obtenido una puntuacion de ${this.#puntuacion} sobre ${this.#preguntas.length}`;
        sectionResultado.appendChild(p);

        main.appendChild(sectionResultado);
    }
}