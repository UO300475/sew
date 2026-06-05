<?php
require_once __DIR__ . '/BaseDatos.php';

class Usuario {

    private $bd;

    public function __construct() {
        $this->bd = new BaseDatos();
    }

    public function registrar($datos) {
        $db = $this->bd->conectar();

        $sql = $db->prepare(
            "INSERT INTO Usuario (nombre, apellidos, email, password, telefono)
             VALUES (?, ?, ?, ?, ?)"
        );
        $passwordHash = password_hash($datos['password'], PASSWORD_DEFAULT);
        $sql->bind_param(
            "sssss",
            $datos['nombre'],
            $datos['apellidos'],
            $datos['email'],
            $passwordHash,
            $datos['telefono']
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

    public function login($email, $password) {
        $db = $this->bd->conectar();

        $sql = $db->prepare(
            "SELECT id_usuario, nombre, password FROM Usuario WHERE email = ?"
        );
        $sql->bind_param("s", $email);
        $sql->execute();
        $resultado = $sql->get_result();

        if ($resultado->num_rows === 1) {
            $usuario = $resultado->fetch_assoc();
            if (password_verify($password, $usuario['password'])) {
                $sql->close();
                $this->bd->cerrar();
                return $usuario;
            }
        }
        $sql->close();
        $this->bd->cerrar();
        return null;
    }
}
?>