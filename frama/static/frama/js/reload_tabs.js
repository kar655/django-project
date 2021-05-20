function tab_clicked(tab) {
    $.ajax({
        type: "GET",
        url: "/frama/tabs",
        data: {
            "chosen_tab": tab,
            "chosen_file": tab === "result" ? $('#chosen_file_path').text() : "",
        },

        success: function (data) {
            $('#tabs-data').html(data)
        }
    })
}

function navigation_clicked(nav) {
    $.ajax({
        type: "GET",
        url: "/frama/" + nav,

        success: function (data) {
            $('#page-data').html(data)
        }
    })
}

function change_file(new_file, new_file_path) {
    $('#chosen_file_path').text(new_file_path)
    tab_clicked('result', new_file_path)

    $.ajax({
        type: "GET",
        url: "/frama/file-content",
        data: {
            "chosen_file": new_file,
        },

        success: function (data) {
            $('#file-content-data').html(data)
        }
    })

    $.ajax({
        type: "GET",
        url: "/frama/program-elements",
        data: {
            "chosen_file": new_file,
        },

        success: function (data) {
            $('#program-elements-data').html(data)
        }
    })

    $('[id^=choose-file]').each(function () {
        $(this).css("color", "blue")
    })

    $('#choose-file-' + new_file).css("color", "red")
}
