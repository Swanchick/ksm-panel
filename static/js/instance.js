let saved_output = [];

$("#console-submit").click((event) => {
    const command_input = $("#console-input");
    let command = command_input.val();

    if (command === ""){
        return;
    }

    command_input.val("");

    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/call/server_send/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({command: command}),
        success: (response) => {
            setTimeout(updateState, 100);
        }
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

function createOutput(output_text){
    let output_panel = $("#outputs");
    let output = document.createElement("p");
    let output_node = document.createTextNode(output_text);
    output.appendChild(output_node)
    output_panel.append(output);
}

function compareArrays(array1, array2){
    if (array2.length === array1.length){
        if (array1[0] === array2[0]){
            return [];
        }
    }

    if (array1.length === 0){
        return array2;
    }

    let last_line = array1[array1.length - 1];
    let write = false;
    let out = []

    for (let i = 0; i < array2.length; i++){
        let current_line = array2[i];

        if (!write){
            if (current_line === last_line){
                write = true;
            }

            continue;
        }



        out.push(current_line);
    }

    return out
}

function createLastOutput(instance_id){
    $.ajax({
        url: "/instance/" + instance_id + "/call/get_output/",
        type: "GET",
        success: (response) => {
            let output = response["instance"]["output"];
            let edited_output = compareArrays(saved_output, output);

            if (edited_output.length === 0) {
                return
            }

            saved_output = output;

            for (let i = 0; i < edited_output.length; i++){
                let text = edited_output[i];

                createOutput(text);
            }
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

setInterval(updateState, 5000)