# Provenance and publication notes

## Original group work, Fall 2025

Course: Business Intelligence for Data Science, Tilburg University, Fall 2025 / Block 2.

Submitted topic: Monitoring airline operations based on flight schedules and delay analysis.

The submitted group report lists Barkın Kaya, Ozan Safak Kocak, Gorgud Shirinzade, Seçkin Sayin, and Tansel Karagoz. Their student identifiers are omitted. The final report credits the team jointly. Ozan’s CV describes his work on the star-schema design, Pentaho ETL, and SQL views/reporting within that group project, and reports an assignment grade of 10/10. The grade is supplied by Ozan; a transcript is not republished here. Shared assets are credited to the group.

Retained evidence:

- `models/flights_oltp.mwb` and `models/dw_airline.mwb`: supplied MySQL Workbench model definitions and diagrams, with embedded table rows removed and lock/backup entries omitted. Original schema fields are retained.
- `docs/images/original-oltp.webp` and `original-warehouse.webp`: supplied model screenshots, losslessly re-encoded for repository size.
- `docs/images/original-fact-transformation.jpg`: supplied Pentaho transformation screenshot.
- `docs/images/original-airport-view.jpg`: supplied MySQL view screenshot.
- `reports/original/airport-delay-report.pdf`: supplied report export, including the documented historical rollover issue.
- `data/sample/*.csv`: minimized versions of the supplied five source CSVs. The public copy excludes pilot names, dates of birth, licence numbers, and airport phone numbers.

## Added for public portfolio, October 2026

The README, case study, data/method notes, minimized-data preparation, SQLite schema/views, Python reproduction, regression tests, chart, and aggregate exports were prepared with AI assistance for this portfolio. They explain and extend the saved evidence; they are not presented as recovered original Pentaho source code. The saved model has four dimensions; brainstorming notes mentioning six dimensions were not treated as implemented work.

Private chats and planning notes were consulted only to help identify context. They are not included, and their suggested features are not used as proof of implementation. The original Word report, assignment template, team agreement, lecture recording and notes, and backups remain outside this public copy. The original local folder is unchanged.

A subsequently supplied folder from Barkın provided five original `.ktr` transformations, the editable `.prpt` report, and original MySQL view definitions. Public copies are in `pentaho/` and `sql/original/`; credentials and connection metadata are sanitized, and the pilot transformation filename is normalized. Transformation logic, step connections, report query, and report layout are retained. Additional raw warehouse and personal-field CSV exports were inspected for validation but not republished. The new folder confirmed both the original delay-flag definition and the midnight-duration issue. See `docs/original-pentaho.md` for setup and differences. There is no evidence here of a production deployment, a predictive model, or measured operational improvements.

## Rights

This repository is a credited portfolio presentation. The available course files do not establish an external data licence or grant a new licence over other contributors' material. No blanket licence is asserted. Contact the relevant authors before reusing original group assets or sample data beyond review of this portfolio.
