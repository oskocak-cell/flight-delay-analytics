# Original Pentaho project files

These are the recovered group-project sources, with connection credentials and machine-specific metadata removed for publication. Transformations, SQL calculations, report layout, and the original delay definition are retained. This is an **inspection-ready source archive**; the original desktop stack has not been executed as part of this portfolio preparation.

| File | Purpose |
|---|---|
| `transformations/DIM_TIME.ktr` | Loads `dim_date`; the original file name says TIME but this is the date dimension |
| `transformations/DIM_AIRPORT.ktr` | Airport lookup, surrogate keys, and dimension load |
| `transformations/DIM_AIRCRAFT.ktr` | Aircraft lookup, surrogate keys, and dimension load |
| `transformations/DIM_PILOT.ktr` | Pilot cleanup and insert/update load; filename normalized from `DIM_PİLOT.ktr` |
| `transformations/FACT_FLIGHT.ktr` | Schedule/execution join, dimension lookups, measures, and fact load |
| `reports/airport-delay-report.prpt` | Editable Pentaho airport-delay report |

For configuration, load order, and known original limitations, see [the native workflow guide](../docs/original-pentaho.md). The portable demonstration remains available through the [main README](../README.md).

Run `python3 scripts/validate_pentaho_sources.py` from the repository root to check XML, step connections, report archive integrity, and blank credential fields. GitHub runs this check automatically; it is not a Pentaho runtime test.
