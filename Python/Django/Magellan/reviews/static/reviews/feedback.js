// Function to apply sentiment color dynamically
function applySentimentColor() {
    const sentimentTextElement = document.getElementById('sentimentText');
    const sentimentText = sentimentTextElement.textContent.trim();

    // Extract the sentiment category (the second word after "Sentiment:")
    const sentimentCategory = sentimentText.split(':')[1]?.trim();

    // Define sentiment category to color mapping
    const sentimentColors = {
        'Extremely Positive': 'green',     // Success color
        'Very Positive': 'green',          // Success color
        'Positive': 'green',               // Success color
        'Neutral': 'orange',               // Warning color
        'Negative': 'orange',              // Warning color
        'Very Negative': 'red',            // Error color
        'Extremely Negative': 'red'        // Error color
    };

    // Check if the sentiment category exists in our mapping
    if (sentimentCategory && sentimentColors[sentimentCategory]) {
        // Get the span that holds the sentiment category, or create one if not present
        let sentimentSpan = sentimentTextElement.querySelector('.sentiment-category');

        if (!sentimentSpan) {
            // If there's no span already, wrap the sentiment category in a span and preserve "Sentiment:"
            const sentimentStartIndex = sentimentText.indexOf(sentimentCategory);
            const sentimentEndIndex = sentimentStartIndex + sentimentCategory.length;
            const sentimentTextPart = sentimentText.slice(0, sentimentStartIndex) + 
                `<span class="sentiment-category">${sentimentCategory}</span>` + 
                sentimentText.slice(sentimentEndIndex);

            // Update the innerHTML with the span wrapped around the sentiment category
            sentimentTextElement.innerHTML = sentimentTextPart;
            sentimentSpan = sentimentTextElement.querySelector('.sentiment-category');
        }

        // Apply the color to the sentiment category
        sentimentSpan.style.color = sentimentColors[sentimentCategory];
    }
}
// Call this function after the page is loaded or when new content is rendered
document.addEventListener('DOMContentLoaded', applySentimentColor);



function applyFeedbackFilters() {
    const date = document.getElementById('date').value;
    const creditType = document.getElementById('credit_type').value;
    const sentimentCategory = document.getElementById('sentiment_category').value;
    const dominantTopic = document.getElementById('dominant_topic').value;

    // Send AJAX request to filter reviews
    fetch(`/feedback/filter_reviews/?date=${date}&credit_type=${creditType}&sentiment_category=${sentimentCategory}&dominant_topic=${dominantTopic}`)
        .then(response => response.json())
        .then(data => {
            const feedbackContainer = document.getElementById('feedback-container');
            feedbackContainer.innerHTML = '';

            // Define the CSS class for sentiment categories
            const sentimentClasses = {
                'Extremely Positive': 'sentiment-success',  // Green
                'Very Positive': 'sentiment-success',      // Green
                'Positive': 'sentiment-success',           // Green
                'Neutral': 'sentiment-warning',            // Orange
                'Negative': 'sentiment-warning',           // Orange
                'Very Negative': 'sentiment-error',        // Red
                'Extremely Negative': 'sentiment-error'    // Red
            };

            // Update reviews container with filtered data
            data.feedback_data.forEach(item => {
                const feedbackCard = document.createElement('div');
                feedbackCard.classList.add('feedback-card');

                // Apply the CSS class for sentiment based on the category
                const sentimentClass = sentimentClasses[item.sentiment_category] || 'sentiment-warning';  // Default to warning if not found

                feedbackCard.innerHTML = `
                    <h2>${item.product}</h2>
                    <p><strong>Rating:</strong> ${item.rating_int}</p>
                    <p><strong>Sentiment:</strong> <span class="${sentimentClass}">${item.sentiment_category}</span></p>
                    <p><strong>Topic:</strong> ${item.dominant_topic}</p>
                    <p><strong>Review Date:</strong> ${item.date}</p>
                `;
                feedbackContainer.appendChild(feedbackCard);
            });
        })
        .catch(error => console.error('Error fetching filtered feedback:', error));
}