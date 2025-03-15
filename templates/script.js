// Get the canvas element
const ctx = document.getElementById('radarChart').getContext('2d');

// Data for the radar chart
const data = {
    labels: ['Speed', 'Strength', 'Agility', 'Endurance', 'Flexibility'],
    datasets: [
        {
            label: 'Athlete A',
            data: [80, 90, 75, 85, 70], // Data points
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2
        },
        {
            label: 'Athlete B',
            data: [60, 85, 95, 70, 80],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2
        }
    ]
};

// Radar chart configuration
const config = {
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
};

// Create the radar chart
new Chart(ctx, config);