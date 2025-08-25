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
});
