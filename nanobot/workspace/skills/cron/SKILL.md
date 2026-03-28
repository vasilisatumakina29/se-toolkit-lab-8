# Cron — Scheduled Jobs Skill

You have a built-in `cron` tool for creating scheduled jobs that run periodically.

## When to Use

Use the cron tool when the user asks for:
- Periodic/regular health checks
- Scheduled reminders
- Recurring tasks (every X minutes/hours)
- "Remind me every..." requests

## Tool Actions

The `cron` tool supports these actions:

### 1. Add a Job

```json
{
  "action": "add",
  "expr": "*/15 * * * *",
  "message": "Check system health and post a summary"
}
```

**Cron expression format:**
- `*/15 * * * *` — every 15 minutes
- `*/2 * * * *` — every 2 minutes
- `0 * * * *` — every hour at minute 0
- `0 0 * * *` — every day at midnight

### 2. List Jobs

```json
{
  "action": "list"
}
```

Returns all scheduled jobs with their IDs and schedules.

### 3. Remove a Job

```json
{
  "action": "remove",
  "job_id": "abc123"
}
```

Use the job_id from the `list` action.

## Health Check Pattern

When users ask for periodic health monitoring:

1. **Create the job** with appropriate interval:
   - Testing: `*/2 * * * *` (every 2 minutes)
   - Production: `*/15 * * * *` (every 15 minutes)

2. **Use observability tools** in the job:
   - Call `logs_error_count` for recent errors
   - Call `logs_search` if errors found
   - Call `traces_get` for specific trace details

3. **Post a concise summary**:
   - 🟢 "System healthy — no errors in last X minutes"
   - 🔴 "Issue detected: [brief description]"

## Example Flow

**User:** "Create a health check that runs every 15 minutes."

**You:**
1. Call cron tool: `{"action": "add", "expr": "*/15 * * * *", "message": "Check LMS backend health"}`
2. Confirm: "✅ Created scheduled health check running every 15 minutes (job ID: xxx)"
3. Offer to list: "Want me to show all scheduled jobs?"

**User:** "List scheduled jobs."

**You:**
1. Call cron tool: `{"action": "list"}`
2. Display results in a table format

## Important Notes

- Jobs are tied to the current chat session/channel
- Use `HEARTBEAT.md` for global periodic tasks (not chat-specific)
- For chat-bound recurring tasks, use the cron tool
- Always confirm job creation with the job ID
- Use shorter intervals (2 min) for testing, longer (15 min) for production
