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
	
	function createButton(src, color, backcolor, title, text) {
		var canvas = document.createElement("canvas");
		var ctx = canvas.getContext("2d");
		canvas.width = screen.width - 50;
		canvas.height = 64;
		
		ctx.imageSmoothingEnabled = false;
		ctx.mozImageSmoothingEnabled = false;
		ctx.imageSmoothingEnabled = false;
		
		this.src = src;
		this.color = color;
		this.backcolor = backcolor;
		this.title = title;
		this.text = text;
		
		ctx.fillStyle = this.color;
		ctx.fillRect(0, 0, canvas.width, canvas.height);
		
		ctx.font="16px 'Press Start 2P'";
		ctx.fillStyle = backcolor;
		
		var text = title + ": " + text;
		
		var tooBig = false;
		if(ctx.measureText(title + ": " + text).width > canvas.width) tooBig = true;
		
		if(tooBig) {
			while(tooBig) {
				text = text.slice(0, -1);
				if(ctx.measureText(title + ": " + text).width > canvas.width) tooBig = true;
				else tooBig = false;
			}
			
			text = text.slice(0, -3);
			text += "...";
		}
		
		ctx.fillText(text, canvas.height + 5, 40);
		
		var badgePic = new Image();
		badgePic.onload = function () {
			ctx.drawImage(badgePic, 0, 0, canvas.height, canvas.height);
		}
		badgePic.src = "Default_Badge.png";
		document.getElementById("badges").appendChild(canvas);
	}