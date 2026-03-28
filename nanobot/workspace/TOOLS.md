# Tool Usage Notes

Tool signatures are provided automatically via function calling.
This file documents non-obvious constraints and usage patterns.

## exec — Safety Limits

- Commands have a configurable timeout (default 60s)
- Dangerous commands are blocked (rm -rf, format, dd, shutdown, etc.)
- Output is truncated at 10,000 characters
- `restrictToWorkspace` config can limit file access to the workspace

## cron — Scheduled Jobs

The `cron` tool is a built-in tool for creating scheduled jobs. See `skills/cron/SKILL.md` for full usage.

**Actions:**
- `{"action": "add", "expr": "*/15 * * * *", "message": "..."}` — add a job
- `{"action": "list"}` — list all scheduled jobs
- `{"action": "remove", "job_id": "..."}` — remove a job

**Cron expressions:**
- `*/2 * * * *` — every 2 minutes
- `*/15 * * * *` — every 15 minutes
- `0 * * * *` — every hour
- `0 0 * * *` — every day at midnight

**Note:** Jobs are tied to the current chat session. For global periodic tasks, use `HEARTBEAT.md` instead.
