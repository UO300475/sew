class Ciudad {

    #nombre
    #pais
    #gentilicio
    #poblacion
    #coordenadas

    constructor(nombre, pais, gentilicio) {
        this.#nombre = nombre;
        this.#pais = pais;
        this.#gentilicio = gentilicio;
    }

    rellenar(poblacion, coordenadas) {
        this.#poblacion = poblacion;
        this.#coordenadas = coordenadas;
    }

    getNombreCiudad() {
        return this.#nombre;
    }

    getPais() {
        return this.#pais;
    }

    getInfoSecundaria() {
        const ul = document.createElement("ul");

        const liGentilicio = document.createElement("li");
        liGentilicio.textContent = `Gentilicio: ${this.#gentilicio}`;
        ul.appendChild(liGentilicio);

        const liPoblacion = document.createElement("li");
        liPoblacion.textContent = `Poblacion: ${this.#poblacion ?? "Desconocida"}`;
        ul.appendChild(liPoblacion);

        return ul;
    }

    escribirCoordenadas() {
        const main = document.querySelector("main section");

        if (this.#coordenadas && this.#coordenadas.lat && this.#coordenadas.lng) {
            const pTitulo = document.createElement("p");
            pTitulo.textContent = `Coordenadas de ${this.#nombre}:`;
            main.appendChild(pTitulo);

            const ul = document.createElement("ul");

            const liLat = document.createElement("li");
            liLat.textContent = `Latitud: ${this.#coordenadas.lat}`;
            ul.appendChild(liLat);

            const liLng = document.createElement("li");
            liLng.textContent = `Longitud: ${this.#coordenadas.lng}`;
            ul.appendChild(liLng);

            main.appendChild(ul);

        } else {
            const pNoCoords = document.createElement("p");
            pNoCoords.textContent = `No se han definido coordenadas para ${this.#nombre}.`;
            main.appendChild(pNoCoords);
        }
    }

    mostrarDatos() {
        const main = document.querySelector("main");
        const section = document.createElement("section");

        const h2 = document.createElement("h2");
        h2.textContent = `Meteorologia de ${this.#nombre}`;
        section.appendChild(h2);

        const pCiudad = document.createElement("p");
        pCiudad.textContent = `Ciudad: ${this.getNombreCiudad()}`;
        section.appendChild(pCiudad);

        const pPais = document.createElement("p");
        pPais.textContent = `Pais: ${this.getPais()}`;
        section.appendChild(pPais);

        const h3Info = document.createElement("h3");
        h3Info.textContent = "Informacion adicional";
        section.appendChild(h3Info);

        section.appendChild(this.getInfoSecundaria());
        main.appendChild(section);

        this.escribirCoordenadas();
    }

    getMeteorologia() {
        const url = "https://api.open-meteo.com/v1/forecast";

        $.ajax({
            url: url,
            method: "GET",
            dataType: "json",
            data: {
                latitude: this.#coordenadas.lat,
                longitude: this.#coordenadas.lng,
                current: "temperature_2m,apparent_temperature,precipitation,relativehumidity_2m,windspeed_10m,winddirection_10m,weathercode",
                daily: "sunrise,sunset",
                timezone: "auto",
                forecast_days: 1
            },
            success: (json) => {
                const jsonProcesado = this.procesarJSONMeteorologia(json);
                this.mostrarMeteorologia(jsonProcesado);
            },
            error: () => {
                console.error("ERROR: No se pudo obtener la meteorologia de Leon");
            }
        });
    }

    procesarJSONMeteorologia(json) {
        const jsonProcesado = {
            temperatura: json.current.temperature_2m,
            termica: json.current.apparent_temperature,
            lluvia: json.current.precipitation,
            humedad: json.current.relativehumidity_2m,
            vientoVel: json.current.windspeed_10m,
            vientoDir: json.current.winddirection_10m,
            amanecer: json.daily.sunrise[0],
            anochecer: json.daily.sunset[0]
        };

        return jsonProcesado;
    }

    mostrarMeteorologia(datos) {
        if (!datos) return;

        const contenedor = document.querySelector("main");
        const section = document.createElement("section");

        const amanecerFormateado = datos.amanecer.replace("T", " ");
        const anochecerFormateado = datos.anochecer.replace("T", " ");

        $("<h3>Meteorologia actual en Leon</h3>").appendTo(section);
        $("<p>Salida del sol: " + amanecerFormateado + "</p>").appendTo(section);
        $("<p>Puesta del sol: " + anochecerFormateado + "</p>").appendTo(section);

        const lista = $("<ul></ul>");
        lista.append(`
            <li>Temperatura: ${datos.temperatura} C</li>
            <li>Sensacion termica: ${datos.termica} C</li>
            <li>Lluvia: ${datos.lluvia} mm</li>
            <li>Humedad: ${datos.humedad} %</li>
            <li>Velocidad viento: ${datos.vientoVel} km/h</li>
            <li>Direccion viento: ${datos.vientoDir} grados</li>
        `);
        lista.appendTo(section);
        contenedor.appendChild(section);
    }

    getPrevisiones() {
        const url = "https://api.open-meteo.com/v1/forecast";

        $.ajax({
            url: url,
            method: "GET",
            dataType: "json",
            data: {
                latitude: this.#coordenadas.lat,
                longitude: this.#coordenadas.lng,
                daily: "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,weathercode",
                timezone: "auto",
                forecast_days: 7
            },
            success: (json) => {
                const jsonProcesado = this.procesarJSONPrevisiones(json);
                this.mostrarPrevisiones(jsonProcesado);
            },
            error: () => {
                console.error("ERROR: No se pudo obtener las previsiones de Leon");
            }
        });
    }

    procesarJSONPrevisiones(json) {
        const resultado = [];

        for (let i = 0; i < json.daily.time.length; i++) {
            resultado.push({
                fecha: json.daily.time[i],
                tempMax: json.daily.temperature_2m_max[i],
                tempMin: json.daily.temperature_2m_min[i],
                lluvia: json.daily.precipitation_sum[i],
                viento: json.daily.windspeed_10m_max[i]
            });
        }

        return resultado;
    }

    mostrarPrevisiones(datos) {
        const contenedor = document.querySelector("main");
        const section = document.createElement("section");

        $("<h3>Prevision meteorologica para los proximos 7 dias</h3>").appendTo(section);

        datos.forEach(dia => {
            $("<h4>").text(`Dia: ${dia.fecha}`).appendTo(section);

            const ul = $("<ul></ul>").appendTo(section);
            $("<li>").text(`Temperatura maxima: ${dia.tempMax} C`).appendTo(ul);
            $("<li>").text(`Temperatura minima: ${dia.tempMin} C`).appendTo(ul);
            $("<li>").text(`Lluvia: ${dia.lluvia} mm`).appendTo(ul);
            $("<li>").text(`Viento maximo: ${dia.viento} km/h`).appendTo(ul);
        });

        contenedor.appendChild(section);
    }
}