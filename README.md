# notify-api

A lightweight FastAPI service that forwards notifications to a Telegram chat via Bot API. Drop it behind any CI/CD pipeline, script, or internal tool to get instant Telegram alerts with a single HTTP call.

---

## How it works

```
POST /send  →  [✅ my-project]\nDeploy finished  →  Telegram
```

The API receives a JSON payload, formats it as `[{emoji} {project}]\n{message}`, and sends it to a configured Telegram chat. Authentication is done via a static Bearer token.

---

## Requirements

- Python 3.12+
- A [Telegram Bot](https://core.telegram.org/bots#botfather) token
- The chat ID where notifications should land (user, group, or channel)

---

## Environment variables

| Variable              | Required | Description                                      |
|-----------------------|----------|--------------------------------------------------|
| `TELEGRAM_BOT_TOKEN`  | yes      | Token from [@BotFather](https://t.me/BotFather)  |
| `TELEGRAM_CHAT_ID`    | yes      | Target chat ID (e.g. `-100xxxxxxxxxx` for groups)|
| `API_TOKEN`           | yes      | Secret used to authenticate incoming requests    |

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

---

## Running locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The interactive docs will be available at `http://localhost:8000/docs`.

---

## Running with Docker

```bash
docker build -t notify-api .
docker run --env-file .env -p 8000:8000 notify-api
```

---

## API reference

### `POST /send`

**Headers**

```
Authorization: Bearer <API_TOKEN>
Content-Type: application/json
```

**Body**

| Field     | Type   | Required | Default | Description                        |
|-----------|--------|----------|---------|------------------------------------|
| `project` | string | yes      | —       | Project or service name            |
| `message` | string | yes      | —       | Notification body                  |
| `emoji`   | string | no       | `🔔`   | Emoji prefix shown in the header   |

**Example request**

```bash
curl -X POST https://your-api.railway.app/send \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"project":"my-app","message":"Deploy finished in 42s","emoji":"✅"}'
```

**Responses**

| Status | Meaning                                         |
|--------|-------------------------------------------------|
| `204`  | Notification sent successfully                  |
| `401`  | Missing or invalid Bearer token                 |
| `422`  | Malformed request body                          |
| `502`  | Telegram API returned an error                  |

**Resulting Telegram message**

```
[✅ my-app]
Deploy finished in 42s
```

---

## Clients

### Shell (`notify.sh`)

Reads `NOTIFY_URL` and `NOTIFY_TOKEN` from the environment.

```bash
chmod +x notify.sh

# Basic usage
./notify.sh "my-app" "Deploy finished" "✅"

# With explicit env vars
NOTIFY_URL=https://your-api.railway.app \
NOTIFY_TOKEN=your-token \
  ./notify.sh "my-app" "Deploy finished" "✅"
```

Add it to a CI step:

```yaml
# GitHub Actions example
- name: Notify
  env:
    NOTIFY_URL: ${{ secrets.NOTIFY_URL }}
    NOTIFY_TOKEN: ${{ secrets.NOTIFY_TOKEN }}
  run: ./notify.sh "my-app" "Deploy to production succeeded" "🚀"
```

### Python (`notify.py`)

Requires `httpx` (`pip install httpx`). Can be used as a script or imported as a module.

```bash
# As a script
NOTIFY_URL=https://your-api.railway.app \
NOTIFY_TOKEN=your-token \
  python notify.py "my-app" "Deploy finished" "✅"
```

```python
# As a module
import os
os.environ["NOTIFY_URL"] = "https://your-api.railway.app"
os.environ["NOTIFY_TOKEN"] = "your-token"

from notify import send
send(project="my-app", message="Migration complete", emoji="🗄️")
```

---

## Deploy on Railway

This repo includes a `railway.toml` pre-configured for Railway.

1. Push this repository to GitHub.
2. Create a new Railway project and connect the repo.
3. Set the environment variables in the Railway dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `API_TOKEN`
4. Railway detects the `Dockerfile` via `railway.toml` and deploys automatically.

Railway injects `$PORT` at runtime — the start command in `railway.toml` handles that automatically.

---

## Getting your Telegram credentials

**Bot token**

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the token (format: `123456789:AAxxxx...`)

**Chat ID**

- **Personal chat:** message [@userinfobot](https://t.me/userinfobot) — it replies with your chat ID.
- **Group:** add your bot to the group, send a message, then call:
  ```
  https://api.telegram.org/bot<TOKEN>/getUpdates
  ```
  Look for `"chat":{"id":...}` in the response.
- **Channel:** add your bot as admin, then use the channel username (e.g. `@mychannel`) or its numeric ID (prefixed with `-100`).

---

## Project structure

```
notify-api/
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container image
├── railway.toml      # Railway deployment config
├── .env.example      # Environment variable template
├── notify.sh         # Bash client
└── notify.py         # Python client
```

---

## License

MIT
