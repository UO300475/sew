<?php
session_start();

class Configuracion {

    private $mensaje = "";
    private $servername = "localhost";
    private $username = "DBUSER2026";
    private $password = "DBPWD2026";
    private $database = "uo300475_db";

    public function crearBD() {
        $db = new mysqli($this->servername, $this->username, $this->password);

        if ($db->connect_error) {
            $this->mensaje = "<p>Error de conexion: " . $db->connect_error . "</p>";
            return;
        }

        $rutaSQL = __DIR__ . '/CrearBD.sql';

        if (!file_exists($rutaSQL)) {
            $this->mensaje = "<p>No se encuentra el archivo SQL</p>";
            return;
        }

        $sql = file_get_contents($rutaSQL);

        if ($db->multi_query($sql)) {
            do {
                if ($resultado = $db->store_result()) {
                    $resultado->free();
                }
            } while ($db->more_results() && $db->next_result());
            $this->mensaje = "<p>Base de datos creada correctamente.</p>";
        } else {
            $this->mensaje = "<p>Error al crear la base de datos: " . $db->error . "</p>";
        }

        $db->close();
    }

    public function reiniciar() {
        $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

        if ($db->connect_error) {
            $this->mensaje = "<p>Error de conexion: " . $db->connect_error . "</p>";
            return;
        }

        $db->query("SET FOREIGN_KEY_CHECKS = 0");
        $db->query("DELETE FROM Reserva");
        $db->query("DELETE FROM Usuario");
        $db->query("DELETE FROM RecursoTuristico");
        $db->query("DELETE FROM EstadoReserva");
        $db->query("DELETE FROM TipoRecurso");
        $db->query("SET FOREIGN_KEY_CHECKS = 1");

        $this->mensaje = "<p>Base de datos reiniciada correctamente</p>";
        $db->close();
    }

    public function eliminar() {
        $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

        if ($db->connect_error) {
            $this->mensaje = "<p>Error de conexion: " . $db->connect_error . "</p>";
            return;
        }

        if ($db->query("DROP DATABASE uo300475_db")) {
            $this->mensaje = "<p>Base de datos eliminada correctamente</p>";
        } else {
            $this->mensaje = "<p>Error al eliminar la base de datos: " . $db->error . "</p>";
        }

        $db->close();
    }

    public function cargarDesdeCSV() {
        $archivoCSV = __DIR__ . '/datos.csv';

        if (!file_exists($archivoCSV)) {
            $this->mensaje = "<p>Error: No se encuentra el archivo CSV</p>";
            return;
        }

        $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

        if ($db->connect_error) {
            $this->mensaje = "<p>Error de conexion: " . $db->connect_error . "</p>";
            return;
        }

        $handle      = fopen($archivoCSV, 'r');
        $tablaActual = '';
        $columnas    = [];
        $insertados  = 0;

        while (($linea = fgetcsv($handle, 1000, ',')) !== false) {
            if (strpos($linea[0], '--- TABLA:') !== false) {
                preg_match('/--- TABLA: (\w+) ---/', $linea[0], $matches);
                $tablaActual = $matches[1] ?? '';
                $columnas    = [];
                continue;
            }

            if (!empty($tablaActual) && empty($columnas)) {
                $columnas = $linea;
                continue;
            }

            if (!empty($tablaActual) && !empty($columnas) && !empty($linea[0])) {
                $placeholders = implode(',', array_fill(0, count($columnas), '?'));
                $colNames     = implode(',', $columnas);
                $sql = $db->prepare(
                    "INSERT IGNORE INTO {$tablaActual} ({$colNames}) VALUES ({$placeholders})"
                );
                $tipos = str_repeat('s', count($linea));
                $sql->bind_param($tipos, ...$linea);
                if ($sql->execute()) {
                    $insertados++;
                }
                $sql->close();
            }
        }

        fclose($handle);
        $db->close();
        $this->mensaje = "<p>Se han cargado {$insertados} registros desde el CSV</p>";
    }

    public function exportarCSV() {
        $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

        if ($db->connect_error) {
            $this->mensaje = "<p>Error de conexion: " . $db->connect_error . "</p>";
            return;
        }

        $tablas = ['TipoRecurso', 'EstadoReserva', 'RecursoTuristico', 'Usuario', 'Reserva'];

        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename=datos_exportados.csv');

        $output = fopen('php://output', 'w');

        foreach ($tablas as $tabla) {
            fputcsv($output, ["--- TABLA: $tabla ---"]);

            $resultado = $db->query("SELECT * FROM $tabla");

            if ($resultado && $resultado->num_rows > 0) {
                $finfo     = $resultado->fetch_fields();
                $cabeceras = [];
                foreach ($finfo as $val) {
                    $cabeceras[] = $val->name;
                }
                fputcsv($output, $cabeceras);

                while ($fila = $resultado->fetch_assoc()) {
                    fputcsv($output, $fila);
                }
                fputcsv($output, []);
            }
        }

        fclose($output);
        $db->close();
        exit();
    }

    public function getMensaje() {
        return $this->mensaje;
    }
}

$configuracion = new Configuracion();

if (isset($_POST['accion'])) {
    switch ($_POST['accion']) {
        case 'crearBD':
            $configuracion->crearBD();
            break;
        case 'reiniciar':
            $configuracion->reiniciar();
            break;
        case 'eliminar':
            $configuracion->eliminar();
            break;
        case 'cargarCSV':
            $configuracion->cargarDesdeCSV();
            break;
        case 'exportarCSV':
            $configuracion->exportarCSV();
            break;
    }
}
?>

<!DOCTYPE HTML>

<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>Leon - Configuracion</title>
    <meta name="author" content="Guillermo Gil Naves" />
    <meta name="description" content="Configuracion de la base de datos de Leon Desktop" />
    <meta name="keywords" content="Leon, configuracion, base de datos" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" type="text/css" href="../estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="../estilo/layout.css" />
    <link rel="icon" href="../multimedia/favicon.ico" type="image/ico" />
</head>

<body>
    <main>
        <h2>Configuracion de la base de datos</h2>
        <section>
            <h3>Operaciones</h3>
            <form method="post">
                <button type="submit" name="accion" value="crearBD">Crear BD</button>
                <button type="submit" name="accion" value="reiniciar">Reiniciar BD</button>
                <button type="submit" name="accion" value="eliminar">Eliminar BD</button>
                <button type="submit" name="accion" value="cargarCSV">Cargar CSV</button>
                <button type="submit" name="accion" value="exportarCSV">Exportar CSV</button>
            </form>
            <?php echo $configuracion->getMensaje(); ?>
        </section>
    </main>
</body>
</html>