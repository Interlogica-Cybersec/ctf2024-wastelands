<!DOCTYPE html>
<html>
<head>
    <title>Survivors' Hub</title>
    <style>
        body {
            background-color: #333; /* Dark grey background */
            color: #fff; /* White text */
            font-family: Arial, sans-serif; /* Font style */
        }
        ul {
            list-style-type: none; /* Remove bullet points */
            padding: 0;
            margin: 0;
            overflow: hidden;
            background-color: #222; /* Dark grey for the menu */
        }
        li {
            float: left; /* Float menu items horizontally */
        }
        li a {
            display: block;
            padding: 16px;
            text-decoration: none;
            color: #fff; /* White text color for links */
            text-align: center; /* Center align text */
        }
        li a:hover {
            background-color: #ffa500; /* Orange highlight on hover */
            color: #000; /* Black text color on hover */
        }
        .content {
            padding-left: 20px; /* Add left padding to content */
        }
        .content a {
            color: #ffa500; /* Orange text color for links within content */
            text-decoration: none; /* Remove underline */
        }
        .content a:hover {
            color: #000; /* Black text color on hover */
            background-color: #ffa500; /* Orange background color on hover */
        }
    </style>
</head>
<body>
<?php
error_reporting(0); // Disable error reporting
$targetDir = "/var/www/html/sharing/uploads/";
$targetFile = $targetDir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));

echo "<div class=\"content\">";
if($imageFileType != "txt" && $imageFileType != "png" && $imageFileType != "jpg") {
    echo "Sorry, only TXT, PNG, and JPG files are allowed.<br>Go back to <a href='/index.php?id=1'>Home</a><br>";
    $uploadOk = 0;
}

if (file_exists($targetFile)) {
    echo "Sorry, file already exists.<br>Go back to <a href='/index.php?id=1'>Home</a><br>";
    $uploadOk = 0;
}

if ($_FILES["fileToUpload"]["size"] > 500000) {
    echo "Sorry, your file is too large.<br>Go back to <a href='/index.php?id=1'>Home</a><br>";
    $uploadOk = 0;
}

if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.<br>Go back to <a href='/index.php?id=1'>Home</a><br>";
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $targetFile)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.<br>Go back to <a href='/index.php?id=1'>Home</a><br>";
    } else {
        echo "Sorry, there was an error uploading your file.<br>Go back to <a href='/index.php?id=1'>Home</a><br>";
    }
}
echo "</div>";
?>
</body>
</html>
