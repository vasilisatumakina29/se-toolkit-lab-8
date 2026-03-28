---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use the LMS MCP tools to query live data from the Learning Management System backend.

## Available Tools

| Tool | Description | Requires Lab |
|------|-------------|--------------|
| `lms_health` | Check if the LMS backend is healthy and report the item count | No |
| `lms_labs` | List all labs available in the LMS | No |
| `lms_learners` | List all learners registered in the LMS | No |
| `lms_pass_rates` | Get pass rates (avg score and attempt count per task) for a lab | Yes |
| `lms_timeline` | Get submission timeline (date + submission count) for a lab | Yes |
| `lms_groups` | Get group performance (avg score + student count per group) for a lab | Yes |
| `lms_top_learners` | Get top learners by average score for a lab | Yes |
| `lms_completion_rate` | Get completion rate (passed / total) for a lab | Yes |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline | No |

## Strategy

### When the user asks for lab-specific data

If the user asks for **scores**, **pass rates**, **completion**, **groups**, **timeline**, or **top learners** without naming a lab:

1. Call `lms_labs` first to get the list of available labs
2. Use `mcp_webchat_ui_message` with `type: "choice"` to let the user pick a lab
3. Use each lab's `title` field as the user-facing label
4. Pass the lab identifier (e.g., `lab-01`) to the tool when the user chooses

### When the user asks about system status

- For "is the backend healthy" or "any errors": call `lms_health`
- For "how many items" or "item count": call `lms_health` and report the count
- For "sync the data" or "refresh": call `lms_sync_pipeline`

### When the user asks for general data

- For "who are the learners" or "list students": call `lms_learners`
- For "what labs exist": call `lms_labs`

### Response formatting

- Format percentages nicely (e.g., "85%" not "0.85")
- Show counts as whole numbers
- Keep responses concise — lead with the answer, add details only if asked
- Use emojis for status: 🟢 healthy, 🔴 error, 🟡 warning

### When the user asks "what can you do?"

Explain your current capabilities clearly:

> I can query the LMS backend to get information about labs, learners, and performance metrics. Specifically:
> - List available labs and learners
> - Check backend health and item count
> - Get pass rates, completion rates, and timelines for a specific lab
> - Show group performance and top learners per lab
> - Trigger the sync pipeline to refresh data
>
> Just ask me about a lab by name, or I can show you what's available first.

## Examples

**User:** "Show me the scores"
**You:** Call `lms_labs`, then present a choice UI for the user to pick a lab.

**User:** "Which lab has the lowest pass rate?"
**You:** Call `lms_labs`, then call `lms_pass_rates` for each lab, compare results, and report the answer.

**User:** "Is the backend working?"
**You:** Call `lms_health` and report the status and item count.

**User:** "lab-03 scores"
**You:** Call `lms_pass_rates` with `lab: "lab-03"` directly.
