$("#create-folder").click((event) => {
    event.preventDefault();

    let folder_name = prompt("Enter folder name");

    if (folder_name === null || folder_name === ""){
        return;
    }

    $.ajax({
        url: window.url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({method: "folder", name: folder_name}),
        success: (response) => {
            console.log(response);
            console.log("Success");

            location.reload();
        }
    });
});

$("#create-file").click((event) => {
    event.preventDefault();

    let file_name = prompt("Enter file name");

    if (file_name == null || file_name === ""){
        return;
    }

    $.ajax({
        url: window.url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({method: "file", name: file_name}),
        success: (response) => {
            console.log(response);
            console.log("Success");

            location.reload();
        }
    });
});

$(".delete-button").click((event) => {
    event.preventDefault();

    let target = event.target;

    let name = target.id;
    let type = target.href;

    $.ajax({
        url: window.url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({method: "remove", name: name, type: type}),
        success: (response) => {
            console.log(response);
            console.log("Success");

            location.reload();
        }
    });
});