$(document).ready(function() {

    // Count of checks to be completed 
    const checksCount = $('.check-box').length /2;
    $("#countOfChecks").text(checksCount)
    console.log("Count of checks: "+checksCount)
    // Function to update the count
    console.log("ready to update")
    function updateCount() {
        // Count the number of checked checkboxes
        const checkedCount = $('.check-box:checked').length;
        console.log('Items checked: '+checkedCount)
        // Update the count in the HTML
        $('#count').text(checkedCount);
        const checksLeft = checksCount - checkedCount
        $('#countOfChecksLeft').text(checksLeft);
    }

    // Attach event listener to all checkboxes
    $('.check-box').change(updateCount);


    let notesAndImages = {}; // Store base64 images with their associated check item
    const maxImageSizeBytes = 25 * 1024; // 25KB limit
  
    // Event listener for paste on the editable div
    $("div[contenteditable=true]").on("paste", function(e) {
        const notesDivId = $(this).attr("id");
        handlePaste(e, notesDivId);
    });
  
    function handlePaste(e, notesDivId) {
        const items = (e.clipboardData || e.originalEvent.clipboardData).items;
  
        for (const item of items) {
            if (item.type.indexOf("image") === 0) {
                e.preventDefault();
                const file = item.getAsFile();
  
                if (file.size > maxImageSizeBytes) {
                    alert("NOTE: This image will NOT be posted to MSTeams but it will be included in the Ticket being logged.");
                }
  
                const reader = new FileReader();
                reader.onload = function(event) {
                    // Append the image to the notes div for display
                    const img = document.createElement("img");
                    img.src = event.target.result;
                    img.classList.add("image-preview");
  
                    $("#" + notesDivId).append(img);
  
                    // Initialize array for this notesDivId if not already done
                    if (!notesAndImages[notesDivId]) {
                        notesAndImages[notesDivId] = { notes: '', images: [] };
                    }
  
                    // Store the image in the array for this notesDivId
                    notesAndImages[notesDivId].images.push(event.target.result);
                };
                reader.readAsDataURL(file);
            }
        }
    }
  
    $('.custom-checkbox').click(function() {
        const checkItem = $(this).closest('.check-item');
        const okCheckbox = checkItem.find('input[type="checkbox"][value="OK"]');
        const problemCheckbox = checkItem.find('input[type="checkbox"][value="PROBLEM"]');
        const notes = checkItem.find('.notes');
  
        // Handle mutually exclusive checkboxes
        if ($(this).find('input[type="checkbox"]').val() === "OK") {
            if (okCheckbox.prop('checked')) {
                problemCheckbox.prop('checked', false); // Uncheck 'PROBLEM' if 'OK' is checked
                notes.hide().html(''); // Hide and clear notes if "OK" is checked
            }
        } else if ($(this).find('input[type="checkbox"]').val() === "PROBLEM") {
            if (problemCheckbox.prop('checked')) {
                okCheckbox.prop('checked', false); // Uncheck 'OK' if 'PROBLEM' is checked
                notes.show(); // Show notes if "PROBLEM" is checked
            } else {
                notes.hide().html(''); // Hide and clear notes if "PROBLEM" is unchecked
            }
        }
  
        // Check for completion after every change
        checkCompletion();
    });
  
    // Check if all check items have a selected value
    function checkCompletion() {
        const totalItems = $('.check-item').length;
        const selectedItems = $('.check-box:checked').length;
  
        if (selectedItems === totalItems) {
            $('#complete-btn').show(); // Show the button when all checks are answered
        } else {
            $('#complete-btn').hide(); // Hide the button if not all checks are answered
        }
    }
  
    // Handle form submission
    $('#checklist-form').submit(function(event) {
        event.preventDefault();
        $('#loading-spinner').show();
  
        // Collect data from the form
        let formData = {};
        $('.check-item').each(function() {
            const checkId = $(this).attr('id');
            const checkValue = $(this).find('input[type="checkbox"]:checked').map(function() {
                return $(this).val();
            }).get(); // Get all selected values
  
            const notes = $(this).find('.notes').clone(); // Clone the notes div to manipulate it
            notes.find('img').remove(); // Remove any images from the notes
            const notesContent = notes.html(); // Get the remaining notes content
  
            formData[checkId] = {
                result: checkValue.length > 0 ? checkValue : null, // Include selected values if they exist
                notes: notesContent || null, // Include only text notes, if they exist
                image: notesAndImages[checkId + "-notes"] ? notesAndImages[checkId + "-notes"].images : null // Include images if they exist
            };
        });
  
        // Send data via AJAX
        $.ajax({
            url: '/catch',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                // Update the HTML elements with the response data
                $('#ticketsLogged').html('<strong style="color: black;">Number of Tickets Logged:</strong> <span class="response-text">' + response.ticketsLogged + '</span>');
                $('#ticketsLoggedPassed').html('<strong style="color: black;">Tickets Logged Successfully:</strong> <span class="response-text">' + response.ticketsLoggedPassed + '</span>');
                $('#ticketsAssignedTo').html('<strong style="color: black;">Tickets Logged Assigned:</strong> <span class="response-text">' + response.ticketsAssignedTo + '</span>');
                $('#teamsPostSentStatus').html('<strong style="color: black;">MSTeams Messages Posted:</strong> <span class="response-text">' + response.teamsPostSentStatus + '</span>');
  
                // Hide loading spinner
                $('#loading-spinner').hide();
  
                // Show success message
                $('#success-message').show();
  
                // Reset form to prevent a duplicate submission
                $('#checklist-form')[0].reset();
                $('.custom-checkbox').removeClass('checked'); // Clear the custom checkbox states
                notesAndImages = {}; // Clear the notes and images
                checkCompletion();
  
                // Scroll to the top of the page
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth' // Makes the scroll smooth
                });
            },
            error: function(xhr, status, error) {
                $('#loading-spinner').hide();
                console.error('Error submitting checklist:', error);
            }
        });
    });
  });
  