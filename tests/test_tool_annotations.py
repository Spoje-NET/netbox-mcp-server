"""Every tool must carry a title and complete ToolAnnotations."""

import asyncio

from netbox_mcp_server.server import mcp


def test_every_tool_has_title_and_annotations():
    tools = asyncio.run(mcp.list_tools())
    assert tools
    for tool in tools:
        assert tool.title and tool.title != tool.name, tool.name
        a = tool.annotations
        assert a is not None, tool.name
        for hint in (
            "read_only_hint",
            "destructive_hint",
            "idempotent_hint",
            "open_world_hint",
        ):
            assert getattr(a, hint) is not None, f"{tool.name}: {hint} unset"
        assert not (a.read_only_hint and a.destructive_hint), tool.name
        if tool.name.startswith(("get_", "list_", "search_", "netbox_get", "netbox_search")):
            assert a.read_only_hint is True, tool.name
