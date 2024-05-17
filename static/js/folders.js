// $(document).on("click", "a.file", (e) => {
//     e.preventDefault();
//     let search_params = new URLSearchParams(window.location.search);
//     if (!search_params.has("path"))
//         return;
//
//     let instance_id = $("#instance_id").val();
//     let filename = e.target.text;
//
//     let url = "/instance/" + instance_id + "/file/" + filename + "/?path=/" + search_params.get("path");
//     console.log(url)
//
//     window.location.href = url;
//
//
// });
//
// $(document).on("click", "a.folder", (e) => {
//     e.preventDefault();
//
//     let instance_id = $("#instance_id").val();
//
//     let search_params = new URLSearchParams(window.location.search);
//     if (!search_params.has("path"))
//         return;
//
//     let path = search_params.get("path");
//     let folder_name = e.target.text;
//     search_params.set("path", path + folder_name + "/");
//
//     window.location.href = window.location.origin + window.location.pathname + '?' + search_params.toString();
// });