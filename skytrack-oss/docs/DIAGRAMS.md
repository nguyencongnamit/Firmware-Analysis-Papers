# Diagrams — SkyTrack OSS (ASCII, render-free)

All ecosystem diagrams in one place. ASCII by preference (portable, no renderer).

## 1. Ecosystem layers

```
  ┌──────────────────────────────────────────────────────────────────────┐
  │  COMMUNITY    docs site · examples gallery · tutorials · RFCs ·        │
  │               Discord/forum · firmware-papers awareness hub            │
  ├──────────────────────────────────────────────────────────────────────┤
  │  PILLARS      sn360-bridge   robot-brain   drone-rehost   scenario-fmt │
  │               (connect)      (intelligence)(security)     (tests)      │
  ├──────────────────────────────────────────────────────────────────────┤
  │  STANDARDS    scenario spec · telemetry/log · model API ·              │
  │               brain↔HAL contract · result/report schema               │
  ├──────────────────────────────────────────────────────────────────────┤
  │  CORE         skytrack-core: ENU frame · message types · units · utils │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ASSETS/DATA  datasets · benchmarks+leaderboard · model zoo ·          │
  │               scenario library · body packs                           │
  └──────────────────────────────────────────────────────────────────────┘
                    every layer ─────────────▶  sn360 (paid hub)
```

## 2. Platform — open rim, closed hub

```
            OPEN RIM  (Apache-2.0 · skytrack-oss)
  ┌─────────────────────────────────────────────────────────────┐
  │  scenario-format ─▶ robot-brain ─▶ sn360-bridge ─▶ engine I/O │
  │        drone-rehost ····· SITL firmware target ····▶         │
  └───────┬──────────────┬───────────────┬───────────────┬───────┘
          ▼              ▼               ▼               ▼
  ┌─────────────────────────────────────────────────────────────┐
  │              CLOSED HUB — sn360 (proprietary)                 │
  │  photoreal      hosted big-       hi-fidelity     scaled      │
  │  worlds         model brain       sensor/physics  cloud sim   │
  └─────────────────────────────────────────────────────────────┘
```

## 3. Dependency map (who builds on / feeds whom)

```
                          ┌───────────────────────────┐
                          │       skytrack-core       │ ◀── everything builds on this
                          └─────┬─────┬─────┬─────┬─────┘
              ┌─────────────────┘     │     │     └─────────────────┐
              ▼                       ▼     ▼                       ▼
     ┌─────────────────┐   ┌──────────────────┐   ┌──────────────┐   ┌──────────────┐
     │ scenario-format │   │   robot-brain    │   │ sn360-bridge │   │ drone-rehost │
     └────────┬────────┘   └─────────┬────────┘   └──────┬───────┘   └──────┬───────┘
              │ feeds missions/faults │ sends commands    │ MAVLink         │ SITL
              └──────────────────────▶  ◀────binds HAL────┘ ◀───────────────┘
```

## 4. The flywheel

```
   scenario-format ─more tests─▶ datasets/benchmarks ─train─▶ model zoo
        ▲                              │ leaderboard ranks        │
        │                              ▼                          │ better brains
        └────────── harder tests ◀──── robot-brain ◀──────────────┘
   drone-rehost ─bugs─▶ crash corpus ─hardens─▶ the whole stack
```

## 5. sn360-bridge (the AirSim successor)

```
   FLIGHT STACK                 common/  (ENU canonical)            GAME ENGINE
 ┌──────────────┐   MAVLink   ┌────────────────────────┐  local   ┌──────────────┐
 │ PX4/ArduPilot │◀──────────▶│ transport              │  socket  │ unity/ (C#)  │
 │ SITL          │            │  mavlink_bridge.py     │◀────────▶│  Publisher   │
 ├──────────────┤            │  ros2_bridge.py        │          │  Subscriber  │
 │ ROS 2 / DDS  │◀──────────▶│ msg mapping + clk sync │          ├──────────────┤
 │ micro-ROS    │   DDS      │ frame conv  NED ◀▶ ENU │          │ unreal/ (C++)│
 └──────────────┘            └────────────────────────┘          └──────┬───────┘
                                IBridgeTransport seam ─────────────────┘
                                (LogTransport → UDP / ROS 2)
```

