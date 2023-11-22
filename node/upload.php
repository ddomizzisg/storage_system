<?php
/**
 * Validar que los datos no esten vacios
 */

include_once './Config.php';
include_once './functions.php';

// print_r($_FILES);/

function uploadFile($file, $disk=True)
{
        //obtener la clave principal del usuario
//      $keyuser = getkeyuser($tokenuser);
        $fileData = file_get_contents('php://input');

        if($disk){
                $file = FOLDER_UPLOADS.$file;
        }#}else{
        #       $file = "php://temp/maxmemory:".LIMIT_MEMORY; 
        #}

        print($file);

        $fhandle = fopen($file, 'wb');
        fwrite($fhandle, $fileData);
        fclose($fhandle);
        //header('Content-type: application/json; charset=utf-8');
        //echo json_encode(array("status" => 200, "message" => "ok"));
        $response['status'] = 200;
        $response['message'] = 'ok';
        return $response;
}

function upload($file)
{
        if (isset($_FILES['uploadedfile']['tmp_name'])) {
                $tmp_name = $_FILES['uploadedfile']['tmp_name'];
                $name = $_FILES['uploadedfile']['name'];
                // $target_path = FOLDER_UPLOADS.$name;
                $target_path = $file;
                if (move_uploaded_file($tmp_name, $target_path)) {
                        $response['status'] = 200;
                        $response['message'] = 'File uploaded successfully';
                        $response['fileId'] = $name;
                } else {
                        $response['status'] = 'error';
                        $response['message'] = 'You can not write to the file';
                }
        } else {
                $response['status'] = 'error';
                $response['message'] = 'Fields empty';
        }
        return $response;
}


if (isset($_GET['file'])) {
        if (!empty($_GET['file']))
                $response = uploadFile($_GET['file']);
}
