from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import httpx
from typing import Optional

app = FastAPI(
    title="Valorant Fanbase API",
    description="A fanbase API wrapper for Valorant agents, built on top of valorant-api.com",
    version="1.0.0"
)

VALORANT_API_BASE = "https://valorant-api.com/v1"


async def fetch_from_valorant(path: str, params: dict = None):
    async with httpx.AsyncClient(timeout=10.0) as client:
        url = f"{VALORANT_API_BASE}{path}"
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


# ── Characters (Agents) ────────────────────────────────────────────────────────

@app.get("/characters", summary="List all Valorant agents/characters")
async def get_all_characters(language: Optional[str] = "en-US"):
    """Returns a list of all Valorant agents (characters)."""
    data = await fetch_from_valorant("/agents", params={"language": language, "isPlayableCharacter": "true"})
    agents = data.get("data", [])
    return {
        "count": len(agents),
        "characters": [
            {
                "uuid": a["uuid"],
                "name": a["displayName"],
                "role": a.get("role", {}).get("displayName") if a.get("role") else None,
                "description": a.get("description"),
                "portrait": a.get("fullPortraitV2") or a.get("fullPortrait"),
                "icon": a.get("displayIcon"),
                "background": a.get("background"),
                "role_icon": a.get("role", {}).get("displayIcon") if a.get("role") else None,
            }
            for a in agents
        ]
    }


@app.get("/characters/{name}", summary="Get a single character by name")
async def get_character(name: str, language: Optional[str] = "en-US"):
    """Returns detailed info for a specific Valorant agent by name (case-insensitive)."""
    data = await fetch_from_valorant("/agents", params={"language": language, "isPlayableCharacter": "true"})
    agents = data.get("data", [])
    match = next(
        (a for a in agents if a["displayName"].lower() == name.lower()),
        None
    )
    if not match:
        available = [a["displayName"] for a in agents]
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Character '{name}' not found.",
                "available_characters": available
            }
        )
    abilities = [
        {
            "slot": ab.get("slot"),
            "name": ab.get("displayName"),
            "description": ab.get("description"),
            "icon": ab.get("displayIcon"),
        }
        for ab in match.get("abilities", [])
    ]
    return {
        "uuid": match["uuid"],
        "name": match["displayName"],
        "role": match.get("role", {}).get("displayName") if match.get("role") else None,
        "role_icon": match.get("role", {}).get("displayIcon") if match.get("role") else None,
        "description": match.get("description"),
        "portrait": match.get("fullPortraitV2") or match.get("fullPortrait"),
        "icon": match.get("displayIcon"),
        "background": match.get("background"),
        "background_gradient_colors": match.get("backgroundGradientColors", []),
        "abilities": abilities,
    }


# ── Actors (voice actors / dev info) ──────────────────────────────────────────

@app.get("/actors", summary="List all agent names (actors in the Valorant universe)")
async def get_actors(language: Optional[str] = "en-US"):
    """Returns a simplified list of all agent names — the 'cast' of Valorant."""
    data = await fetch_from_valorant("/agents", params={"language": language, "isPlayableCharacter": "true"})
    agents = data.get("data", [])
    return {
        "count": len(agents),
        "actors": [
            {
                "name": a["displayName"],
                "role": a.get("role", {}).get("displayName") if a.get("role") else None,
                "icon": a.get("displayIconSmall") or a.get("displayIcon"),
            }
            for a in agents
        ]
    }


# ── Root / HTML frontend ───────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    with open("static/index.html") as f:
        return f.read()


app.mount("/static", StaticFiles(directory="static"), name="static")
