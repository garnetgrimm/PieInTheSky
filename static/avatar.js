var currNum = 1;

var currSkin = 0;
var maxSkin = 4;

var x = 75;
var y = 30;

var hatY = 0;

var currEyeColor = 0;

function changeImgLeft(imgType, maxPart) {
	currNum++;
	if(currNum > maxPart) currNum = 1;
	var x = document.getElementById(imgType);
	x.src = "parts/" + imgType + "/" + imgType + " (" + currNum + ").png"; 
}

function changeImgRight(imgType, maxPart) {
	currNum--;
	if(currNum < 1) currNum = maxPart;
	var x = document.getElementById(imgType);
	x.src = "parts/" + imgType + "/" + imgType + " (" + currNum + ").png"; 
}

function colorSkinLeft() {
	currSkin++;
	var x = document.getElementsByClassName("skin");
	for(i = 0; i < x.length; i++) {
		var currStyle = x[i].getAttribute("style");
		
		var Find = ["hue-rotate", "-webkit-filter"];
		var New = [" hue-rotate(" + (currSkin * 20) + "deg);", " -webkit-filter: hue-rotate("+ (currSkin * 20) + "deg);"];
	
		x[i].setAttribute("style", replaceAttributes(currStyle, Find, New));
	}
}

function colorSkinRight() {
	currSkin--;
	var x = document.getElementsByClassName("skin");
	for(i = 0; i < x.length; i++) {
		var currStyle = x[i].getAttribute("style");
		
		var Find = ["hue-rotate", "-webkit-filter"];
		var New = [" hue-rotate(" + (currSkin * 20) + "deg);", " -webkit-filter: hue-rotate("+ (currSkin * 20) + "deg);"];
	
		x[i].setAttribute("style", replaceAttributes(currStyle, Find, New));
	}
}

function colorEyeLeft() {
	currEyeColor++;
	var eye = document.getElementById("eye");
	var currStyle = eye.getAttribute("style");
	
	var Find = ["hue-rotate", "-webkit-filter"];
	var New = [" hue-rotate(" + (currEyeColor * 20) + "deg);", " -webkit-filter: hue-rotate("+ (currEyeColor * 20) + "deg);"];
	
	eye.setAttribute("style", replaceAttributes(currStyle, Find, New));
}

function colorEyeRight() {
	currEyeColor--;
	var eye = document.getElementById("eye");
	var currStyle = eye.getAttribute("style");
	
	var Find = ["hue-rotate", "-webkit-filter"];
	var New = [" hue-rotate(" + (currEyeColor * 20) + "deg);", " -webkit-filter: hue-rotate("+ (currEyeColor * 20) + "deg);"];
	
	eye.setAttribute("style", replaceAttributes(currStyle, Find, New));
}

function replaceAttributes(currStyle, ogStrings, newStrings) {
	var chars = Object.assign([], currStyle);
	var isColon = false;
	for(i = 0; i < chars.length; i++) {
		if(chars[i] == ';') isColon = true;
	}
	
	if(isColon) {
		var tokens = currStyle.split(";");
		var newStyle = "";
		for(i = 0; i < tokens.length; i++) {
			var dontAdd = false;	
			
			if(tokens[i] == " ") dontAdd = true;
			
			for(t = 0; t < ogStrings.length; t++)  {
				if(tokens[i].substring(0, ogStrings[t].length + 1) == " " + ogStrings[t]) { dontAdd = true; }
			}
			
			if(!dontAdd && i != tokens.length - 1) newStyle += tokens[i] + ";";
			
		}
		
		for(i = 0; i < newStrings.length; i++) newStyle += newStrings[i];
		return newStyle;
	} else {
		var newStyle = "";
		for(i = 0; i < newStrings.length; i++) newStyle += newStrings[i];
		return newStyle;
	}
}

function setLoc(id, x, y) {
	var obj = document.getElementById(id);
	
	var test = obj.getAttribute("style");
	var Find = ["left", "top", "position"];
	var New = [ "left: " + (x) + "px;", "top: " + (y) + "px; ", "position: absolute; "];
	
	obj.setAttribute("style", replaceAttributes(test,Find,New));

}

function setCss() {	
	setLoc("head", 50 + x, 40 + y);
	setLoc("mouth", 63 + x, 85 + y);
	setLoc("nose", 63 + x, 65 + y);
	setLoc("brow", 60 + x, 49 + y);
	setLoc("eye", 60 + x, 60 + y);
	setLoc("hair", 56 + x, 21 + y);
	setLoc("facial_hair", 58 + x, 68 + y);
}  setCss();