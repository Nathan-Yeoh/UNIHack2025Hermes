document.addEventListener("DOMContentLoaded", function () {
    fetch('/chart-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('radarChart').getContext('2d');

            new Chart(ctx, {
                type: 'radar',
                data: data,
                options: {
                    responsive: true,
                    scales: {
                        r: {
                            beginAtZero: true,
                            suggestedMax: 100
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading chart data:', error));
});