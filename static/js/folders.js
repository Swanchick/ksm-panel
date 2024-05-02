let current_folder = [];

$(document).on("click", "a.file", (e) => {
    let instance_id = $("#instance_id").val();

    e.preventDefault();
    let filename = e.target.text;



});

$(document).on("click", "a.folder", (e) => {
    let instance_id = $("#instance_id").val();

    e.preventDefault();
    let filename = e.target.text;

    $.ajax({
        url: "/instance/" + instance_id + "/folders",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({"folder": filename, current_folder: current_folder}),
        success: (response) => {
            current_folder = response["folder"];
            let folders_files = response["data"]["folders"];
            $("div.file_button").remove();

            for (let folder of folders_files) {
                let button = $("<div>", {
                    "class": "file_button",
                });

                let link_button;

                if (folder["file_type"] === 1){
                    link_button = $("<a>", {
                        "class": "folder",
                        "href": "#",
                        text: folder["file_name"]
                    });
                } else {
                    link_button = $("<a>", {
                        "class": "file",
                        "href": "#",
                        text: folder["file_name"]
                    });
                }

                button.append(link_button);

                $(".folders").append(button);
            }
        }
    });
});