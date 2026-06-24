# STRATEGY — drone-rehost

## Positioning

`drone-rehost` is the **credibility flagship** of [skytrack-oss](../README.md). It
is, as far as we know, the **only drone-specific firmware rehoster**: the academic
rehosting literature (HALucinator, P2IM, FirmAE, Avatar, para-rehosting, FIRM-AFL,
IoTFuzzer) is mature but unpackaged for flight firmware. This repo makes that
research **executable** and ties it directly to the curated
[Firmware-Analysis-Papers](../../README.md) list — research depth you can run.

It is a **loud, niche** play (per [OSS-STRATEGY](../OSS-STRATEGY.md): medium
painpoint, medium-but-vocal interest, uniquely ours). Its job is not mass adoption;
it is to establish firmware-security credibility for the whole SkyTrack platform and
funnel serious users to **sn360**.

## "Open rim, closed hub" — the split

Open the parts developers touch daily (the harness and fuzzer); keep the
proprietary value (scale, fidelity, curated data) in sn360.

| Open (this repo, Apache-2.0) | sn360 (proprietary, the hub) |
|------------------------------|------------------------------|
| Rehosting harness (`MmioBus`, QEMU bring-up scaffold) | Managed **continuous fuzzing at scale** |
| Peripheral models (IMU / GPS / ESC) + the `Peripheral` interface | **High-fidelity sensor / physics oracle** |
| MAVLink mutation fuzzer + seed corpus | **Curated vulnerability datasets / reports** |
| Bring-up docs, P2IM-style unmodeled-MMIO workflow | Fleet-scale orchestration, dashboards, triage automation |
| Second-target (ground-robot) bring-up recipe | Cross-target campaign management |

Rule of thumb: ship the tools that earn trust and citations; sell the scale and the
fidelity. Every entry point ends with a "scale this up -> **sn360**" CTA.

## Licensing

**Apache-2.0** (`LICENSE` in this folder), consistent with the rest of skytrack-oss:
permissive for maximum adoption, with a patent grant. The folder is a splittable
mini-repo with its own LICENSE so it stays correct after a `git subtree split` into
a standalone public repo.

## Go-to-market

- **Security community first:** this is where the audience lives. Publish the harness
  and fuzzer, engage on firmware-security forums and embedded-CTF circles.
- **Conference talks & write-ups:** demoing drone-firmware rehosting + a MAVLink
  fuzzer is a strong talk; tie each one back to the paper list for legitimacy.
- **Citations & the paper repo:** the parent [Firmware-Analysis-Papers](../../README.md)
  is an SEO/credibility magnet; `drone-rehost` is its executable companion.
  Encourage citation of the harness in follow-on research.
- **Generality demo:** bringing up a **ground-robot** firmware as a second target is
  a concrete "this toolchain is general" proof point for talks and posts.
- **Funnel:** readers who need scaled/continuous fuzzing, a hi-fi oracle, or curated
  findings convert to **sn360**.

## Success metrics

- GitHub stars / forks and inbound issues from the **security** community
  (quality of audience over raw volume).
- Citations / references to the harness in firmware-analysis research and talks.
- Conference talk acceptances and write-ups featuring drone-rehost.
- Number of **firmware targets brought up** (drone images + the ground-robot second
  target) — proof of generality.
- **Conversions to sn360** attributable to drone-rehost (the real bottom line).

## Guardrails

- Keep proprietary value (hi-fi oracle, scaled fuzzing infra, curated datasets) out
  of this repo.
- The ground robot is a **second firmware target**, not a second product — only
  invest in it where it strengthens the shared firmware toolchain.
- Drone (SkyTrack) remains the product focus.
