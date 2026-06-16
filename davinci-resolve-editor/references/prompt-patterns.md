# Prompt Patterns — Natural Language → MCP Action

## Project Management

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Create a new project called Wedding" | `project_manager` | `create_project` | `name: "Wedding"` |
| "Save the current project" | `project_manager` | `save_project` | — |
| "Load my project 'Promo Edit'" | `project_manager` | `load_project` | `name: "Promo Edit"` |
| "List all my projects" | `project_manager` | `list_projects` | — |
| "Export the project as a DRP" | `project_manager` | `export_project` | `filePath: "/path/project.drp"` |
| "What version of Resolve is running?" | `resolve` | `get_version` | — |
| "Switch to the Color page" | `resolve` | `open_page` | `page: "color"` |
| "Go to Fusion" | `resolve` | `open_page` | `page: "fusion"` |
| "What page am I on?" | `resolve` | `get_current_page` | — |
| "Get the project settings" | `project` | `get_setting` | `name: "timelineResolutionWidth"` |
| "Set the timeline frame rate to 23.976" | `project` | `set_setting` | `name: "timelineFrameRate", value: "23.976"` |
| "Change the database" | `database` | `set_current` | `db: <db_object>` |
| "List databases" | `database` | `get_list` | — |

## Media Pool

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Import these clips" | `media_pool` | `import_media` | `items: ["/path/file.mov"]` |
| "Create a new bin called Interviews" | `media_pool` | `add_sub_folder` | `name: "Interviews"` |
| "Create a timeline from selected clips" | `media_pool` | `create_timeline_from_clips` | `name: "Assembly", clips: [...]` |
| "Append clip to the current timeline" | `media_pool` | `append_to_timeline` | `clips: [...]` |
| "Delete this clip from the pool" | `media_pool` | `delete_clips` | `clips: [<item>]` |
| "Relink the missing media" | `media_pool` | `relink_clips` | `clips: [...], folderPath: "/new/path"` |
| "Get all clips in the root bin" | `media_pool` | `get_root_folder` | → then `folder → get_clips` |
| "Set clip metadata scene to 12" | `media_pool_item` | `set_metadata` | `type: "Scene", value: "12"` |
| "Get the clip properties" | `media_pool_item` | `get_clip_property` | `property: "fps"` |
| "Link a proxy to this clip" | `media_pool_item` | `link_proxy_media` | `proxyMediaFilePath: "/path/proxy.mov"` |
| "Add a marker at frame 100 in blue" | `media_pool_item` | `add_marker` | `frameId: 100, color: "Blue", name: "Review"` |
| "Get all markers on this clip" | `media_pool_item` | `get_markers` | — |

## Timeline & Editing

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Get all clips on video track 1" | `timeline` | `get_items_in_track` | `type: "video", index: 1` |
| "How many tracks are there?" | `timeline` | `get_track_count` | `type: "video"` |
| "Add a new audio track" | `timeline` | `add_track` | `type: "audio"` |
| "Delete video track 3" | `timeline` | `delete_track` | `type: "video", index: 3` |
| "Duplicate this timeline" | `timeline` | `duplicate_timeline` | `name: "Timeline v2"` |
| "Export as AAF for Avid" | `timeline` | `export` | `fileName: "out.aaf", exportType: "EXPORT_AAF"` |
| "Export as XML for Premiere" | `timeline` | `export` | `fileName: "out.xml", exportType: "EXPORT_FCPXML_1_9"` |
| "Detect scene cuts" | `timeline` | `detect_scene_cuts` | — |
| "Add a marker at the playhead" | `timeline` | `add_marker` | `frameId: <current_frame>, color: "Yellow"` |
| "Get the timeline settings" | `timeline` | `get_setting` | `name: "useCustomSettings"` |
| "Grab a still from the current frame" | `timeline` | `grab_still` | — |

