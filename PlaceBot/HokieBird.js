// ==UserScript==
// @name         PlacePaintBot HOKIE Bird
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  Domination of Place!
// @author       mbarkhau, modified by Anthony Wagner for VT
// @match        https://www.reddit.com/place?webview=true
// @grant        none
// @updateURL    https://github.com/wagnera/Projects/blob/master/PlaceBot/HokieBird.js
// ==/UserScript==

(function() {
    'use strict';

    var imageX = 33;
    var imageY = 884;
    var image = [
		"BBBBBBBBBBBBBBBBBBBBBBBBBBBB",
		"BWWWWWWWWWWWWWWWWWWWWWWWWWWB",
		"BWWWWWWWWWWWWMMMMWWWWWWWWWWB",
		"BWWWWWWWWWMMMMMMMMMWWWWWWWWB",
		"BWWWWWWWMMMMMMMMMMMMMWWWWWWB",
		"BWWWWWWMMMMMMMMMMMMMMMMWWWWB",
		"BWWWWWMMMMMMMMMMMMMMMMMMWWWB",
		"BWWWWWMMMMMMMMMMMMMMMMMMWWWB",
		"BWWWWMMMMMWWMMMMMMMMMMMMMWWB",
		"BWWWWMMMMMWWWWMMMMMMMMMMMWWB",
		"BWWWWMMMMMWMMMWMMMMMMMMMMMWB",
		"BWWWWMMMMMMMMMWWMMMMMMMMMWWB",
		"BWWWMMMMMMMMMMWMMMMMMMWMMWWB",
		"BWWMOOOOOMMMMMMMMMMMMMWMWWWB",
		"BWMOOMMMOOMMMMMMOOOOMWWMWWWB",
		"BWWMOOOMOOOOOMMMMOOMOMMMWWWB",
		"BWWWMOOOOMOOOOOOOOMOMOOOWWWB",
		"BWWWMMMOOOOOOOMMOOOOOOMOMWWB",
		"BWWWMMMMMMOOOOOOOMOOOOOOWWWB",
		"BWWWMMMOMMMMMMMMMMMOOOOWWWWB",
		"BWWWMMMMOOMMMMMMMMMMMOOWWWWB",
		"BWWWMMMMMOOOOMMMMMMMMOOWWWWB",
		"BWWWMMMMMMMOOOOOOOMMOOMWWWWB",
		"BWWWMMMMMMMMMMMMOOOOWMMWWWWB",
		"BWWWMMMMMMMMMMMMMMMOOOMWWWWB",
		"BWWWWMMMMMMMMMMMMMMMMOOMWWWB",
		"BWWWWWWWWWWMMMMMMMMMMMOOWWWB",
		"BWWWWWWWWWWWWWWWWWWMMMMOWWWB",
		"BWWWWWWWWWWWWWWWWWWWWWMMMWWB",
		"BWWWWWWWWWWWWWWWWWWWWWWWMWWB",
		"WWWWWWWWWWWWWWWWWWWWWWWWWWWB",
		"BBBBBBBBBBBBBBBBBBBBBBBBBBBB"
		
    ];

    var colors = {
        "W": 1,
		"B": 3,
	    "M": 5,
        "O": 6,
    };

    var image_data = [];
    for (var relY = 0; relY < image.length; relY++) {
        var row = image[relY];
        for (var relX = 0; relX < row.length; relX++) {
            var color = colors[row[relX]] || -1;
            if (color < 0) {
                continue;
            }
            var absX = imageX + relX;
            var absY = imageY + relY;
            image_data.push(absX);
            image_data.push(absY);
            image_data.push(color);
        }
    }

    var default_panX = 189;
    var default_panY = -380;

    var p = r.place;
    p.panX = default_panX;
    p.panY = default_panY;
    
    p.setCameraLocation(imageX, imageY);
    
    r.placeModule("placePaintBot", function(loader) {
        var c = loader("canvasse");

        setInterval(function() {
            var ms = p.getCooldownTimeRemaining();
            if (ms > 200) {
                if (ms > 1000 && ms < 3000) {
                    window.location.reload();
                }
                return;
            }
            for (var i = 0; i < image_data.length; i += 3) {
                var j = Math.floor((Math.random() * image_data.length) / 3) * 3;
                var x = image_data[j + 0];
                var y = image_data[j + 1];
                var color = image_data[j + 2];
                var currentColor = p.state[c.getIndexFromCoords(x, y)];

                if (currentColor != color) {
                    console.log("set color for", x, y, "old", currentColor, "new", color);
                    p.setColor(color);
                    p.drawTile(x, y);
                    return;
                }
            }
            console.log("noop");
        }, 1500);
    });
})();
