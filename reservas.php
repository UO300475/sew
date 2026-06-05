<?php
session_start();

require_once __DIR__ . '/php/Usuario.php';
require_once __DIR__ . '/php/Recurso.php';
require_once __DIR__ . '/php/Reserva.php';

if (!isset($_SESSION['estado'])) {
    $_SESSION['estado'] = 'inicio';
}

$usuario = new Usuario();
$recurso = new Recurso();
$reserva = new Reserva();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    switch ($_POST['accion']) {

        case 'registro':
            $idUsuario = $usuario->registrar([
                'nombre'    => $_POST['nombre'],
                'apellidos' => $_POST['apellidos'],
                'email'     => $_POST['email'],
                'password'  => $_POST['password'],
                'telefono'  => $_POST['telefono']
            ]);
            if ($idUsuario) {
                $_SESSION['id_usuario']     = $idUsuario;
                $_SESSION['nombre_usuario'] = $_POST['nombre'];
                $_SESSION['estado']         = 'recursos';
                $_SESSION['mensaje']        = "Registro completado correctamente. Bienvenido, " . $_POST['nombre'] . ".";
            } else {
                $_SESSION['mensaje'] = "Error al registrar el usuario. El email puede estar ya en uso.";
            }
            break;

        case 'login':
            $usuarioData = $usuario->login($_POST['email'], $_POST['password']);
            if ($usuarioData) {
                $_SESSION['id_usuario']     = $usuarioData['id_usuario'];
                $_SESSION['nombre_usuario'] = $usuarioData['nombre'];
                $_SESSION['estado']         = 'recursos';
                $_SESSION['mensaje']        = "Bienvenido, " . $usuarioData['nombre'] . ".";
            } else {
                $_SESSION['mensaje'] = "Email o contrasena incorrectos.";
            }
            break;

        case 'seleccionar_recurso':
            $_SESSION['recurso_seleccionado'] = $recurso->getById($_POST['id_recurso']);
            $_SESSION['estado']               = 'presupuesto';
            break;

        case 'confirmar_reserva':
            $idReserva = $reserva->crear(
                $_SESSION['id_usuario'],
                $_POST['id_recurso'],
                $_POST['num_personas']
            );
            if ($idReserva) {
                $reserva->confirmar($idReserva);
                $_SESSION['mensaje'] = "Reserva confirmada correctamente. Numero de reserva: " . $idReserva;
            } else {
                $_SESSION['mensaje'] = "Error al realizar la reserva.";
            }
            $_SESSION['estado'] = 'recursos';
            break;

        case 'ver_reservas':
            $_SESSION['estado'] = 'mis_reservas';
            break;

        case 'anular_reserva':
            $reserva->anular($_POST['id_reserva'], $_SESSION['id_usuario']);
            $_SESSION['mensaje'] = "Reserva anulada correctamente.";
            $_SESSION['estado']  = 'mis_reservas';
            break;

        case 'volver':
            $_SESSION['estado'] = 'recursos';
            break;

        case 'logout':
            session_destroy();
            header("Location: reservas.php");
            exit();
    }
}
?>

<!DOCTYPE HTML>

<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>Leon - Reservas</title>
    <meta name="author" content="Guillermo Gil Naves" />
    <meta name="description" content="Central de reservas de recursos turisticos de Leon" />
    <meta name="keywords" content="Leon, reservas, turismo, recursos turisticos" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="estilo/layout.css" />
    <link rel="icon" href="multimedia/favicon.ico" type="image/ico" />
</head>

