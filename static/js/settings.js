$(".delete").click((event) => {
    event.preventDefault();

    let target = event.target;
    let argument_id = target.id;

    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/call/delete_argument/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"argument_id": argument_id}),
        success: (response) => {
            console.log(response);

            location.reload();
        }
    });
});

$("#send-argument").click((event) => {
    event.preventDefault();

    let argument = $("#input-argument").val();
    if (argument === ""){
        return;
    }

    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/call/add_argument/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"argument": argument}),
        success: (response) => {
            console.log(response);

            location.reload();
        }
    });
});

$(".unpin-port").click((event) => {
    event.preventDefault();

    let port = event.target;

    $.ajax({
        url: "/settings/call/unpin_port/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"port": port}),
        success: (response) => {
            console.log(response);

            location.reload();
        }
    });

});

$(".delete-port").click((event) => {
    event.preventDefault();

    let target = event.target;
    let port = target.id;

    $.ajax({
        url: "/settings/call/delete_port/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"port": port}),
        success: (response) => {
            console.log(response);

            location.reload();
        }
    });
});
$("#send-port").click((event) => {
    event.preventDefault();

    let port = $("#input-port").val();
    if (port === ""){
        return;
    }

    $.ajax({
        url: "/settings/call/add_port/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"port": port}),
        success: (response) => {
            console.log(response);

            location.reload();
        }
    });
});

$("#change-port").click((event) => {
    event.preventDefault();

    let port = $("#instance-ports").val();
    if (port === null){
        return;
    }

    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/call/change_port/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"port": port}),
        success: (response) => {
            console.log(response);

            location.reload();
        }
    });

})
