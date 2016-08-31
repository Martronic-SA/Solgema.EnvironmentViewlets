var carousel_interval;

function rotateBanners(index, value) {
    var carousel_rotate = function() {
        features = $(value).children('.carousel-banner');
        if (features.length < 2) return;

        var visible = $(value).children('.carousel-banner:visible');
        $(value).css('height', visible.height());
        var next = visible.next('.carousel-banner');
        if (next.length==0) {
            next = $(value).find('#carousel-banner-0');
        }
        next.css('position', 'absolute').css('z-index','9').show();
        visible.css('position', 'absolute').css('z-index','10').fadeOut(1200);
        next.css('position', 'absolute');
        $(value).css('height', next.height());
    };
    $(function() {
        carousel_interval = setInterval(carousel_rotate, 8000);
        setTimeout(function() {
            $('#inner-portal-bandeau .link-https, #inner-portal-bandeau .link-external').each( function() {
                $(this).replaceWith($(this).html());
            })
        }, 1000);
        $(value).hover(
            function() { clearInterval(carousel_interval); },
            function() { carousel_interval = setInterval(carousel_rotate, 8000)}
        );
    });
}

function activateCarousel() {
    if ( $('.carousel-banner').length < 2 ) return;
    jQuery.each($('div.bannersContainer'), function(index, value) {
       rotateBanners(index, value);
        }
    );
};

$(activateCarousel);
