$("#console-load").click((event) => {
    let output_panel = $("#outputs");
    let instance_id = $("#instance_id").val();

    let outputs = output_panel.children();

    for (let i = 0; i < outputs.length; i++) {
        let output = outputs[i];
        output.removeChild()
    }

    createOutput(instance_id);
})

$("#console-submit").click((event) => {
    let command = $("#console-input").val();

    if (command === ""){
        return;
    }

    console.log(command);
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

function createOutput(instance_id){
    $.ajax({
        url: "/instance/" + instance_id + "/call/get_output/",
        type: "GET",
        success: (response) => {
            let output_panel = $("#outputs");
            let outputs = response["instance"]["output"];

            for (let i = 0; i < outputs.length; i++){
                let output_text = outputs[i];

                console.log(output_text);
                let output = document.createElement("p");
                let node = document.createTextNode(output_text);
                output.appendChild(node);
                output_panel.append(output)
            }
        }
    })

}
