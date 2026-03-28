# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Response:**

The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:

1. **Perceive** — Gather information from the environment (user input, files, APIs, sensors, etc.)
2. **Reason/Plan** — Analyze the information, determine goals, and decide on a course of action
3. **Act** — Execute actions using available tools (write files, run commands, call APIs, send messages, etc.)
4. **Observe** — Receive feedback from the actions taken (outputs, errors, state changes)
5. **Iterate** — Repeat the loop until the goal is achieved or a stopping condition is met

This loop enables agents to:
- Break complex tasks into steps
- Adapt based on feedback
- Handle errors and recover
- Work autonomously toward goals

### Question 2: "What labs are available in our LMS?"

**Response:**

Based on my exploration of the workspace, I found the following labs available in your LMS:

**Available Labs**

1. **Lab 1 (wiki/lab-1/)**
   - Contains documentation and diagrams for the first lab
   - Located at: /root/se-toolkit-lab-8/wiki/lab-1/
2. **General Lab Resources (lab/)**
   - Contains setup files, tasks, and images
   - Located at: /root/se-toolkit-lab-8/lab/

The current lab repository is se-toolkit-lab-8, which appears to be Lab 8 in the Software Engineering toolkit series.

**Note:** The bare agent cannot query the live LMS backend yet — it only searches local files. It does not return real lab data from the backend API.

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available?"

**Response:**

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

**Evidence of MCP tools working:** The log shows `MCP server 'lms': connected, 9 tools registered` and the tool call `mcp_lms_lms_labs({})`.

### Question 2: "Is the LMS backend healthy?"

**Response:**

Yes, the LMS backend is healthy! 🟢

- **Status**: healthy
- **Item count**: 56 items
- **Errors**: none

**Evidence of MCP tools working:** The agent called `mcp_lms_lms_health({})` and returned real backend data.

## Task 1C — Skill prompt

### Question: "Show me the scores" (without specifying a lab)

**Response:**

Here are the available labs. Which lab would you like to see the scores for?

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Please let me know which lab you're interested in, or I can show you scores for all of them.

**Evidence of skill working:** The agent followed the skill strategy:
1. Recognized that "scores" requires a lab parameter
2. Called `lms_labs` first to get available labs
3. Presented the list and asked the user to choose

**Skill file created:** `nanobot/workspace/skills/lms/SKILL.md`

## Task 2A — Deployed agent

**Nanobot startup log excerpt:**

```
nanobot-1  | Using config: /tmp/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-03-28 10:33:51.160 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | 2026-03-28 10:33:54.708 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-03-28 10:33:57.181 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
nanobot-1  | 2026-03-28 10:33:57.181 | INFO     | nanobot.agent.loop:run:280 - Agent loop started
```

**Verification:**
- `docker compose --env-file .env.docker.secret ps` shows nanobot service is "Up"
- WebChat channel is enabled
- MCP servers 'lms' (9 tools) and 'webchat' (1 tool) are connected
- Agent loop is running

## Task 2B — Web client

**WebSocket test response:**

```
Response: {"type":"text","content":"Here are the available labs in the LMS:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy\n4. **Lab 04** — Testing, Front-end, and AI Agents\n5. **Lab 05** — Data Pipeline and Analytics Dashboard\n6. **Lab 06** — Build Your Own Agent\n7. **Lab 07** — Build a Client with an AI Coding Agent\n8. **Lab 08** — lab-08\n\nWould you like to see performance data, pass rates, or completion stats for any specific lab?","format":"markdown"}
```

**Flutter client:**
- Accessible at `http://localhost:42002/flutter/`
- Login screen appears and accepts `NANOBOT_ACCESS_KEY=vasilisa`
- Agent responds to questions with real LMS backend data

**Test conversation:**
1. Question: "What labs are available?"
2. Response: Lists all 8 labs from the LMS backend with offer to show more details

**Files modified/created for Task 2:**
- `nanobot/entrypoint.py` — resolves env vars into config at runtime
- `nanobot/Dockerfile` — multi-stage build with uv
- `nanobot/config.json` — webchat channel enabled
- `nanobot/pyproject.toml` — dependencies on nanobot-webchat and mcp-webchat
- `docker-compose.yml` — nanobot, client-web-flutter, and caddy services configured
- `caddy/Caddyfile` — /ws/chat and /flutter routes enabled
- `pyproject.toml` — workspace members for nanobot-websocket-channel packages

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