## Clip Operations

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Set this clip's opacity to 50%" | `timeline_item` | `set_property` | `key: "Opacity", value: 50` |
| "Zoom this clip to 120%" | `timeline_item` | `set_property` | `key: "ZoomX", value: 1.2` + `ZoomY: 1.2` |
| "Pan the clip 200px to the right" | `timeline_item` | `set_property` | `key: "Pan", value: 200` |
| "Set composite mode to Screen" | `timeline_item` | `set_property` | `key: "CompositeMode", value: 16` |
| "Use Optical Flow retiming" | `timeline_item` | `set_property` | `key: "RetimeProcess", value: 2` |
| "Use Speed Warp" | `timeline_item` | `set_property` | `key: "RetimeProcess", value: 3` |
| "Flip the clip horizontally" | `timeline_item` | `set_property` | `key: "FlipX", value: 1` |
| "Rotate 90 degrees" | `timeline_item` | `set_property` | `key: "RotationAngle", value: 90` |
| "Copy this grade to the next clip" | `timeline_item` | `copy_grades` | `targets: [next_item]` |
| "Create a Magic Mask" | `timeline_item` | `create_magic_mask` | `mode: "person"` |
| "Stabilize this shot" | `timeline_item` | `stabilize` | — |
| "Smart reframe for vertical" | `timeline_item` | `smart_reframe` | — |
| "Add a flag to this clip" | `timeline_item_flags` | `add_flag` | `color: "Red"` |
| "Set this clip's color to blue" | `timeline_item_flags` | `set_clip_color` | `color: "Blue"` |
| "Create a new grade version" | `timeline_item_version` | `add_version` | `name: "Client v2"` |
| "Switch to version 2" | `timeline_item_version` | `load_version` | `name: "Client v2"` |
| "List all grade versions" | `timeline_item_version` | `get_version_names` | — |

## Color Grading

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Apply this LUT to node 2" | `timeline_item_node` | `set_lut` | `nodeIndex: 2, lutPath: "/path/to.cube"` |
| "Add a serial node" | `timeline_item_node` | `add_node` | — |
| "Get the node graph" | `timeline_item_node` | `get_node_graph` | — |
| "Apply CDL values" | `timeline_item_node` | `set_cdl` | `{Slope: [r,g,b], Offset: [r,g,b], Power: [r,g,b], Saturation: 1.0}` |
| "Delete node 3" | `timeline_item_node` | `delete_node` | `nodeIndex: 3` |
| "Get all color groups" | `color_group` | `get_list` | — |
| "Add a new color group" | `color_group` | `add` | `name: "Exteriors"` |

## Gallery Stills

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Grab a still" | `gallery_stills` | `grab_still` | — |
| "Export stills to a folder" | `gallery_stills` | `export_stills` | `folderPath: "/exports/stills"` |
| "Apply this still's grade to the current clip" | `gallery_stills` | `apply_still` | `still: <still_obj>` |
| "Delete this still" | `gallery_stills` | `delete_stills` | `stills: [<still>]` |
| "List all albums" | `gallery` | `get_albums` | — |
| "Get the current album" | `gallery` | `get_current_album` | — |
| "Create a new album" | `gallery` | `create_album` | `name: "Selects"` |

## Rendering & Delivery

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Load the YouTube preset" | `render_preset` | `load` | `name: "YouTube"` |
| "Set render to 4K H.265" | `render` | `set_render_settings` | `{FormatWidth: 3840, FormatHeight: 2160}` |
| "Add to render queue" | `render` | `add_render_job` | — |
| "Start rendering" | `render` | `start_rendering` | — |
| "Stop rendering" | `render` | `stop_rendering` | — |
| "What's the render status?" | `render` | `get_render_job_status` | `jobId: "..."` |
| "List all render jobs" | `render` | `get_render_job_list` | — |
| "Delete render job 1" | `render` | `delete_render_job` | `jobId: "..."` |
| "What formats are available?" | `render` | `get_render_formats` | — |
| "What codecs are available for MP4?" | `render` | `get_render_codecs` | `renderFormat: "mp4"` |

## Fusion Compositing

| User Says | Tool | Action | Key Parameters |
|-----------|------|--------|----------------|
| "Add a Fusion comp to this clip" | `timeline_item_fusion` | `add_fusion_comp` | — |
| "How many Fusion comps does this clip have?" | `timeline_item_fusion` | `get_fusion_comp_count` | — |
| "Export the Fusion comp" | `timeline_item_fusion` | `export_fusion_comp` | `path: "/exports/comp.setting"` |
| "Delete the Fusion comp" | `timeline_item_fusion` | `delete_fusion_comp` | `name: "Comp1"` |
| "Add a Text+ node" | `fusion_comp` | `add_node` | `node_type: "TextPlus"` |
| "Add a Merge node" | `fusion_comp` | `add_node` | `node_type: "Merge"` |
| "Connect Text1 to Merge1" | `fusion_comp` | `wire_connection` | `from: "Text1", to: "Merge1"` |
| "Set font size to 0.08" | `fusion_comp` | `set_parameter` | `node: "Text1", param: "Size", value: 0.08` |
| "Add a keyframe at frame 30" | `fusion_comp` | `set_keyframe` | `node: "Text1", param: "Size", frame: 30, value: 0.2` |
| "Find the MediaIn node" | `fusion_comp` | `find_node` | `name: "MediaIn1"` |
| "Render the Fusion comp" | `fusion_comp` | `render` | — |
