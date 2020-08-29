<html> 
  <form id="form1">
  <label for="url">URL:</label>
  <input type="text" id="url" name="url" required="required" size=45>
  <br><br>
  <label for="video">video</label>
  <input type="radio" id="video" name="type" value="video">
  <br><br>
  <label for="audio">audio</label>
  <input type="radio" id="audio" name="type" value="audio">
  <br><br>
  <label for="format">format:</label>
  <select id="format" name="format">
  </select>
  <br><br>
  <input type="submit" value="Submit">
</form>
<br><br>
<div id="out">Press submit to download</div>
<script>
function changeOpts(opts){
	var select = document.getElementById('format');
	select.textContent = "";
	for (let i = 0; i < opts.length; i++){
		var opt = document.createElement('option');
		opt.value = opts[i];
		opt.innerHTML = opts[i];
		select.appendChild(opt);
	}
}
var audio_opts = ["wav","mp3","aac","flac","m4a","opus","vorbis"];
var video_opts = ["mkv","mp4","flv","ogg","webm","avi"];
var audio_btn = document.getElementById('audio');
var video_btn = document.getElementById('video');
audio_btn.onclick = ()=>changeOpts(audio_opts); 
video_btn.onclick = ()=>changeOpts(video_opts); 
video_btn.checked = true;
changeOpts(video_opts);


function formSubmit(event) {
  var url = "dlscript.py";
  var request = new XMLHttpRequest();
  var out = document.getElementById("out"); 
  request.open('POST', url, true);
  request.onload = function() { // request successful
  // we can use server response to our request now
  	out.innerHTML = request.responseText;
  };

  request.onerror = function() {
  	out.innerHTML = "Download failed.";
    // request failed
  };

  request.send(new FormData(event.target)); // create FormData from form that triggered event
  out.innerHTML = "Preparing download, please wait.";
  event.preventDefault();
}

document.getElementById("form1").addEventListener("submit", formSubmit);
</script>
</html>