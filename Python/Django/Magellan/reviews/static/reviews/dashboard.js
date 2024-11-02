let myChart;


function initializeChart(labels, data) {
    const ctx = document.getElementById('total_reviews_count');
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Reviews',
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


function updateChart(data) {
    const labels = Object.keys(data.total_reviews_by_date);
    const values = Object.values(data.total_reviews_by_date);

    // Update chart data
    myChart.data.labels = labels;
    myChart.data.datasets[0].data = values;
    myChart.update();
}


function applyFilters() {
    const date = document.getElementById('date').value;
    const creditType = document.getElementById('credit_type').value;
    const sentimentCategory = document.getElementById('sentiment_category').value;
    const dominantTopic = document.getElementById('dominant_topic').value;

    // Make AJAX request with filter parameters
    fetch(`/dashboard/filter_data/?date=${date}&credit_type=${creditType}&sentiment_category=${sentimentCategory}&topic=${dominantTopic}`)
        .then(response => response.json())
        .then(data => {
            updateChart(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Load initial chart with default data
document.addEventListener('DOMContentLoaded', () => {
    // Fetch initial data
    fetch('/dashboard/filter_data/')
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data.total_reviews_by_date);
            const values = Object.values(data.total_reviews_by_date);
            initializeChart(labels, values);
        });
});

