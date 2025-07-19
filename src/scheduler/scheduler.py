import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

# Setup scheduler
scheduler = BackgroundScheduler()

def notify_user(schedule):
    print(f"[{datetime.now()}] Triggered: {schedule['name']} ({schedule['id']})")

def schedule_from_object(schedule):
    if not schedule.get("enabled", True):
        return

    job_id = schedule["id"]
    job_name = schedule["name"]

    if schedule["type"] == "fixed":
        anchor = schedule["anchor"]
        dt = datetime(
            year=anchor["year"],
            month=anchor["month"],
            day=anchor["dayOfMonth"],
            hour=int(anchor["time"].split(":")[0]),
            minute=int(anchor["time"].split(":")[1]),
        )
        scheduler.add_job(
            notify_user,
            trigger=DateTrigger(run_date=dt),
            id=job_id,
            name=job_name,
            args=[schedule]
        )

    elif schedule["type"] == "recurring":
        anchor = schedule["anchor"]
        days = anchor.get("daysOfWeek", [])
        days_cron = ",".join(day[:3].lower() for day in days) if days else "*"
        hour, minute = map(int, anchor["time"].split(":"))
        scheduler.add_job(
            notify_user,
            trigger=CronTrigger(day_of_week=days_cron, hour=hour, minute=minute),
            id=job_id,
            name=job_name,
            args=[schedule]
        )

def load_all_schedules():
    with open("schedules.json") as f:
        all_schedules = json.load(f)
        for sched in all_schedules:
            schedule_from_object(sched)

if __name__ == "__main__":
    load_all_schedules()
    scheduler.start()

    print("✅ Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        scheduler.shutdown()
