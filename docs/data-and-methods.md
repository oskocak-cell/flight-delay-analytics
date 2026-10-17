# Data and calculation assumptions

## Source and minimization

The original folder contains five CSV tables with 250 rows each. They appear in an educational assignment and include repeated airport/terminal labels and generated-looking records, but their exact external provenance is not verified. They must not be represented as authoritative aviation records.

The public copy removes pilot names, birth dates, licence numbers, and airport phone numbers. `pilots.csv` retains only the surrogate source identifier needed for relational joins; no demographics or pilot-level performance ranking is published. Names of airlines and airports are retained to demonstrate aggregation, without claims about real-world performance.

The original models retain schema column definitions, but their embedded SQLite table data is emptied before publication. Direct personal fields shown in unused screenshots and the original Word report cover sheet are not republished.

## Grain, keys, and dimensions

The operational tables are loaded with primary and foreign key constraints. The analytical grain is **one row per `actual_flight_id`**. `flight_key` is a generated warehouse key; `actual_flight_id` is retained with a unique constraint. A schedule may have more than one execution in the conceptual design.

Date keys use `YYYYMMDD`. Airport, aircraft, and pilot warehouse keys are generated in sorted source-ID order, making the build deterministic. Day of week follows ISO numbering: Monday = 1, Sunday = 7. Airports play two roles in the fact table. No time, route, weather, or airline dimension is inferred; airline company is an aircraft attribute in the available design.

## Clock-time rollover

Source times are `HH:MM:SS`, all at whole-minute precision. They do not provide actual dates, arrival dates, time zones, or UTC offsets.

Let `A` and `S` be actual and scheduled clock minutes after midnight:

```text
signed delay = ((A - S + 720) mod 1440) - 720
scheduled duration = (scheduled arrival - scheduled departure) mod 1440
actual duration = scheduled duration + arrival delay - departure delay
is_delayed = departure delay > 15 OR arrival delay > 15
```

Examples: 00:10 actual vs 23:55 scheduled is +15 minutes; 23:55 actual vs 00:10 scheduled is −15 minutes. Exactly 15 minutes is not flagged by this reproduction's strict `> 15` threshold.

The delay calculation assumes a true difference in `[-720, 720)` minutes. Durations assume compatible clock frames and an overnight scheduled journey shorter than 24 hours. Without timezone information, computed durations are **inferred clock durations**, not verified elapsed flight times. A scheduled zero duration or an inferred non-positive actual duration is rejected. The original Pentaho delay-flag formula could not be fully verified from the retained files; the current threshold is an explicit choice for this reproduction.

## Scope of analysis

The sample has 250 executions spanning 2020–2025 and sparse coverage by airport and date. Averages include both early (negative) and late (positive) values. They measure net timing deviation rather than average lateness among delayed flights. Rankings at low counts are unstable. There is no weather information, cancellation status, ground-truth delay cause, or evidence supporting causal conclusions, forecasts, business savings, or real airline comparisons.

## Reproduction checks

Eleven automated tests cover midnight rollover, invalid times, delay thresholds, duration consistency, unique flight grain, foreign keys, aggregation counts, current sample totals, and deterministic exports. The GitHub workflow runs these tests and builds a fresh warehouse. The original MySQL/Pentaho desktop workflows are evidenced by models and screenshots rather than re-executed here.
