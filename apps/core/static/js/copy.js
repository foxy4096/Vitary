function copyLink(id) {
    var copyText = "https://vitary.pythonanywhere.com/vit/" + id + "/";
    navigator.clipboard.writeText(copyText);
    document.getElementById("copyLink_" + id).innerHTML = "Copied!";
    setTimeout(function () {
        document.getElementById("copyLink" + id).innerHTML = "Copy";
    }, 2000);
}