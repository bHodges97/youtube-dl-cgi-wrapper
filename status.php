 <?php
header('Cache-Control: no-cache');
header('Content-Type: text/event-stream');

echo "event: message\n";
echo 'data: ';
readfile("status");
echo "\n\n";
flush();
?>

