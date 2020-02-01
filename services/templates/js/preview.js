function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result);
            document.getElementById("preview").style.display = 'block';
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$("#image").change(function () {
    readURL(this);
});