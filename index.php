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
  <div id="subtitle">
  <label for="subtitle_box">Include subtitles</label>
  <input type="checkbox" id=subtitle_box name="subtitle" value="true">
  <br><br>
  </div>
  <input type="submit" value="Submit">
</form>
<br><br>
<div>Status: <span id="stat">On standby</span></div>
<div>Progress: <span id="out">Press submit to download</span></div>
<div>Download: <span id="dl">Unavaliable</span></div>

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

	var subtitles = document.getElementById('subtitle');
	if(opts == audio_opts){
		subtitles.style.display = "none";
	}else{
		subtitles.style.display = "block";
	}
}
var audio_opts = ["wav","mp3","aac","flac","m4a","opus","vorbis"];
var video_opts = ["best","mkv","mp4","flv","ogg","webm","avi"];
var audio_btn = document.getElementById('audio');
var video_btn = document.getElementById('video');
audio_btn.onclick = ()=>changeOpts(audio_opts); 
video_btn.onclick = ()=>changeOpts(video_opts); 
video_btn.checked = true;
changeOpts(video_opts);
</script>
<script src="submit.js"></script>
</html>
