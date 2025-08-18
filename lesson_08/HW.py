import asyncio
from datetime import datetime
from statistics import mean
from random import randint, choice

students = {
    1: {"name": "Alice", "marks": []},
    2: {"name": "Bob", "marks": []},
}

def add_mark(student_id, mark):
    students[student_id]["marks"].append({
        "value": mark,
        "creation_date": datetime.now().date()
    })

async def auto_add_marks():
    while True:
        sid = choice(list(students.keys()))
        add_mark(sid, randint(1, 5))
        print(f"\n[AUTO] Added random mark to {students[sid]['name']}")
        await asyncio.sleep(7)

async def send_daily_average():
    while True:
        today = datetime.now().date()
        all_marks_today = [
            m["value"]
            for s in students.values()
            for m in s["marks"]
            if m["creation_date"] == today
        ]
        if all_marks_today:
            avg = mean(all_marks_today)
            print(f"\n[EMAIL] Daily average for {today}: {avg:.2f}")
        await asyncio.sleep(5)

async def send_monthly_students():
    while True:
        total_students = len(students)
        print(f"\n[EMAIL] Monthly students count: {total_students}")
        await asyncio.sleep(10)

async def user_input():
    loop = asyncio.get_event_loop()
    while True:
        cmd = await loop.run_in_executor(None, input, "Command (1=show, 2=add mark): ")
        if cmd == "1":
            for sid, s in students.items():
                print(f"{sid}: {s['name']}, Marks: {[m['value'] for m in s['marks']]}")
        elif cmd == "2":
            sid = choice(list(students.keys()))
            add_mark(sid, randint(1, 5))
            print(f"\n[MANUAL] Added mark to {students[sid]['name']}")

async def main():
    asyncio.create_task(auto_add_marks())
    asyncio.create_task(send_daily_average())
    asyncio.create_task(send_monthly_students())
    await user_input()

asyncio.run(main())
