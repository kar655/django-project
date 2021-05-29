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
    $('#chosen_file_name').text(new_file)
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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function save_file() {
    const file_name = $('#chosen_file_name').text()
    const file_content = editor.getValue()

    $.ajax({
        type: "POST",
        url: "/frama/file-content",
        data: {
            "chosen_file": file_name,
            "file_content": file_content,
            "csrfmiddlewaretoken": getCookie('csrftoken'),
        },
    })
}
