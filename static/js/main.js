$(document).ready(function() {
    console.log('jQuery version:', $.fn.jquery);
    const date = new Date();
    document.querySelector('.year').innerHTML = date.getFullYear();

    console.log('Document ready, setting up alert fadeout');
    setTimeout(() => {
        console.log('Timeout fired, checking for .message');
        console.log('Number of .message elements:', $('.message').length);
        if ($('.message').length) {
            console.log('Found ' + $('.message').length + ' .message elements, fading out');
            // Test: change background color to red before fadeOut
            $('.message').css('background-color', 'red');
            // Try fadeOut with callback
            $('.message').fadeOut("slow", function() {
                console.log('FadeOut complete');
            });
            // Fallback: if after 2 seconds still visible, force hide
            setTimeout(() => {
                if ($('.message').is(':visible')) {
                    console.log('Fallback: forcing hide');
                    $('.message').hide();
                }
            }, 2000);
        } else {
            console.log('No .message elements found');
        }
    },5000);
});
