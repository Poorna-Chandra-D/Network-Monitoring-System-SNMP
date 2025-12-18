import { useEffect, useState } from 'react'
import { formatTimeEST } from '../utils/timezone'

export function Clock() {
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date())
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ 
      textAlign: 'right',
      fontSize: '0.9rem',
      color: 'rgba(255,255,255,0.7)'
    }}>
      <div style={{ fontWeight: '500', color: 'rgba(255,255,255,0.9)' }}>
        {formatTimeEST(time)}
      </div>
      <div style={{ fontSize: '0.85rem', marginTop: '4px' }}>
        Eastern Time
      </div>
    </div>
  )
}
