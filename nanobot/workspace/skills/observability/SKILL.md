# Observability Skill

You have access to observability tools for querying VictoriaLogs and VictoriaTraces. Use these tools to investigate system behavior, debug errors, and monitor service health.

## Available Tools

### `logs_search`
Search logs using LogsQL queries. Use this to find specific events, errors, or patterns.

**Example queries:**
- `severity:ERROR _time:-10m` — Errors in the last 10 minutes
- `service.name:"Learning Management Service" event:db_query` — Database queries from LMS
- `trace_id:abc123` — All logs for a specific trace

### `logs_error_count`
Count errors by service over a time window. Use this first to quickly check if there are recent errors.

### `traces_list`
List recent traces for a service. Returns trace IDs and span counts.

### `traces_get`
Get full details of a specific trace by ID. Use this to inspect the span hierarchy and timing of a request.

## Workflow

### When the user asks about errors or issues:

1. **Start with `logs_error_count`** to see if there are recent errors and which services are affected.

2. **Use `logs_search`** to inspect the error details:
   - Filter by service: `service.name:"Learning Management Service" severity:ERROR`
   - Narrow time range: `_time:-10m`
   - Look for specific events: `event:db_query`

3. **Extract trace IDs** from error logs if present (look for `trace_id` field).

4. **Use `traces_get`** to fetch the full trace and understand the request flow.

5. **Summarize findings** concisely — don't dump raw JSON.

### Example reasoning flow:

User: "Any LMS backend errors in the last 10 minutes?"

1. Call `logs_error_count(service="Learning Management Service", time_range="-10m")`
2. If errors found, call `logs_search(query='service.name:"Learning Management Service" severity:ERROR _time:-10m')`
3. Extract a `trace_id` from the error logs
4. Call `traces_get(trace_id="<extracted_id>")` to see the full request flow
5. Summarize: what failed, where, and why

## Tips

- Always narrow the time range when possible (`_time:-10m`, `_time:-1h`)
- Use service names to filter logs from specific components
- When you find an error, look for the `trace_id` to correlate with traces
- Traces show the full request flow across services — useful for understanding cascading failures
- Don't dump raw JSON — summarize the key findings

## Common Queries

**Check for recent errors:**
```
logs_error_count(time_range="-1h")
```

**Search LMS errors:**
```
logs_search(query='service.name:"Learning Management Service" severity:ERROR _time:-10m')
```

**Find a specific trace:**
```
traces_get(trace_id="99cf8b0cdd50d8ee7d5f5c88010b499c")
```

**List recent traces for a service:**
```
traces_list(service="Learning Management Service", limit=10)
```
