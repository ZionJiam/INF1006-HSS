

$(document).ready(function() {
    $('#systemSwitch').change(function() {
        if ($(this).is(':checked')) {

            $('.control-button').addClass('disabled-section');


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

            $('.control-button').removeClass('disabled-section');


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