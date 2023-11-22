
<?php
$directory = 'c/'; // Replace with the directory path you want to list files from

// Check if the directory exists
if (is_dir($directory)) {
    // Get the list of files in the directory
    $files = scandir($directory);

    // Remove the "." and ".." entries from the list
    $files = array_diff($files, array('.', '..'));

    // Output the list of files
    foreach ($files as $file) {
        // Get the file path
        $filePath = $directory . $file;

        // Check if the file is a regular file
        if (is_file($filePath)) {
            // Generate the download URL
            $downloadUrl = 'http://localhost:20006/' . urlencode($filePath);

            // Print the download URL
            echo $downloadUrl . PHP_EOL;
        }
    }
} else {
    echo "Directory does not exist.";
}
