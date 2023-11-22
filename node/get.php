
<?php
// Check if the file path is provided in the POST request
if (isset($_POST['file_name'])) {
    // Get the file path from the POST request
    $file = $_POST['file_name'];

    $file = 'c/'.$file;

    // Read the file contents
    $content = file_get_contents($file);

    // Set the response headers
    header('Content-Type: text/plain');
    header('Content-Disposition: attachment; filename="file.txt"');

    // Output the file contents to the response
    echo $content;
} else {
    // File path not provided in the POST request
    echo "File path not specified.";
}
