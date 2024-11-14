function applyFeedbackFilters() {
    const date = document.getElementById('date').value;
    const creditType = document.getElementById('credit_type').value;
    const sentimentCategory = document.getElementById('sentiment_category').value;
    const dominantTopic = document.getElementById('dominant_topic').value;

    // Send AJAX request to filter reviews
    fetch(`/feedback/filter_reviews/?date=${date}&credit_type=${creditType}&sentiment_category=${sentimentCategory}&dominant_topic=${dominantTopic}`)
        .then(response => response.text())
        .then(html => {
            const feedbackContainer = document.getElementById('feedback-container');
            feedbackContainer.innerHTML = html;
        })
        .catch(error => console.error('Error fetching filtered feedback:', error));
}