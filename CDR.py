import csv
import uuid
import random
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter


STATUSES = ("ANSWERED", "FAILED", "BUSY")

DIRTY_KINDS = (
    "null_caller",
    "negative_duration",
    "answered_zero",
    "bad_timestamp",
)

def generate_cdrs(
    filename="cdrs.csv",
    num_records=1_000,
    num_callers=25,
    seed=42,
    base_time=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    dirty_rate=0.0,
):
    """Generate deterministic CDRs and write them to a CSV file."""
    rng = random.Random(seed)
    dirty_rng = random.Random(seed + 1)
    injected = Counter()

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

        written = []

        for _ in range(num_records):
            caller = rng.choice(callers)
            callee = f"+4812345{rng.randint(2000, 9999):04d}"

            status = rng.choices(
                STATUSES,
                weights=(75, 15, 10),
                k=1,
            )[0]

            start_ts = base_time - timedelta(
                minutes=rng.randint(0, 60 * 24 * 30),
                seconds=rng.randint(0, 59),
            )

            duration_s = (
                rng.randint(10, 1800)
                if status == "ANSWERED"
                else 0
            )

            record = {
                "call_id": str(uuid.uuid4()),
                "caller": caller,
                "callee": callee,
                "start_ts": start_ts.isoformat(),
                "duration_s": duration_s,
                "status": status,
            }

            kind = None
            if dirty_rng.random() < dirty_rate:
                kind = dirty_rng.choice(DIRTY_KINDS)
                injected[kind] += 1
                if kind != "duplicate":
                    record = corrupt(record, kind)

            writer.writerow(record)
            written.append(record)

            if kind == "duplicate":
                writer.writerow(dirty_rng.choice(written))  # extra row, same call_id

    return injected

def analyze_cdrs(filename="cdrs.csv"):
    """Read CDRs and compute per-caller statistics."""
    stats = defaultdict(
        lambda: {
            "answered_duration": 0,
            "failed_calls": 0,
            "call_count": 0,
        }
    )

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            caller = row["caller"]
            status = row["status"]
            duration_s = int(row["duration_s"])

            stats[caller]["call_count"] += 1

            if status == "ANSWERED":
                stats[caller]["answered_duration"] += duration_s
            elif status == "FAILED":
                stats[caller]["failed_calls"] += 1

    # Add failure rate to each caller's results.
    for caller_stats in stats.values():
        caller_stats["failure_rate"] = (
            caller_stats["failed_calls"] / caller_stats["call_count"]
        )

    return dict(stats)


def print_top_callers(stats, top_n=5):
    """Print callers with the highest total answered duration."""
    top_callers = sorted(
        stats.items(),
        key=lambda item: item[1]["answered_duration"],
        reverse=True,
    )[:top_n]

    print(f"Top {top_n} callers by answered duration:")
    print("-" * 75)
    print(
        f"{'Caller':<18}"
        f"{'Answered Duration (s)':>22}"
        f"{'Failure Rate':>16}"
        f"{'Call Count':>14}"
    )
    print("-" * 75)

    for caller, data in top_callers:
        print(
            f"{caller:<18}"
            f"{data['answered_duration']:>22}"
            f"{data['failure_rate']:>15.2%}"
            f"{data['call_count']:>14}"
        )
def corrupt(record, kind):
    """Return a corrupted copy of a CDR record."""
    bad = dict(record)          # copy, don't mutate the original
    if kind == "null_caller":
        bad["caller"] = "NULL"
    elif kind == "negative_duration":
        bad["duration_s"] = -1
    elif kind == "answered_zero":
        bad["status"] = "ANSWERED"
        bad["duration_s"] = 0
    elif kind == "bad_timestamp":
        bad["start_ts"] = "not_a_timestamp"
    return bad

def main():
    filename = "cdrs.csv"

    injected = generate_cdrs(
        filename="cdrs_dirty.csv",
        dirty_rate=0.05,
        seed=42,
        base_time=datetime(
            2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        ),
    )
    stats = analyze_cdrs(filename)
    print_top_callers(stats)

    print("\nInjected corruptions:")
    for kind, count in injected.items():
        print(f"{kind}: {count}")

if __name__ == "__main__":
    main()