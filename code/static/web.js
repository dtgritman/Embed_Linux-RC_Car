window.onload = resetManualMode;
updateDetectionsTable();
setInterval(updateDetectionsTable, 15000);

var obj, x, y, prev_x, prev_y, cannonState;
cannonState = 0;
tankActive = 1;

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
    obj.style.background = '#ff0000';
}

function move(e) {
    // Always track and record the mouse's current position.
    if (e.pageX) {
        x = e.pageX;
        y = e.pageY;
    }
    
    // If the object specifically is selected, then move it to the X/Y coordinates that are always being tracked.
    if (obj) {
        var box, newX, newY, relX, relY;
    
        if (obj.id == "drive_ball")
            box = document.getElementById("drive_box");
        else if (obj.id == "cannon_ball")
            box = document.getElementById("cannon_box");
        
        newX = x - prev_x;
        if (newX < box.offsetLeft)
            newX = box.offsetLeft;
        else if (newX > box.offsetLeft + box.offsetWidth - obj.offsetWidth)
            newX = box.offsetLeft + box.offsetWidth - obj.offsetWidth;
        
        newY = y - prev_y;
        if (newY < box.offsetTop)
            newY = box.offsetTop;
        else if (newY > box.offsetTop + box.offsetHeight - obj.offsetHeight)
            newY = box.offsetTop + box.offsetHeight - obj.offsetHeight;
        
        if (tankActive) {
            if (obj.id == "drive_ball")
                updateCar();
            else if (obj.id == "cannon_ball")
                updateCannonPos();
        }
        obj.style.left = newX + "px";
        obj.style.top = newY + "px";
    }
}

function drop() {
    if (obj) {
        if (obj.id == "drive_ball") {
            // set ball back to the center of the box when released
            centerBall("drive_box", "drive_ball");
            updateCar();
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
    
    if (ballElem == "cannon_ball")
        updateCannonPos();
}

function resetManualMode() {
    // center drive ball
    centerBall("drive_box", "drive_ball");
    
    // center cannon ball
    centerBall("cannon_box", "cannon_ball");
}

function changeMode(mode) {
    var autoActive = 0;
    if (mode == "manual") {
        autoActive = 0
        document.getElementById("toggleCannonBtn").style.display = "block";
        document.getElementById("manual_controls").style.display = "block";
        document.getElementById("controlsBtn_reset").style.display = "block";
        document.getElementById("modeBtn_manual").style.display = "none";
        document.getElementById("modeBtn_auto").style.display = "block";
    }
    else if (mode == "auto") {
        autoActive = 1
        centerBall("cannon_box", "cannon_ball");
        document.getElementById("toggleCannonBtn").style.display = "none";
        document.getElementById("manual_controls").style.display = "none";
        document.getElementById("controlsBtn_reset").style.display = "none";
        document.getElementById("modeBtn_manual").style.display = "block";
        document.getElementById("modeBtn_auto").style.display = "none";
    }
    
    $.post('/autoactive', { "autoActive": autoActive });
}

function displayDetectionImage(datetime, image) {
    var htmlout = "Detection Date/Time: " + datetime + "<br>";
    htmlout += "<img src='/static/img/" + image + "' alt='Where the hell is that image'>";
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

function updateCannonPos() {
    var relX, relY;
    var ball = document.getElementById("cannon_ball");
    var box =  document.getElementById("cannon_box");
    var cannonPos = { "cannonAngle": 0, "cannonBaseAngle": 0, "cannonState": cannonState };
    
    relX = ball.offsetLeft - box.offsetLeft + (ball.offsetWidth / 2) - (box.offsetWidth / 2);
    cannonPos["cannonBaseAngle"] = Math.round(relX * (90 / (box.offsetWidth - ball.offsetWidth)));
    
    relY = -(ball.offsetTop - box.offsetTop + (ball.offsetHeight / 2) - (box.offsetHeight / 2));
    cannonPos["cannonAngle"] = Math.round(relY * (180 / (box.offsetHeight - ball.offsetHeight)));
    
    $.post('/cannoncontrol', cannonPos);
}

function updateCar() {
    var relX, relY;
    var ball = document.getElementById("drive_ball");
    var box =  document.getElementById("drive_box");
    var carPos = { "steering": 0, "drive": 0 };
    
    relX = ball.offsetLeft - box.offsetLeft + (ball.offsetWidth / 2) - (box.offsetWidth / 2);
    if (relX > 20 || relX < -20)
        carPos["steering"] = Math.round(relX * (200 / (box.offsetWidth - ball.offsetWidth)));
    
    relY = -(ball.offsetTop - box.offsetTop + (ball.offsetHeight / 2) - (box.offsetHeight / 2));
    if (relY > 20 || relY < -20)
        carPos["drive"] = Math.round(relY * (200 / (box.offsetHeight - ball.offsetHeight)));
    
    $.post('/carcontrol', carPos);
}

function toggleCannonState() {
    if (!cannonState)
        cannonState = 1;
    else
        cannonState = 0;
    
    updateCannonPos();
}

function toggleTankActive() {
    if (!tankActive)
        tankActive = 1;
    else
        tankActive = 0;
    
    $.post('/tankactive', { "tankActive": tankActive });
}

// Make a specific element movable
document.getElementById('drive_ball').onmousedown = drag;
document.getElementById('cannon_ball').onmousedown = drag;
document.onmousemove = move;
document.onmouseup = drop;
