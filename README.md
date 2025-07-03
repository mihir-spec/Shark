# Shark HQ – KPI Dashboard
A Streamlit application that tracks sales, inventory, marketing ROAS and operations for **Shark**, the Downtown-Dubai premium sportswear brand.

## Quick start
```bash
# clone & enter repo
$ git clone https://github.com/<you>/shark_dashboard.git
$ cd shark_dashboard

# install deps
$ pip install -r requirements.txt

# run locally
$ streamlit run app.py
```

If you don’t have a database yet the app will fall back to the sample CSVs under `data/` so you can see every page live.

## Deploy to Streamlit Cloud
1. Push this repo to GitHub.
2. Log in to **streamlit.io/cloud**, click *New app*, choose repo/branch, set **app.py** as the entry‑point and Deploy.
3. Add any secrets (e.g. `DB_URI`) in *Settings → Secrets*.

© 2025 Shark Sportswear Trading LLC.  Built with 🦈 + Streamlit.
