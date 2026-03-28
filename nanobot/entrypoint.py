#!/usr/bin/env python3
"""
Entrypoint for nanobot Docker container.

Resolves environment variables (LLM API key, gateway host/port, backend URL)
into the config at runtime, then launches `nanobot gateway`.
"""

import json
import os
from pathlib import Path


def resolve_config():
    """Read config.json, override fields from env vars, write config.resolved.json."""
    config_path = Path(__file__).parent / "config.json"
    # Write resolved config to /tmp since the mounted volume may not be writable
    resolved_path = Path("/tmp/nanobot/config.resolved.json")
    resolved_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path) as f:
        config = json.load(f)

    # Override provider API key and base URL from env vars
    if api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = api_key

    if api_base := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = api_base

    # Override model from env var
    if model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = model

    # Override gateway host/port from env vars
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = gateway_host

    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(gateway_port)

    # Override MCP server env vars (backend URL and API key)
    if backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url

    if lms_api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Enable webchat channel and set its host/port from env vars
    if os.environ.get("NANOBOT_WEBCHAT_ENABLED", "false").lower() == "true":
        config["channels"]["webchat"] = {
            "enabled": True,
            "allowFrom": ["*"],
        }
        if webchat_host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
            config["channels"]["webchat"]["host"] = webchat_host
        if webchat_port := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT"):
            config["channels"]["webchat"]["port"] = int(webchat_port)

    # Configure mcp_webchat MCP server if enabled
    if os.environ.get("NANOBOT_MCP_WEBSOCKET_ENABLED", "false").lower() == "true":
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "NANOBOT_UI_RELAY_URL": os.environ.get("NANOBOT_UI_RELAY_URL", ""),
                "NANOBOT_UI_RELAY_TOKEN": os.environ.get("NANOBOT_UI_RELAY_TOKEN", ""),
            },
        }

    # Configure mcp_obs MCP server for observability tools
    config["tools"]["mcpServers"]["obs"] = {
        "command": "python",
        "args": ["-m", "mcp_obs"],
        "env": {
            "NANOBOT_VICTORIALOGS_URL": os.environ.get(
                "NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"
            ),
            "NANOBOT_VICTORIATRACES_URL": os.environ.get(
                "NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:8428"
            ),
        },
    }

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}")

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", str(resolved_path), "--workspace", "./workspace"])


if __name__ == "__main__":
    resolve_config()
