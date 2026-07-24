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
| F-03 | | | | |
| F-04 | | | | |
| F-05 | | | | |
| F-06 | | | | |
| F-07 | | | | |
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