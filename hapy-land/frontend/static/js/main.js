// j-QUERYYYY




// get all querystrings, from https://stackoverflow.com/a/7732379/10382407
location.queryString = {};
location.search.substr(1).split("&").forEach(function (pair) {
    if (pair === "") return;
    var parts = pair.split("=");
    location.queryString[parts[0]] = parts[1] &&
        decodeURIComponent(parts[1].replace(/\+/g, " "));
});

$( window ).on("load", function() {

    // show toasts
    if(location.queryString.hasOwnProperty("show_toast")) {
        console.log($(".toast"))
        $(".toast").toast("show");
        $(".toast .toast-body").text(location.queryString.msg);
    }
});

function close_toast() {
    $(".toast").toast("hide");
}