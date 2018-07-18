// Base js functions to get list of messages from DB, submit form, and update results
$(document).ready(function(){

    // Function to get parameter for use with api_filter
    var query = getParameterByName('q_set')
    var tweetList = [];
    var startCharsCount = 140;
    var currentCharCount = 0;
;
    // Running method to get initial set of tweets from database
    getTweets()

    $("#tweet-form").append("<span id='chars_count'>CHARACTERS LEFT" +  startCharsCount + " </span>")
    
    // Child input value of textarea with console log and display of changes
    // Creating span that is updated when iser modifies form field
    $("#tweet-form textarea").keyup(function(e){
        var tweetValue = $(this).val()
        currentCharCount = startCharsCount - tweetValue.length
        var spanCharsCount = $("#chars_count")
        spanCharsCount.text("CHARACTERS LEFT " + currentCharCount)

        // if(currentCharCount <= 0 ) {
        //     spanCharsCount.text("Over 140 Limit.  Cannot submit message")
        // }
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
            addTweet(data)
            // getTweets()
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
    function addTweet(tweetValue){
        var dateDisplay = tweetValue.date_display
        var timesince = tweetValue.timesince
        var tweetContent = tweetValue.text
        var tweetUser = tweetValue.creator.username
        $(".tweet-container").append(
            "<li>" + tweetUser + " | " + timesince + " | " + " | " + dateDisplay + " | " + tweetContent + "</li>"
        )
    }

    // Ajax function checking for length of search result and displaying tweet or "no results message"...then calling function
    function getTweets() {
        console.log("getting messages")
        $.ajax({
            url: "/api/tweets/all_messages/",
            data: { "q": query },
            method: "GET", 
            success: function(data){
                tweetList = data
                parseTweets(data)
            },
            error: function(data) {
                console.log("error in search", data)
            }
        });
    }

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

