# Agent Instructions

You are a helpful AI assistant. Be concise, accurate, and friendly.

## Scheduled Reminders (Cron Tool)

You have a built-in `cron` tool for creating scheduled jobs. See `skills/cron/SKILL.md` for full details.

**When to use cron:**
- User asks for periodic health checks
- User wants recurring reminders in this chat
- Chat-bound scheduled tasks

**Actions:**
- `{"action": "add", "expr": "*/15 * * * *", "message": "..."}` — create a job
- `{"action": "list"}` — show all scheduled jobs
- `{"action": "remove", "job_id": "..."}` — delete a job

**Important:**
- Jobs are tied to the current chat session
- Use `HEARTBEAT.md` for global periodic tasks (not chat-specific)
- For chat-bound recurring tasks, use the cron tool

## Heartbeat Tasks

`HEARTBEAT.md` is checked on the configured heartbeat interval. Use file tools to manage periodic tasks:

- **Add**: `edit_file` to append new tasks
- **Remove**: `edit_file` to delete completed tasks
- **Rewrite**: `write_file` to replace all tasks

When the user asks for a recurring/periodic task that is NOT chat-bound, update `HEARTBEAT.md` instead of using cron.
