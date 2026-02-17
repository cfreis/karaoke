<?php
require("./database.php");
error_reporting(1);

extract($_POST);

$codigo = $_GET["id"];


$sql = "SELECT titulo, cantor, codigo FROM musicas where codigo = '".$codigo."';";

$result = $db->query($sql);
$row = $result->fetchArray();

//Montando o corpo da pagina
?>

<!DOCTYPE HTML PUBLIC>
<html>
<head>
    <title>Karaoke - by Clovis Reis</title>
    <meta name="viewport" content="width=device-width">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<link href="./quiz.css" rel="stylesheet" type="text/css">

<script type="text/javascript" src="./js/jquery-1.7.js"></script>

<script>
    function check() {
      nome=document.form1.nome.value;
      if (nome.length<1) {
        alert("Digite o seu nome antes de salvar.");
        document.form1.nome.focus();
          return false;
      }
      return true;
    }


    
    function cancela() {
         location.href="./index.php";
    }
    
</script>

</head>

<body>
    <center>
     <img src="./karaoke.png" width="213" height="130">
     </center>
    <h2 class="style7" align=center>Insere música na fila</h2>

    <div class="divCinza">
        <font size="1"><br></font>
        <form name="form1" method="post" onSubmit="return check();">
        <font size="12">
            <table width="40%"  border="0" align="center" >
            <tr>
                <td width="20%" align="center">Nome</td>
                <td width="20%" align="center"><input name="nome" placeholder="Seu Nome" type="text" id="nome" value="">
                <tr>
                <td width="20%" align="center">Título</td>
<?php
    echo '  <td width="20%" align="center"><input name="titulo" placeholder="Título" type="text" id="titulo"value="'.$row['Titulo'].'" readonly>';
    echo '              </tr>';
    echo '              <tr>';
    echo '                <td width="20%" align="center">Intérprete  </td>';
    echo '                <td width="20%" align="center"><input name="cantor" type="text" id="cantor" value="'.$row['Cantor'].'" readonly>';
    ?>
            </tr>
            <tr>
            <td><br></td>
            </tr>
            <tr>
                <td width="20%" align="center"><input type="button" class="but" name="cancel" value="Cancelar" onclick="cancela()" >
                <td width="20%" align="center"><input type="submit" class="but"  name="submit" value="Salvar" ></td>
            </td>
            </tr>
        </table>
        </form>
        <font size="1"><br></font>
    </div>

</body>
</html>

<?php
if($submit=='Salvar')
{
    $sql = 'INSERT INTO fila VALUES("'.$nome.'","'.$titulo.'","'.$codigo.'");';
    $db->exec($sql);
//    echo "Error in fetch ".$db->lastErrorMsg();
    
//    mysqli_query($cn,'insert into professor (login, nome, senha, ativo) values ("'.$login.'", "'.$nome.'","'.md5('1234').'",1);') or die(mysqli_error());
    echo ' <p align="center" style="font-size:12px; color: red;"> Cadastro realizado com sucesso.</p>';
    $submit="";
    echo "<script>location.href='./index.php';</script>";

}
exit;
?>


