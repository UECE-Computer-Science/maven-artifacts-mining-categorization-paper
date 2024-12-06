<?php

$linhas = explode("\n", `cat artefatos_categorizados_v7.log`);


$inicio = true;

foreach ($linhas as $linha) {
    $linha = trim($linha);
    $partes = explode("#", $linha); 
    
    foreach ($partes as $parte) {
	
	    if($inicio) {
		
		$groupId = explode(":", $parte)[0];
		echo $parte;
		$inicio = false;
		continue;
	}

	
        if (trim($parte) != $groupId) { 
            echo "#".$parte;
        }
    }
    $inicio = true;
    $groupId = "";
    echo "\n"; 
}

?>
