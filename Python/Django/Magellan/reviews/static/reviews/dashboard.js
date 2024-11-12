let totalReviewsChart;
let averageRatingChart;
let averageSentimentChart;
let dominantTopicSentimentChart;
let scatterSentimentRatingChart;


function initializeChart(chartId, labels, data, type, datasetLabel, borderColor, backgroundColor, options = {}) {
    const ctx = document.getElementById(chartId);
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: datasetLabel,
                data: data,
                borderColor: borderColor,
                backgroundColor: backgroundColor,
                borderWidth: 2,
                fill: true
            }]
        },
        options: options
    });
}


function initializeStackedBarChart(chartId, labels, datasets, options = {}) {
    const ctx = document.getElementById(chartId);
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            indexAxis: 'y',
            scales: {
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 10
                        }
                    }
                },
                y: {
                    stacked: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 10
                        }
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    labels: {
                        font: {
                            size: 11
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Dominant Topic by Sentiment Category',
                    align: 'start',
                }
            }
        }
    });
}

function updateChart(chart, labels, data) {
    // Update chart data
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();
}

function updateStackedBarChart(chart, labels, datasets) {
    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
}



function applyFilters() {
    const date = document.getElementById('date').value;
    const creditType = document.getElementById('credit_type').value;
    const sentimentCategory = document.getElementById('sentiment_category').value;
    const dominantTopic = document.getElementById('dominant_topic').value;

    // Make AJAX request with filter parameters
    fetch(`/dashboard/filter_data/?date=${date}&credit_type=${creditType}&sentiment_category=${sentimentCategory}&dominant_topic=${dominantTopic}`)
        .then(response => response.json())
        .then(data => {
            // Update total reviews chart
            const totalReviewLabels = Object.keys(data.total_reviews_by_date);
            const totalReviewValues = Object.values(data.total_reviews_by_date);
            updateChart(totalReviewsChart, totalReviewLabels, totalReviewValues);

            // Update average rating chart
            const avgRatingLabels = Object.keys(data.average_rating_by_date);
            const avgRatingValues = Object.values(data.average_rating_by_date);
            updateChart(averageRatingChart, avgRatingLabels, avgRatingValues);

            // Update average sentiment chart
            const avgSentimentLabels = Object.keys(data.average_sentiment_by_date);
            const avgSentimentValues = Object.values(data.average_sentiment_by_date);
            updateChart(averageSentimentChart, avgSentimentLabels, avgSentimentValues);

            // Update sentiment category stacked bar chart
            updateStackedBarChart(dominantTopicSentimentChart, data.dominantTopicSentimentlabels, data.dominantTopicSentimentdatasets);

            // Update scatter plot sentiment by rating chart
            // const scatterLabels = Object.keys(data.scatter_plot_data);
            // const scatterData = data.scatter_plot_data.map(item => ({
            //     x: item.scatterAverageSentiments,
            //     y: item.scatterAverageRatings
            // }));
        })
        .catch(error => console.error('Error fetching data:', error));
}


// Load initial chart with default data
document.addEventListener('DOMContentLoaded', () => {
    // Fetch initial data
    fetch('/dashboard/filter_data/')
        .then(response => response.json())
        .then(data => {
            const totalReviewLabels = Object.keys(data.total_reviews_by_date);
            const totalReviewValues = Object.values(data.total_reviews_by_date);
            totalReviewsChart = initializeChart(
                'total_reviews_count',
                totalReviewLabels,
                totalReviewValues,
                'line',
                'Total Reviews',
                'rgba(115, 128, 236, 1)',
                'rgba(115, 128, 236, 0.2)',
                {responsive: true,
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 10
                            }
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 11
                            }
                        }
                    }
                }
                }
            );


            // Initialize additional chart for average sentiment score timeline
            const avgRatingLabels = Object.keys(data.average_rating_by_date);
            const avgRatingValues = Object.values(data.average_rating_by_date);
            averageRatingChart = initializeChart(
                'average_rating_timeline',
                avgRatingLabels,
                avgRatingValues,
                'line',
                'Average Rating',
                'rgba(75, 192, 192, 1)',
                'rgba(75, 192, 192, 0.2)',
                {responsive: true,
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 10
                            }
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 11
                            }
                        }
                    }
                }
                }
            );


            // Initialize additional chart for average sentiment score timeline
            const avgSentimentLabels = Object.keys(data.average_sentiment_by_date);
            const avgSentimentValues = Object.values(data.average_sentiment_by_date);
            averageSentimentChart = initializeChart(
                'average_sentiment_timeline',
                avgSentimentLabels,
                avgSentimentValues,
                'line',
                'Average Sentiment',
                'rgba(233, 116, 81, 1)',
                'rgba(233, 116, 81, 0.2)',
                {responsive: true,
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 10
                            }
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 11
                            }
                        }
                    }
                }
                }
            );


            // Initialize the stacked vbar chart
            dominantTopicSentimentChart = initializeStackedBarChart(
                'topic_sentiment_vbar',
                data.dominantTopicSentimentlabels,
                data.dominantTopicSentimentdatasets
            );


            // Intialize the scatter plot
            const scatterLabels = data.scatter_plot_data.products;
            const scatterData = data.scatter_plot_data.products.map((product, index) => ({
                x: data.scatter_plot_data.average_sentiments[index],
                y: data.scatter_plot_data.average_ratings[index],
                backgroundColor: data.scatter_plot_data.colors[index]
            }));
            scatterSentimentRatingChart = initializeChart(
                'sentiment_topic_scatter',
                scatterLabels,
                scatterData,
                'scatter',
                'Sentiment vs Rating',
                'rgba(0, 0, 0, 0.5)',
                data.scatter_plot_data.colors,
                {responsive: true,
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 10
                            }
                        },
                        beginAtZero: true
                    },
                    y: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 10
                            }
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Avg. Sentiment (X-Axis) v. Avg. Rating (Y-Axis)',
                        align: 'start',
                        padding: {
                            bottom: 30
                        }
                    }
                },
                elements: {
                    point: {
                        radius: 8,
                        hoverRadius: 8
                    }
                }
                }
            );
        });
});

