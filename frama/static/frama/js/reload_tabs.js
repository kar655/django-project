function tab_clicked(tab, chosen_file) {
    $.ajax({
        type: "GET",
        url: "/frama/tabs",
        data: {
            "chosen_tab": tab,
            "chosen_file": chosen_file,
        },

        success: function(data) {
            $('#tabs-data').html(data)
        }
    })
}
