import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { formatTimeESTShort } from '../utils/timezone'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

export function MetricChart({ title, dataPoints, color = '#60a5fa' }) {
  const labels = dataPoints.map((m) => formatTimeESTShort(m.timestamp))
  const data = {
    labels,
    datasets: [
      {
        label: title,
        data: dataPoints.map((m) => m.value),
        borderColor: color,
        backgroundColor: color,
        tension: 0.35,
        pointRadius: 2,
      },
    ],
  }

  return <Line data={data} options={{ plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }} />
}
