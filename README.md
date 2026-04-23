# Valorant Fanbase API

A FastAPI wrapper around [valorant-api.com](https://valorant-api.com) — structured like a fanbase wiki, similar to PokéAPI.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | HTML frontend (agent browser + API explorer) |
| GET | `/characters` | List all playable Valorant agents |
| GET | `/characters/{name}` | Get a single agent by name (case-insensitive) |
| GET | `/actors` | Simplified cast list (name, role, icon) |
| GET | `/docs` | Auto-generated Swagger UI |

## Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: http://localhost:8000

## Deploy to Render (Free Tier)

1. Push this folder to a GitHub repository
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3
5. Click **Deploy**

The `render.yaml` file is already included — Render will auto-detect it.

## Example Responses

### `GET /characters`
```json
{
  "count": 25,
  "characters": [
    {
      "uuid": "...",
      "name": "Jett",
      "role": "Duelist",
      "description": "Representing her home country of South Korea...",
      "portrait": "https://media.valorant-api.com/agents/.../fullportrait.png",
      "icon": "...",
      "background": "...",
      "role_icon": "..."
    }
  ]
}
```

### `GET /characters/jett`
Returns full agent detail including `abilities[]` array with slot, name, description, and icon.

### `GET /actors`
```json
{
  "count": 25,
  "actors": [
    { "name": "Brimstone", "role": "Controller", "icon": "..." }
  ]
}
```

---
Data © Riot Games. This is an unofficial fan project.
