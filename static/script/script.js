// Function to display the current question and options
function displayQuestion(currentQuestionId, questionData) {
    $('#question').text(questionData.stats_question);
    var optionsContainer = $('#options').empty();
    // console.log(questionData)
    console.log(currentQuestionId);
    var isString = typeof questionData.next_question[0] !== 'number';
    var backOption = questionData.options.pop();
    $.each(questionData.options, function(index, option) {
        var optionButton = $('<button>').text(option).click(function() {
            if (typeof questionData.next_question[index] !== 'number') {
                optionsContainer.append(backButton); // Append back button
                $('#question').empty();
                $('#answer').text(questionData.next_question[index]);
                $('#options').empty(); // Clear options
            } else {
                // If the next question ID is a number, fetch and display the next question
                selectOption(questionData.next_question[index]);
            }
        });
        optionsContainer.append(optionButton);
    });
    // Add Back button at the bottom left
    var backButton = $('<button>').text(backOption).click(function() {
        // Display the question corresponding to "Back" option
        selectOption(questionData.next_question[questionData.options.length]);
    }).addClass('back-button'); // Add class for styling
    optionsContainer.append(backButton);
}

// Function to select an option and fetch the next question
function selectOption(nextQuestionId) {
    $.ajax({
        url: '/next/' + nextQuestionId,
        type: 'GET',
        contentType: 'application/json',
        success: function(questionData) {
            displayQuestion(nextQuestionId, questionData); // Update the question and options
        },
        error: function(xhr, status, error) {
            console.error('Error:', error); // Log any errors to the console
        }
    });
}

// Function to fetch the initial question when the page loads
function loadInitialQuestion() {
    $.getJSON('/next/0', function(questionData) {
        displayQuestion(0, questionData); // Pass the initial question ID
        $('#restart-button').click(function() {
            // Load question with ID 1
            $('#answer').empty()
            selectOption(0);
        });
    });
}


var particles = Particles.init({
	selector: '.background',
  sizeVariations: 10,
  color: ['#00bbdd', '#404B69', '#DBEDF3'],
  connectParticles: true
});

// Load the initial question when the page loads
$(document).ready(function() {
    loadInitialQuestion();
});

