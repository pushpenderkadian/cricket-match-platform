# Cricket Live Data API

This project is a FastAPI-based backend that provides live cricket match data, including match listings, live scores, and real-time updates via WebSockets. It integrates with external APIs to fetch match details and stores data in MongoDB.

## Features
- Fetch upcoming cricket matches with pagination
- Retrieve live scorecards for specific matches
- WebSocket-based real-time match updates
- Automated schedulers to update match data periodically
- MongoDB integration for storing match-related data

## Project Structure
```
backend/
│── routes/
│   ├── matches.py    # Endpoint for fetching match list
│   ├── scorecards.py  # Endpoint for fetching live scorecards
│   ├── sockets.py    # WebSocket for real-time updates
│── database.py       # MongoDB connection and collections
│── models.py         # Pydantic models for data validation
│── scheduler.py     # Background jobs for fetching match data
│── scraper.py        # Functions to fetch data from external APIs
```

```
frontend/
│── static/
│   ├── index.js    # file for javascript required on homepage
│   ├── match_script.js  # file for javascript required on match details page
│── templates/
│   ├── index.html    # html file for homepage
│   ├── matches.html  # html file for match details
```

## Installation
### Prerequisites
- Python 3.8+
- MongoDB instance
- Environment variables (`.env` file):
  ```
  MONGO_URI=<your_mongo_connection_string>
  ```

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/cricket-match-platform.git
   cd cricket-match-platform
   cp .env.example .env   # then update mongodb uri
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn backend.main:app --host <host> --port <port> --reload
   ```
   OR
   ```bash
   python main.py
   ```


## API Endpoints
### Matches List
Fetch upcoming matches with pagination:
```http
GET /matches-list?page=1&page_size=10
```
**Response:**
```json
{
    "page": 1,
    "page_size": 10,
    "matches": [
        {
            "mf": "T6Y",
            "bf": "11U",
            "cc": 1,
            "date": "2/26/2025",
            "fi": "https://cricketvectors.akamaized.net/cFancode/119733.png",
            "fid": 119733,
            "fsr": "P",
            "ft": 4,
            "g": 1,
            "id": 37834,
            "ifs": "C",
            "mn": "14",
            "mt": 5,
            "o1": "9.5",
            "o2": "9.5",
            "result": "DCC Won by 4 wickets",
            "s1": "112/10",
            "s2": "113/6",
            "sed": 1742495400000,
            "sf": "European Cricket League 2025",
            "ssd": 1740335400000,
            "st": 15,
            "status": 2,
            "t": 1740592800000,
            "t1f": "Dreux",
            "t2f": "Darmstadt CC",
            "tt": 0,
            "vf": "EN",
            "w": "FL"
        }
    ]
}
```

### Live Scorecard
Retrieve the live scorecard for a match:
```http
GET /scorecard/{match_id}
```
**Response:**
```json
[
    {
        "a": [
            "Zubair Ashraf.36.12.0.0",
            "Spyridon Vasilakis.33.12.0.0",
            "Sinan Khan.47.12.0.1",
            "Sajid Afridi.28.12.0.1",
            "Shabbir Arslan.42.12.0.0"
        ],
        "b": [
            "George Hankins.46.18.6.3.31.91.2.Sajid Afridi.Aslam Mohammad/-/",
            "Ian Cockbain.39.13.3.4.30.91.2.Sinan Khan.Marios Vasilakis/-/",
            "Jalpesh Vijay.7.7.1.0/-",
            "Mohammad Irfan Jnr.88.22.4.11/-",
            "Adeel Malik/-",
            "Gavin Griffiths/-",
            "Marc Whitlock/-",
            "Paul Murray/-",
            "Harry Hankins/-",
            "Billy Gordon/-",
            "Lesbourne Edwards/-"
        ],
        "c": "122",
        "d": "189/2(60",
        "e": "2.1.6.0.0",
        "st": "15",
        "x": "Marc Whitlock/Paul Murray"
    },
    {
        "a": [
            "Mohammad Irfan Jnr.18.12.0.1",
            "Harry Hankins.27.12.0.2",
            "Lesbourne Edwards.31.12.0.0",
            "Adeel Malik.22.12.0.0",
            "Gavin Griffiths.17.6.0.0",
            "Billy Gordon.19.6.0.1"
        ],
        "b": [
            "Sajid Afridi.13.5.3.0.14.35.2.Mohammad Irfan Jnr.Paul Murray/49.29-269.53/",
            "Sinan Khan.62.25.2.8.41.106.2.Billy Gordon.Gavin Griffiths/30.94-276.84/",
            "Zubair Ashraf.24.17.3.1.51.119.2.Harry Hankins.George Hankins/-/",
            "Shabbir Arslan.15.12.1.1/-",
            "Aslam Mohammad.0.1.0.0.52.119.1.Harry Hankins/35.50-220.50/",
            "Alexis Souvlakis.3.4.0.0/18.00-145.95",
            "Spyridon Vasilakis/-",
            "Nick Katechis/-",
            "Marios Vasilakis/-",
            "Christos Mollinaris/-",
            "Anastasios Gialourakos/-"
        ],
        "c": "123",
        "d": "135/4(60",
        "e": "0.1.13.4.0",
        "st": "15",
        "x": "Aslam Mohammad/Nick Katechis"
    }
]
```

### WebSocket Live Updates
Receive real-time match updates:
```websocket
ws://localhost:8000/live-updates/{match_id}
```

## Background Tasks
- `fetch_match_list()`: Retrieves upcoming matches and stores them in MongoDB.
- `fetch_live_data()`: Fetches live scores and updates MongoDB every 5 seconds.

