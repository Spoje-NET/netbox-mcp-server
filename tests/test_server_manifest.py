"""server.json (read by mcprack) must stay in sync with the README env table and Settings."""

import json
import re
from pathlib import Path

from netbox_mcp_server.config import Settings

ROOT = Path(__file__).resolve().parent.parent


def _manifest_names():
    data = json.loads((ROOT / "debian" / "server.json").read_text())
    return data, [e["name"] for e in data["environmentVariables"]]


def test_manifest_variables_are_documented_in_readme():
    _, names = _manifest_names()
    readme = (ROOT / "README.md").read_text()
    table = readme.split("### Configuration Reference", 1)[1].split("###", 1)[0]
    documented = set(re.findall(r"^\| `([A-Z_]+)` \|", table, re.M))
    assert set(names) == documented


def test_manifest_variables_match_settings_fields():
    _, names = _manifest_names()
    fields = {n.upper() for n in Settings.model_fields}
    assert set(names) <= fields


def test_manifest_flags_secrets_and_required():
    data, _ = _manifest_names()
    by_name = {e["name"]: e for e in data["environmentVariables"]}
    assert by_name["NETBOX_URL"]["isRequired"] and not by_name["NETBOX_URL"].get("isSecret")
    assert by_name["NETBOX_TOKEN"]["isRequired"] and by_name["NETBOX_TOKEN"]["isSecret"]
    assert by_name["MCP_AUTH_TOKEN"]["isSecret"]
    assert all("default" not in by_name[n] for n in ("NETBOX_TOKEN", "MCP_AUTH_TOKEN"))
