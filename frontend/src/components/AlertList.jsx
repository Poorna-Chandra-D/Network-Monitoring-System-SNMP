import { formatTimeEST } from '../utils/timezone'

export function AlertList({ alerts }) {
  if (!alerts?.length) {
    return <div className="card">No alerts yet 🎉</div>
  }
  return (
    <div className="card">
      <div className="header">
        <h3>Recent Alerts</h3>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Device</th>
            <th>Metric</th>
            <th>Value</th>
            <th>Severity</th>
            <th>Time (EST)</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((a) => (
            <tr key={a.id}>
              <td>{a.device_id}</td>
              <td>{a.metric_type}</td>
              <td>{a.value?.toFixed(2)}</td>
              <td>
                <span className={`badge ${a.severity === 'high' ? 'high' : 'info'}`}>{a.severity}</span>
              </td>
              <td>{formatTimeEST(a.timestamp)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
