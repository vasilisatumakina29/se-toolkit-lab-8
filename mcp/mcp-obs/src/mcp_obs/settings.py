"""Settings for the observability MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ObsSettings:
    """Settings for connecting to VictoriaLogs and VictoriaTraces."""

    victorialogs_url: str
    victoriatraces_url: str

    @classmethod
    def from_env(cls) -> "ObsSettings":
        """Load settings from environment variables."""
        return cls(
            victorialogs_url=os.environ.get(
                "NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"
            ),
            victoriatraces_url=os.environ.get(
                "NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:8428"
            ),
        )


def resolve_settings() -> ObsSettings:
    """Resolve settings from environment or use defaults."""
    return ObsSettings.from_env()
