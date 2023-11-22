
<?php

// Check if a file was uploaded successfully
if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    // Retrieve the file data
    $file = $_FILES['file'];

    // Specify the destination directory
    $destinationDir = 'c/';

    // Generate a unique filename
    $filename = $file['name'];

    // Write the file data to the destination directory
    if (move_uploaded_file($file['tmp_name'], $destinationDir . $filenames)) {
        echo 'File uploaded successfully.';
    } else {
        echo 'Failed to upload file.';
    }
} else {
    echo 'No file uploaded or an error occurred during upload.';
}
