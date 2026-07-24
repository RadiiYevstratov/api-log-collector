# TESTING — auth-event-analyzer

## 1. Test data files

| File | Description |
|---|---|
| clean.json | |
| type_a.json | |
| type_b.json | |
| overlap.json | |
| unordered.json | |
| boundary.json | |
| mixed.json | |
| (error files below) | |

## 2. Functional tests

| ID | File | Args | Expected findings | Exit |
|---|---|---|---|---|
| F-01 | clean.json | ` --input testing-data/clean.json ` | 0 findings; events_processed=3; unique_ips=1 | 0 |
| F-02 | type_a.json | ` --input  testing-data/type_a.json` | 1 finding: type=A, ip=192.168.1.20, failed=6;  events_processed=6 | 1 |
| F-03 | type_b.json | `--input testing-data/type_b.json` | 1 finding: type=B, ip=192.168.1.20, failed=6, first_success_after=2026-07-24T09:09:30, users=[radii]; events_processed=7 | 1 |
| F-04 | overlap.json | `--input testing-data/overlap.json`  | 2 findings: type=B ip=203.0.113.45, failed=5, first_success_after=2026-07-24T10:12:00, users=[admin, root], events_processed=6; type=A, ip=198.51.100.7, failed=5, events_processed=5 | 1 |
| F-05 | unordered.json | `--input testing-data/unordered.json`  | 1 finding: type=B, ip=192.168.1.20, user=[radii], first_success_after=2026-07-24T09:09:30, events_processed=7| 1 |
| F-06 | boundry.json | ` --input testing-data/`  | 1 finding: type=A, ip=203.0.113.10, failed = 5, events_processed=9| 1 |
| F-07 | mixed.json | ` --input testing-data/mixed.json`  | 2 findings: type=A, ip=203.0.113.99, failed=5, events_processed=7; type=A, ip=198.51.100.22, users=[admin, test, guest], failed=6, events_processed=7| 1 |
| F-08 | | | | |

## 3. Error handling tests

| ID | File | Expected stderr message | Exit |
|---|---|---|---|
| E-01 | (nonexistent path) | | 2 |
| E-02 | | | 2 |
| E-03 | | | 2 |
| E-04 | | | 2 |
| E-05 | | | 2 |
| E-06 | | | 2 |
| E-07 | | | 2 |

## 4. Output format tests

| ID | Description | Expected |
|---|---|---|
| O-01 | | |
| O-02 | | |

## 5. Not covered

-   