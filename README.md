# ✈️ SkySearch — Flight Search Interface

Portfolio-ready Streamlit flight search dashboard with realistic generated demo inventory.

## Features
- One-way / round-trip search interface
- Origin, destination, date, passengers and cabin controls
- Airline, price, stops, refundable and departure-time filters
- Cheapest / fastest / departure sorting
- Detailed itinerary and fare information
- Seat availability, baggage, aircraft and meal information
- CSV and JSON export
- Polished responsive dashboard UI
- No API key required

## Run on Windows
```powershell
cd "Flight Search Interface"
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local Streamlit URL, normally `http://localhost:8501`.

## Important
Flight data, fares and availability are simulated demo data. This project does not perform real bookings.
