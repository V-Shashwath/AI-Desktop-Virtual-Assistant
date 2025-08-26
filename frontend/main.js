$(document).ready(function () {
    $('.text').textillate({
        loop: true,
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
        loop: true,
        in: {
            effect: 'fadeIn',
            sync: false 
        },
        out: {
            effect: 'fadeOut',
            sync: true 
        }
    });

    
});
