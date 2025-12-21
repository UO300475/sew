<?php
class Clasificacion {
    protected $documento;
    protected $campeon;
    protected $tiempoCampeon;
    protected $clasificacionMundial;

    public function __construct() {
        $this->documento = "xml/circuitoEsquema.xml";
        $this->campeon = "";
        $this->tiempoCampeon = "";
        $this->clasificacionMundial = [];
    }

    public function consultar() {

        if (!file_exists($this->documento)) {
            return;
        }

        $xml = simplexml_load_file($this->documento);

        if (isset($xml->vencedor)) {
            $this->campeon = (string) $xml->vencedor->nombrePiloto;
            $this->tiempoCampeon = (string) $xml->vencedor->tiempo;
        }

        if (isset($xml->clasificacionMundial)) {
            foreach ($xml->clasificacionMundial->piloto as $piloto) {
                $this->clasificacionMundial[] = [
                    'posicion' => (string) $piloto['posicion'],
                    'piloto'   => (string) $piloto->nombrePiloto,
                    'puntos'   => (string) $piloto['puntos'],
                    'equipo'   => (string) $piloto['equipo']
                ];
            }
        }
    }


    public function mostrarCampeon() {
        return "Ganador: {$this->campeon} - Tiempo: {$this->tiempoCampeon}";
    }

    public function mostrarClasificacion() {
        if (empty($this->clasificacionMundial)) {
            return "<p>No hay clasificación disponible.</p>";
        }

        $html = "<ol>";
        foreach ($this->clasificacionMundial as $p) {
            $html .= "<li>{$p['piloto']} - {$p['puntos']} puntos</li>";
        }
        $html .= "</ol>";
        return $html;
    }
}

$clas = new Clasificacion();
$clas->consultar();
?>


<!DOCTYPE HTML>

<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />

    <meta name ="author" content ="Guillermo Gil Naves" />

    <meta name ="description" content ="Información de clasificaciones del proyecto MotoGp-Desktop" />

    <meta name ="keywords" content ="aquí cada documento debe tener la lista
    de las palabras clave del mismo separadas por comas" />

    <meta name ="viewport" content ="width=device-width, initial-scale=1.0" />

    <title>MotoGP-Clasificaciones</title>
    <link rel="icon" href="multimedia/favicon.ico">
    <link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="estilo/layout.css" />
</head>

<body>
    <header>
        <!-- Datos con el contenidos que aparece en el navegador -->
        <h1><a href="index.html" title = "Inicio de MotoGp-Desktop">MotoGP Desktop</a></h1>
        <nav>
            <a href="index.html" title = "Inicio de MotoGp-Desktop">Inicio</a>
            <a href="piloto.html" title = "Información del piloto">Piloto</a>
            <a href="circuito.html" title = "Inicio del circuito">Circuito</a>
            <a href="meteorologia.html" title = "Información de la meteorologia">Meteorologia</a>
            <a class="activate" href="clasificaciones.php" title = "Información de las clasificaciones">Clasificaciones</a>
            <a href="juegos.html" title = "Información de los juegos">Juegos</a>
            <a href="ayuda.html" title = "Información de la ayuda">Ayuda</a>
        </nav>
    </header>

    <p>Estas en: <a href="index.html" title = "Inicio de MotoGp-Desktop">Inicio</a> >> <strong>Clasificaciones</strong></p>

    <main>
        <h2>Clasificaciones de MotoGp-Desktop</h2>
        <h3>Campeon de la carrera</h3>
        <p><?php echo $clas->mostrarCampeon(); ?></p>

        <h3>Clasificación Mundial tras la carrera</h3>
        <?php echo $clas->mostrarClasificacion(); ?>
    </main>
</body>
</html>