#CDR Generator & Analyzer

This is a simple Python data-engineering project that generates fake Call Detail Records and stores them in CSV format. At the end it calculates caller statistics.

#Features:

* Generates 1,000 fake CDRs with 25 distinct callers
* Writes data to "cdrs.csv"
* Operates with "ANSWERED", "FAILED", and "BUSY" statuses
* Calculates per caller:

  - Total answered duration
  - Failure rate
  - Call count
As a result it prints out the top 5 callers by answered duration.

#CDR Columns

"call_id, caller, callee, start_ts, duration_s, status"

#Run

```bash
python cdr_generator.py
```

No external dependencies are required - only Python standard library is used.

Data Engineering Concepts:

This project demonstrates synthetic data generation, CSV I/O, aggregation, derived metrics, sorting, and reproducible processing.

> Note: "call_id" is generated with "uuid.uuid4()", so the CSV is not completely byte-for-byte reproducible. The generated call attributes and analysis results are deterministic.
******
