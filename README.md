# LogiSense - Logistics Solution Designer Agent (Starter) — OFI Solutions Limited

Quick-start:
1. Put the seven CSV files into the `data/` folder (orders.csv, delivery_performance.csv, routes_distance.csv, vehicle_fleet.csv, warehouse_inventory.csv, customer_feedback.csv, cost_breakdown.csv).
2. Create and activate a Python virtual environment.
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run services/streamlit_app/app/logisense_app.py
   ```
4. Or use docker-compose:
   ```
   docker-compose up --build
   ```


Agent API: The agent runs as a FastAPI service at /recommend. Set GEMINI_API_KEY in .env and run docker-compose up.
