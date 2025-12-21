<?php
session_start();
    class Configuracion {

        private $servername;
        private $username;
        private $password;
        private $database;
        private $message = "";

        public function __construct(){
            $this->servername = "localhost";
            $this->username = "DBUSER2025";
            $this->password = "DBPSWD2025";
            $this->database = "UO300475_DB";
        }
        
        public function crearBaseDatos(){
            $db = new mysqli($this->servername, $this->username, $this->password);

             if ($db->connect_error) {
                $this->message = "<p>Error de conexión: " . $db->connect_error . "</p>";
                return;
            }

            $rutaSQL = "crear_BD_Tablas.sql";

            if (!file_exists($rutaSQL)) {
                $this->message = "<p>No se encuentra el archivo SQL</p>";
                return;
            }

            $sql = file_get_contents($rutaSQL);

            if ($db->multi_query($sql)) {
                do {
                    if ($resultado = $db->store_result()) {
                        $resultado->free();
                    }
                } while ($db->more_results() && $db->next_result());

                $this->message = "<p>Base de datos creada correctamente.</p>";
            } else {
                $this->message = "<p>Error al crear la base de datos: " . $db->error . "</p>";
            }

            $db->close();
        }

        public function reiniciar(){
            $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

            if($db->connect_error) {
                $this->message = "<p>ERROR de conexión:".$db->connect_error."</p>";  
                return;
            } else {$this->message = "<p>Conexión establecida</p>";}

            $db->query("SET FOREIGN_KEY_CHECKS = 0");

            $this->borrarDatosObservacionFacilitador($db);
            $this->borrarDatosResultadoUsabilidad($db);
            $this->borrarDatosDispositivo($db);
            $this->borrarDatosUsuario($db);
            $this->borrarDatosPericiaInformatica($db);
            $this->borrarDatosGenero($db);
            $this->borrarDatosProfesion($db);

            $db->query("SET FOREIGN_KEY_CHECKS = 1");
            $this->message = "<p> Base de datos reiniciada </p>";
            $db->close();
        }

        private function borrarDatosProfesion($db){
            $consulta = $db->prepare("DELETE FROM Profesion");
            $consulta->execute();
            $consulta->close();
        }

        private function borrarDatosGenero($db){
            $consulta = $db->prepare("DELETE FROM Genero");
            $consulta->execute();
            $consulta->close();
        }

        private function borrarDatosPericiaInformatica($db){
            $consulta = $db->prepare("DELETE FROM PericiaInformatica");
            $consulta->execute();
            $consulta->close();
        }

        private function borrarDatosUsuario($db){
            $consulta = $db->prepare("DELETE FROM Usuario");
            $consulta->execute();
            $consulta->close();
        }

        private function borrarDatosDispositivo($db){
            $consulta = $db->prepare("DELETE FROM Dispositivo");
            $consulta->execute();
            $consulta->close();
        }

        private function borrarDatosResultadoUsabilidad($db){
            $consulta = $db->prepare("DELETE FROM ResultadoUsabilidad");
            $consulta->execute();
            $consulta->close();
        }

        private function borrarDatosObservacionFacilitador($db){
            $consulta = $db->prepare("DELETE FROM ObservacionFacilitador");
            $consulta->execute();
            $consulta->close();
        }

        public function eliminar(){
            $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

            if($db->connect_error) {
                $this->message = "<h2>ERROR de conexión:".$db->connect_error."</h2>";
                return;  
            } else {$this->message = "<h2>Conexión establecida</h2>";}

            $consulta = "DROP DATABASE UO300475_DB";

            if($db->query($consulta))
                $this->message = "<p>Base de datos eliminada</p>";
            else
                $this->message = "<p>No se ha podido eliminar la base de datos 'agenda'. Error: " . $db->error . "</p>";

            $db->close();

        }

        public function datosCSV(){
            $db = new mysqli($this->servername, $this->username, $this->password, $this->database);
            if($db->connect_error) {
                return;
            }

            $tablas = [
                "Profesion", "Genero", "PericiaInformatica", "Usuario", 
                "Dispositivo", "ResultadoUsabilidad", "ObservacionFacilitador"
            ];

            header('Content-Type: text/csv; charset=utf-8');
            header('Content-Disposition: attachment; filename=datos_usabilidad.csv');

            $output = fopen('php://output', 'w');

            foreach ($tablas as $tabla) {
                fputcsv($output, ["--- TABLA: $tabla ---"]);
                
                $query = "SELECT * FROM $tabla";
                $result = $db->query($query);

                if ($result && $result->num_rows > 0) {
                    $finfo = $result->fetch_fields();
                    $cabeceras = [];
                    foreach ($finfo as $val) {
                        $cabeceras[] = $val->name;
                    }
                    fputcsv($output, $cabeceras);

                    while ($row = $result->fetch_assoc()) {
                        fputcsv($output, $row);
                    }
                    fputcsv($output, []); 
                }
            }
            
            fclose($output);
            $db->close();
            exit(); 
        }

        public function getMessage(){
            return $this->message;
        }
        
    }

    if (!isset($_SESSION['configuracion'])) {
        $_SESSION['configuracion'] = new Configuracion();
    }

    $configuracion = $_SESSION['configuracion'];

    if (isset($_POST['accion'])) {
        switch ($_POST['accion']) {
            case 'crear':
                $configuracion->crearBaseDatos();
                break;
            case 'reiniciar':
                $configuracion->reiniciar();
                break;

            case 'eliminar':
                $configuracion->eliminar();
                break;

            case 'exportarCSV':
                $configuracion->datosCSV();
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

    <meta name ="description" content ="Configuracion test" />

    <meta name ="keywords" content ="aquí cada documento debe tener la lista
    de las palabras clave del mismo separadas por comas" />

    <meta name ="viewport" content ="width=device-width, initial-scale=1.0" />

    <title>MotoGP</title>
    <link rel="icon" href="../multimedia/favicon.ico">
    <link rel="stylesheet" type="text/css" href="../estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="../estilo/layout.css" />
</head>

<body>
    <header>
        <!-- Datos con el contenidos que aparece en el navegador -->
        <h1>MotoGP Desktop</h1>
        <nav>
            <a href="../index.html" title = "Inicio de MotoGp-Desktop">Inicio</a>
            <a href="../piloto.html" title = "Información del piloto">Piloto</a>
            <a href="../circuito.html" title = "Inicio del circuito">Circuito</a>
            <a href="../meteorologia.html" title = "Información de la meteorologia">Meteorologia</a>
            <a href="../clasificaciones.html" title = "Información de las clasificaciones">Clasificaciones</a>
            <a href="../juegos.html" title = "Información de los juegos">Juegos</a>
            <a href="../ayuda.html" title = "Información de la ayuda">Ayuda</a>
        </nav>
    </header>
    <p>Estas en: <a href="../index.html" title = "Inicio de MotoGp-Desktop">Inicio</a> >> <a href="../juegos.html" title = "Información de los juegos">Juegos</a>  >> <strong>Configuracion Test</strong></p>
    <main>
        <h2>Configuracion Test</h2>

        <form method="post">
            <button type="submit" name="accion" value="crear">Crear Base de Datos</button>
            <button type="submit" name="accion" value="reiniciar">Reiniciar</button>
            <button type="submit" name="accion" value="eliminar">Eliminar</button>
            <button type="submit" name="accion" value="exportarCSV">Exportar a CSV</button>
        </form>

        <?php echo $configuracion->getMessage(); ?>
    </main>
</body>
</html>