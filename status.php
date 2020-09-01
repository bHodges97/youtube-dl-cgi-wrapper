 <?php
header('Cache-Control: no-cache');
header('Content-Type: text/event-stream');

// Open an inotify instance
$fd = inotify_init();

// Watch __FILE__ for metadata changes (e.g. mtime)
$watch_descriptor = inotify_add_watch($fd, 'status', IN_MODIFY);

// Read events
while(True){
	$filecontent=file_get_contents("status");
	echo "event: message\n";
	echo 'data: ' . $filecontent;
	echo "\n\n";
	ob_end_flush();
	flush();
	if(substr( $filecontent, 11, 9 ) === "Completed" || substr($filecontent,11,6) === "Failed"){
		break;
	}
	$events = inotify_read($fd);
}
inotify_rm_watch($fd, $watch_descriptor);
fclose($fd);
?>


