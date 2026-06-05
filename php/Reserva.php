<?php
require_once __DIR__ . '/BaseDatos.php';
require_once __DIR__ . '/Recurso.php';

class Reserva {

    private $bd;
    private $recurso;

    public function __construct() {
        $this->bd      = new BaseDatos();
        $this->recurso = new Recurso();
    }

    public function crear($idUsuario, $idRecurso, $numPersonas) {
        $recurso     = $this->recurso->getById($idRecurso);
        $precioTotal = $recurso['precio'] * $numPersonas;
        $fechaReserva = date('Y-m-d H:i:s');
        $idEstado    = 1;

        $db  = $this->bd->conectar();
        $sql = $db->prepare(
            "INSERT INTO Reserva
             (id_usuario, id_recurso, id_estado, fecha_reserva, num_personas, precio_total)
             VALUES (?, ?, ?, ?, ?, ?)"
        );
        $sql->bind_param(
            "iiisid",
            $idUsuario,
            $idRecurso,
            $idEstado,
            $fechaReserva,
            $numPersonas,
            $precioTotal
        );

        if ($sql->execute()) {
            $id = $db->insert_id;
            $sql->close();
            $this->bd->cerrar();
            return $id;
        }
        $sql->close();
        $this->bd->cerrar();
        return null;
    }

    public function confirmar($idReserva) {
        $db       = $this->bd->conectar();
        $idEstado = 2;

        $sql = $db->prepare(
            "UPDATE Reserva SET id_estado = ? WHERE id_reserva = ?"
        );
        $sql->bind_param("ii", $idEstado, $idReserva);
        $sql->execute();
        $sql->close();
        $this->bd->cerrar();
    }

    public function getByUsuario($idUsuario) {
        $db  = $this->bd->conectar();
        $sql = $db->prepare(
            "SELECT res.id_reserva, rec.nombre AS recurso, res.fecha_reserva,
             res.num_personas, res.precio_total, e.nombre AS estado
             FROM Reserva res
             JOIN RecursoTuristico rec ON res.id_recurso = rec.id_recurso
             JOIN EstadoReserva e ON res.id_estado = e.id_estado
             WHERE res.id_usuario = ?"
        );
        $sql->bind_param("i", $idUsuario);
        $sql->execute();
        $resultado = $sql->get_result();
        $reservas  = [];
        while ($fila = $resultado->fetch_assoc()) {
            $reservas[] = $fila;
        }
        $sql->close();
        $this->bd->cerrar();
        return $reservas;
    }

    public function anular($idReserva, $idUsuario) {
        $db       = $this->bd->conectar();
        $idEstado = 3;

        $sql = $db->prepare(
            "UPDATE Reserva SET id_estado = ?
             WHERE id_reserva = ? AND id_usuario = ?"
        );
        $sql->bind_param("iii", $idEstado, $idReserva, $idUsuario);
        $sql->execute();
        $sql->close();
        $this->bd->cerrar();
    }
}
?>