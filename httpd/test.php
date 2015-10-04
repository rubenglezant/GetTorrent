<?php

// Conexión a la base de datos y seleccion de registros
$con=mysql_connect("localhost","root","root");
$sql = "SELECT * FROM pelis WHERE title like '%$buscar%'";
mysql_select_db("DB", $con); 

echo "HOLA";

?>



