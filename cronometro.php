<?php

class Cronometro{
    private $tiempo;
    private $inicio;
    private $fin;


    public function __construct(){
        $this->tiempo = 0;
    }

    public function arrancar(){
        $this->inicio = microtime(true);
    }
    
    public function parar(): void
    {
        if ($this->inicio === null) {
            return; // No se arrancó el cronómetro
        }
        $fin = microtime(true);
        $this->tiempo = $fin - $this->inicio;
        $this-
        
        >inicio = null; // opcional: limpiar estado
    }
    
    public function mostrar(): string
    {
        $totalSegundos = $this->tiempo;
        $minutos = (int) floor($totalSegundos / 60);
        $segundos = (int) floor($totalSegundos % 60);
        $decimas = (int) floor(($totalSegundos - floor($totalSegundos)) * 10);

        echo "<p>Tiempo = " . sprintf('%02d:%02d.%01d', $minutos, $segundos, $decimas) . "</p>"; ;
    }

    if (count($_POST)>0) 
    {   
        $cronometro = new Cronometro();

        if(isset($_POST['arrancar'])) $cronometro->arrancar();
        if(isset($_POST['parar'])) $cronometro->parar();
        if(isset($_POST['mostrar'])) $miBocronometrotonera->mostrar();

    }

    echo "  
            <form action='#' method='post' name='botones'>
                <div>
                    <input type = 'submit' class='button' name = 'arrancar' value = 'Arrancar'/>
                    <input type = 'submit' class='button' name = 'parar' value = 'Parar'/>
                    <input type = 'submit' class='button' name = 'mostrar' value = 'Mostrar'/>
                </div>                 
            </form>
        ";
}
?>

<!DOCTYPE HTML>
<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />

    <meta name ="author" content ="Guillermo Gil Naves" />

    <meta name ="description" content ="Cronometro" />

    <meta name ="keywords" content ="aquí cada documento debe tener la lista
    de las palabras clave del mismo separadas por comas" />

    <meta name ="viewport" content ="width=device-width, initial-scale=1.0" />

    <title>MotoGP</title>
    <link rel="icon" href="multimedia/favicon.ico">
    <link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="estilo/layout.css" />
</head>

<body>
    <header>
        <!-- Datos con el contenidos que aparece en el navegador -->
        <h1>MotoGP Desktop</h1>
        <nav>
            <a href="index.html" title = "Inicio de MotoGp-Desktop">Inicio</a>
            <a href="piloto.html" title = "Información del piloto">Piloto</a>
            <a href="circuito.html" title = "Inicio del circuito">Circuito</a>
            <a href="meteorologia.html" title = "Información de la meteorologia">Meteorologia</a>
            <a href="clasificaciones.html" title = "Información de las clasificaciones">Clasificaciones</a>
            <a href="juegos.html" title = "Información de los juegos">Juegos</a>
            <a href="ayuda.html" title = "Información de la ayuda">Ayuda</a>
        </nav>
    </header>
    <p>Estas en: <a href="juegos.html" title = "Información de los juegos">Juegos</a> >> <strong>Cronometro</strong></p>
    <main>
        <h2>Cronometro de MotoGp-Desktop</h2>
        <?php
            eval($codigoFuente);
        ?>
    </main>
</body>
</html>