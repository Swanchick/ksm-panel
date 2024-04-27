let last_output = "";

$("#console-submit").click((event) => {
    let command = $("#console-input").val();

    if (command === ""){
        return;
    }

    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/call/server_send/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({command: command}),
    })
})

$("#start-server").click((event) => {
    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/call/start_server/",
        type: "GET",
        success: () => {
            location.reload();
        }
    })
})

$("#stop-server").click((event) => {
    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/call/stop_server/",
        type: "GET",
        success: (response) => {
            location.reload();
        }
    })
})

function createLastOutput(instance_id){
    $.ajax({
        url: "/instance/" + instance_id + "/call/get_last_output/",
        type: "GET",
        success: (response) => {
            let output_text = response["instance"]["output"];
            if (last_output === output_text){
                return
            }
            last_output = output_text;

            let output_panel = $("#outputs");
            let output = document.createElement("p");
            let output_node = document.createTextNode(output_text);
            output.appendChild(output_node)
            output_panel.append(output);
        }
    })
}

function updateState(){
    let instance_id = $("#instance_id").val();
    let instance_state = $("#instance_state").val();

    if (instance_state === "1") {
        return
    }

    createLastOutput(instance_id);
}

setInterval(updateState, 1000)