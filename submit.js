function formSubmit(event) {
	var url = "dlscript.py";
	var request = new XMLHttpRequest();
	var out = document.getElementById("out"); 
	document.getElementById("dl").innerHTML = "Unvaliable"
	request.open('POST', url, true);
	request.onload = function() { // request successful
		// we can use server response to our request now
		var responce = request.responseText.trim();
		document.getElementById("stat").innerHTML = responce
		const source = new EventSource("status.php");
		source.addEventListener("message", function(event) {
			var out = document.getElementById("out"); 
			let res = JSON.parse(event.data);
			out.innerHTML = res.status;
			if(res.status==="Completed" ){
				let link = "<a href=\"" + res.url  +"\">"+ res.url.substring(12) + "</a>";
				document.getElementById("dl").innerHTML = link
			}
			if(res.status==="Completed" || res.status==="Failed"){
				source.close()
			//	document.getElementById("stat").innerHTML = "On standby";
			}
		});
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
