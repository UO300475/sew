<?php 
session_start();

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
        $this->inicio = null; // opcional: limpiar estado
    }
    
    public function mostrar()
    {
        $totalSegundos = $this->tiempo;
        $minutos = (int) floor($totalSegundos / 60);
        $segundos = (int) floor($totalSegundos % 60);
        $decimas = (int) floor(($totalSegundos - floor($totalSegundos)) * 10);

        return sprintf('%02d:%02d.%01d', $minutos, $segundos, $decimas); 
    }
}

    if (!isset($_SESSION['crono'])) {
        $_SESSION['crono'] = new Cronometro();
    }

    $crono = $_SESSION['crono'];
    $salida = "00:00.0";

    if (isset($_POST['accion'])) {
        switch ($_POST['accion']) {
            case 'arrancar':
                $crono->arrancar();
                break;

            case 'parar':
                $crono->parar();
                break;

            case 'mostrar':
                $salida = $crono->mostrar();
                break;
        }
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
            <a href="clasificaciones.php" title = "Información de las clasificaciones">Clasificaciones</a>
            <a href="juegos.html" title = "Información de los juegos">Juegos</a>
            <a href="ayuda.html" title = "Información de la ayuda">Ayuda</a>
        </nav>
    </header>
    <p>Estas en: <a href="juegos.html" title = "Información de los juegos">Juegos</a> >> <strong>Cronometro PHP</strong></p>
    <main>
        <h2>Cronometro de MotoGp-Desktop</h2>
        <p><strong><?php echo $salida; ?></strong></p>

        <form method="post">
            <button type="submit" name="accion" value="arrancar">Arrancar</button>
            <button type="submit" name="accion" value="parar">Parar</button>
            <button type="submit" name="accion" value="mostrar">Mostrar</button>
        </form>
    </main>
</body>
</html>