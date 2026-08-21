# Meridian Pivot — Sync Service Prototype & Solstice Events Check-In

Individual submission for Week 2 (The Meridian Pivot) of the PLP 1MILL Devs
Software Engineering Programme. Simulates a solo mini-prototype build using
genuinely unfamiliar tools, followed by a non-negotiable mid-sprint pivot
delivered by the client, per the assignment brief.

**Assigned tools (Days 1–2):** retry/backoff, webhook verification.

## Stack
- Django + Django REST Framework
- PostgreSQL
- python-dotenv for environment config
- (Django/Postgres scaffold retained for the original placeholder scenario;
  the Day 4 pivot solution itself is a standalone Python prototype — see
  below)

## Assignment 1 — Independent Learning & Blocker Journal
Built and tested in isolation, no outside help:
- `retry_backoff_prototype/` — retry/backoff mini-prototype, tested against
  both a failure path and an eventual-success path.
- `webhook_verification_prototype/` — HMAC-SHA256 webhook signature
  generation and verification, including a tampered-payload test proving
  invalid signatures are correctly rejected.
- `sync_service_prototype/` — an early integration exercise (placeholder
  Northstar Retail warehouse scenario) combining both tools before the real
  Day 4 pivot brief arrived.

  **Deprecated** - superseded by `solstice_pivot/` once the actual Solstice Events pivot scenario was released.

Full process, real terminal output, and blockers are documented in
`journal.md`, logged live as the work happened.

## Day 4 — The Meridian Pivot
**Client:** Solstice Events Co. — a multi-day tech conference.

**Original spec:** an attendee check-in kiosk calls a badge-printer vendor
synchronously via REST, waits for the print result, and shows "Checked In"
only on success.

**The pivot:** the vendor deprecated the synchronous print API. The service
now:
1. Publishes a print request to the vendor's **message queue** instead of
   calling it directly.
2. Waits for a **webhook callback** when the print job completes.
3. Shows a *pending* state until that webhook confirms.
4. Must protect against duplicate scans, and must handle webhook
   confirmations that **arrive out of order** relative to when attendees
   scanned.

### Solution — `solstice_pivot/`
| File | Purpose |
|---|---|
| `attendee_state_transitions.py` | `Attendee` model with explicit, guarded state transitions: `not_checked_in → pending → checked_in`, and `pending → failed`. Invalid transitions are rejected. |
| `attendee_registry.py` | Stores attendees, with lookup by `attendee_id` and by `print_job_id` — required since webhook confirmations can't be matched by scan order. |
| `check_in_service.py` | Handles a scan: rejects unknown attendees and duplicate scans, generates a `print_job_id`, transitions the attendee to `pending`. |
| `print_queue.py` | Simulated vendor message queue. Distinguishes retryable (`TemporaryQueueError`) from non-retryable (`PermanentQueueError`) failures. Includes `retry_with_backoff()`, reusing the exponential backoff pattern proven in Assignment 1. |
| `webhook_handler.py` | Verifies the callback's HMAC signature, looks up the attendee by `print_job_id`, and transitions them to `checked_in` — idempotently, so a repeated confirmation is recognized and not reapplied. |
| `pivot_demo.py` | End-to-end demo: two attendees scan, both print jobs fail transiently and recover via retry/backoff, webhook confirmations arrive out of order, a duplicate webhook is sent, and final state is printed. |

See `Scope_Delta_Analysis.md` for what changed between the original spec and
the pivoted solution, and `journal.md` for the full, real-time build log —
including bugs found and fixed along the way (e.g. a shared-queue-instance
bug that briefly masked one attendee's retry path during the demo).

## How to run

**Original Django scaffold (placeholder scenario):**
1. `python -m venv .venv` and activate it
2. `pip install -r requirements.txt`
3. Set up `.env` with your local Postgres credentials
4. `python manage.py migrate`
5. `python manage.py runserver`

**Day 4 pivot demo:**
```bash
python -m solstice_pivot.pivot_demo
```

## Project Structure
```
meridian-pivot/
├── journal.md
├── README.md
├── Scope_Delta_Analysis.md
├── webhook_verification_prototype/
├── retry_backoff_prototype/
├── sync_service_prototype/
└── solstice_pivot/
```