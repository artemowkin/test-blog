function success(position) {
    alert(position);
}


function error(err) {
    alert(err);
}


if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error)
} else {
    alert("ERROR ERROR ERROR")
}
