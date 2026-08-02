# The Room Where Only You Have the Key

*A story about KChat, UNEY, and why the boring plumbing of encryption is actually about being human.*

---

There's a specific kind of quiet that happens after you say something you didn't mean anyone else to hear.

Maybe it's the message to your sister about the diagnosis. Maybe it's the group thread where your neighbors are organizing something the landlord wouldn't like. Maybe it's nothing dramatic at all — just you and a friend, at 1 a.m., saying the unpolished version of what you actually think. And then, a beat later, the small cold thought arrives: *who else can see this?*

We've all learned to live with that thought. We shrug it off. We've been trained to treat surveillance as weather — just the climate of being online now. You type the message anyway, because what's the alternative? Not talking to the people you love?

KChat exists because a few people refused to accept that shrug.

## What KChat actually is

Strip away the marketing and KChat is a messaging app — the kind you already know how to use. You text people. You make group chats. You build communities that can hold up to a couple thousand members, with threads and sub-groups so a big room doesn't turn into chaos. You send photos, videos, files. You have secret chats and messages that quietly delete themselves after they've been read. You can log in on your phone and your laptop and it all just stays in sync.

The difference is what happens underneath, and what *doesn't* happen underneath.

It doesn't ask for your phone number. It doesn't ask who you really are. And here's the line that matters most: the messages are end-to-end encrypted, which means they stay between you and the person you're talking to — **not even the company can read them.** They're not quietly reading your life to sell it back to you as an ad. They say it flatly: they don't monetize your information. In an industry that turned "free" into "you are the product," that plainness feels almost radical.

The people building it are a company called **UNEY** — a small outfit with roots in Germany and a base in Dubai, with a team betting that people are tired of choosing between *easy to use* and *safe to use*. KChat is their answer to that false choice. (They've got a companion app too, AutoSec, aimed at locking down your device — but KChat is the heart of it.)

## Why group chats are the hard part (and the human part)

Here's a thing most people never think about, and it's beautiful once you see it.

Encrypting a message between *two* people has been more or less solved for a while. Two people, one shared secret, done. But two people isn't where your life actually happens. Your life happens in the family thread. The twelve-person friend group that's been going since college. The parents' group at school. The mutual-aid channel. The group where your community makes decisions.

And groups are *messy*. People join. People leave. Someone's offline for three days. Someone's on their phone and their tablet and a laptop. Someone gets a new device. Every one of those moments is a tiny crisis for encryption — a door that has to be relocked so that the person who just left can't read what's said after they're gone, and the person who just joined can't read what was said before they arrived.

For years, doing that securely *and* at scale was genuinely hard. So a lot of apps just… didn't, not really. They locked the two-person door and left the group room a little more open than they let on.

## The quiet revolution called MLS

Then something unglamorous and wonderful happened. A bunch of engineers, cryptographers, and companies who normally compete with each other sat down together at the IETF — the same kind of standards body that quietly built the internet — and agreed on a shared way to do encrypted *group* messaging. They called it **Messaging Layer Security**, MLS for short. In 2023 it became an official internet standard, RFC 9420.

I want to translate what MLS gives you out of engineer-speak, because the guarantees are genuinely moving when you say them as human promises:

- **Forward secrecy:** if someone steals a key tomorrow, they still can't read what you said last year. The past stays shut.
- **Post-compromise security:** even if a room *does* get broken into, once the door is relocked, the room becomes safe again. It heals.
- **It works for two people or twenty thousand,** and it handles the real mess — people coming, going, offline, on five devices — without falling apart.

And the part that matters for trust: **MLS is open.** The design is public. Anyone can read it, poke holes in it, and check the math. There are open-source implementations out in the daylight — [OpenMLS](https://github.com/openmls/openmls) written in Rust, AWS's [mls-rs](https://github.com/awslabs/mls-rs), Cisco's [mlspp](https://github.com/cisco/mlspp) — that researchers have gone over line by line. Some are already reaching toward **post-quantum** encryption, so the secrets you keep today survive the computers of a decade from now.

This is the piece people miss. Open-source encryption isn't just about "free software." It's about *not having to take anyone's word for it.* You shouldn't have to trust a company's promise that it's protecting you. With open standards, you don't. The lock is on the table for everyone to inspect. Trust stops being a feeling and becomes something you can check.

That's the world KChat is building itself into — the world MLS made possible. A world where "private" isn't a premium feature or a marketing word, but the plain default, resting on foundations anyone can audit.

## Why any of this matters at 1 a.m.

You will never think about forward secrecy while you're texting your sister. You shouldn't have to. That's the whole point.

Good encryption is like good plumbing or good brakes — the measure of it is that you never once have to think about it. It just quietly keeps the promise so you can be a person. So you can say the unpolished thing. Organize the meeting. Send the photo. Have the hard conversation. And feel, underneath it, that small warmth of a door that's actually closed.

For a long time, we were told that door was a luxury. That if you wanted real privacy you had to become a bit of a paranoid, learn the tools, give up the ease. KChat and the open standards it stands on are a quiet argument that this was always a lie — that private, secure, human conversation can also just be *nice to use.*

The room can be yours. The key can be yours. And the fact that only you hold it doesn't have to be a fight anymore. It can just be the way things are.

That's worth building. Honestly, it might be one of the more human things a piece of software can do.

---

*Draft — reporting notes and full source list in `kchat-research-dossier.md`. Before publishing, verify KChat's exact encryption stack on kchat.com's own security page: public materials confirm end-to-end encryption and AES-256, but whether KChat implements MLS/RFC 9420 specifically should be confirmed on the record rather than assumed.*