## 6. robot-brain (one brain, many bodies)

```
                       ┌─────────────────────────────┐
                       │  Brain (abstract)           │
                       │   perceive → plan → act     │  └ ReferenceBrain
                       └──────────────┬──────────────┘    └ ObstacleAvoidBrain (example)
                          run() loop  │  drives
                       ┌──────────────▼──────────────┐
                       │  HAL (abstract)             │
                       │  read_sensors/send/reached  │
                       └──────────────┬──────────────┘
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                        ▼
        ┌───────────┐          ┌─────────────┐         ┌────────────────┐
        │  SimHAL   │          │  DroneHAL   │         │ GroundRobotHAL │
        │ pure sim  │          │ multirotor  │──binds─▶│ (Vector        │
        └───────────┘          └─────────────┘ bridge  │  testbed/demo) │
                                                        └────────────────┘
```

## 7. drone-rehost (firmware emulation + fuzzer)

```
   firmware.elf (Cortex-M)
        │ boots under
        ▼
  ┌───────────────┐  MMIO fault  ┌──────────────┐ dispatch ┌───────────────────┐
  │ qemu-system-  │─────────────▶│ MMIO hook    │─────────▶│ harness/rehost.py │
  │ arm (gdb)     │  (TODO)      │ gdb/Unicorn  │          │   MmioBus         │
  └───────────────┘              └──────────────┘          └─────────┬─────────┘
                                                  ┌──────────┬────────┼────────┐
                                                  ▼          ▼        ▼        │
                                              IMU 0x4000 GPS 0x5000 ESC 0x6000 │
                                              WHO 0x68   UBX/fix_ok PWM duty    │
                                                  ▲          ▲                 │
                                       set_truth/fix_ok ─ sim/scenario (oracle)┘
   fuzzer/mavlink_fuzzer.py ──MAVLink frames (corpus)──▶ firmware parser
   unmodeled MMIO → return 0 + log (P2IM style)
```

## 8. scenario-format (own the format)

```
  OBJECT MODEL                              AUTHOR → RUN PIPELINE
  Scenario                              scenario.json
   ├─ World                                 │
   │   └─ Environment (wind, gps)           ▼
   ├─ Agent[] (id, body)             ┌──────────────────┐ errors
   │   └─ MissionStep[] (action)     │ validate.py      │──────┐
   ├─ Fault[] (type, at_s)           │ Schema + lint    │      │
   └─ Criterion[] (type, radius)     └────────┬─────────┘  ┌───▼────┐
                                          valid│           │ author │
                                              ▼            └────────┘
                                     ┌──────────────────┐
                                     │ reference player │ (TODO) → drives sn360-bridge
                                     └────────┬─────────┘
                                              ▼  evaluate criteria → pass/fail → sn360
```

## 9. Build-your-own (extension seams)

```
        YOUR PRODUCT / RESEARCH
   ┌───────────────────────────────┐
   │ your Brain  │ your HAL/body    │  ← you write only these
   │ your sensor │ your scenario    │
   └──────┬──────┴────────┬─────────┘
          ▼ plugs into     ▼
   ┌─────────────────────────────────┐
   │ skytrack-oss interfaces + core   │  ← given, free, Apache-2.0
   └─────────────────────────────────┘
```

## 10. Funnel — every door leads to sn360

```
   ENTRY (free)                CEILING                        CONVERT
   sn360-bridge     ─▶ photoreal worlds, swarm scale ─┐
   robot-brain      ─▶ hosted big-model brain, fleet ─┤
   drone-rehost     ─▶ scaled fuzzing, hi-fi oracle   ─┼──▶ [ sn360 ]
   scenario-format  ─▶ 1000s runs + analytics         ─┤
   datasets/bench   ─▶ data generation at scale       ─┤
   SBOM/compliance  ─▶ procurement-grade reports      ─┘
   examples · tutorials · papers hub ──attract every audience──▶ enter a pillar
```
