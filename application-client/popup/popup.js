chrome.runtime.sendMessage({ action: "commentReq" }, (res)=>{
	if(!res){
		console.log("undefined error: background doesn't respond!");
	}
	else if(!res.status){
		console.log(res.error);
	}
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "commentFound") {
		const no = document.getElementById("no");
		const thumbnail = document.getElementById("thumbnail");
		const exp = document.getElementById("exp");
		const txt = document.getElementById("txt");

		no.style.display = "none";
		thumbnail.style.display = "block";
		exp.style.display = "block";
		txt.style.color = "#71DFBE";
	
		thumbnail.src = message.img; 
		exp.innerHTML = message.title;
    }
});

document.addEventListener("unload", ()=>{
	chrome.runtime.sendMessage({ action: "stopFindComment" });
})



var basicTimeline = anime.timeline({
	autoplay: false
});

var pathEls = $(".check");
for (var i = 0; i < pathEls.length; i++) {
	var pathEl = pathEls[i];
	var offset = anime.setDashoffset(pathEl);
	pathEl.setAttribute("stroke-dashoffset", offset);
}

basicTimeline
.add({
	targets: ".text",
	duration: 1,
	opacity: "0"
})
.add({
	targets: ".button",
	duration: 1300,
	height: 10,
	width: 250,
	backgroundColor: "#65717d",
	border: "0",
	borderRadius: 100
})
.add({
	targets: ".progress-bar",
	// 2000
	duration: 2000,
	width: 250,
	easing: "linear"
})
.add({
	targets: ".button",
	width: 0,
	duration: 1
})
.add({
	targets: ".progress-bar",
	width: 80,
	height: 80,
	delay: 500,
	duration: 750,
	borderRadius: 80,
	backgroundColor: "#71DFBE"
})
.add({
	targets: pathEl,
	strokeDashoffset: [offset, 0],
	duration: 200,
	easing: "easeInOutSine",
	complete: function() {
		chrome.runtime.sendMessage({ action: "summarizeReq" });
	}
});

$(".button").click(function() {
	basicTimeline.play();
	
});

// $(".text").click(function() {
// 	basicTimeline.play();
// });