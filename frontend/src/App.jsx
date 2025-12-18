import { useEffect, useState } from 'react'
import axios from 'axios'
import { MetricChart } from './components/MetricChart'
import { AlertList } from './components/AlertList'
import { Clock } from './components/Clock'
import { formatTimeEST } from './utils/timezone'

const API_KEY = import.meta.env.VITE_API_KEY || 'change-me'

export default function App() {
  const [devices, setDevices] = useState([])
  const [selectedDevice, setSelectedDevice] = useState(null)
  const [metrics, setMetrics] = useState({ cpu: [], memory: [], packet_loss: [] })
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(false)
  const [lastUpdate, setLastUpdate] = useState(null)

  useEffect(() => {
    fetchDevices()
  }, [])

  useEffect(() => {
    if (selectedDevice) {
      refreshData()
      const id = setInterval(refreshData, 10000)
      return () => clearInterval(id)
    }
  }, [selectedDevice])

  const client = axios.create({ headers: { 'X-API-KEY': API_KEY } })

  async function fetchDevices() {
    const res = await client.get('/api/devices')
    setDevices(res.data)
    setSelectedDevice(res.data?.[0]?.id ?? null)
  }

  async function refreshData() {
    if (!selectedDevice) return
    setLoading(true)
    const [cpu, mem, loss, alertsRes] = await Promise.all([
      client.get(`/api/metrics/${selectedDevice}?metric=cpu&minutes=60`),
      client.get(`/api/metrics/${selectedDevice}?metric=memory&minutes=60`),
      client.get(`/api/metrics/${selectedDevice}?metric=packet_loss&minutes=60`),
      client.get('/api/alerts?limit=20'),
    ])
    setMetrics({ cpu: cpu.data, memory: mem.data, packet_loss: loss.data })
    setAlerts(alertsRes.data)
    setLastUpdate(new Date())
    setLoading(false)
  }

  async function pollNow() {
    setLoading(true)
    await client.post('/api/poll')
    await refreshData()
  }

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1>Network Monitoring Dashboard</h1>
          <p style={{ opacity: 0.7 }}>Real-time health, bandwidth, and alerts</p>
          {lastUpdate && (
            <p style={{ opacity: 0.6, fontSize: '0.85rem', margin: '8px 0 0 0' }}>
              Last updated: {formatTimeEST(lastUpdate)}
            </p>
          )}
        </div>
        <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          <Clock />
          <button className="button" onClick={pollNow} disabled={loading}>
            {loading ? 'Polling…' : 'Poll Now'}
          </button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <div className="header">
          <div>
            <strong>Devices</strong>
            <p style={{ opacity: 0.7, margin: 0 }}>Select a device to view metrics</p>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            {devices.map((d) => (
              <button
                key={d.id}
                className="button"
                style={{
                  background: selectedDevice === d.id ? '#1d4ed8' : '#0f172a',
                  border: '1px solid rgba(255,255,255,0.1)',
                }}
                onClick={() => setSelectedDevice(d.id)}
              >
                {d.id}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))' }}>
        <div className="card">
          <h3>CPU Utilization</h3>
          <MetricChart title="CPU %" dataPoints={metrics.cpu} color="#60a5fa" />
        </div>
        <div className="card">
          <h3>Memory Utilization</h3>
          <MetricChart title="Memory %" dataPoints={metrics.memory} color="#f472b6" />
        </div>
        <div className="card">
          <h3>Packet Loss</h3>
          <MetricChart title="Packet Loss %" dataPoints={metrics.packet_loss} color="#f97316" />
        </div>
      </div>

      <div style={{ marginTop: 16 }}>
        <AlertList alerts={alerts} />
      </div>
    </div>
  )
}
