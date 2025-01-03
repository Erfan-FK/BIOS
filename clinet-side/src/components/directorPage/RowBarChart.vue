  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import {
      Chart,
      BarController,
      BarElement,
      CategoryScale,
      LinearScale,
      Tooltip,
      Legend,
    } from 'chart.js';
  
  // Register Chart.js components
  Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);
  
  // Props definition
  const props = defineProps({
      chartData: {
      type: Object,
      default: () => ({
          labels: ['January', 'February', 'March', 'April', 'May'],
          datasets: [
          {
              label: '', // Prevent 'undefined' label
              data: [150, 200, 180, 220, 170],
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
            },
        ],
    }),
},
options: {
    type: Object,
    default: () => ({
        indexAxis: 'y', // Horizontal bar chart
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false, // Hide legend
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                return context.parsed.x; // Show only the data value
              },
            },
        },
    },
    scales: {
        x: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Sales Amount',
                font: {
                    size: 14,
                    weight: 'bold',
                },
            },
            ticks: {
                precision: 0,
            },
        },
        y: {
            title: {
                display: true,
                text: 'Months',
                font: {
                    size: 14,
                    weight: 'bold',
                },
            },
        },
    },
      }),
    },
});
  
  // Ref for the canvas element
  const rowBarChart = ref(null);
  let chartInstance = null;
  
  // Function to render the chart
  const renderChart = () => {
    // Destroy existing chart instance if it exists to prevent duplication
    if (chartInstance) {
      chartInstance.destroy();
    }
  
    chartInstance = new Chart(rowBarChart.value, {
        type: 'bar',
        data: props.chartData,
        options: props.options,
    });
  };
  
  // Lifecycle hook: mounted
  onMounted(() => {
    renderChart();
  });
  
  // Lifecycle hook: beforeUnmount
  onBeforeUnmount(() => {
    if (chartInstance) {
      chartInstance.destroy();
    }
  });
  </script>
  
  <template>
      <div class="flex justify-center items-center w-full max-w-6xl mx-auto">
        <canvas ref="rowBarChart"></canvas>
      </div>
    </template>

  <style scoped>
  canvas {
      width: 100% !important;
      height: 100% !important;
    }
    </style>
  