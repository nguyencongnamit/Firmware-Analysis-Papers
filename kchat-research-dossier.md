# KChat / UNEY — Research Dossier

> Everything gathered for the blog post. Sources are linked inline and listed at the bottom.
> Research date: 2 August 2026. Note: `kchat.com`, `uney.com`, the app stores, and the
> press-release hosts were unreachable from the research environment (blocked by egress
> policy), so the details below come from search-engine snippets and secondary coverage.
> Anything I could not independently confirm on the open web is flagged **[verify]**.

---

## 0. First, clear up the name collision

There are **three unrelated things** called "kChat." Don't let them bleed into the blog.

| Product | Who's behind it | What it is |
|---|---|---|
| **KChat** (`kchat.com`, `k-chat.org`) | **UNEY / Uney GmbH** (Dubai + Germany) | The one we're writing about — a secure, private community messenger. |
| **Infomaniak kChat** | Infomaniak (Switzerland) | A team-collaboration tool inside kSuite, built on Mattermost, with "sovereign AI." Enterprise/Slack-style. Different company entirely. |
| **kChat — Safe Chat for Kids** | Knesis | A kids' messaging app with parental controls. Unrelated. |

Our subject is **UNEY's KChat**. The MLS / open-source-protocol angle belongs to the wider
secure-messaging world that KChat positions itself within.

---

## 1. The app — KChat by UNEY

**Tagline / promise:** "Secure and private messaging by default." "Where communities come to life."
Communications with family, friends and communities stay between you and the recipient — *no one
else can read them, including the company.* They state plainly that they **don't monetize your
information in any way**.

**Store identities**
- iOS: *KChat: Secure Talk & Community* — developer **Uney GmbH** (App Store id 6746121354)
- Android: `com.kchat.app` — *KChat: Secure Talk & Community*, by Uney GmbH
- (An older/parallel Android package `com.itc.kchat` also exists.)
- Web presence: `kchat.com` (marketing + privacy policy + terms), `k-chat.org` (consumer-privacy framing)

**Core features (from store listings and coverage)**
- **End-to-end encrypted** 1:1 and group messages
- **Secret chats** and **self-destructing / auto-delete messages** (after read or after a timer)
- **No phone number and no personal info required** to sign up
- **Groups up to 2,000 members**
- **Threaded conversations, sub-groups, and announcements** to keep big rooms organized
- **Communities** ("Create Community") and a newer **"Gathering"** feature inside chats
- **KChat Official Account** for admins to broadcast announcements to all users
- **Multi-device**: log in on several devices at once, messages sync across all
- Send **photos, videos, and documents of any format**; contact sync; online-status; tuned push notifications

**Security framing (from `k-chat.org`)**
- "Military-grade **256-bit AES** encryption," encrypted on-device, decryptable only by the recipient
- Claim that **messages are never stored on servers**
- **Anonymization** to mask the user's digital footprint
- Claim: **KChat cannot access your messages even if requested by authorities**
- **[verify]** These are marketing claims; the exact protocol (Signal-style vs. MLS) isn't spelled out in public snippets.

---

## 2. The business — UNEY

- **Company:** UNEY, legal entity **Uney GmbH** (German GmbH). Marketing/press positions the brand
  out of **Dubai, UAE**. So: German entity + Dubai operations.
- **Mission (paraphrased from press):** make secure communication "safer, simpler, and more
  reliable" for both businesses and everyday users — security **without giving up usability**, and
  solutions that "work in real-world scenarios."
- **Product family:**
  - **KChat** — the secure messenger / community platform (our focus)
  - **AutoSec** — an "all-in-one security app" that safeguards data and privacy (device-level security)
- **Leadership (named in press coverage) [verify names/titles]:**
  - **Tamas Zumpf** — Chief Technology Officer
  - **Ruben Tran** — Chief Operating Officer
  - **Chih-Heng Kwan** — Head of Marketing (Dubai)
- **AI direction (from the "AI Innovations" release):**
  - **Adaptive Encryption** + **AI-powered threat intelligence** that "continuously learns from
    user behavior and communication patterns" for real-time protection
  - Positioned to **scale with organizations** as they grow

**Press timeline (three PR Newswire releases, ~late 2024 → early 2025)**
1. *"UNEY Is Building the Future of Secure Communication — And It's Changing the Game"*
2. *"Reinventing Communication: Security Without Compromise"*
3. *"UNEY's AI Innovations for the Next Generation of Communication"*

---

## 3. The MLS angle — the open-source protocol story

This is the *technology-and-values* backbone of the blog. Even where KChat's own MLS
implementation isn't publicly documented **[verify]**, MLS is the movement KChat's story lives inside.

**What MLS is**
- **Messaging Layer Security (MLS)** — an open IETF standard, **RFC 9420** (published **2023**),
  with the architecture in **RFC 9750**.
- Purpose-built for **end-to-end encrypted group messaging** — not just 1:1. Designed to be
  efficient and secure for groups from **two to tens of thousands** of members.
