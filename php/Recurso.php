<?php
require_once __DIR__ . '/BaseDatos.php';

class Recurso {

    private $bd;

    public function __construct() {
        $this->bd = new BaseDatos();
    }

    public function getAll() {
        $db = $this->bd->conectar();

        $sql = $db->prepare(
            "SELECT r.id_recurso, r.nombre, r.descripcion, r.precio,
             r.plazas, r.fecha_inicio, r.fecha_fin, t.nombre AS tipo
             FROM RecursoTuristico r
             JOIN TipoRecurso t ON r.id_tipo = t.id_tipo"
        );
        $sql->execute();
        $resultado = $sql->get_result();
        $recursos = [];
        while ($fila = $resultado->fetch_assoc()) {
            $recursos[] = $fila;
        }
        $sql->close();
        $this->bd->cerrar();
        return $recursos;
    }

    public function getById($idRecurso) {
        $db = $this->bd->conectar();

        $sql = $db->prepare(
            "SELECT r.id_recurso, r.nombre, r.descripcion, r.precio,
             r.plazas, r.fecha_inicio, r.fecha_fin, t.nombre AS tipo
             FROM RecursoTuristico r
             JOIN TipoRecurso t ON r.id_tipo = t.id_tipo
             WHERE r.id_recurso = ?"
        );
        $sql->bind_param("i", $idRecurso);
        $sql->execute();
        $resultado = $sql->get_result();
        $recurso = $resultado->fetch_assoc();
        $sql->close();
        $this->bd->cerrar();
        return $recurso;
    }
}
?>