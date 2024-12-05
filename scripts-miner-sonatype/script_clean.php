<?php

$linhas = explode("\n", `cat artefatos_categorizados_v7.log`); // Lê o arquivo e o transforma em um array de linhas


$inicio = true;

foreach ($linhas as $linha) {
    $linha = trim($linha);
    $partes = explode("#", $linha); // Divide a linha pelo caractere #
    
    
    foreach ($partes as $parte) {
	
	    if($inicio) {
		// Armazenando o groupID    
		$groupId = explode(":", $parte)[0];
		echo $parte;
		$inicio = false;
		continue;
	}

	// Eliminando a hashtag GroupID
        if (trim($parte) != $groupId) { 
            echo "#".$parte;
        }
    }
    $inicio = true;
    $groupId = "";
    echo "\n"; // Adiciona uma linha em branco entre as linhas processadas
}

?>
