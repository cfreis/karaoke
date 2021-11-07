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
    <h2 class="style7" align=center>Lista de músicas</h2>
    <h3 class="style7" align=center>Digite um pedaço do título ou nome do intérprete para filtrar</h3>
    <h3 class="style7" align=center> e clique no título da música para selecioná-la.</h3>
 
    <div class="divCinza">
        <font size="1"><br></font>
        <form name="form1" method="post" action="buscaMusica.php">
        <font size="12">
            <table width="40%"  border="0" align="center">
            <tr>
            
                <td width="20%" align="center">Título</td>
            <?php echo '<td width="20%" align="center"><input name="titulo" placeholder="Título da música" type="text" id="titulo" value="'.$titulo.'">';?>
            </tr>
            <tr>
                <td width="20%" align="center">Intérprete</td>
            <?php echo '<td width="20%" align="center"><input name="cantor" placeholder="Nome do interprete" type="text" id="cantor" value="'.$cantor.'">';?>
            </tr>
            <tr>
            <td><br></td>
            </tr>
            <tr>
                <td width="20%" align="center"><input type="submit" class="but" name="submit" value="Procurar"></td>
                <td width="20%" align="center"><input type="button" class="but" name="cancel" value="Cancelar" onclick="cancela()" ></td>

            </tr>
        </table>
        </form>
        <font size="1"><br></font>
    </div>
    
   
<!--    <p class="barNav2" accesskey=""align=center>
        <a href="incluiProfessor.php?id=novo" >Procurar</a>
    </p>-->
    <div class="divCinza">
          <font size="1"><br></font>
          
<?php

$sql = 'SELECT titulo, cantor, codigo FROM musicas';

if(! empty($cantor) && ! empty($titulo)){
    $sql = $sql.' WHERE titulo like "%'.$titulo.'%" and cantor like "%'.$cantor.'%";';
}else 
    if(empty($cantor) && ! empty($titulo)){
        $sql = $sql.' WHERE titulo like "%'.$titulo.'%";';
    }else
        if(! empty($cantor) && empty($titulo)){
            $sql = $sql.' WHERE cantor like "%'.$cantor.'%";';
        }else{
            $sql = $sql.' limit 50;';
        }
            

//echo $sql;

$results = $db->query($sql);
 
//Montando o cabeçalho da tabela
$table = '<table border=1 width="98%"  style="border-collapse: collapse" align="center"><tr>';
$table .= '<th align="center">TÍTULO</th><th align="center">INTÉRPRETE</th>';

//Montando o corpo da tabela
$table .= '<tbody>';
while($row = $results->fetchArray()){
	$table .= '<tr>';
    $table .= '<td align="center"> <a href="incluiMusica.php?id='.$row['Codigo'].'">'.$row['Titulo'].'</a></td>';
    $table .= '<td align="center"> '.$row['Cantor'].'</td>';
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


