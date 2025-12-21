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