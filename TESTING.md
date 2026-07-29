# TESTING — auth-event-analyzer

## 1. Test data files

| File | Description |
|---|---|
| clean.json | One employee, one typo. No attack. |
| type_a.json | One IP, 6 failures within the window, no success. |
| type_b.json | One IP, 6 failures within the window, success afterwards. |
| overlap.json | 	IP 203.0.113.45: 5 failures + later success. IP 198.51.100.7: 5 failures, no success. |
| unordered.json | Same events as type_b.json, shuffled order in the file. |
| boundary.json | IP 203.0.113.10: exactly 5 failures in window. IP 203.0.113.11: exactly 4. |
| mixed.json | Three IPs: 203.0.113.99 (5 failures + success at 08:20), 198.51.100.22 (6 failures, 3 users, no success), 192.168.1.50 (success, 1 failure, success). |
| success_before.json | Success at 09:00, then 5 failures at 14:00–14:04. |
| scattered.json | 	5 failures spread over 5 days, plus one success. |
| (error files below) | |

## 2. Functional tests

| ID | File | Args | Expected findings | Exit |
|---|---|---|---|---|
| F-01 | clean.json | ` testing-data/clean.json ` | 0 findings; events_processed=3; unique_ips=1 | 0 |
| F-02 | type_a.json | `  testing-data/type_a.json` | 1 finding: type=A, ip=192.168.1.20, failed=6;  events_processed=6 | 1 |
| F-03 | type_b.json | `input testing-data/type_b.json` | 1 finding: type=B, ip=192.168.1.20, failed=6, first_success_after=2026-07-24T09:09:30, users=[radii]; events_processed=7 | 1 |
| F-04 | overlap.json | `input testing-data/overlap.json`  | 2 findings: type=B ip=203.0.113.45, failed=5, first_success_after=2026-07-24T10:12:00, users=[admin, root], events_processed=11; type=A, ip=198.51.100.7, failed=5, events_processed=5 | 1 |
| F-05 | unordered.json | `input testing-data/unordered.json`  | 1 finding: type=B, ip=192.168.1.20, user=[radii], first_success_after=2026-07-24T09:09:30, events_processed=7| 1 |
| F-06 | boundary.json | ` testing-data/boundary.json `  | 1 finding: type=A, ip=203.0.113.10, failed = 5, events_processed=9, 203.0.113.11 (4 failures) → no finding| 1 |
| F-07 | mixed.json | ` testing-data/mixed.json`  | 2 findings: type=A, ip=203.0.113.99, failed=5, events_processed=14; type=A, ip=198.51.100.22, users=[admin, test, guest], failed=6, events_processed=14; 192.168.1.50 → no finding| 1 |
| F-08 | success_before.json | ` testing-data/success_before.json ` | 1 finding: type=A, id=192.168.1.30, failed=5, events_processed=6| 1 |
| F-09 | scattered.json | ` testing-data/scattered.json ` |0 finding: events_processed=6 | 0 |

## 3. Error handling tests

| ID | File | Expected stderr message | Exit |
|---|---|---|---|
| E-01 | (nonexistent path) | ERROR: file not found: <path> | 2 |
| E-02 | empty.json | ERROR: invalid JSON: <detail> | 2 |
| E-03 | malformed.json | ERROR: invalid JSON: <detail> | 2 |
| E-04 | not_a_list.json | ERROR: input root must be a JSON array | 2 |
| E-05 | missing_key.json | ERROR: record 1: missing required key 'ip' | 2 |
| E-06 | element_not_dict.json | ERROR: record 1: expected object, got str | 2 |
| E-07 | unknown_event.json | ERROR: record 1: unknown event value 'password_change' | 2 |
| E-08 | bad_timestamp.json | ERROR: record 1: invalid timestamp '24/07/2026 09:01' | 2 |
| E-09 | no_permission.json | ERROR: permission denied: <path> | 2 |

## 4. Output format tests

| ID | Description | Expected |
|---|---|---|
| O-01 | --json output piped through python3 -m json.tool | return final result in json format |
| O-02 | Same input run with and without --json | Return result as string |

## 5. Not covered

-   