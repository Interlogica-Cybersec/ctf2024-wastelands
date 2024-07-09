<?php
// Function to validate integer input
function validateInteger($input) {
    return filter_var($input, FILTER_VALIDATE_INT) !== false && $input > 0;
}

// Function to validate absolute path
function validateAbsolutePath($path) {
    return strpos($path, '/') === 0; // Check if the path starts with '/'
}

// Check if all parameters are provided
if (!isset($_GET['path']) || !isset($_GET['width']) || !isset($_GET['height'])) {
    // Check which parameter is missing and display an error message
    if (!isset($_GET['path'])) {
        echo "Error: Path parameter is missing.";
    } elseif (!isset($_GET['width'])) {
        echo "Error: Width parameter is missing.";
    } elseif (!isset($_GET['height'])) {
        echo "Error: Height parameter is missing.";
    }
} else {
    // All parameters are provided, so proceed with image resizing
    $path = $_GET['path'];
    $width = $_GET['width'];
    $height = $_GET['height'];

    // Validate image path
    if (!file_exists($path)) {
        echo "Error: Image not found at the specified path.";
    } elseif (!validateAbsolutePath($path)) {
        echo "Error: Invalid path. Only absolute paths are allowed.";
    } else {
        // Validate file extension to ensure it's an allowed image format
        $allowedExtensions = array('png', 'jpg', 'jpeg', 'gif');
        $fileExtension = pathinfo($path, PATHINFO_EXTENSION);
        if (in_array(strtolower($fileExtension), $allowedExtensions)) {
            // Validate width and height parameters
            if (!validateInteger($width)) {
                echo "Error: Invalid width parameter.";
            } elseif (!validateInteger($height)) {
                echo "Error: Invalid height parameter.";
            } else {
                // Resize the image using ImageMagick
                $tempFilePath = '/var/www/html/sharing/resized/' . uniqid('resized_image_') . '.png'; // Path to store resized image
                $command = "convert -resize {$width}x{$height} " . escapeshellarg($path) . " " . escapeshellarg($tempFilePath);
                shell_exec($command);
                // Check if the image was resized successfully

                if (file_exists($tempFilePath)) {
                        // Display the resized image
                    echo "<img src='../resized/" . basename($tempFilePath) . "' alt='Resized Image'>";
                } else {
                    echo "Error: Failed to resize the image.";
                }
            }
        } else {
            echo "Error: Invalid file format. Only PNG, JPG, JPEG, and GIF files are allowed.";
        }
    }
}
?>
