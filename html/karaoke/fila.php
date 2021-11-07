<?php
//session_start();
require("./database.php");
//include("header.php");
//error_reporting(1);

extract($_POST);


$titulo = $_POST["titulo"];
$cantor = $_POST["cantor"];



//Montando o corpo da pagina
?>

<!DOCTYPE HTML PUBLIC>
<html>
<head>
    <title>Karaoke - by Clovis Reis</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<link href="./quiz.css" rel="stylesheet" type="text/css">

<script type="text/javascript" src="./js/jquery-1.7.js"></script>

<script>
    function cancela() {
         location.href="./index.php";
    }
    
</script>

</head>

<body>
    <center>
     <img src="./karaoke.png" width="213" height="130">
     </center>
    <h2 class="style7" align=center>Fila de execução</h2>

    <div class="divCinza">
        <br>
        <center>
            <input type="button" class="but" name="cancel" value="Voltar" onclick="cancela()" ></td>
        </center>
        <br>
    </div>

    <div class="divCinza">
          <font size="1"><br></font>
          
<?php

$sql = 'SELECT nome, titulo FROM fila';

$results = $db->query($sql);
 
//Pegando os nomes dos campos
$table = '<table border=1 width="98%"  style="border-collapse: collapse" align="center"><tr>';
$table .= '<th align="center">INTÉRPRETE</th><th align="center">TÍTULO</th>';

//Montando o corpo da tabela
$table .= '<tbody>';
while($row = $results->fetchArray()){
	$table .= '<tr>';
    $table .= '<td align="center"> '.$row['nome'].'</a></td>';
    $table .= '<td align="center"> '.$row['titulo'].'</td>';
	$table .= '</tr>';
}
 
//Finalizando a tabela
$table .= '</tbody></table>';
 
//Imprimindo a tabela
echo $table;
?>

          <font size="1"><br></font>

    </div>

</body>
</html>


