"""Async HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

from typing import Any

import httpx


class VictoriaLogsClient:
    """Client for the VictoriaLogs HTTP API."""

    def __init__(
        self,
        base_url: str,
        *,
        http_client: httpx.AsyncClient | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )

    async def __aenter__(self) -> "VictoriaLogsClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._http_client.aclose()

    async def search_logs(
        self,
        query: str,
        limit: int = 100,
        start: str | None = None,
        end: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search logs using LogsQL query.

        Args:
            query: LogsQL query string (e.g., 'service.name:"LMS" severity:ERROR')
            limit: Maximum number of log entries to return
            start: Start time (RFC3339 or relative like '-1h')
            end: End time (RFC3339 or relative like 'now')

        Returns:
            List of log entries as dictionaries
        """
        params: dict[str, str | int] = {"query": query, "limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        response = await self._http_client.get(
            "/select/logsql/query", params=params
        )
        response.raise_for_status()

        # VictoriaLogs returns newline-delimited JSON
        lines = response.text.strip().split("\n")
        results = []
        for line in lines:
            if line.strip():
                try:
                    results.append(httpx.Response(line.encode()).json() if False else __import__('json').loads(line))
                except Exception:
                    continue
        return results

    async def count_errors(
        self,
        service: str | None = None,
        time_range: str = "-1h",
    ) -> dict[str, int]:
        """
        Count errors by service over a time window.

        Args:
            service: Optional service name filter
            time_range: Time range like '-1h', '-24h'

        Returns:
            Dictionary mapping service names to error counts
        """
        query = f"severity:ERROR _time:{time_range}"
        if service:
            query = f'service.name:"{service}" {query}'

        results = await self.search_logs(query=query, limit=10000)

        # Count by service
        error_counts: dict[str, int] = {}
        for entry in results:
            attrs = entry.get("_msg", {})
            if isinstance(attrs, dict):
                service_name = attrs.get("service.name", "unknown")
            else:
                service_name = "unknown"
            error_counts[service_name] = error_counts.get(service_name, 0) + 1

        return error_counts


class VictoriaTracesClient:
    """Client for the VictoriaTraces HTTP API (Jaeger-compatible)."""

    def __init__(
        self,
        base_url: str,
        *,
        http_client: httpx.AsyncClient | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )

    async def __aenter__(self) -> "VictoriaTracesClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._http_client.aclose()

    async def list_traces(
        self,
        service: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """
        List recent traces for a service.

        Args:
            service: Service name to filter traces
            limit: Maximum number of traces to return

        Returns:
            List of trace summaries
        """
        response = await self._http_client.get(
            "/select/jaeger/api/traces",
            params={"service": service, "limit": limit},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    async def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        """
        Get a specific trace by ID.

        Args:
            trace_id: The trace ID to fetch

        Returns:
            Full trace data or None if not found
        """
        response = await self._http_client.get(
            f"/select/jaeger/api/traces/{trace_id}"
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        traces = data.get("data", [])
        return traces[0] if traces else None
