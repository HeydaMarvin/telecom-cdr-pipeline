# CDR Generator & Analyzer

This is a simple Python data-engineering project that generates fake Call Detail Records and stores them in CSV format. At the end it calculates caller statistics.

## Features:

* Generates 1,000 fake CDRs with 25 distinct callers
* Writes data to "cdrs.csv"
* Operates with "ANSWERED", "FAILED", and "BUSY" statuses
* Calculates per caller:

  - Total answered duration
  - Failure rate
  - Call count
As a result it prints out the top 5 callers by answered duration.

### CDR Columns

"call_id, caller, callee, start_ts, duration_s, status"

### Run

```bash
python CDR.py
```
#### Sample output:

Top 5 callers by answered duration:
---------------------------------------------------------------------------
Caller             Answered Duration (s)    Failure Rate    Call Count
---------------------------------------------------------------------------
+48123451014                       48431          8.77%            57
+48123451007                       42938          8.89%            45
+48123451021                       37006          4.35%            46
+48123451020                       33031         10.64%            47
+48123451002                       31714         18.75%            48

No external dependencies are required - only Python standard library is used.

This project combines my current work experience as Care Engineer in a Telecom company with my future career pursuit.  

Data Engineering Concepts:

This project demonstrates synthetic data generation, CSV I/O, aggregation, derived metrics, sorting, and reproducible processing.

Note: "call_id" is generated with "uuid.uuid4()", so the CSV is not completely byte-for-byte reproducible. The generated call attributes and analysis results are deterministic.
