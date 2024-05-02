$(document).on("click", "#save", (e) => {
    let path = $("#path").val();
    let file_data = $("#file").val()

    console.log(window.location.pathname)

    $.ajax({
        url: window.location.pathname + "?path=" + path,
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"file_data": file_data}),
        success: (response) => {
            console.log(response);
        }
    });
});
