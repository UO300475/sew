    class Ciudad{
        #nombreCiudad
        #pais
        #gentilicio
        #poblacion
        #coordenadas

        constructor(nombreCiudad, pais, gentilicio){
            this.#nombreCiudad = nombreCiudad;
            this.#pais = pais;
            this.#gentilicio = gentilicio;
        }

        rellenar(poblacion, coordenadas){
            this.#poblacion = poblacion;
            this.#coordenadas = coordenadas;
        }

        getNombreCiudad(){
            return this.#nombreCiudad;
        }

        getNombrePais(){
            return this.#pais;
        }

        getSecundaryInfo(){
            
            return `
                        <ul>
                            <li>Gentilicio: ${this.#gentilicio}</li>
                            <li>Población: ${this.#poblacion ?? 'No disponible'}</li>
                        </ul>
                    `;

        }

        escribirCoordenadas(){

            // Seleccionamos el main
            const main = document.querySelector("main");

            // Creamos el contenedor principal
            const seccion = document.createElement("section");

            // Crear el contenedor principal <p>
            const p = document.createElement("p");
            p.textContent = `Coordenadas de ${this.#nombreCiudad}:`;

            // Crear la lista <ul>
            const ul = document.createElement("ul");

            // Crear los elementos <li> para latitud y longitud
            const liLatitud = document.createElement("li");
            liLatitud.textContent = `Latitud: ${this.#coordenadas.latitud}`;

            const liLongitud = document.createElement("li");
            liLongitud.textContent = `Longitud: ${this.#coordenadas.longitud}`;

            // Insertar los <li> en la lista
            ul.appendChild(liLatitud);
            ul.appendChild(liLongitud);

            // Insertar la lista en el párrafo
            p.appendChild(ul);

            seccion.appendChild(p);

            main.appendChild(seccion);

        }

        mostrarDatos(){

            // Seleccionamos el main
            const main = document.querySelector("main");

            // Creamos el contenedor principal
            const seccion = document.createElement("section");

            // Crear y añadir <p> Ciudad
            const pCiudad = document.createElement("p");
            pCiudad.textContent = `Ciudad: ${this.getNombreCiudad()}`;
            seccion.appendChild(pCiudad);

            // Crear y añadir <p> País
            const pPais = document.createElement("p");
            pPais.textContent = `País: ${this.getNombrePais()}`;
            seccion.appendChild(pPais);

            // Crear y añadir <h3> Información secundaria
            
            const h3 = document.createElement("h3");
            h3.textContent = "Información secundaria";
            seccion.appendChild(h3);

            // Insertar la información secundaria
            const infoSecundaria = document.createElement("div");
            infoSecundaria.innerHTML = this.getSecundaryInfo();
            seccion.appendChild(infoSecundaria);

            main.appendChild(seccion);

            this.escribirCoordenadas();
        }

        getMeteorologiaCarrera() {

            const url = "https://archive-api.open-meteo.com/v1/archive";

            $.ajax({
                url: url,
                method: "GET",
                dataType: "json",
                data: {
                    latitude: this.#coordenadas.latitud,
                    longitude: this.#coordenadas.longitud,
                    hourly: "temperature_2m,apparent_temperature,precipitation,relativehumidity_2m,windspeed_10m,winddirection_10m",
                    daily: "sunrise,sunset",
                    timezone: "auto",
                    start_date: "2025-11-09",
                    end_date: "2025-11-09"
                },
                success: (json) => {
                    const datos = this.procesarJSONCarrera(json);
                    this.mostrarMeteoEnHTML(datos);
                },
                error: () => {
                    console.error("ERROR: No se pudo obtener la meteorología del circuito");
                }
            });
        }

        procesarJSONCarrera(json) {

            // Buscar el índice de las 14:00
            const indice = json.hourly.time.findIndex(hora =>
                hora.endsWith("14:00")
            );

            if (indice === -1) {
                console.error("No se encontraron datos para las 14:00");
                return null;
            }

            const jsonProcesado = {
                hora: json.hourly.time[indice],
                temperatura: json.hourly.temperature_2m[indice],
                termica: json.hourly.apparent_temperature[indice],
                lluvia: json.hourly.precipitation[indice],
                humedad: json.hourly.relativehumidity_2m[indice],
                vientoVel: json.hourly.windspeed_10m[indice],
                vientoDir: json.hourly.winddirection_10m[indice],
                amanecer: json.daily.sunrise[0],
                anochecer: json.daily.sunset[0]
            };

            return jsonProcesado;
        }

       mostrarMeteoEnHTML(datos) {

            // Seleccionamos el main
            const main = $("main");

            // Creamos el contenedor principal
            const seccion = $("<section></section>");

            // Título
            seccion.append("<h3>Información meteorológica del circuito</h3>");

            // Amanecer / anochecer
            const diario = $(`
                <p>
                    <strong>Amanecer:</strong> ${datos.amanecer.replace("T", " ")}<br>
                    <strong>Anochecer:</strong> ${datos.anochecer.replace("T", " ")}
                </p>
            `);
            seccion.append(diario);

            // Subtítulo
            seccion.append("<h4>Datos horarios</h4>");

            // ---------- TABLA ----------
            // border="1" cellspacing="0" cellpadding="5"
            const tabla = $(`
                <table>
                    <thead>
                        <tr>
                            <th>Hora</th>
                            <th>Temperatura (°C)</th>
                            <th>Sensación Térmica (°C)</th>
                            <th>Lluvia (mm)</th>
                            <th>Humedad (%)</th>
                            <th>Viento (km/h)</th>
                            <th>Dirección (°)</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            `);

            const tbody = tabla.find("tbody");

            // Crear filas
            for (let i = 0; i < datos.horas.length; i++) {
                const fila = $(`
                    <tr>
                        <td>${datos.horas[i].split("T")[1]}</td>
                        <td>${datos.temperatura[i]}</td>
                        <td>${datos.termica[i]}</td>
                        <td>${datos.lluvia[i]}</td>
                        <td>${datos.humedad[i]}</td>
                        <td>${datos.vientoVel[i]}</td>
                        <td>${datos.vientoDir[i]}</td>
                    </tr>
                `);

                tbody.append(fila);
            }

            seccion.append(tabla);

            // Finalmente añadimos la sección a <main>
            main.append(seccion);
        }

        getMeteorologiaEntrenos(fechaCarrera) {

            const start_date = "2025-11-07";
            const end_date = "2025-11-08";

            const url = "https://archive-api.open-meteo.com/v1/archive";

            $.ajax({
                url: url,
                method: "GET",
                dataType: "json",
                data: {
                    latitude: this.#coordenadas.latitud,
                    longitude: this.#coordenadas.longitud,
                    hourly: "temperature_2m,precipitation,relativehumidity_2m,windspeed_10m",
                    timezone: "auto",
                    start_date: start_date,
                    end_date: end_date
                },
                success: (json) => {
                    const medias = this.procesarJSONEntrenos(json);
                    this.mostrarMediaEntrenosEnHTML(medias);
                },
                error: () => {
                    console.error("ERROR: No se pudo obtener la meteorología de entrenamientos");
                }
            });
        }

        procesarJSONEntrenos(json) {

            if (!json.hourly || !json.hourly.time) return null;

            const horas = json.hourly.time;
            const temp = json.hourly.temperature_2m;
            const lluvia = json.hourly.precipitation;
            const humedad = json.hourly.relativehumidity_2m;
            const viento = json.hourly.windspeed_10m;

            // Crear objeto para acumular datos por fecha
            const dias = {};

            for (let i = 0; i < horas.length; i++) {
                const fecha = horas[i].split("T")[0];

                if (!dias[fecha]) {
                    dias[fecha] = {temp: [], lluvia: [], humedad: [], viento: []};
                }

                dias[fecha].temp.push(temp[i]);
                dias[fecha].lluvia.push(lluvia[i]);
                dias[fecha].humedad.push(humedad[i]);
                dias[fecha].viento.push(viento[i]);
            }

            // Calcular medias
            const medias = [];

            for (const fecha in dias) {
                const d = dias[fecha];
                const mediaTemp = (d.temp.reduce((a,b)=>a+b,0)/d.temp.length).toFixed(2);
                const mediaLluvia = (d.lluvia.reduce((a,b)=>a+b,0)/d.lluvia.length).toFixed(2);
                const mediaHumedad = (d.humedad.reduce((a,b)=>a+b,0)/d.humedad.length).toFixed(2);
                const mediaViento = (d.viento.reduce((a,b)=>a+b,0)/d.viento.length).toFixed(2);

                medias.push({
                    fecha,
                    temp: mediaTemp,
                    lluvia: mediaLluvia,
                    humedad: mediaHumedad,
                    viento: mediaViento
                });
            }

            return medias;
        }

        mostrarMediaEntrenosEnHTML(medias) {

            if (!medias) return;

            const main = $("main");

            const seccion = $("<section></section>");
            seccion.append("<h3>Medias meteorológicas de entrenamientos</h3>");

            for (let i = 0; i < medias.length; i++) {
                const dia = medias[i];

                const p = $(`
                    <p><strong>Fecha:</strong> ${dia.fecha}</p>
                `);

                const ul = $(`
                    <ul>
                        <li>Temperatura media: ${dia.temp} °C</li>
                        <li>Lluvia media: ${dia.lluvia} mm</li>
                        <li>Humedad media: ${dia.humedad} %</li>
                        <li>Viento medio: ${dia.viento} km/h</li>
                    </ul>
                `);

                seccion.append(p);
                seccion.append(ul);
            }

            main.append(seccion);
        }
    }

