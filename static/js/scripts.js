$(document).ready(function(){
    $.get("/getBoard", function(data){
        refreshBoard();
      });
});

function refreshBoard() {
    $.get("/getBoard", function(data){
        console.log(data);
        for (var i = 0; i < 81; i++) {
            $("#" + i).text(data["board"][i][0]);
            $("#" +i).css("color", data["board"][i][1]); 
        }
      });
}

function addVal() {
    if ($("#" + event.target.id).text() != "" && $('#' + event.target.id).css("color") == "rgb(0, 0, 0)" ) {
        return;
    }

    $("#nums").html("<table> \
    <tr> \
        <td onclick=\"submitCell(" + event.target.id + ")\">1</td> \
        <td onclick=\"submitCell(" + event.target.id + ")\">2</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">3</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">4</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">5</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">6</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">7</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">8</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">9</td>\
        <td onclick=\"submitCell(" + event.target.id + ")\">X</td>\
    </tr>\
    </table>" );

}

function submitCell(cell) {

    if (event.target.innerText == "X") {
        $.post('/remove', 
            {'cell' : cell},
            function(){
                refreshBoard();
                $("#nums").html("");
            }
        );
        return;
    }

    console.log(event.target.innerText);
    $.post('/submit', 
        {'cell' : cell, 'value' : event.target.innerText},
        function(data){
            console.log();
            refreshBoard();
            $("#nums").html("");
        }
    );
}

function save() {
    $.post('/save', function(){alert("Saved!")});
}
