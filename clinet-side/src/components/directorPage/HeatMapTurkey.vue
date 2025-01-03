<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import * as echarts from 'echarts';
import turkeyGeoJson from '@/assets/turkey.json';

// Reference for the heatmap container
const heatmap = ref(null);
let chartInstance = null;

// Data for the heatmap
const data = ref([
    { name: "Adana", value: 120, highSchools: [{ name: "High School 1", students: 50 }, { name: "High School 2", students: 70 }] },
    { name: "Adıyaman", value: 80, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 50 }] },
    { name: "Afyonkarahisar", value: 90, highSchools: [{ name: "High School 1", students: 40 }, { name: "High School 2", students: 50 }] },
    { name: "Ağrı", value: 70, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 40 }] },
    { name: "Aksaray", value: 50, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 30 }] },
    { name: "Amasya", value: 60, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 30 }] },
    { name: "Ankara", value: 200, highSchools: [{ name: "High School 1", students: 100 }, { name: "High School 2", students: 100 }] },
    { name: "Antalya", value: 100, highSchools: [{ name: "High School 1", students: 50 }, { name: "High School 2", students: 50 }] },
    { name: "Ardahan", value: 20, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 10 }] },
    { name: "Artvin", value: 30, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 15 }] },
    { name: "Aydın", value: 110, highSchools: [{ name: "High School 1", students: 60 }, { name: "High School 2", students: 50 }] },
    { name: "Balıkesir", value: 95, highSchools: [{ name: "High School 1", students: 45 }, { name: "High School 2", students: 50 }] },
    { name: "Bartın", value: 35, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 20 }] },
    { name: "Batman", value: 75, highSchools: [{ name: "High School 1", students: 35 }, { name: "High School 2", students: 40 }] },
    { name: "Bayburt", value: 15, highSchools: [{ name: "High School 1", students: 5 }, { name: "High School 2", students: 10 }] },
    { name: "Bilecik", value: 25, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 15 }] },
    { name: "Bingöl", value: 55, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 30 }] },
    { name: "Bitlis", value: 40, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 20 }] },
    { name: "Bolu", value: 45, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 25 }] },
    { name: "Burdur", value: 30, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 15 }] },
    { name: "Bursa", value: 180, highSchools: [{ name: "High School 1", students: 90 }, { name: "High School 2", students: 90 }] },
    { name: "Çanakkale", value: 85, highSchools: [{ name: "High School 1", students: 40 }, { name: "High School 2", students: 45 }] },
    { name: "Çankırı", value: 20, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 10 }] },
    { name: "Çorum", value: 50, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 25 }] },
    { name: "Denizli", value: 95, highSchools: [{ name: "High School 1", students: 45 }, { name: "High School 2", students: 50 }] },
    { name: "Diyarbakır", value: 130, highSchools: [{ name: "High School 1", students: 60 }, { name: "High School 2", students: 70 }] },
    { name: "Düzce", value: 40, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 20 }] },
    { name: "Edirne", value: 65, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 35 }] },
    { name: "Elazığ", value: 75, highSchools: [{ name: "High School 1", students: 35 }, { name: "High School 2", students: 40 }] },
    { name: "Erzincan", value: 50, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 25 }] },
    { name: "Erzurum", value: 90, highSchools: [{ name: "High School 1", students: 40 }, { name: "High School 2", students: 50 }] },
    { name: "Eskişehir", value: 120, highSchools: [{ name: "High School 1", students: 60 }, { name: "High School 2", students: 60 }] },
    { name: "Gaziantep", value: 150, highSchools: [{ name: "High School 1", students: 70 }, { name: "High School 2", students: 80 }] },
    { name: "Giresun", value: 55, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 30 }] },
    { name: "Gümüşhane", value: 25, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 15 }] },
    { name: "Hakkari", value: 30, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 15 }] },
    { name: "Hatay", value: 100, highSchools: [{ name: "High School 1", students: 50 }, { name: "High School 2", students: 50 }] },
    { name: "Iğdır", value: 20, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 10 }] },
    { name: "Isparta", value: 60, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 30 }] },
    { name: "Istanbul", value: 220, highSchools: [{ name: "High School 1", students: 200 }, { name: "High School 2", students: 25 }, { name: "High School 3", students: 25 }] },
    { name: "İzmir", value: 150, highSchools: [{ name: "High School 1", students: 75 }, { name: "High School 2", students: 75 }] },
    { name: "Kahramanmaraş", value: 110, highSchools: [{ name: "High School 1", students: 55 }, { name: "High School 2", students: 55 }] },
    { name: "Karabük", value: 35, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 20 }] },
    { name: "Karaman", value: 40, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 20 }] },
    { name: "Kars", value: 45, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 25 }] },
    { name: "Kastamonu", value: 50, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 25 }] },
    { name: "Kayseri", value: 120, highSchools: [{ name: "High School 1", students: 60 }, { name: "High School 2", students: 60 }] },
    { name: "Kilis", value: 25, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 15 }] },
    { name: "Kırıkkale", value: 30, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 15 }] },
    { name: "Kırklareli", value: 40, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 20 }] },
    { name: "Kırşehir", value: 35, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 20 }] },
    { name: "Kocaeli", value: 140, highSchools: [{ name: "High School 1", students: 70 }, { name: "High School 2", students: 70 }] },
    { name: "Konya", value: 150, highSchools: [{ name: "High School 1", students: 75 }, { name: "High School 2", students: 75 }] },
    { name: "Kütahya", value: 55, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 30 }] },
    { name: "Malatya", value: 90, highSchools: [{ name: "High School 1", students: 40 }, { name: "High School 2", students: 50 }] },
    { name: "Manisa", value: 110, highSchools: [{ name: "High School 1", students: 55 }, { name: "High School 2", students: 55 }] },
    { name: "Mardin", value: 80, highSchools: [{ name: "High School 1", students: 40 }, { name: "High School 2", students: 40 }] },
    { name: "Mersin", value: 130, highSchools: [{ name: "High School 1", students: 65 }, { name: "High School 2", students: 65 }] },
    { name: "Muğla", value: 100, highSchools: [{ name: "High School 1", students: 50 }, { name: "High School 2", students: 50 }] },
    { name: "Muş", value: 40, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 20 }] },
    { name: "Nevşehir", value: 50, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 25 }] },
    { name: "Niğde", value: 45, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 25 }] },
    { name: "Ordu", value: 65, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 35 }] },
    { name: "Osmaniye", value: 60, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 30 }] },
    { name: "Rize", value: 55, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 30 }] },
    { name: "Sakarya", value: 95, highSchools: [{ name: "High School 1", students: 45 }, { name: "High School 2", students: 50 }] },
    { name: "Samsun", value: 120, highSchools: [{ name: "High School 1", students: 60 }, { name: "High School 2", students: 60 }] },
    { name: "Siirt", value: 40, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 20 }] },
    { name: "Sinop", value: 30, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 15 }] },
    { name: "Sivas", value: 80, highSchools: [{ name: "High School 1", students: 40 }, { name: "High School 2", students: 40 }] },
    { name: "Şanlıurfa", value: 150, highSchools: [{ name: "High School 1", students: 75 }, { name: "High School 2", students: 75 }] },
    { name: "Şırnak", value: 35, highSchools: [{ name: "High School 1", students: 15 }, { name: "High School 2", students: 20 }] },
    { name: "Tekirdağ", value: 100, highSchools: [{ name: "High School 1", students: 50 }, { name: "High School 2", students: 50 }] },
    { name: "Tokat", value: 60, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 30 }] },
    { name: "Trabzon", value: 90, highSchools: [{ name: "High School 1", students: 40 }, { name: "High School 2", students: 50 }] },
    { name: "Tunceli", value: 20, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 10 }] },
    { name: "Uşak", value: 40, highSchools: [{ name: "High School 1", students: 20 }, { name: "High School 2", students: 20 }] },
    { name: "Van", value: 110, highSchools: [{ name: "High School 1", students: 55 }, { name: "High School 2", students: 55 }] },
    { name: "Yalova", value: 25, highSchools: [{ name: "High School 1", students: 10 }, { name: "High School 2", students: 15 }] },
    { name: "Yozgat", value: 50, highSchools: [{ name: "High School 1", students: 25 }, { name: "High School 2", students: 25 }] },
    { name: "Zonguldak", value: 60, highSchools: [{ name: "High School 1", students: 30 }, { name: "High School 2", students: 30 }] },
]);

