# Configuration

## Decision Order

1. Detect local tools and configured environment variables.
2. Explain which requested stage needs which dependency.
3. Ask whether the user wants to configure each missing optional dependency.
4. Configure only what the user accepts.
5. Test without printing secrets.
6. Skip declined optional stages.

## Multimodal LLM

Use an OpenAI-compatible endpoint:

```env
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=...
LLM_MODEL=...
LLM_SUPPORTS_IMAGES=1
```

The chosen model must support image input for frame analysis. Never assume a
specific provider or model. Ask permission before a large/billable batch.

## TTS

TTS is optional:

```env
TTS_BASE_URL=https://provider.example/v1
TTS_API_KEY=...
TTS_MODEL=...
TTS_REFERENCE_AUDIO=/absolute/path/to/reference.wav
```

The bundled script supports JSON and multipart HTTP modes through command-line
options. Provider-specific payload fields belong in a user-owned JSON config.
If the user declines TTS configuration, disable TTS and continue.

## DaVinci Resolve MCP

Install upstream:

```bash
npx davinci-resolve-mcp setup
```

Open Resolve Studio and set external scripting to `Local`. Restart or refresh
the MCP client after configuration. Verify with `resolve -> get_version`.

An `.mcp.json` entry proves configuration, not successful registration.

## Local Tools

- Python 3.10+
- `ffmpeg`
- `ffprobe`
- Optional Node.js 18.17+ for the Resolve MCP installer
- DaVinci Resolve Studio 18.5+ for external scripting
