/**
 * Author Nat Lee (c) 2018
 * Free to use
 * https://github.com/lee-ratinan/showTimer
 */
(function ($) {
    $.fn.showTimer = function(options) {
        var settings = $.extend({
                                    returnType: "text",
                                    timeZone: "+00:00",
                                    wrapper_id: "",
                                    timesup_wrapper_id: "",
                                    noshow_wrapper_id: "",
                                    local_s_days: "d",
                                    local_s_hrs: "h",
                                    local_s_min: "m",
                                    local_s_sec: "s",
                                    local_l_days: "DAYS",
                                    local_l_hrs: "HRS",
                                    local_l_min: "MIN",
                                    local_l_sec: "SEC",
                                }, options);
        return this.each(function() {
            // timezone
            var timezone = settings.timeZone;
            if (undefined !== $(this).attr('data-timezone')) { timezone = $(this).attr('data-timezone'); }
            // start and end time
            var start = $(this).attr('data-start') + timezone,
                end   = $(this).attr('data-end') + timezone;
            var dtStart = new Date(start),
                dtEnd   = new Date(end),
                dtNow   = new Date();
            // return type
            var return_type = settings.returnType;
            if (undefined !== $(this).attr('data-return-type')) { return_type = $(this).attr('data-return-type'); }
            // prepare IDs
            // 1. this ID
            var timer_id = '#'+$(this).attr('id');
            // 2. timer wrapper ID
            var wrapper_id = settings.wrapper_id;
            if (undefined !== $(this).attr('data-wrapper-id')) { wrapper_id = $(this).attr('data-wrapper-id'); }
            if ("" !== wrapper_id && wrapper_id.indexOf('.') === -1 && wrapper_id.indexOf('#') === -1) { wrapper_id = '#'+wrapper_id; }
            // 3. time's up wrapper ID
            var timesup_wrapper_id = settings.timesup_wrapper_id;
            if (undefined !== $(this).attr('data-timesup-wrapper-id')) { timesup_wrapper_id = $(this).attr('data-timesup-wrapper-id'); }
            if ("" !== timesup_wrapper_id && timesup_wrapper_id.indexOf('.') === -1 && timesup_wrapper_id.indexOf('#') === -1) { timesup_wrapper_id = '#'+timesup_wrapper_id; }
            // 4. no show wrapper ID
            var noshow_wrapper_id = settings.noshow_wrapper_id;
            if (undefined !== $(this).attr('data-noshow-wrapper-id')) { noshow_wrapper_id = $(this).attr('data-noshow-wrapper-id'); }
            if ("" !== noshow_wrapper_id && noshow_wrapper_id.indexOf('.') === -1 && noshow_wrapper_id.indexOf('#') === -1) {noshow_wrapper_id = '#'+noshow_wrapper_id; }
            // calculation
            if (dtStart > dtNow || dtEnd < dtNow) {
                // no show: hide the timer and wrapper, show the noshow id
                $(this).hide();
                if ("" !== wrapper_id) { $(wrapper_id).hide(); }
                if ("" !== noshow_wrapper_id) { $(noshow_wrapper_id).show(); }
            } else {
                calculateTimeDifferent(dtEnd, return_type, timer_id, wrapper_id, timesup_wrapper_id, settings.local_s_days, settings.local_s_hrs, settings.local_s_min, settings.local_s_sec, settings.local_l_days, settings.local_l_hrs, settings.local_l_min, settings.local_l_sec);
            }
        });
    };
    function calculateTimeDifferent(endTime, type, timer_id, wrapper_id, timesup_wrapper_id, local_s_days, local_s_hrs, local_s_min, local_s_sec, local_l_days, local_l_hrs, local_l_min, local_l_sec) {
        var now = new Date(),
            difference = endTime.getTime() - now.getTime();
        if (difference <= 0) {
            $(timer_id).hide();
            if ("" !== wrapper_id) { $(wrapper_id).hide(); }
            if ("" !== timesup_wrapper_id) { $(timesup_wrapper_id).show(); }
        } else {
            var seconds = Math.floor(difference / 1000),
                sec = Math.floor(seconds % 60),
                minutes = Math.floor(seconds / 60),
                min = Math.floor(minutes % 60),
                hours = Math.floor(minutes / 60),
                hrs = Math.floor(hours % 24),
                days = Math.floor(hours / 24);
            if ("text" === type) {
                var str = days + local_s_days + ' ' + hrs + local_s_hrs + ' ' + min + local_s_min + ' ' + sec + local_s_sec;
                if (0 === days) {
                    if (0 == hrs) {
                        if (0 == min) {
                            str = sec + local_s_sec;
                        } else {
                            str = min + local_s_min + ' ' + sec + local_s_sec;
                        }
                    } else {
                        str = hrs + local_s_hrs + ' ' + min + local_s_min + ' ' + sec + local_s_sec;
                    }
                }
                $(timer_id).html(str);
            } else {
                if (10 > days) { days = "0" + days; }
                if (10 > hrs) { hrs = "0" + hrs; }
                if (10 > min) { min = "0" + min; }
                if (10 > sec) { sec = "0" + sec; }
                var str = '<div class="countdown_box countdown_day"><b>' + days + '</b><br />' + local_l_days + '</div>';
                str += '<div class="countdown_box countdown_hours"><b>' + hrs + '</b><br />' + local_l_hrs + '</div>';
                str += '<div class="countdown_box countdown_mins"><b>' + min + '</b><br />' + local_l_min + '</div>';
                str += '<div class="countdown_box countdown_sec"><b>' + sec + '</b><br />' + local_l_sec + '</div>';
                $(timer_id).html(str);
            }
            setTimeout(function () {
                calculateTimeDifferent(endTime, type, timer_id, wrapper_id, timesup_wrapper_id, local_s_days, local_s_hrs, local_s_min, local_s_sec, local_l_days, local_l_hrs, local_l_min, local_l_sec);
            }, 1000);
        }
    }
}(jQuery));