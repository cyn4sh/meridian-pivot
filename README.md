# Meridian Pivot — Sync Service Prototype

Individual submission for Week 2 (The Meridian Pivot) of the PLP 1MILL Devs
Software Engineering Programme. Simulates a stock-sync service for Northstar
Retail Co., built solo using genuinely unfamiliar tools per the assignment
brief.

## Stack
- Django + Django REST Framework
- PostgreSQL
- python-dotenv for environment config

## Structure
- `journal.md` — live Learning & Blocker Journal, logged in real time
  during Days 1–2 solo recon
- `retry_backoff_prototype/` — retry/backoff mini-prototype (tested)
- (webhook verification prototype — coming next)

## How to run
1. `python -m venv .venv` and activate it
2. `pip install -r requirements.txt`
3. Set up `.env` with your local Postgres credentials
4. `python manage.py migrate`
5. `python manage.py runserver`