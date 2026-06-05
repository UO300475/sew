<?php
class BaseDatos {

    private $servername;
    private $username;
    private $password;
    private $database;
    private $conexion;

    public function __construct() {
        $this->servername = "localhost";
        $this->username   = "DBUSER2026";
        $this->password   = "DBPWD2026";
        $this->database   = "uo300475_db";
    }

    public function conectar() {
        $this->conexion = new mysqli(
            $this->servername,
            $this->username,
            $this->password,
            $this->database
        );
        if ($this->conexion->connect_error) {
            die("<p>Error de conexion: " . $this->conexion->connect_error . "</p>");
        }
        return $this->conexion;
    }

    public function cerrar() {
        if ($this->conexion) {
            $this->conexion->close();
        }
    }
}
?>