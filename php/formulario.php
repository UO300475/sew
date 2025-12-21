<?php
require_once("Cronometro.php");
$servername = "localhost";
$username = "DBUSER2025";
$password = "DBPSWD2025";
$database = "UO300475_DB";

/* ------------------ ESTADOS ------------------ */
define("ESTADO_DATOS", 1);
define("ESTADO_TEST", 2);
define("ESTADO_COMENTARIOS", 3);

/* Estado inicial */
if (!isset($_SESSION['estado'])) {
    $_SESSION['estado'] = ESTADO_DATOS;
}

/* ------------------ PROCESAR ACCIONES ------------------ */
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    /* FASE 1 → Iniciar prueba */
    if (isset($_POST['accion']) && $_POST['accion'] === 'iniciar') {

        $_SESSION['usuario'] = [
            'nombre' => $_POST['nombre'],
            'apellidos' => $_POST['apellidos'],
            'genero' => $_POST['genero'],
            'profesion' => $_POST['profesion'],
            'edad' => $_POST['edad'],
            'pericia' => $_POST['pericia'],
            'dispositivo' => $_POST['dispositivo']
        ];

        $_SESSION['cronometro'] = new Cronometro();
        $_SESSION['cronometro']->arrancar();

        $_SESSION['estado'] = ESTADO_TEST;
    }

    /* FASE 2 → Terminar test */
    if (isset($_POST['accion']) && $_POST['accion'] === 'terminar') {

        $_SESSION['respuestas'] = $_POST;

        $_SESSION['cronometro']->parar();
        $_SESSION['tiempo'] = $_SESSION['cronometro']->mostrar();

        $_SESSION['estado'] = ESTADO_COMENTARIOS;
    }

    /* FASE 3 → Guardar todo */
    if (isset($_POST['accion']) && $_POST['accion'] === 'guardar') {

        $comentarios = $_POST['comentarios'] ?? "";

        $db = new mysqli($servername, $username, $password, $database);

        if ($db->connect_error) {
            die("Error de conexión: " . $db->connect_error);
        }

        // A. Profesión
        $stmt = $db->prepare("INSERT INTO Profesion (nombre) VALUES (?)");
        $stmt->bind_param("s", $_SESSION['usuario']['profesion']);
        $stmt->execute();
        $id_profesion = $db->insert_id;
        $stmt->close();

        // B. Género
        $stmt = $db->prepare("INSERT INTO Genero (nombre) VALUES (?)");
        $stmt->bind_param("s", $_SESSION['usuario']['genero']);
        $stmt->execute();
        $id_genero = $db->insert_id;
        $stmt->close();

        // C. Pericia Informática
        $stmt = $db->prepare("INSERT INTO PericiaInformatica (nivel) VALUES (?)");
        $stmt->bind_param("i", $_SESSION['usuario']['pericia']);
        $stmt->execute();
        $id_pericia = $db->insert_id;
        $stmt->close();

        // D. Dispositivo
        $stmt = $db->prepare("INSERT INTO Dispositivo (nombre) VALUES (?)");
        $stmt->bind_param("s", $_SESSION['usuario']['dispositivo']);
        $stmt->execute();
        $id_dispositivo = $db->insert_id;
        $stmt->close();


        $stmt = $db->prepare("INSERT INTO Usuario (id_profesion, edad, id_genero, id_pericia) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("iiii", $id_profesion, $_SESSION['usuario']['edad'], $id_genero, $id_pericia);
        $stmt->execute();
        $id_usuario = $db->insert_id; 
        $stmt->close();

        $tiempo_cronometro = $_SESSION['tiempo'];
        $tiempo_formateado = "00:" . $tiempo_cronometro;
        
        $tarea_completada = 1;
        
        // Recoger datos del formulario actual (Fase 3)
        $comentarios_usuario = $_POST['comentarios'] ?? "";
        $propuestas_mejora = $_POST['propuestas_mejora'] ?? "";
        $valoracion = $_POST['valoracion'] ?? 0;
        $comentarios_observador = $_POST['comentarios_observador'] ?? "";

        // 4. INSERTAR RESULTADO DE USABILIDAD
        $stmt = $db->prepare("INSERT INTO ResultadoUsabilidad (id_usuario, id_dispositivo, tiempo_completado, tarea_completada, comentarios, propuestas_mejora, valoracion) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $stmt->bind_param("iisisss", $id_usuario, $id_dispositivo, $tiempo_formateado, $tarea_completada, $comentarios_usuario, $propuestas_mejora, $valoracion);
        $stmt->execute();
        $stmt->close();

        // 5. INSERTAR OBSERVACIÓN DEL FACILITADOR (Si existe)
        if (!empty($comentarios_observador)) {
            $stmt = $db->prepare("INSERT INTO ObservacionFacilitador (id_usuario, comentario) VALUES (?, ?)");
            $stmt->bind_param("is", $id_usuario, $comentarios_observador);
            $stmt->execute();
            $stmt->close();
        }

        // CERRAR Y LIMPIAR
        $db->close();
        session_destroy();
        $finalizado = true;
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
    <main>
        <h1>Prueba de Usabilidad – MotoGP Desktop</h1>

        <?php if (isset($finalizado)): ?>
            <p>La prueba ha sido guardada correctamente.</p>
        <?php else: ?>

        <form method="post" action="">

        <!-- ================== FASE 1 ================== -->
        <?php if ($_SESSION['estado'] === ESTADO_DATOS): ?>
        <fieldset>
            <legend>Datos del participante</legend>

            <label>
                Nombre:
                <input type="text" name="nombre" required>
            </label><br><br>

            <label>
                Apellidos:
                <input type="text" name="apellidos" required>
            </label><br><br>

            <label>
                Género:
                    <select name="genero" required>
                        <option value="">Seleccione</option>
                        <option value="1">Hombre</option>
                        <option value="2">Mujer</option>
                    </select>      
            </label><br><br>

            <label>
                Profesión:
                <input type="text" name="profesion" required>
            </label><br><br>

            <label>
                Edad:
                <input type="number" name="edad" required>
            </label><br><br>

            <label>
                Pericia Informatica:
                <input type="number" name="pericia" min="0" max="10" required>
            </label><br><br>

            <label>
                Dispositivo:
                <select name="dispositivo" required>
                    <option value="">Seleccione</option>
                    <option value="1">Teléfono</option>
                    <option value="2">Tablet</option>
                    <option value="2">Ordenador</option>
                </select>
            </label><br><br>

            <button type="submit" name="accion" value="iniciar">
                Iniciar prueba
            </button>
        </fieldset>
        <?php endif; ?>

        <!-- ================== FASE 2 ================== -->
        <?php if ($_SESSION['estado'] === ESTADO_TEST): ?>
        <fieldset>
            <legend>Prueba de usabilidad</legend>

            <p>1. ¿Dónde nació Ai Ogura?</p>
            <input type="text" name="p1" required>

            <p>2. ¿Se ven correctamente las fotos de inicio?</p>
            <input type="text" name="p2" required>

            <p>3. ¿Cuál es el nombre del circuito?</p>
            <input type="text" name="p3" required>

            <p>4. ¿En qué equipo esta corriendo Ai Ogura?</p>
            <input type="text" name="p4" required>

            <p>5. ¿Funciona correctamente el juego de memoria?</p>
            <input type="text" name="p5" required>

            <p>6. ¿Funciona correctamente el cronometro?</p>
            <input type="text" name="p6" required>

            <p>7. ¿Cuántos puntos hizo Ai Ogura en la última temporada?</p>
            <input type="text" name="p7" required>

            <p>8. ¿Cuál es el nombre de la ciudad del circuito?</p>
            <input type="text" name="p8" required>

            <p>9. ¿Funcionan los enlaces a otras paginas en la pestaña del piloto?</p>
            <input type="text" name="p9" required>

            <p>10. ¿Se ve correctamente el vídeo del circuito?</p>
            <input type="text" name="p10" required>

            <br>
            <button type="submit" name="accion" value="terminar">
                Terminar prueba
            </button>
        </fieldset>
        <?php endif; ?>

        <!-- ================== FASE 3 ================== -->
        <?php if ($_SESSION['estado'] === ESTADO_COMENTARIOS): ?>
        <fieldset>
            <legend>Valoración del observador</legend>

            <label>
                Comentarios adicionales:
                <br>
                <textarea name="comentarios" rows="6" cols="50"></textarea>
            </label><br><br>

            <label>Propuestas de mejora:
                <br>
                <textarea name="propuestas_mejora"></textarea>
            </label><br><br>

             <label>Valoración:
                <br>
                <input type="number" name="valoracion" min="0" max="10" required>
            </label><br><br>

             <label>Comentarios del observador:
                <br>
                <textarea name="comentarios_observador"></textarea>
            </label><br><br>

            <button type="submit" name="accion" value="guardar">
                Guardar resultados
            </button>
        </fieldset>
        <?php endif; ?>

        </form>
        <?php endif; ?>

    </main>
</body>
</html>
