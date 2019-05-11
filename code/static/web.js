window.onload = resetManualMode;
updateDetectionsTable();
setInterval(updateDetectionsTable, 15000);

var obj, x, y, prev_x, prev_y;

function drag(e) {
    if (e.target.id != "drive_ball" && e.target.id != "cannon_ball")
        return;
    // get object clicked on
    obj = e.target;
    
    // Set current X coordinate minus distance left from offsetParent node.
    prev_x = x - obj.offsetLeft;
    // Set current Y coordinate minus distance top from offsetParent node.
    prev_y = y - obj.offsetTop;
    // Change the object's color so it looks like it's usable/moveable.
    obj.style.background = '#00ff00';
}

function move(e) {
    // Always track and record the mouse's current position.
    if (e.pageX) {
        x = e.pageX;
        y = e.pageY;
    }
    
    // If the object specifically is selected, then move it to the X/Y coordinates that are always being tracked.
    if (obj) {
        var box, newX, newY;
    
        if (obj.id == "drive_ball") {
            box = document.getElementById("drive_box");
        }
        else if (obj.id == "cannon_ball") {
            box = document.getElementById("cannon_box");
        }
        
        newX = x - prev_x;
        if (newX < box.offsetLeft) {
            newX = box.offsetLeft;
        }
        else if (newX > box.offsetLeft + box.offsetWidth - obj.offsetWidth) {
            newX = box.offsetLeft + box.offsetWidth - obj.offsetWidth;
        }
        
        newY = y - prev_y;
        if (newY < box.offsetTop) {
            newY = box.offsetTop;
        }
        else if (newY > box.offsetTop + box.offsetHeight - obj.offsetHeight) {
            newY = box.offsetTop + box.offsetHeight - obj.offsetHeight;
        }
        
        obj.style.left = newX + "px";
        obj.style.top = newY + "px";
    }
}

function drop() {
    if (obj) {
        if (obj.id == "drive_ball") {
            // set ball back to the center of the box
            centerBall("drive_box", "drive_ball");
        }
        // Revert to the default css style.
        obj.style.background = "";
        // Remove the attached event from the element so it doesn't keep following your mouse. :)
        obj = false;
    }
}

function centerBall(boxElem, ballElem) {
    box = document.getElementById(boxElem);
    ball = document.getElementById(ballElem);
    
    ball.style.left = (box.offsetLeft + box.offsetWidth / 2 - ball.offsetWidth / 2) + "px";
    ball.style.top = (box.offsetTop + box.offsetHeight / 2 - ball.offsetWidth / 2) + "px";
}

function resetManualMode() {
    // center drive ball
    centerBall("drive_box", "drive_ball");
    
    // center cannon ball
    centerBall("cannon_box", "cannon_ball");
}

function changeMode(mode) {
    if (mode == "manual") {
        document.getElementById("manual_controls").style.display = "block";
        document.getElementById("controlsBtn_reset").style.display = "block";
        document.getElementById("modeBtn_manual").style.display = "none";
        document.getElementById("modeBtn_auto").style.display = "block";
    }
    else if (mode == "auto") {
        centerBall("cannon_box", "cannon_ball");
        document.getElementById("manual_controls").style.display = "none";
        document.getElementById("controlsBtn_reset").style.display = "none";
        document.getElementById("modeBtn_manual").style.display = "block";
        document.getElementById("modeBtn_auto").style.display = "none";
    }
}

function displayDetectionImage(datetime, image) {
    var htmlout = "Detection Date/Time: " + datetime + "<br>";
    htmlout += "<img src='/img/" + image + "' alt='Where the hell is that image'>";
    $("#detections_display").html(htmlout);
}

function updateDetectionsTable() {
    $.getJSON('/detectionlogs', function(data) {
        console.log(data);
        
        var tableData = "<tr><th width='150px'>Date/Time</th><th width='100px'>Type</th><th width='80px'>Image</th></tr>";
        for (var i = 0; i < data.length; i++) {
            tableData += "<tr><td>" + data[i].Date + "</td><td>" + data[i].Type + "</td>";
            tableData += "<td><button onclick=\"displayDetectionImage('" + data[i].Date + "', '" + data[i].Image + "')\">View</button></td>";
            tableData += "</tr>";
        }
        $("#detections_info").html(tableData);
    });
}

// Make a specific element movable
document.getElementById('drive_ball').onmousedown = drag;
document.getElementById('cannon_ball').onmousedown = drag;
document.onmousemove = move;
document.onmouseup = drop;