<body>
    <!-- Datos con el contenido que aparece en el navegador -->
    <header>
        <h1><a href="index.html" title="Pantalla Principal">Leon Desktop</a></h1>
        <nav>
            <a href="index.html" title="Pagina principal">Inicio</a>
            <a href="gastronomia.html" title="Gastronomia tipica de Leon">Gastronomia</a>
            <a href="rutas.html" title="Rutas turisticas por Leon">Rutas</a>
            <a href="meteorologia.html" title="Informacion meteorologica de Leon">Meteorologia</a>
            <a href="juego.html" title="Juego sobre Leon">Juego</a>
            <a class="activate" href="reservas.php" title="Reservas de recursos turisticos">Reservas</a>
            <a href="ayuda.html" title="Ayuda del sitio web">Ayuda</a>
        </nav>
    </header>
    <p>
        Estas en : <a href="index.html" title="Pantalla Principal">Inicio</a> >> <strong>Reservas</strong>
    </p>
    <main>
        <h2>Central de reservas de Leon</h2>

        <?php if (isset($_SESSION['mensaje'])): ?>
            <p><?php echo $_SESSION['mensaje']; unset($_SESSION['mensaje']); ?></p>
        <?php endif; ?>

        <?php if ($_SESSION['estado'] === 'inicio'): ?>
            <section>
                <h3>Iniciar sesion</h3>
                <form method="post">
                    <input type="hidden" name="accion" value="login" />
                    <fieldset>
                        <legend>Acceso de usuario</legend>
                        <label>Email:
                            <input type="email" name="email" required />
                        </label>
                        <label>Contrasena:
                            <input type="password" name="password" required />
                        </label>
                        <button type="submit">Iniciar sesion</button>
                    </fieldset>
                </form>
            </section>
            <section>
                <h3>Registro de nuevo usuario</h3>
                <form method="post">
                    <input type="hidden" name="accion" value="registro" />
                    <fieldset>
                        <legend>Datos del nuevo usuario</legend>
                        <label>Nombre:
                            <input type="text" name="nombre" required />
                        </label>
                        <label>Apellidos:
                            <input type="text" name="apellidos" required />
                        </label>
                        <label>Email:
                            <input type="email" name="email" required />
                        </label>
                        <label>Contrasena:
                            <input type="password" name="password" required />
                        </label>
                        <label>Telefono:
                            <input type="tel" name="telefono" />
                        </label>
                        <button type="submit">Registrarse</button>
                    </fieldset>
                </form>
            </section>
            <section>
                <h3>Administracion</h3>
                <p><a href="php/configuracion.php" title="Configuracion de la base de datos">Configuracion de la base de datos</a></p>
            </section>

        <?php elseif ($_SESSION['estado'] === 'recursos'): ?>
            <section>
                <h3>Bienvenido, <?php echo $_SESSION['nombre_usuario']; ?></h3>
                <form method="post">
                    <input type="hidden" name="accion" value="ver_reservas" />
                    <button type="submit">Ver mis reservas</button>
                </form>
                <form method="post">
                    <input type="hidden" name="accion" value="logout" />
                    <button type="submit">Cerrar sesion</button>
                </form>
            </section>
            <section>
                <h3>Recursos turisticos disponibles</h3>
                <?php
                $listaRecursos = $recurso->getAll();
                foreach ($listaRecursos as $r):
                ?>
                <article>
                    <h4><?php echo $r['nombre']; ?></h4>
                    <ul>
                        <li>Tipo: <?php echo $r['tipo']; ?></li>
                        <li>Descripcion: <?php echo $r['descripcion']; ?></li>
                        <li>Precio: <?php echo $r['precio']; ?> euros por persona</li>
                        <li>Plazas disponibles: <?php echo $r['plazas']; ?></li>
                        <li>Fecha inicio: <?php echo $r['fecha_inicio']; ?></li>
                        <li>Fecha fin: <?php echo $r['fecha_fin']; ?></li>
                    </ul>
                    <form method="post">
                        <input type="hidden" name="accion" value="seleccionar_recurso" />
                        <input type="hidden" name="id_recurso" value="<?php echo $r['id_recurso']; ?>" />
                        <button type="submit">Reservar</button>
                    </form>
                </article>
                <?php endforeach; ?>
            </section>

        <?php elseif ($_SESSION['estado'] === 'presupuesto'): ?>
            <?php $r = $_SESSION['recurso_seleccionado']; ?>
            <section>
                <h3>Presupuesto de reserva</h3>
                <article>
                    <h4><?php echo $r['nombre']; ?></h4>
                    <ul>
                        <li>Tipo: <?php echo $r['tipo']; ?></li>
                        <li>Descripcion: <?php echo $r['descripcion']; ?></li>
                        <li>Precio por persona: <?php echo $r['precio']; ?> euros</li>
                        <li>Fecha inicio: <?php echo $r['fecha_inicio']; ?></li>
                        <li>Fecha fin: <?php echo $r['fecha_fin']; ?></li>
                    </ul>
                </article>
                <form method="post">
                    <input type="hidden" name="accion" value="confirmar_reserva" />
                    <input type="hidden" name="id_recurso" value="<?php echo $r['id_recurso']; ?>" />
                    <fieldset>
                        <legend>Confirmar reserva</legend>
                        <label>Numero de personas:
                            <input type="number" name="num_personas" min="1"
                                max="<?php echo $r['plazas']; ?>" required />
                        </label>
                        <button type="submit">Confirmar reserva</button>
                    </fieldset>
                </form>
                <form method="post">
                    <input type="hidden" name="accion" value="volver" />
                    <button type="submit">Volver</button>
                </form>
            </section>

        <?php elseif ($_SESSION['estado'] === 'mis_reservas'): ?>
            <section>
                <h3>Mis reservas</h3>
                <?php
                $misReservas = $reserva->getByUsuario($_SESSION['id_usuario']);
                if (count($misReservas) === 0):
                ?>
                    <p>No tienes reservas realizadas.</p>
                <?php else: ?>
                    <?php foreach ($misReservas as $res): ?>
                    <article>
                        <h4><?php echo $res['recurso']; ?></h4>
                        <ul>
                            <li>Fecha de reserva: <?php echo $res['fecha_reserva']; ?></li>
                            <li>Numero de personas: <?php echo $res['num_personas']; ?></li>
                            <li>Precio total: <?php echo $res['precio_total']; ?> euros</li>
                            <li>Estado: <?php echo $res['estado']; ?></li>
                        </ul>
                        <?php if ($res['estado'] !== 'Anulada'): ?>
                        <form method="post">
                            <input type="hidden" name="accion" value="anular_reserva" />
                            <input type="hidden" name="id_reserva" value="<?php echo $res['id_reserva']; ?>" />
                            <button type="submit">Anular reserva</button>
                        </form>
                        <?php endif; ?>
                    </article>
                    <?php endforeach; ?>
                <?php endif; ?>
                <form method="post">
                    <input type="hidden" name="accion" value="volver" />
                    <button type="submit">Volver</button>
                </form>
            </section>

        <?php endif; ?>
    </main>
</body>
</html>