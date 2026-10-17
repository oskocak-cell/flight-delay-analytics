# Original MySQL and Pentaho workflow

The recovered sources support direct inspection of the original ETL and report, in addition to the already published screenshots and PDF. The files retain the submitted business logic; the corrected Python/SQLite demonstration remains a separate implementation.

## Open and configure locally

1. Use compatible installations of MySQL, MySQL Workbench, Pentaho Data Integration (Spoon), and Pentaho Report Designer. Configure a compatible MySQL JDBC driver in the Pentaho tools as needed. The exact original tool versions have not been verified.
2. Open `models/flights_oltp.mwb` and `models/dw_airline.mwb` in Workbench. Review and forward-engineer them to local `flights` and `dw_airline` schemas. The model archives contain schema definitions, not stored rows.
3. Supply full-schema input data in your local `flights` database. The public `data/sample/` files are minimized for the portable SQLite workflow: they omit names, licence numbers, birth dates, and phone fields, so they are **not a direct full-schema import for these original transformations**. Use appropriately authorized local data or clearly synthetic fixtures for those columns. The friend's raw personal-field CSVs are not republished.
4. In each `.ktr`, configure `mysql_oltp` for `flights` and `mysql_dw` for `dw_airline`. The public files use `localhost:3306` and blank usernames/passwords. Supply your own local credentials in Spoon and keep them out of Git.
5. Load dimensions first: `DIM_TIME.ktr` (which populates **dim_date**), `DIM_AIRPORT.ktr`, `DIM_AIRCRAFT.ktr`, and `DIM_PILOT.ktr`. Then load `FACT_FLIGHT.ktr`.
6. Inspect and execute `sql/original/mysql_views.sql` against MySQL. The original file includes both view creation and example SELECT statements. On repeat runs, manage existing views deliberately; it is preserved as supplied rather than changed to silently replace them.
7. Open `pentaho/reports/airport-delay-report.prpt` in Report Designer and set its JDBC connection to your local `dw_airline` schema. Its public JDBC endpoint is `jdbc:mysql://localhost:3306/dw_airline`, with credentials removed. The report query can also be read in `sql/original/airport_report_query.sql`.

This is a source/configuration guide, not a claim that the archived native workflows execute without changes on a fresh installation. In particular, address the original issues below before relying on their outputs. Use a fresh or deliberately reset warehouse: key sequences and dimension loads are not presented as an incremental loading strategy.

## Verified differences from the portable reproduction

| Topic | Original Pentaho / exported warehouse | Portable reproduction |
|---|---|---|
| Database | MySQL `flights` and `dw_airline` | Local SQLite database |
| Date key | Generated sequence in `DIM_TIME.ktr` | Deterministic `YYYYMMDD` |
| Pilot fields | Names, licence, birth date in native schema | Source ID only |
| Fact identifier | Flight key and schedule ID | Also retains unique actual execution ID |
| Delay flag | `arrival_delay_min > 0` | `departure_delay_min > 15 OR arrival_delay_min > 15` |
| Delay arithmetic | Same scheduled date attached to both clock values | Nearest signed clock difference, with documented assumptions |
| Durations | Direct same-date timestamp differences | Inferred duration consistent with normalized delays |

The original `.ktr` formula is `(arrival_delay_min != null && arrival_delay_min.intValue() > 0) ? 1 : 0`. The recovered fact CSV agrees with that formula. Both versions flag 196 of 250 flights, but **66 flight assignments differ**; identical headline counts do not imply equivalent definitions.

## Original quality issues retained for transparency

- The original fact query attaches the scheduled date to both arrival and departure times. The recovered warehouse export contains **35 negative scheduled durations**, **40 negative actual durations**, and arrival delays as low as **−1,430 minutes**. These are consistent with the midnight arithmetic issue already visible in the original PDF. The public archive preserves that code so its history is not confused with the later fix.
- In `DIM_PILOT.ktr`, the `first_name` target is mapped from the `last_name` input. Review this mapping before using that transformation with local data.
- Original airport-view SQL groups by airport name; the reproduction groups by airport ID, name, and city. The original report query separately groups by ID/name/city/country and filters US country labels. Comparisons should account for the query and grouping used.

The original sources are now available to inspect. Runtime validation performed here covers the portable workflow and source sanitization/structure; it does not replace testing the original tools in a configured MySQL/Pentaho environment.
