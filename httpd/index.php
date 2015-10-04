<html>
<head>
<title>Buscador simple en PHP</title>
</head>
<body>
<form action="index.php" method="post">
Buscar: <input name="palabra">
<input type="submit" name="buscador" value="Buscar">
</form>
<?php

if ($_POST['buscador'])
{ 
	// Tomamos el valor ingresado
	$buscar = $_POST['palabra'];

	// Si está vacío, lo informamos, sino realizamos la búsqueda
	if(empty($buscar))
	{
		echo "No se ha ingresado una cadena a buscar";
	} else {
		echo "NO EMPTY POST".$buscar;
		// Conexión a la base de datos y seleccion de registros
		$con=mysql_connect("localhost","root","root");
		$sql = "SELECT * FROM pelis WHERE title like '%$buscar%'";
		mysql_select_db("DB", $con); 

		$result = mysql_query($sql, $con); 

		// Tomamos el total de los resultados
		$total = mysql_num_rows($result);

		echo "TOTAL".$total;

		// Imprimimos los resultados
		if ($row = mysql_fetch_array($result)){ 
			echo "Resultados para: <b>$buscar</b>";
			do { 
				echo "Valor: ".$row['title']; 
			} while ($row = mysql_fetch_array($result)); 
			echo "<p>Resultados: $total</p>";
		} else { 
			// En caso de no encontrar resultados
			echo "No se encontraron resultados para: <b>$buscar</b>"; 
		}
	}
} else {
	// En caso de no encontrar resultados
	echo "No llega el POST"; 
}
?>
</body>
</html>
