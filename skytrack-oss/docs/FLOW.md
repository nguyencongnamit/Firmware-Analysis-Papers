# Flow — how data moves through the ecosystem

End-to-end runtime flows, ASCII (no renderer). Per-project `docs/FLOW.md` files
have the detailed views.

## A. End-to-end scenario run (the happy path)

```
  scenario.json
      │ load (mission, faults, success_criteria)
      ▼
  ┌─────────────────┐     Goal[]      ┌──────────────┐
  │ scenario-format │ ───────────────▶│  robot-brain │
  │  validate+load  │                 │  run() loop  │
  └─────────────────┘                 └──────┬───────┘
                                             │  each tick:
        ┌────────────────────────────────────┘
        ▼
   read_sensors ──▶ perceive ──▶ plan ──▶ act ──▶ send_commands
        ▲                                              │
        │ Observation (ENU)                            │ Command (velocity/goto)
        │                                              ▼
   ┌──────────────┐   sensor frame   ┌──────────────────────────┐
   │ Unity/Unreal │ ◀───────────────│  sn360-bridge            │
   │ engine (or   │ ───────────────▶│  ENU ◀▶ NED/engine conv  │
   │ sn360 cloud) │   setpoint       │  MAVLink / ROS 2         │
   └──────────────┘                 └──────────────────────────┘
        │                                              ▲
        │ (optional firmware-in-the-loop)              │ MAVLink
        └──────────────▶ drone-rehost (SITL firmware) ─┘

   …loop until goals done…
      ▼
  evaluate success_criteria ──▶ pass/fail report ──▶ (scale + analytics → sn360)
```

## B. Brain control loop (one tick)

```
   ┌─────────── run(brain, hal, goals) ───────────┐
   │  while not hal.goal_reached(goal):            │
   │      obs   = hal.read_sensors()      (sensors)│
   │      state = brain.perceive(obs)     (fuse)   │
   │      plan  = brain.plan(state, goal) (decide) │
   │      cmds  = brain.act(plan)         (lower)  │
   │      hal.send_commands(cmds)         (actuate)│
   └───────────────────────────────────────────────┘
      goto branch:           gps_ok? ──no──▶ localization_ok=False
                                │ yes               │ (fly on inertial)
                                ▼                   ▼
                       steer toward target at min(speed, distance)
```

## C. Scenario validation

```
   scenario.json ──▶ load JSON ──▶ JSON Schema (draft 2020-12) ──pass─▶ cross-field lint
        │                              │ fail                              │ warn
        ▼                              ▼                                   ▼
     author  ◀──────────────────── error report ◀───────────── unknown-agent refs, etc.
                                                                          │ ok
                                                                          ▼
                                                                   ready to run
```

## D. Rehosting: servicing an MMIO fault

```
   firmware reads 0x4000_4000+0x75 (IMU WHO_AM_I)
        │ traps in QEMU
        ▼
   MMIO hook ──▶ MmioBus.read(addr) ──▶ find owner peripheral
                                            │ IMU.handles(addr)? yes
                                            ▼
                                     IMU.read(0x75) = 0x68
        ┌───────────────────────────────────┘
        ▼
   value 0x68 returned to firmware ──▶ firmware proceeds (sees a real IMU)

   unmodeled addr ──▶ no owner ──▶ return 0 + log (promote later)
```

## E. Fuzz loop

```
   corpus seed ──▶ mutate (bitflip/insert/delete) ──▶ feed target parser
        ▲                                                    │
        │                                          crash? ──no──▶ next iter
        │                                                    │ yes
        └──────── add minimized regression seed ◀─── triage ─┘
```

## F. The flywheel (why flows compound)

```
   more scenarios ──▶ more runs ──▶ more data ──▶ better brains ──▶ harder scenarios
        ▲                                                                   │
        └───────────────────────────────────────────────────────────────────┘
   rehost crashes ──▶ harden firmware/parsers ──▶ feeds back into every run
```
