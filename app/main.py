from fastapi import FastAPI, HTTPException
from app.database import engine, Base
from app.routers import incidents, user, volunteers
from app import models
from pathlib import Path
import csv
import time

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeTracker API")


app.include_router(incidents.router)
app.include_router(volunteers.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Welcome to SafeTracker API"}


@app.get("/send-messages")
def send_messages():
    """
    Read `users.csv` and `volunteers.csv` from the project root, find volunteers
    whose address matches each user's address, and send a WhatsApp message to
    each matched volunteer using `pywhatkit`.

    Notes for beginners:
    - CSVs are expected at the project root next to `requirements.txt`.
    - Phone numbers must include the country code, e.g. +15551234567.
    - `pywhatkit` will open a browser window for WhatsApp Web to send messages.
      You must be logged into WhatsApp Web in that browser for sending to work.
    """
    # Determine project root (two levels up from this file: app/ -> project root)
    base_dir = Path(__file__).resolve().parent.parent
    users_file = base_dir / "users.csv"
    volunteers_file = base_dir / "volunteers.csv"

    # Check that files exist and return a helpful error if not
    if not users_file.exists():
        raise HTTPException(status_code=404, detail=f"users.csv not found at {users_file}")
    if not volunteers_file.exists():
        raise HTTPException(status_code=404, detail=f"volunteers.csv not found at {volunteers_file}")

    # Helper: read a CSV into a list of dictionaries (one dict per row)
    def read_csv_to_dicts(path: Path):
        with path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    users = read_csv_to_dicts(users_file)
    volunteers = read_csv_to_dicts(volunteers_file)

    # Import pywhatkit here so the app can still start if the package is missing.
    try:
        import pywhatkit
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"pywhatkit import error: {e}")

    results = []

    # For each user, find volunteers with the same address (case-insensitive match)
    for user in users:
        user_name = user.get('name', '').strip()
        user_address = user.get('address', '').strip().lower()
        user_phone = user.get('phone', '').strip()

        matched = [v for v in volunteers if v.get('address', '').strip().lower() == user_address]

        if not matched:
            results.append({'user': user_name, 'matched_volunteers': 0})
            continue

        for vol in matched:
            vol_name = vol.get('name', '').strip()
            vol_phone = vol.get('phone', '').strip()

            # Compose a simple notification message for the volunteer
            message = (
                f"Hello {vol_name}, please assist {user_name} located at {user.get('address','')}. "
                f"You can contact them at {user_phone}."
            )

            try:
                # pywhatkit.sendwhatmsg_instantly attempts to send immediately via WhatsApp Web.
                # It will open a browser tab — make sure you're logged into WhatsApp Web.
                # The phone number must include the country code, for example: +11234567890
                pywhatkit.sendwhatmsg_instantly(vol_phone, message, wait_time=10, tab_close=True, close_time=3)
                # Small pause between messages so the browser can process each send
                time.sleep(2)
                results.append({'user': user_name, 'volunteer': vol_name, 'status': 'sent'})
            except Exception as e:
                results.append({'user': user_name, 'volunteer': vol_name, 'status': 'error', 'error': str(e)})

    return {"results": results}
