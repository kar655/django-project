function tab_clicked(tab, chosen_file) {
    $.ajax({
        type: "GET",
        url: "/frama/tabs",
        data: {
            "chosen_tab": tab,
            "chosen_file": chosen_file,
        },

        success: function (data) {
            $('#tabs-data').html(data)
        }
    })
}


function change_file(new_file) {
    console.log(new_file)

    $.ajax({
        type: "GET",
        url: "/frama/program-elements",
        data: {
            "chosen_file": new_file,
        },

        success: function (data) {
            console.log("Got " + data)
            $('#program-elements-data').html(data)
        }
    })
}
