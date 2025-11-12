// frontend/src/pages/HumanActivity.jsx
import React, { useContext, useEffect, useState, useRef } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import MapView from '../components/MapView'
import MetricCard from '../components/MetricCard'
import Heatmap from '../components/Heatmap'
import { LocationContext } from '../context/LocationContext'

const styles = {
  page: {
    fontFamily: 'Poppins, sans-serif',
    background: '#04121f',
    color: '#e6f7ff',
    minHeight: '100vh',
    padding: 24,
  },
  header: {
    fontFamily: 'Merriweather, serif',
    marginBottom: 12,
  },
  subtitle: {
    color: '#bfefff',
    marginBottom: 20,
  },
  container: {
    display: 'grid',
    gridTemplateColumns: '1fr 360px',
    gap: 20,
  },
  rightPanel: {
    background: 'rgba(255,255,255,0.02)',
    borderRadius: 14,
    padding: 16,
    backdropFilter: 'blur(6px)',
    boxShadow: '0 6px 30px rgba(0, 196, 255, 0.04)',
    border: '1px solid rgba(0,196,255,0.06)'
  },
  cardsGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr',
    gap: 12,
    marginBottom: 12,
  },
  aiBox: {
    marginTop: 12,
    fontSize: 14,
    color: '#dff7ff'
  },
  backBtn: {
    marginTop: 16,
    padding: '10px 14px',
    borderRadius: 12,
    background: 'linear-gradient(90deg,#00b4d8, #00c6ff)',
    border: 'none',
    color: '#04121f',
    fontWeight: 600,
    cursor: 'pointer',
    boxShadow: '0 6px 18px rgba(0,196,255,0.12)',
  }
}

export default function HumanActivity(){
  const { lat, lon } = useContext(LocationContext)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const timerRef = useRef(null)
  const navigate = useNavigate()

  const fetchData = async () => {
    if (lat == null || lon == null) return
    setLoading(true)
    setError(null)
    try{
      const res = await axios.get(`/api/activity?lat=${lat}&lon=${lon}`)
      setData(res.data)
    }catch(err){
      setError('Failed to fetch activity')
    }finally{
      setLoading(false)
    }
  }

  useEffect(()=>{
    fetchData()
    timerRef.current = setInterval(fetchData, 30000) // refresh every 30s
    return ()=> clearInterval(timerRef.current)
  }, [lat, lon])

  return (
    <div style={styles.page}>
      <h1 style={{...styles.header, fontSize: 28}}>Marine Human Activity Analysis</h1>
      <div style={styles.subtitle}>Live vessel traffic and human impact near your coordinates.</div>

      <div style={styles.container}>
        <div style={{minHeight: 520, borderRadius: 14, overflow: 'hidden'}}>
          <MapView data={data} loading={loading} center={[lat, lon]} />
        </div>

        <div style={styles.rightPanel}>
          <div style={styles.cardsGrid}>
            <MetricCard label="Total Vessels Detected" value={data?.total_vessels ?? 0} loading={loading} />
            <MetricCard label="Cargo Activity" value={data?.cargo ?? 0} loading={loading} />
            <MetricCard label="Tourism Activity" value={data?.passenger ?? 0} loading={loading} />
            <MetricCard label="Local Fishing Density" value={data?.fishing ?? 0} loading={loading} />
            <MetricCard label="Risk Score" value={data?.risk_score ?? 0} loading={loading} highlight />
          </div>

          <Heatmap score={data?.risk_score ?? 0} />

          <div style={styles.aiBox}>
            {loading && <div>Analysing live vessel traffic...</div>}
            {!loading && data && data.total_vessels === 0 && (
              <div>No significant human activity detected in this zone.</div>
            )}
            {!loading && data && data.total_vessels > 0 && (
              <div>{generateAISummary(data)}</div>
            )}
            {!loading && error && <div style={{color: '#ffb4b4'}}>{error}</div>}
          </div>

          <button style={styles.backBtn} onClick={()=>navigate(-1)}>← Back to Dashboard</button>
        </div>
      </div>
    </div>
  )
}

function generateAISummary(data){
  const { total_vessels, cargo, passenger, fishing, risk_score } = data
  if(total_vessels === 0) return 'No vessels detected.'
  let level = 'Moderate'
  if(risk_score > 75) level = 'High'
  else if(risk_score < 30) level = 'Low'
  return `${level} vessel density detected near the analysis area. Cargo: ${cargo}, Tourism: ${passenger}, Fishing: ${fishing}. Estimated impact level: ${risk_score}/100. Increased monitoring recommended.`
}