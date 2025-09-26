$(document).ready(function () {
    $('.text').textillate({
        // loop: true,
        loop: false,
        in: {
            effect: 'fadeIn',
            sync: false 
        },
        out: {
            effect: 'fadeOut',
            sync: true 
        }
    });

    //siri-config
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style:"ios9",
        amplitude: 1,
        speed: "0.30",
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        // loop: true,
        loop: false,
        in: {
            effect: 'fadeIn',
            sync: false 
        },
        out: {
            effect: 'fadeOut',
            sync: true 
        }
    });

    // Mic Button Click Event
    $('#MicBtn').click(function () {
        eel.playAssistantSound();
        $("#oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();
    });

    //shortcut key
    function doc_keyUp(e) {
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);
});
