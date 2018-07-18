$(document).ready(function(){
    console.log("working");

    $.ajax({
        url: "/api/tweets/all_messages",
        method: "GET", 
        success: function(data){
            console.log(data)}, 
        error: function(data) {
            console.log("error")
                console.log(data)
        }
        });
})