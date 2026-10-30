"""Every tool parameter must carry a description (MCP server standards, section 1)."""

import asyncio

from netbox_mcp_server.server import mcp


def test_every_tool_parameter_has_description():
    tools = asyncio.run(mcp.list_tools())
    assert tools
    for tool in tools:
        for name, schema in tool.parameters["properties"].items():
            assert schema.get("description"), f"{tool.name}.{name} has no description"