// Modal state
const isModalOpen = ref(false);
const selectedCity = ref(null);
const selectedCityHighSchools = ref([]);

const renderChart = () => {
  if (heatmap.value) {
    chartInstance = echarts.init(heatmap.value);
    echarts.registerMap('turkey', turkeyGeoJson);
    
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: params => `${params.name}: ${params.value || 'No data'}`
      },
      visualMap: {
        left: 'left',
        text: ['High', 'Low'],
        calculable: true,
        min: 0, // Set the minimum value for the visualMap
        max: 250, // Set the maximum value for the visualMap
        inRange: {
          color: ['#fff5f5', '#ffcccc', '#ff9999', '#ff6666', '#ff3333', '#ff0000', '#cc0000', '#990000', '#660000']
        }
      },
      geo: {
        map: 'turkey',
        roam: false,
        label: {
          emphasis: { show: false }
        },
        itemStyle: {
          normal: {
            areaColor: '#323c48',
            borderColor: '#111'
          },
          emphasis: {
            areaColor: '#323c48', // Prevent highlighting by keeping the same color
            borderColor: '#111' // Keep the border color the same
          }
        }
      },
      series: [
        {
          type: 'map',
          map: 'turkey',
          geoIndex: 0,
          data: data.value
        }
      ]
    };
    
    chartInstance.setOption(option);
    chartInstance.on('click', onChartClick);
    
    window.addEventListener('resize', resizeChart);
  }
};

onMounted(() => {
  renderChart();
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.off('click', onChartClick);
    chartInstance.dispose();
    window.removeEventListener('resize', resizeChart);
  }
});

function onChartClick(params) {
  selectedCity.value = params.name;
  const cityData = data.value.find(city => city.name === params.name);
  selectedCityHighSchools.value = cityData ? cityData.highSchools : [];
  isModalOpen.value = true;
}

function resizeChart() {
  if (chartInstance) {
    chartInstance.resize();
  }
}

function closeModal() {
  isModalOpen.value = false;
}
</script>

<template>
  <div class="flex justify-center items-center h-full w-full">
    <div ref="heatmap" class="w-full h-full"></div>
    
    <!-- Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-bold mb-4">City Information</h2>
        <p><strong>City:</strong> {{ selectedCity }}</p>
        <table class="min-w-full bg-white">
          <thead>
            <tr>
              <th class="py-2">High School</th>
              <th class="py-2">Number of Students</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(school, index) in selectedCityHighSchools" :key="index">
              <td class="border px-4 py-2">{{ school.name }}</td>
              <td class="border px-4 py-2">{{ school.students }}</td>
            </tr>
          </tbody>
        </table>
        <button @click="closeModal" class="mt-4 px-4 py-2 rounded bg-red-500 text-white hover:bg-red-700">Close</button>
      </div>
    </div>
  </div>
</template>