

$(document).ready(function() {
    $('#systemSwitch').change(function() {
        if ($(this).is(':checked')) {
            $('.control-div').removeClass('disabled-section');
            $('.system-row-wrapper').removeClass('no-shadow');



            $.ajax({
                url: '/trigger_enable_system',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle On: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }else{
            $('.control-div').addClass('disabled-section');
            $('.system-row-wrapper').addClass('no-shadow');

            $('#alarmSwitch').prop('checked', false);
            $('#lightSwitch').prop('checked', false);

            $.ajax({
                url: '/trigger_disable_system',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle Off: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }
    });


    $('#lightRoomSwitch').change(function() {
        if ($(this).is(':checked')) {
            $.ajax({
                url: '/trigger_enable_lightRoom',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle On: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }else{
            $.ajax({
                url: '/trigger_disable_lightRoom',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle Off: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    $('#fanRoomSwitch').change(function() {
        if ($(this).is(':checked')) {
            $.ajax({
                url: '/trigger_enable_fanRoom',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle On: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }else{
            $.ajax({
                url: '/trigger_disable_fanRoom',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle Off: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    $('#alarmSwitch').change(function() {
        if ($(this).is(':checked')) {
            $.ajax({
                url: '/trigger_enable_alarm',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle On: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }else{
            $.ajax({
                url: '/trigger_disable_alarm',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle Off: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    $('#lightSwitch').change(function() {
        if ($(this).is(':checked')) {
            $.ajax({
                url: '/trigger_enable_light',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle On: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }else{
            $.ajax({
                url: '/trigger_disable_light',  // Flask route to trigger Python code
                type: 'GET',
                success: function(response) {
                    console.log('Toggle Off: Python code executed successfully');
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }
    });
});