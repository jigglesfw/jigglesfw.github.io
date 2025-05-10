<?php
$directory = "OBJs/";
$files = array_values(array_filter(scandir($directory), function($file) use ($directory) {
    return pathinfo($file, PATHINFO_EXTENSION) === 'obj';
}));
echo json_encode($files);
?>