jQuery(document).ready(function($) {

    'use strict';

    $(function() {

        // Vars
        var modBtn  = $('#modBtn'),
            modal   = $('#modal'),
            close   = modal.find('.close-btn img'),
            modContent = modal.find('.modal-content');

        // Open modal when clicking on modBtn (anchor as button)
        modBtn.on('click', function(event) {
            event.preventDefault(); // Prevents anchor from following href
            modal.css('display', 'block');
            modContent.removeClass('modal-animated-out').addClass('modal-animated-in');
        });

        // Close modal when clicking close button or outside modal content
        $(document).on('click', function(e) {
            var target = $(e.target);
            if(target.is(modal) || target.is(close)) {
                modContent.removeClass('modal-animated-in').addClass('modal-animated-out').delay(300).queue(function(next) {
                    modal.css('display', 'none');
                    next();
                });
            }
        });

    });

    // On click event for all anchors with class scrollTo
    $('a.scrollTo').on('click', function() {

        // Data-scrollTo = section scrolling to name
        var scrollTo = $(this).attr('data-scrollTo');

        // Toggle active class on and off
        $("a.scrollTo").each(function() {
            if(scrollTo == $(this).attr('data-scrollTo')){
                $(this).addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });

        // Animate and scroll to the section
        $('body, html').animate({
            "scrollTop": $('#' + scrollTo).offset().top
        }, 1000);
        return false;
    });

    // Menu icon click event
    $(".menu-icon").click(function() {
        $(this).toggleClass("active");
        $(".overlay-menu").toggleClass("open");
    });

});
