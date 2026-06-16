# MCP Operations

Use the compound tools exposed by `davinci-resolve-mcp`.

| Tool | Purpose |
| --- | --- |
| `resolve` | Version, pages, app state |
| `project_manager` | Create, load, save, export projects |
| `project` | Settings, current timeline, media pool |
| `media_storage` | Filesystem and media import |
| `media_pool` | Bins, imports, timeline creation |
| `timeline` | Tracks, markers, exports, item queries |
| `timeline_item` | Properties, stabilization, markers |
| `timeline_item_node` | LUT, CDL, and node operations |
| `render` | Settings, queue, start, and status |

Always probe the current project/timeline before a write and read it back
afterward. Consult the installed MCP server's current documentation for exact
action names because its tool surface evolves independently of this skill.
