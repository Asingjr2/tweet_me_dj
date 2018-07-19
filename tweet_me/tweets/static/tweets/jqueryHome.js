// Base js functions to get list of messages from DB, submit form, and update results
$(document).ready(function(){

    // Function to get parameter for use with api_filter
    var query = getParameterByName('q_set')
    var tweetList = [];
    var startCharsCount = 140;
    var currentCharCount = 0;
    var nextMessageSetUrl; 
;
    // Running method to get initial set of tweets from database
    getTweets()

    $("#tweet-form").append("<span id='chars_count'>CHARACTERS LEFT" +  startCharsCount + " </span>")
    
    /*
        Identifying form with child input value of textarea with console log and display of changes
        Creating span that is updated when iser modifies form field
    */
    $("#tweet-form textarea").keyup(function(e){
        var tweetValue = $(this).val()
        currentCharCount = startCharsCount - tweetValue.length
        var spanCharsCount = $("#chars_count")
        spanCharsCount.text("CHARACTERS LEFT " + currentCharCount)

    })

    $("#tweet-form").submit(function(event){
        event.preventDefault()
        console.log("trying something")
        var _this = $(this)
        var createFormData = _this.serialize()

        $.ajax({
        url: "/api/tweets/create/",
        data: createFormData,
        method: "POST", 
        success: function(data){
            // Logic to clear specific field
            _this.find("input[type=text], textarea").val("")
            addTweet(data, true)
        },
        error: function(data) {
            console.log("error in creation of tweet", data)
        }
                });
    })

    // Updates html using message key information and addTweet().  
    function parseTweets(){
        if(tweetList == 0 ){
            $(".tweet-container").append(
                    "<div class='jumbotron'>"+
                    "<h1>" + "NO MATCHING TWEETS" + "</h1>"+
                    "</div>"
                );
        } else{
        $.each(tweetList, function(key, value){
            var tweetKey = key
            addTweet(value)
        })
        }
    }

    // Appends list of tweets to page.  Timesince, dateDisplay are serializer methods. Timesince also built in Django method.
    function addTweet(tweetValue, preprend){
        var dateDisplay = tweetValue.date_display
        var timesince = tweetValue.timesince
        var tweetContent = tweetValue.text
        var tweetUser = tweetValue.creator.username
        var formattedHtml = "<li>" + tweetUser + " | " + timesince + " | " + " | " + dateDisplay + " | " + tweetContent + "</li>"

        if(preprend == true ){ 
            $(".tweet-container").prepend(formattedHtml)
        } else {
            $(".tweet-container").append(formattedHtml)
        }
    
    }

    /*
        Ajax function getting tweets if they exist.  Creates std url using rest_framework pagination next and previus values.  If
        url is not sent with  method call, base page is loaded.
     */

    function getTweets(url) {
        console.log("getting messages")
        var fetchUrl;
        
        if(!url){
            fetchUrl = "/api/tweets/all_messages/"
        } else {
            fetchUrl = url
        }

        $.ajax({
            url: fetchUrl,
            data: { "q": query },
            method: "GET", 
            /* 
            Rest framework pagiantion names api value set as "results" so pull becomes data.results.  Restricts value per page
            Additional attributes showing in rest framework api (count, next, previous, results )
            */
            success: function(data){
                tweetList = data.results
                if(data.next){
                    nextMessageSetUrl = data.next
                } else {
                    $("#moreMessages").css("display", "none")
                }
                parseTweets()
            },
            error: function(data) {
                console.log("error in search", data)
            }
        });
    }

    /*
        Selector for pagination button to display more messages using var set in function based on rest framework.
        If next url is null, button disappears.
    */
    $("#moreMessages").click(function(event){
        event.preventDefault()
        if(nextMessageSetUrl){
            getTweets(nextMessageSetUrl)
        }
    })

})

// Pulls query parameter if any and returns full data set if no parameters found.
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

