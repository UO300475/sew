<?php
    class Configuracion {

        private $servername;
        private $inicio;
        private $fin;

        public function __construct(){
            $this->servername = "localhost";
            $this->username = "DBUSER2025";
            $this->password = "DBPSWD2025";
            $this->database = "UO300475_DB";
        }
        
        public function reiniciar(){
            $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

            if($db->connect_error) {
                exit ("<h2>ERROR de conexión:".$db->connect_error."</h2>");  
            } else {echo "<h2>Conexión establecida</h2>";}

            borrarDatosObservacionFacilitador();
            borrarDatosResultadoUsabilidad();
            borrarDatosDispositivo();
            borrarDatosUsuario();
            borrarDatosPericiaInformatica();
            borrarDatosGenero();
            borrarDatosProfesion();

            $db->close();
        }

        private function borrarDatosProfesion(){
            $consulta = $db->prepare("DELETE FROM Profesion");
            $consulta.execute();
            $consulta->close();
        }

        private function borrarDatosGenero(){
            $consulta = $db->prepare("DELETE FROM Genero");
            $consulta.execute();
            $consulta->close();
        }

        private function borrarDatosPericiaInformatica(){
            $consulta = $db->prepare("DELETE FROM PericiaInformatica");
            $consulta.execute();
            $consulta->close();
        }

        private function borrarDatosUsuario(){
            $consulta = $db->prepare("DELETE FROM Usuario");
            $consulta.execute();
            $consulta->close();
        }

        private function borrarDatosDispositivo(){
            $consulta = $db->prepare("DELETE FROM Dispositivo");
            $consulta.execute();
            $consulta->close();
        }

        private function borrarDatosResultadoUsabilidad(){
            $consulta = $db->prepare("DELETE FROM ResultadoUsabilidad");
            $consulta.execute();
            $consulta->close();
        }

        private function borrarDatosObservacionFacilitador(){
            $consulta = $db->prepare("DELETE FROM ObservacionFacilitador");
            $consulta.execute();
            $consulta->close();
        }

        public function eliminar(){
            $db = new mysqli($this->servername, $this->username, $this->password, $this->database);

            if($db->connect_error) {
                exit ("<h2>ERROR de conexión:".$db->connect_error."</h2>");  
            } else {echo "<h2>Conexión establecida</h2>";}

            $consulta = "DROP DATABAS UO300475_DB";

            if($db->query($consulta))
                echo "<p>Eliminada la base de datos 'agenda'</p>";
            else
                echo "<p>No se ha podido eliminar la base de datos 'agenda'. Error: " . $db->error . "</p>";

            $db->close();

        }

        public function datosCSV(){
            
        }
        
    }
?>