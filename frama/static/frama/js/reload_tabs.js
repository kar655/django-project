$("#random").click( function (e) {
    e.preventDefault()
    console.log("In CLick")

    $.ajax({
        type: "GET",
        // url: "/frama/random",
        // url: "/frama/random",
        url: "/frama/tabs",
        data: {
            "is_chosen_file": true,
            "chosen_tab": "result",
            "chosen_file": "randomFile",
        },

        success: function(data) {
            console.log("Success got " + data)
            // $('#random').text(data)
            // $('#here').text(data)
            $('#here').html(data)
        }
    })
})

$('#message').click(function(){
        console.log("Hello")
});

// $('#message').click(function(){
//         console.log("Hello")
//     var catid;
//     catid = $(this).attr("data-catid");
//     $.ajax(
//     {
//         type:"GET",
//         url: "/likepost",
//         data:{
//                  post_id: catid
//         },
//         success: function( data )
//         {
//             $( '#like'+ catid ).remove();
//             $( '#message' ).text(data);
//         }
//      })
// );

// $('#tab-provers').click( function (e) {
//     e.preventDefault()
//     // console.log("Pressed")
//
//         $.ajax({
//         type: "GET",
//         // url: "/frama/random",
//         // url: "/frama/random",
//         url: "/frama/tabs",
//         data: {
//             "is_chosen_file": true,
//             "chosen_tab": "result",
//             "chosen_file": "randomFile",
//         },
//
//         success: function(data) {
//             console.log("Success got " + data)
//             // $('#random').text(data)
//             // $('#here').text(data)
//             $('#here').html(data)
//         }
//     })
// })

function tab_clicked(tab, chosen_file) {
    console.log("In " + tab + " clicked")
    console.log(chosen_file)

    $.ajax({
        type: "GET",
        url: "/frama/tabs",
        data: {
            "chosen_tab": tab,
            "chosen_file": chosen_file,
        },

        success: function(data) {
            console.log("Success got " + data)
            $('#tabs-data').html(data)
        }
    })
}
