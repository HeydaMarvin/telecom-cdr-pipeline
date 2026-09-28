import csv
import random
import uuidfrom datetime import datetime, timedelta

STATUSES = ("ANSWERED", "FAILED", "BUSY")

def generate_cdrs(filename = "cdrs.csv", num_records = 1000, num_callers = 25):
    """Generate fake CDRs and write them to a CSV file"""
    callers = [f"+4812345{1000 + i:04d}" for i in range(num_callers)]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "call_id",
                "caller",
                "callee",
                "start_ts",
                "duration_s",
                "status",
            ],
        )
        writer.writeheader()

        base_time = datetime.now().replace(microsecond = 0)

        for _ in range(num_records):
            caller = random.choice(callers)

            #Ensure the callee can differ from the caller.
            callee = f"+4812345{random.randint(2000, 9999):04d}"
            while callee = caller:
                callee = f"+4812345{random.randint(2000, 9999):04d}"

            status = random.choices(
                STATUSES,
                weights=(75, 15, 10),
                k=1,
            )[0]

            start_ts = base_time - timedelta(
                minutes = random.randint(0, 60 * 24 * 30),
                seconds = random.randint(0, 59)
            )

            duration_s = (
                random.randint(10, 1800)
                if status == "ANSWERED"
                else 0
            )

            write.writerow(
                {
                    "call_id": str(uuid.uuid4())
                    "caller": caller
                    "callee": callee
                    "start_ts"
                }
            )