# Hoopstreet API Documentation v9.3.2

## Core Functions

### execute_phase(phase_num, phase_code, max_retries=3)
Executes a single phase with auto-retry

### detect_phases(code)
Detects # Phase N markers in code

### log(msg)
Logs to DNA.md and logs.txt

## Webhook Endpoints

### POST /webhook/sync
Trigger sync operation

### GET /status
Returns system status

## Environment Variables

| Variable | Purpose |
|----------|---------|
| SUPABASE_URL | Cloud sync URL |
| SUPABASE_ANON_KEY | Supabase API key |
| GITHUB_TOKEN | GitHub authentication |
| TELEGRAM_TOKEN | Telegram bot token |
| TELEGRAM_CHAT_ID | Telegram chat ID |
