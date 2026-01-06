$(document).ready(function () {

    // Display Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message .texts li").text(message);
        $('.siri-message').textillate('start');
    }

    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }



    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(receiverText)
    function receiverText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }

    // Hide Loader and display Face Auth animation
    eel.expose(hideLoader)
    function hideLoader() {

        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);

    }
    // Hide Face auth and display Face Auth success animation
    eel.expose(hideFaceAuth)
    function hideFaceAuth() {

        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);

    }
    // Hide success and display 
    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {

        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);

    }


    // Hide Start Page and display blob
    eel.expose(hideStart)
    function hideStart() {

        $("#Start").attr("hidden", true);

        setTimeout(function () {
            $("#oval").addClass("animate__animated animate__zoomIn");

        }, 1000)
        setTimeout(function () {
            $("#oval").attr("hidden", false);
        }, 1000)
    }

    // Show passcode authentication screen
    eel.expose(showPasscodeAuth)
    function showPasscodeAuth() {
        $("#AuthChoice").attr("hidden", true);
        $("#PasscodeAuth").attr("hidden", false);
        // Focus first input
        $(".passcode-digit").first().focus();
    }

    // Show face authentication screen
    eel.expose(showFaceAuth)
    function showFaceAuth() {
        $("#AuthChoice").attr("hidden", true);
        $("#Start").attr("hidden", false);
        $("#Loader").attr("hidden", false);
    }

    // Hide passcode screen
    eel.expose(hidePasscodeAuth)
    function hidePasscodeAuth() {
        $("#PasscodeAuth").attr("hidden", true);
    }

    // Show passcode success animation
    eel.expose(showPasscodeSuccess)
    function showPasscodeSuccess() {
        $("#Start").attr("hidden", false);
        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);
    }

    // Hide passcode success and proceed
    eel.expose(hidePasscodeSuccess)
    function hidePasscodeSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);
    }

    // Show passcode error
    eel.expose(showPasscodeError)
    function showPasscodeError() {
        $("#PasscodeError").show();
        // Clear all inputs
        $(".passcode-digit").val("").removeClass("filled");
        $(".passcode-digit").first().focus();
        // Hide error after 3 seconds
        setTimeout(function() {
            $("#PasscodeError").hide();
        }, 3000);
    }

    // Delayed authentication success (called after face or passcode success animation)
    eel.expose(delayedAuthSuccess)
    function delayedAuthSuccess() {
        setTimeout(function() {
            // Hide success animation and show HelloGreet
            $("#FaceAuthSuccess").attr("hidden", true);
            $("#HelloGreet").attr("hidden", false);
            // Then complete authentication
            eel.completeAuthentication()();
        }, 1500);
    }
    
});