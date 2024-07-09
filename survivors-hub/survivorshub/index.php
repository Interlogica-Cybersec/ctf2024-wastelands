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

<ul>
    <li><a href="index.php?id=1">Introduction</a></li>
    <li><a href="index.php?id=2">File Upload</a></li>
    <li><a href="index.php?id=3">File Listing</a></li>
    <li><a href="index.php?id=4">Tools</a></li>
</ul>

<?php
// Check if 'id' parameter is set and not empty
if (isset($_GET['id']) && !empty($_GET['id'])) {
    // Check if 'id' parameter is an array
    if (is_array($_GET['id'])) {
        // Print error message with full path of the file
        echo "Error with file ". __FILE__.": 'id' parameter cannot be an array.";
    } else {
        $id = $_GET['id'];
        include_content($id);
    }
} else {
    $id = 1;
    include_content($id);
}

function include_content($id) {
    switch ($id) {
        case 1:
            echo '<div class="content">';
            include 'introduction.php';
            echo '</div>';
            break;
        case 2:
            echo '<div class="content">';
            include 'file_upload.php';
            echo '</div>';
            break;
        case 3:
            echo '<div class="content">';
            include 'file_listing.php';
            echo '</div>';
            break;
        case 4:
            echo '<div class="content">';
            include 'tools.php';
            echo '</div>';
            break;        default:
        echo "Invalid ID";
    }
}
?>

</body>
</html>
