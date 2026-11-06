# Digital Twin: A Tool-Using AI Agent That Represents Me

An LLM agent, deployed as a public web app, that answers questions about my career, skills and experience in my voice. It stays on topic, never invents facts, captures leads, and pings my phone when it meets a question it can't answer.

**Live demo:** https://digital-twin-a2k1.onrender.com/

![Digital Twin](https://i.imgur.com/7TIMZ9O.png)

**Stack:** Python · CrewAI 1.14 · OpenAI · Gradio 6 · pypdf · Pushover API · Render · uv

---

## What it does

A visitor (for example a recruiter) chats with the twin. The agent:

1. Answers from my LinkedIn profile, which is loaded as grounding context.
2. Declines or redirects off-topic questions and keeps the conversation professional.
3. Asks for an email when someone wants to get in touch, then records it.
4. Admits when it doesn't know something, and logs the unanswered question for me. It does not guess.
5. Sends a real-time push notification to my phone for items 3 and 4, so I can follow up.

## Architecture

```
 knowledge/linkedin.pdf
        │  pypdf text extraction (once, at startup)
        ▼
 ┌──────────────┐   {linkedin, message}   ┌──────────────────────────────┐
 │ Gradio Chat  │ ──────────────────────▶ │ CrewAI Crew (sequential)     │
 │  (chat.py)   │                         │  ├─ Agent: digital_twin      │
 │              │ ◀────────────────────── │  │    persona + grounding    │
 └──────────────┘      markdown reply     │  ├─ Task: answer_task        │
                                          │  │    policy + output format │
                                          │  └─ Tool: send_push_notif.   │
                                          └───────────────┬──────────────┘
                                                          │ ReAct loop, function calling
                                                          ▼
                                                 Pushover API → my phone
```

| File | Responsibility |
|---|---|
| [src/digital_twin/crew.py](src/digital_twin/crew.py) | Wires the agent, task and crew using CrewAI's `@CrewBase` decorators |
| [src/digital_twin/config/agents.yaml](src/digital_twin/config/agents.yaml) | Persona, goal, backstory, and the grounding slot `{linkedin}` |
| [src/digital_twin/config/tasks.yaml](src/digital_twin/config/tasks.yaml) | Behavioural policy, guardrails, tool-use rules, output format |
| [src/digital_twin/tools/push_tool.py](src/digital_twin/tools/push_tool.py) | Custom agent tool that calls the Pushover API |
| [src/digital_twin/main.py](src/digital_twin/main.py) | Ingests the LinkedIn PDF into plain text |
| [src/digital_twin/chat.py](src/digital_twin/chat.py) | Gradio `ChatInterface` that calls the crew for each message |
| [src/digital_twin/styles.py](src/digital_twin/styles.py) | Custom dark/light theme, CSS and JS for the UI |

## Agent techniques implemented

### 1. Persona-driven agent design (role / goal / backstory)
The agent is defined declaratively in YAML as a "digital twin" with a role, a goal and a backstory. The backstory tells it that it is an AI representing a real person and that it must say so if asked. That gives it a consistent identity and avoids deceiving visitors.

### 2. Context grounding with a document-to-prompt pipeline
My LinkedIn PDF is parsed with `pypdf` at startup and injected into the agent's backstory through CrewAI's `{linkedin}` template variable on every request. The model answers from this source of truth instead of from its pre-training. This is a full-context approach. The profile is small enough to fit in the prompt, so no vector database or retrieval step is needed.

### 3. Separation of identity and policy (agent vs. task)
Who the agent is (`agents.yaml`) is kept apart from what it must do on each turn (`tasks.yaml`). The task carries the rules: the allowed topic scope, the contact-capture flow, and the fallback behaviour. The user's message enters through `{message}`. Behaviour can then be changed by editing config files, with no code changes.

### 4. Prompt-level guardrails
- **Scope control:** off-topic questions are steered back to professional topics.
- **Anti-hallucination:** "If you don't know the answer… never make up an answer" is an explicit instruction, backed by an action the agent can take (see next item).
- **Character consistency:** the agent must stay in character and represent the person.
- **Output contract:** `expected_output` asks for engaging markdown with no code blocks, which keeps replies clean in the chat UI.

### 5. Tool use / function calling
The agent has a custom tool, `Send Push Notification`, defined with CrewAI's `@tool` decorator. Its docstring is the schema the LLM reads to decide when to call it. The agent reasons about the conversation and chooses to call the tool in two situations:
- a visitor wants to get in touch and has given an email, or
- the agent can't answer a question, so it records the question.

This is a ReAct-style loop of reason, act, observe, respond. It turns a chatbot into an agent that causes real side effects.

### 6. Human-in-the-loop escalation
The tool pushes events to my phone through Pushover, so unknown questions and leads reach a human right away. This is an escalation path from the agent to me. It also gives me a feedback signal for what the profile is missing.

### 7. Orchestration with CrewAI
The agent and task run in a `Crew` with `Process.sequential`, built with the `@CrewBase` / `@agent` / `@task` / `@crew` pattern. The project is a deliberately minimal one-agent, one-task, one-tool design. It keeps the agentic pieces visible and easy to extend (for example `Process.hierarchical`, or extra specialist agents).

### 8. Productionisation
Gradio serves the UI, with a custom theme that has dark/light support, a branded palette and mobile layout. The app is deployed on Render, with secrets (`OPENAI_API_KEY`, `PUSHOVER_*`) kept in environment variables.

## Known limitations and next steps

I list these on purpose, since they are the natural next improvements:

- **No conversation memory.** Each Gradio turn runs a fresh crew call with only the latest `{message}`. The chat `history` is not passed in, so follow-up questions lose context. Next step: pass a condensed history into the task.
- **Full-context grounding.** This works for a single profile. For larger knowledge (blog posts, project write-ups) the next step is chunking, embeddings and retrieval (CrewAI Knowledge sources).
- **Prompt-only guardrails.** They could be hardened with CrewAI task guardrails or an LLM judge that validates the output before it is returned.
- **No automated evals.** A test set of expected and adversarial questions (prompt injection, off-topic, unknown facts) would let me measure the guardrails.

## Run it locally

Requires Python 3.10–3.13 and [uv](https://docs.astral.sh/uv/).

```bash
git clone <this-repo> && cd digital_twin
uv sync
```

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
PUSHOVER_USER=...      # optional, for push notifications
PUSHOVER_TOKEN=...
```

Replace `knowledge/linkedin.pdf` with your own exported LinkedIn profile, edit the persona in `src/digital_twin/config/agents.yaml`, then run from the project root:

```bash
uv run python -m digital_twin.chat
```

The Gradio app opens at http://127.0.0.1:7860.
