<?php

#print_r($_FILES);
$tz = 'Indian/Mahe';   
date_default_timezone_set($tz);
//Get current timestamp in milliseconds
$time_start = microtime(true) * 1000;

// Check if a file was uploaded successfully
if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    // Retrieve the file data
    $file = $_FILES['file'];
    //print_r($file);
    // Specify the destination directory
    $destinationDir = 'c/';

    // Generate a unique filename
    $filename = $_POST['name'];

    // Write the file data to the destination directory
    if (move_uploaded_file($file['tmp_name'], $destinationDir . $filename)) {
        #echo 'File uploaded successfully.';
        //Get current timestamp in milliseconds
        $time_end = microtime(true) * 1000;

        $result = array("code" => 0,"time_start" => $time_start, "time_end" => $time_end, "time" => $time_end - $time_start, "timezone" => date_default_timezone_get());
        echo json_encode($result);

    } else {
        #echo 'Failed to upload file.';
        $result = array("code" => 1);
    }
} else {
    echo 'No file uploaded or an error occurred during upload.';
    $result = array("code" => 1);
}
