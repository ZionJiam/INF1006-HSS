$(document).ready(function() {

    $('#systemSwitch').change(function() {
    const liveFeedImage = document.getElementById('livefeed'); // Select the image element by ID
        if ($(this).is(':checked')) {
            liveFeedImage.src = '/proxy_feed';
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
            liveFeedImage.src = '/static/dental_front.jpg'; // Update this path as needed
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
var socket = io.connect("http://" + document.domain + ":" + location.port);
socket.on("update_images", function(data) {
    console.log("Received update_images:", data);
    data.latest_images.forEach((imageUrl, index) => {
        var imageId = "latest" + (index + 1);
        var imageElement = document.getElementById(imageId);
        if (imageElement) {
            imageElement.src = imageUrl;  // Ensure imageUrl points to the right path
        } else {
            console.error("Could not find image element with ID:", imageId);
        }
    });
});
});
function attemptLiveFeedLoad(attempts, delay) {
    const liveFeedImage = document.getElementById('livefeed');
    if (attempts === 0) {
        console.error('Failed to load live feed after multiple attempts.');
        return;
    }

    // Try to load the live feed
    liveFeedImage.onerror = () => {
        console.log(`Live feed failed to load. Retrying... (${attempts} attempts left)`);
        setTimeout(() => {
            attemptLiveFeedLoad(attempts - 1, delay);
        }, delay);
    };

    // If the image loads successfully, clear the error handler
    liveFeedImage.onload = () => {
        liveFeedImage.onerror = null;
        console.log('Live feed loaded successfully.');
    };

    // Set the source to start loading
    liveFeedImage.src = '/proxy_feed';
}
document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Load and display images from localStorage on page load/refresh
    displayImagesFromLocalStorage();

    socket.on('update_images', function(data) {
        localStorage.setItem('latest_images', JSON.stringify(data.latest_images));
        displayImagesFromLocalStorage();
    });
});

function displayImagesFromLocalStorage() {
    const images = JSON.parse(localStorage.getItem('latest_images') || '[]');
    images.forEach((imageUrl, index) => {
        const imgElement = document.getElementById(`latest${index + 1}`);
        if (imgElement) {
            imgElement.src = imageUrl;
        }
    });
}