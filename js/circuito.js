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

    leerArchivoHTML(files) {

        const archivo = files[0];
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
        const seccion = secciones[secciones.length - 1];
        const parser = new DOMParser();
        const doc = parser.parseFromString(contenidoTexto, "image/svg+xml");
        const elementoSVG = doc.documentElement;
        const articuloContenido = document.createElement("article");
        articuloContenido.innerHTML = '';
        articuloContenido.appendChild(elementoSVG);
        seccion.appendChild(articuloContenido);
    }
}