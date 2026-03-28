"""Tool schemas, handlers, and registry for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import VictoriaLogsClient, VictoriaTracesClient


class LogsSearchQuery(BaseModel):
    query: str = Field(
        description="LogsQL query. Examples: 'severity:ERROR', 'service.name:\"LMS\"', '_time:-1h event:db_query'"
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=1000,
        description="Max log entries to return (default 50, max 1000)",
    )
    time_range: str = Field(
        default="-1h",
        description="Time range like '-1h', '-10m', '-24h' (default: -1h)",
    )


class LogsErrorCountQuery(BaseModel):
    service: str | None = Field(
        default=None,
        description="Optional service name filter (e.g., 'Learning Management Service')",
    )
    time_range: str = Field(
        default="-1h",
        description="Time window like '-1h', '-10m', '-24h' (default: -1h)",
    )


class TracesListQuery(BaseModel):
    service: str = Field(
        description="Service name to filter traces (e.g., 'Learning Management Service')"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Max traces to return (default 10, max 50)",
    )


class TracesGetQuery(BaseModel):
    trace_id: str = Field(
        description="Trace ID to fetch (hex string like '99cf8b0cdd50d8ee7d5f5c88010b499c')"
    )


ToolPayload = BaseModel | list[dict[str, Any]]
ToolHandler = Callable[[VictoriaLogsClient, VictoriaTracesClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(
    logs_client: VictoriaLogsClient,
    _traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """Search logs using LogsQL query."""
    query = args if isinstance(args, LogsSearchQuery) else LogsSearchQuery.model_validate(args)
    results = await logs_client.search_logs(
        query=query.query,
        limit=query.limit,
        start=query.time_range,
        end="now",
    )
    return {"logs": results, "count": len(results)}


async def _logs_error_count(
    logs_client: VictoriaLogsClient,
    _traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """Count errors by service over a time window."""
    query = args if isinstance(args, LogsErrorCountQuery) else LogsErrorCountQuery.model_validate(args)
    counts = await logs_client.count_errors(
        service=query.service,
        time_range=query.time_range,
    )
    return {"error_counts": counts, "time_range": query.time_range}


async def _traces_list(
    _logs_client: VictoriaLogsClient,
    traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """List recent traces for a service."""
    query = args if isinstance(args, TracesListQuery) else TracesListQuery.model_validate(args)
    traces = await traces_client.list_traces(
        service=query.service,
        limit=query.limit,
    )
    # Return simplified trace info
    simplified = [
        {
            "trace_id": t.get("traceID", ""),
            "spans": len(t.get("spans", [])),
            "start_time": t.get("startTime", 0),
        }
        for t in traces
    ]
    return {"traces": simplified, "count": len(simplified)}


async def _traces_get(
    _logs_client: VictoriaLogsClient,
    traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """Get a specific trace by ID."""
    query = args if isinstance(args, TracesGetQuery) else TracesGetQuery.model_validate(args)
    trace = await traces_client.get_trace(query.trace_id)
    if trace is None:
        return {"error": f"Trace {query.trace_id} not found"}

    # Simplify the trace for display
    spans_summary = [
        {
            "span_id": s.get("spanID", ""),
            "operation_name": s.get("operationName", ""),
            "service_name": s.get("process", {}).get("serviceName", ""),
            "duration": s.get("duration", 0),
            "tags": len(s.get("tags", [])),
        }
        for s in trace.get("spans", [])
    ]
    return {
        "trace_id": trace.get("traceID", ""),
        "spans": spans_summary,
        "total_spans": len(spans_summary),
    }


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search logs using LogsQL. Use for finding errors, debugging issues, or exploring service behavior. "
        "Example queries: 'severity:ERROR _time:-10m', 'service.name:\"LMS\" event:db_query'",
        LogsSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count errors by service over a time window. Use to quickly check if there are recent errors.",
        LogsErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces for a service. Returns trace IDs and span counts.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Get full details of a specific trace by ID. Use to inspect the span hierarchy and timing of a request.",
        TracesGetQuery,
        _traces_get,
    ),
)
TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
