	var fullOpen = false;
	
	function removeMenu() {
		fullOpen = false;
		var element = document.getElementsByTagName("html");
		var div = document.getElementById("full");
		element[0].removeChild(div);
	}

	function openFull(src, color, backcolor, title, text) {
		fullOpen = true;
		var element = document.getElementsByTagName("html");
		var menuBacking = document.createElement("div");
		menuBacking.id = "full";
		var p = document.createElement("p");
		var linebreak = document.createElement("br");
		var titleText = document.createTextNode(title + ": ");
		var textText = document.createTextNode(text);
		
		var x = document.createElement("button");
		x.appendChild(document.createTextNode("Ok!"));
		x.onclick = function() { removeMenu(); };
		
		p.appendChild(titleText);
		p.appendChild(linebreak);
		p.appendChild(textText);
		
		style = "";
		style +=  "border: 3px solid " + backcolor + ";"
		style += "position: fixed;"
		style += "left: 50%;"
		style += "top: 50%;"
		style += "width: 30em;"
		style += "height:18em;"
		style += "background-color:	" + color + ";"
		style += "margin-top: -9em;"
		style += "margin-left: -15em;" 
		style += "text-align: center;"
		style += "word-wrap:break-word;"
		menuBacking.style = style;
		
		menuBacking.appendChild(p);
		menuBacking.appendChild(x);
		element[0].appendChild(menuBacking);
	}

	function getTextWidth(text, font) {
		// re-use canvas object for better performance
		var canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
		var context = canvas.getContext("2d");
		context.font = font;
		var metrics = context.measureText(text);
		return metrics.width;
	}

	var buttonNum = 1;

	function createButton(src, color, backcolor, title, text) {
		
		this.backcolor = backcolor;
		this.color = color;
		this.src = src;
		this.text = text;
		
	    var styleNode = document.createElement('style');
	    styleNode.type = "text/css";
	    // browser detection (based on prototype.js)
	    if(!!(window.attachEvent && !window.opera)) {
			styleNode.styleSheet.cssText = "#achievement" + buttonNum + ":hover { color: " + backcolor + "; }";
	    } else {
			var styleText = document.createTextNode("#achievement" + buttonNum + ":hover { color: " + backcolor + "; }");
			styleNode.appendChild(styleText);
	    }

		var full = document.createElement("div");
		full.id = "achievement" + buttonNum;
		full.onclick = function() { if(fullOpen == false) openFull(src, color, backcolor, title, text); };
		
		var img = document.createElement("img");
		var sqr = document.createElement("div");
		var txt = document.createElement("p");
		txt.className = "badgeInfo"
		var bold = document.createElement("i");
		
		sqr.className = "sqr";
		
		var ttlText = document.createTextNode(title);
		bold.appendChild(ttlText);
		
		var txtText = document.createTextNode(":  " + text);
		txt.appendChild(bold);
		txt.appendChild(txtText);
		
		img.src = src;
		var element = document.getElementById("badges");
		
		var padding = 90;
		
		var style = "";
		style += "image-rendering: pixelated;"
		style += "transform: scale(5, 5);"
		style += "-ms-transform: scale(5, 5);"
		style += "-webkit-transform: scale(5, 5);"
		style += "position: absolute;"
		style += "left: 38px;"
		style += "top: " + (32 + (buttonNum * padding)) + "px;"
		img.style = style;
		
		style = "";
		style += "position: absolute;"
		style += "left: 1px;"
		style += "top: " + ((buttonNum * padding) - 5) + "px;"
		style += "width: calc(100vw - 5px);"
		style += "height:80px;"
		style += "background-color:	" + color + ";"
		sqr.style = style;
		
		style = "";
		style += "position: absolute; left: " + (100) + "px; top: " + ((buttonNum * padding) + 16) + "px;"
		txt.style = style;
		
		
		buttonNum++;
		full.appendChild(sqr);
		full.appendChild(txt);
		full.appendChild(img);
		element.appendChild(styleNode);
		element.appendChild(full);
	}
	
	createButton('Default_Badge.png', '#654321','gray', "Log In", "You created a digital skypy account!");
	createButton('Default_Badge.png', '#696969','orange', "Log In V2", "This Is just a test because css is touchy");
	createButton('Default_Badge.png', '#00137F', 'green', 'Long Award', 'This is a long description because you never know you could get some weird crazy specific award lol');