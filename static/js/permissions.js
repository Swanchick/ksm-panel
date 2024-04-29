$("#permission_check :checkbox").change((e) => {
    let target = e.target;
    let user_id = target.name;
    let permission_id = target.value;
    let permission_state = target.checked;

    let method;

    if (permission_state){
        method = "add/";
    } else {
        method = "remove/";
    }

    let instance_id = $("#instance_id").val();

    $.ajax({
        url: "/instance/" + instance_id + "/permissions/" + method + "/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            user_id: user_id,
            permission_id: permission_id,
            permission_state: permission_state,
        }),
        success: (response) => {
            console.log(response);
        }
    });
})