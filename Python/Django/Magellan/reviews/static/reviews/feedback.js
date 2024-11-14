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

            // Update reviews container with filtered data
            data.feedback_data.forEach(item => {
                const feedbackCard = document.createElement('div');
                feedbackCard.classList.add('feedback-card');

                feedbackCard.innerHTML = `
                    <h2>${item.product}</h2>
                    <p><strong>Rating:</strong> ${item.rating_int}</p>
                    <p><strong>Sentiment:</strong>${item.sentiment_category}</p>
                    <p><strong>Topic:</strong> ${item.dominant_topic}</p>
                    <p><strong>Review Date:</strong> ${item.date}</p>
                `;
                feedbackContainer.appendChild(feedbackCard);
            });
        })
        .catch(error => console.error('Error fetching filtered feedback:', error));
}