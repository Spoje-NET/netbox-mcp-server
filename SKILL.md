---
name: netbox-lookup
description: Query a NetBox instance (DCIM, IPAM, circuits, virtualization, tenancy, VPN, wireless) through the read-only mcp-server-netbox MCP server. Use when a user asks about devices, sites, racks, IP addresses, prefixes, VLANs, interfaces, circuits or recent NetBox changes.
---

# NetBox Lookup

This skill uses the tools exposed by the `mcp-server-netbox` MCP server
(https://github.com/Spoje-NET/netbox-mcp-server). The server is read-only:
every tool only issues GET requests, so nothing in NetBox can be modified.

## When to use this

- Find a device, site, rack, prefix, IP address, VLAN or circuit.
- Look up a single object when its ID is already known.
- Check who changed what and when (changelog).
- Search across several object types when the object type is unknown.

## Workflow

1. Unsure what the object is: call `netbox_search_objects` with the term
   (optionally restrict `object_types`).
2. Know the type: call `netbox_get_objects` with `object_type`
   (e.g. `dcim.device`) and `filters`. Keep `limit` small and ask only for the
   `fields` you need; use `brief=true` for overviews.
3. Know the ID: call `netbox_get_object_by_id`.
4. For audit questions call `netbox_get_changelogs` with filters such as
   `user`, `changed_object_type` or `time_after`.

## Tips

- Results are paginated (`limit` 1-100, `offset`); report when more exist.
- Filters are NetBox API filters, e.g. `{"site": "praha", "status": "active"}`.
- Never invent object IDs; search first.
