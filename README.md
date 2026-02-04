# ⚡ SpeedRank-API

A high-performance leaderboard API for gaming applications, built with Django REST Framework and Redis. Designed to handle hundreds of concurrent users with sub-second response times.

[![Django](https://img.shields.io/badge/Django-6.0.1-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![Redis](https://img.shields.io/badge/Redis-7.x-red.svg)](https://redis.io/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)

## 🎯 Overview

SpeedRank-API provides a blazing-fast leaderboard system optimized for real-time gaming scenarios. It uses Redis Sorted Sets for lightning-fast queries while maintaining SQLite persistence for data durability.

### Key Features

- **⚡ Ultra-Fast Queries**: Top 10 players and rank lookups in < 1ms using Redis
- **📊 Real-Time Leaderboards**: Handle 500+ concurrent users with 200+ req/s
- **🔄 Dual Persistence**: Redis for speed, SQLite for durability
- **✅ Input Validation**: Points range (0-1M), automatic player creation
- **📈 Load Tested**: Verified with Locust under production-like conditions
- **🔧 Management Commands**: Easy SQL-to-Redis synchronization

---

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│    Django REST Framework    │
│  ┌──────────────────────┐   │
│  │   API Endpoints      │   │
│  │  - POST /api/score/  │   │
│  │  - GET /api/top-10/  │   │
│  │  - GET /api/rank/    │   │
│  └──────────────────────┘   │
└─────┬────────────────┬──────┘
      │                │
      ▼                ▼
┌─────────┐      ┌──────────┐
│  Redis  │      │  SQLite  │
│ (Speed) │      │  (Persist)│
└─────────┘      └──────────┘
```

**Data Flow:**
1. **Reads** (top-players, my-rank): Redis only → O(log N) performance
2. **Writes** (submit-score): SQLite + Redis → Dual persistence
3. **Sync**: Management command populates Redis from SQLite

---

## 🚀 Performance Metrics

Tested with Locust at 500 concurrent users:

| Metric | Value | Target |
|--------|-------|--------|
| **Peak RPS** | 200-220 req/s | ✅ |
| **50th Percentile** | 200-1,000ms | ✅ |
| **95th Percentile** | 1-4 seconds | ✅ |
| **Failure Rate** | ~0% | ✅ |
| **Concurrent Users** | 500+ | ✅ |

### Performance Comparison: SQL vs Redis

| Operation | SQL (Before) | Redis (After) | Improvement |
|-----------|--------------|---------------|-------------|
| Top 10 Players | 5-10 seconds | **< 1ms** | 🚀 **5000x faster** |
| Get User Rank | 5-60 seconds | **< 1ms** | 🚀 **5000x faster** |
| Submit Score | 1-2 seconds | 1-4 seconds | ⚠️ DB bottleneck |

---

## 📋 API Endpoints

### 1. Submit Score
```http
POST /api/score/
Content-Type: application/json

{
  "username": "player123",
  "points": 95000
}
```

**Response:**
```json
{
  "message": "Score submitted"
}
```

**Validations:**
- Points: 0 - 1,000,000
- Username: auto-creates player if new
- Only keeps highest score per player in Redis

---

### 2. Get Top Players
```http
GET /api/top-players/
```

**Response:**
```json
[
  {
    "rank": 1,
    "username": "player123",
    "points": 95000
  },
  {
    "rank": 2,
    "username": "speedrunner",
    "points": 89500
  },
  ...
]
```

---

### 3. Get User Rank
```http
GET /api/my-rank/?username=player123
```

**Response:**
```json
{
  "username": "player123",
  "rank": 1,
  "points": 95000
}
```

**Error Response (404):**
```json
{
  "message": "Player not found in leaderboard."
}
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.12+
- Redis Server 7.x
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SpeedRank-API
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start Redis server**
   ```bash
   redis-server
   # Or use your system's service manager:
   sudo systemctl start redis
   ```

6. **Sync existing data to Redis (if any)**
   ```bash
   python manage.py sync_redis
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Submit a score
curl -X POST http://localhost:8000/api/score/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testplayer", "points": 50000}'

# Get top 10 players
curl http://localhost:8000/api/top-players/

# Check user rank
curl "http://localhost:8000/api/my-rank/?username=testplayer"
```

### Load Testing with Locust

1. **Install Locust** (already in requirements.txt)
   ```bash
   pip install locust
   ```

2. **Run load test**
   ```bash
   cd benchmarks
   locust
   ```

3. **Open browser**
   - Navigate to `http://localhost:8089`
   - Set number of users (e.g., 500)
   - Set spawn rate (e.g., 10 users/second)
   - Set host: `http://localhost:8000`
   - Start swarming

4. **Monitor metrics**
   - RPS (Requests Per Second)
   - Response time percentiles
   - Failure rates

