# Fuzzing corpus

Seed MAVLink v1 frames for `fuzzer/mavlink_fuzzer.py`. Each `*.bin` is a single
well-formed frame the fuzzer mutates.

| File | Message | Notes |
|------|---------|-------|
| `heartbeat.bin` | HEARTBEAT (#0) | smallest useful frame |
| `sys_status.bin` | SYS_STATUS (#1) | longer payload, exercises length handling |
| `param_request.bin` | PARAM_REQUEST_READ (#20) | string param id — classic off-by-one territory |

Add real frames captured from a flight stack here to improve coverage. Crashes
found during fuzzing should be minimized and added as regression seeds.
