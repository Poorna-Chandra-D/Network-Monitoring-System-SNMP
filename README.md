# Network Monitoring Stack

Python + Flask backend with Netmiko, PySNMP, Twilio alerts and a React + Vite + Chart.js frontend for real-time network health, bandwidth, and anomaly alerting.

**Status**: ✅ Complete with full documentation and test data included

---

## 🚀 Quick Start (5 minutes)

### Option 1: Run Everything
```bash
# Terminal 1: Backend
cd backend && source .venv/bin/activate && python -m flask run --port=3000

# Terminal 3: Frontend
cd frontend && npm run dev
```

Then open: **http://localhost:5173**

### Option 2: First Time Setup
```bash
# Backend setup
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m flask run --port=3000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

---

## ✨ Features

- ✅ **Real-time Dashboard**: Charts with CPU, Memory, Packet Loss metrics
- ✅ **Multi-device Support**: Monitor 2+ devices simultaneously  
- ✅ **Smart Alerting**: Auto-generated alerts based on thresholds
- ✅ **REST API**: 6 endpoints with authentication
- ✅ **Simulation Mode**: Test without real network devices
- ✅ **Data Persistence**: SQLite database with 358+ records
- ✅ **Live Polling**: Continuous data generation every 15 seconds
- ✅ **EST Timezone**: All times displayed in Eastern Time
- ✅ **Auto-refresh**: Dashboard updates every 10 seconds
- ✅ **Complete Docs**: 7 markdown guides included

---

## 🔌 API Endpoints

All endpoints require: `X-API-KEY: change-me` header

```bash
# Get devices
curl -H "X-API-KEY: change-me" http://localhost:3000/api/devices

# Get metrics
curl -H "X-API-KEY: change-me" \
  "http://localhost:3000/api/metrics/core-switch-1?metric=cpu&minutes=60"

# Get alerts
curl -H "X-API-KEY: change-me" http://localhost:3000/api/alerts

# Trigger polling
curl -X POST -H "X-API-KEY: change-me" http://localhost:3000/api/poll

# Health check
curl http://localhost:3000/health
```

See **COMMANDS.md** for complete API reference.

---

## 📊 System Architecture

```
Browser (http://localhost:5173)
    ↓ REST API (X-API-KEY)
Flask Backend (http://localhost:3000)
    ↓ SQL Queries
SQLite Database (monitor.db)
    ↓ Collectors
SNMP/Netmiko Clients
    ↓ Simulated Data
Continuous Generator (every 15 seconds)
```

See **ARCHITECTURE.md** for detailed system design.

---

## 💻 Technology Stack

### Backend
- **Python 3.10+**
- **Flask 3.0.2** - Web framework
- **SQLAlchemy 2.0** - ORM
- **SQLite** - Database
- **Netmiko 4.2** - Network automation
- **PySNMP 4.4** - SNMP protocol

### Frontend
- **React 18** - UI framework
- **Vite 5.4** - Build tool
- **Chart.js** - Charting
- **Axios** - HTTP client

---

## 📁 Project Structure

```
backend/
├── app.py                    # Flask REST API
├── config.py                 # Configuration
├── db.py                     # Database setup
├── monitoring/               # Polling logic
├── models/                   # Data models
├── generate_test_data.py     # Create test data
├── continuous_data_generator.py  # Live polling
├── .env                      # Configuration file
└── monitor.db               # SQLite database

frontend/
├── src/
│   ├── App.jsx              # Main component
│   ├── components/          # React components
│   ├── utils/               # Utilities
│   └── styles.css           # Styling
├── vite.config.js           # Vite config
└── package.json             # Dependencies

Documentation/
├── INDEX.md                 # Documentation index
├── INTERVIEW_GUIDE.md       # Interview prep 🎯
├── ARCHITECTURE.md          # System design
├── COMMANDS.md              # Commands reference
├── TESTING_GUIDE.md         # Testing procedures
├── PROJECT_SUMMARY.md       # What was built
└── QUICK_START.md           # Quick reference
```

---

## 🎯 Key Configuration

Edit **backend/.env**:

```env
API_KEY=change-me                # API authentication
SIMULATION_MODE=true             # Use mock data (true) or real devices (false)
CPU_THRESHOLD=80                 # Alert when CPU > 80%
PACKET_LOSS_THRESHOLD=5          # Alert when loss > 5%
DATABASE_URL=sqlite:///monitor.db  # Database location

# Device configuration (optional)
DEVICE1_HOST=192.0.2.10
DEVICE1_USER=admin
DEVICE1_PASS=password
DEVICE1_COMMUNITY=public
```

---

## 🧪 Generate Test Data

Create historical data:
```bash
cd backend && source .venv/bin/activate
python generate_test_data.py          # 24 hours of data
python generate_test_data.py --polls 48 --interval 30  # 2 days
```

---

## 🚀 Current System Status

```
✅ Backend:      Running on http://localhost:3000
✅ Frontend:     Running on http://localhost:5173
✅ Data Gen:     Polling every 15 seconds
✅ Database:     358+ metrics + 22 alerts
✅ Devices:      core-switch-1, core-switch-2 (simulated)
✅ Clock:        EST timezone
✅ Refresh:      Auto-refresh every 10 seconds
```

---

## 🎓 Interview Preparation

This project covers:
- ✅ System design (multi-tier architecture)
- ✅ REST API design
- ✅ Database design & queries
- ✅ React hooks & state management
- ✅ Flask backend development
- ✅ Real-time data handling
- ✅ Monitoring & alerting concepts
- ✅ Configuration management
- ✅ Authentication & security
- ✅ Time zone handling

---

## 📖 Learning Path

### 4 Hours
1. Explore backend/app.py
2. Explore frontend/src/App.jsx
3. Query the database
4. Study design patterns

---

## 🔧 Troubleshooting

**No data in dashboard?**
- Backend running: `curl http://localhost:3000/health`
- Data exists: `cd backend && python generate_test_data.py`
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+F5` (Windows)

**API key error?**
- Check .env file: `cat backend/.env | grep API_KEY`
- Use correct key: `curl -H "X-API-KEY: change-me" ...`

**Port already in use?**
- Kill process: `lsof -i :3000` then `kill -9 <PID>`
- Change port: Edit backend/app.py or frontend/vite.config.js

See **TESTING_GUIDE.md** for detailed troubleshooting.


---

## 📄 License

This project is open source and available for educational purposes.