- Delivers the same strong guarantees people associate with the Signal Protocol —
  **forward secrecy** (a stolen key can't unlock past messages) and **post-compromise security**
  (the group heals after a compromise) — but does it **efficiently at group scale**, where older
  approaches fell over.
- Handles the messy realities: members **joining and leaving**, people who are **offline**,
  and users on **multiple devices**.

**Why it matters / adoption**
- First **cross-industry, standardized** secure group-messaging protocol — so different apps can
  build on the same audited foundation instead of each rolling their own crypto.
- Backed publicly by the IETF; **Google** committed to MLS for Android Messages; broad private-sector
  interest since standardization.

**The open-source implementations (the "open source" in the request)**
- **OpenMLS** — a pure-**Rust** implementation of RFC 9420 (`github.com/openmls/openmls`,
  site `openmls.tech`). Pluggable crypto backends (RustCrypto / Evercrypt).
- **AWS `mls-rs`** — AWS Labs' Rust implementation of RFC 9420 (`github.com/awslabs/mls-rs`).
- **Cisco `mlspp`** — C++ implementation (`github.com/cisco/mlspp`).
- **Molasses** (Trail of Bits) — early Rust implementation.
- **Post-quantum:** OpenMLS has merged **X-Wing** (hybrid ECDH + ML-KEM) support — ciphersuite
  `MLS_256_XWING_CHACHA20POLY1305_SHA256_Ed25519`; there's an active IETF draft for ML-KEM/hybrid
  suites in MLS. Good "future-proofing" material for the blog.

**How to frame it honestly in the blog**
- Safe framing: "KChat is part of a bigger shift toward open, standardized end-to-end encryption —
  the world MLS (RFC 9420) created." Then explain MLS in human terms.
- If we want to say "KChat *uses* MLS," **confirm on kchat.com's own security/whitepaper page first
  [verify]** — the open web snippets I could reach mention AES-256 and E2EE generally, not MLS by name.

---

## 4. Emotional through-lines for a *human* blog (angles, not filler)

- **The quiet violation of being read.** Everyone has felt the ad that follows a private
  conversation. KChat's "not even we can read it, and we don't sell you" is an answer to that dread.
- **No phone number = you don't have to hand over your identity to be reachable.** Small thing,
  huge feeling of relief.
- **Group chats are where real life happens** — family threads, community organizing, friend groups.
  MLS is literally the tech that makes *group* privacy real, not just 1:1. Tie the human need to the protocol.
- **Open standards as trust.** You shouldn't have to *believe* a company's promise — open, audited,
  standardized crypto means you don't have to take their word for it. This is the moral heart.
- **Forward secrecy / post-compromise security, told as human stories:** "even if someone breaks in
  tomorrow, they can't read what you said last year," and "and after we lock the door again, the room
  is safe once more."
- **Small team, big idea** (UNEY out of Dubai/Germany) taking on the giants — underdog warmth.
- **Post-quantum** = "we're not just protecting you today, we're protecting the you of ten years from now."

---

## Sources
- KChat homepage — https://kchat.com/
- KChat (consumer security framing) — https://www.k-chat.org/
- KChat privacy policy — https://kchat.com/privacy-policy
- KChat iOS — https://apps.apple.com/us/app/kchat-secure-community-chat/id6746121354
- KChat Android — https://play.google.com/store/apps/details?id=com.kchat.app
- UNEY press: "Building the Future of Secure Communication" — https://www.prnewswire.com/news-releases/uney-is-building-the-future-of-secure-communicationand-its-changing-the-game-302339284.html
- UNEY press: "Reinventing Communication: Security Without Compromise" — https://www.prnewswire.com/news-releases/reinventing-communication-security-without-compromise-302359635.html
- UNEY press: "AI Innovations for the Next Generation of Communication" — https://www.prnewswire.com/news-releases/uneys-ai-innovations-for-the-next-generation-of-communication-302372338.html
- UNEY coverage — https://channeldrive.in/software-solutions/how-uney-is-reimagining-secure-communications/
- UNEY products — https://uney.com/products.html
- MLS / RFC 9420 — https://datatracker.ietf.org/doc/rfc9420/  and  https://www.rfc-editor.org/info/rfc9420/
- MLS architecture / RFC 9750 — https://datatracker.ietf.org/doc/rfc9750/
- OpenMLS — https://github.com/openmls/openmls  and  https://openmls.tech/
- AWS mls-rs — https://github.com/awslabs/mls-rs
- Cisco mlspp — https://github.com/cisco/mlspp
- Post-Quantum OpenMLS — https://blog.openmls.tech/posts/2024-04-11-pq-openmls/
- IETF on MLS — https://www.ietf.org/blog/mls-protocol-published/
- Wikipedia: Messaging Layer Security — https://en.wikipedia.org/wiki/Messaging_Layer_Security
- (Name-collision, keep separate) Infomaniak kChat — https://www.infomaniak.com/en/ksuite/kchat
