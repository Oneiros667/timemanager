# Optional AI body-doubling and voice design

Status: proposed product direction  
Updated: 2026-07-24

This note defines an optional AI assistant for the ADHD-friendly time-management
system. It is a support feature, not a replacement for a person, therapist,
coach, diagnosis, or treatment.

## Product decision

Offer AI-assisted body doubling as an **opt-in** capability. The primary
experience remains useful without an AI account, microphone, or network
connection: tasks, routines, visible timers, and non-AI co-working modes must
continue to work.

For a custom application, use a programmable voice API such as OpenAI's
Realtime API rather than trying to embed ChatGPT Enterprise Voice. ChatGPT
Voice is a ChatGPT workspace experience; Realtime is the API intended for
low-latency application voice sessions and supports WebRTC connections.

Sources:

- [OpenAI Realtime API reference](https://platform.openai.com/docs/api-reference/realtime?lang=javascript)
- [ChatGPT Voice / Live FAQ](https://help.openai.com/en/articles/20001274-gpt-live-faq)

## Jobs the feature should help with

The assistant should reduce activation friction and help the user return after
interruptions. It should be calm, concrete, predictable, and easy to stop.

| Mode | Intended interaction | Example outcome |
| --- | --- | --- |
| Start ritual | Ask for the smallest visible next action, then agree a short session. | “Open the report and write its title; shall we do ten minutes?” |
| Quiet co-work | Remain available with little or no speech, and check in only at an agreed boundary. | A 25-minute timer and a single end-of-session question. |
| Gentle check-in | Prompt at a chosen cadence, never unexpectedly or continuously. | “Time is up. Continue, take a break, or stop?” |
| Recovery after interruption | Normalise the interruption and present small, reversible choices. | “Would you like to resume for five minutes, park this task, or choose another?” |
| Spoken capture | Convert a spoken thought into a proposed task, reminder, or note. | A draft task displayed for confirmation before saving. |
| Session reflection | Give a brief factual recap that the user may edit or discard. | “You completed the outline and identified two follow-ups.” |

The assistant must not use shame, urgency, or dependency-oriented language. It
should not claim that it is a person, a clinician, or a substitute for either.

## Guardrails and interaction rules

- The user explicitly starts every voice session and can mute or end it
  immediately. Never present the feature as always listening.
- Show a clear microphone/connection indicator and the active session timer.
- Agree the check-in frequency at session start; default to sparse check-ins.
- Treat every task mutation as a proposal unless the user gave a direct,
  unambiguous instruction. Require confirmation before creating ambiguous
  tasks, changing priority, rescheduling, deleting, or marking work complete.
- Keep the assistant's available tools narrow: read relevant daily context,
  start/stop a timer, draft a task, and save a user-confirmed change.
- Do not make clinical, safety, legal, or financial decisions. If a user seeks
  help beyond productivity support, respond safely and direct them to suitable
  human or emergency support when appropriate.
- Voice, transcript retention, summaries, and personalised memory each have
  separate opt-in settings.

## Privacy and data handling

Running the application in a local container does not make an enabled cloud AI
integration fully local: audio and prompts are sent to the chosen AI provider.
The interface must state this before the first voice session.

Defaults:

- Store no raw audio in Timemanager.
- Do not save transcripts or summaries unless the user enables them.
- Send only the minimum context needed for the active session; do not provide
  an entire task history by default.
- Allow the user to review and delete stored summaries and AI memory.
- Keep provider credentials server-side, injected as container secrets or
  environment configuration; never place a long-lived API key in a web or
  mobile client.

OpenAI states that API data is not used to train models by default, but its
platform data-controls documentation describes retention and eligible stronger
controls. Realtime has default abuse-monitoring retention, so the deployment
must document the selected provider, retention terms, and any available data
controls rather than making broad privacy promises.

Source: [OpenAI API data controls](https://platform.openai.com/docs/models/default-usage-policies-by-endpoint)

## Architecture and rollout

```text
Web client / future native mobile client
             |
             | authenticated short-lived session
             v
Timemanager backend ---- limited task/timer tools ---- Timemanager data store
             |
             | provider credential remains here
             v
Voice AI provider (for example, OpenAI Realtime API)
```

### Phase 1: local home-lab container

- Ship the AI connector disabled by default.
- Enable it through explicit server configuration, e.g. an `AI_PROVIDER`
  setting and a secret supplied to the container runtime.
- Keep the main planner fully usable when the provider is offline, unconfigured,
  unaffordable, or deliberately disabled.
- Provide a non-AI focus timer / manual body-doubling screen as the fallback.

### Phase 2: authenticated online service

- Put all AI calls behind the same authenticated user boundary as tasks.
- Enforce tenant isolation, rate limits, per-user usage limits, and cost
  controls at the backend.
- Issue short-lived voice-session credentials/tokens; clients must not receive
  the service's long-lived provider credential.
- Log operational metadata needed for debugging and billing without retaining
  sensitive voice content by default.

### Phase 3: Android and iOS clients

- Use the same authenticated backend and task identifiers as the web app.
- Sync user-confirmed task changes and optional session summaries, not raw
  audio by default.
- Design for interruptions, lost network, and mobile background restrictions:
  an active body-doubling session should always degrade safely to a local timer
  and resumable task state.

## Success measures and evaluation

This feature is a design hypothesis. Evaluate it with opt-in user testing,
especially for whether it makes beginning and returning to tasks easier without
creating distraction, pressure, excessive cost, or unwanted data collection.

Useful measures include session starts, completion of the chosen next action,
return after interruption, manual mute/stop rate, opt-out rate, and qualitative
reports of helpfulness versus intrusiveness. These metrics must not be used to
pressure the user into longer sessions or more disclosure.
