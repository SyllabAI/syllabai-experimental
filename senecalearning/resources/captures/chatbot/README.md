# Chatbot ("Amelia" AI Assistant) captures — session 8, 2026-10-22

Sanitized evidence for the chatbot reverse engineering (see
`research/2026-10-22-chatbot-ai.md` for the full write-up).

| File | What |
|---|---|
| `endpoints-contract.json` | Machine-readable ChatbotServiceClient contract: all 14 methods, wire calls, auth style, streaming-vs-JSON, observed response shapes, StreamErrors enum, model/RAG constants |
| `live-probe-evidence.md` | Sanitized live-probe log (teacher account, free tier): session CRUD works, AI endpoints gated; includes raw response headers proving 200 + `text/event-stream` with error-as-body |

Sanitization statement:

- No JWTs, no credentials, no user IDs, no student PII — probe bodies contain only
  error messages and empty-list responses; checked by grep for token prefix
  (`eyJhbGci`) and account email before commit.
- Probe session UUIDs are random client-generated identifiers, not PII.
- No Seneca content bodies are reproduced here (constants and error strings only,
  consistent with IP-AND-COPYRIGHT-NOTES.md).
- Original raw probe artifacts remain local-only (`probe-results/chatbot/`).
