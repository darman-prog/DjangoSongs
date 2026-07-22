import logging
import time
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

API_BASE = "https://spotify23.p.rapidapi.com"

# Cache en memoria de tracks buscados (evita llamar a la API en el detalle)
_track_cache = {}
_TRACK_CACHE_TTL = 600


def _headers():
    return {
        "x-rapidapi-key": settings.RAPIDAPI_KEY,
        "x-rapidapi-host": "spotify23.p.rapidapi.com",
    }


def _extraer_artistas(artists_data):
    if isinstance(artists_data, list):
        return ", ".join(a.get("name", "") for a in artists_data)
    items = artists_data.get("items") if isinstance(artists_data, dict) else None
    if items:
        return ", ".join(a.get("name", "") for a in items)
    return ""


def _extraer_url_imagen(t):
    album = t.get("album")
    if isinstance(album, dict):
        images = album.get("images") or album.get("coverArt") or {}
        if isinstance(images, list):
            return images[0]["url"] if images else ""
        items = images.get("items") if isinstance(images, dict) else None
        if items:
            return items[0]["url"] if items else ""
    alt = t.get("albumOfTrack")
    if isinstance(alt, dict):
        cover = alt.get("coverArt")
        if isinstance(cover, dict):
            sources = cover.get("sources") or cover.get("items") or []
            if isinstance(sources, list) and sources:
                return sources[0].get("url", "")
    return ""


def _parsear_track(t):
    return {
        "id": t.get("id", ""),
        "nombre": t.get("name", ""),
        "artistas": _extraer_artistas(t.get("artists", [])),
        "album": t.get("album", {}).get("name", "") if isinstance(t.get("album"), dict) else "",
        "portada": _extraer_url_imagen(t),
        "spotify_url": (t.get("external_urls", {}) if isinstance(t.get("external_urls"), dict) else {}).get("spotify", "")
                        or (t.get("uri", "").replace("spotify:track:", "https://open.spotify.com/track/") if t.get("uri") else ""),
        "preview_url": t.get("preview_url"),
        "duracion_ms": t.get("duration_ms", 0),
    }


def _cachear_track(track_data):
    tid = track_data.get("id")
    if tid:
        _track_cache[tid] = {
            "data": track_data,
            "expires": time.time() + _TRACK_CACHE_TTL,
        }


def _obtener_de_cache(track_id):
    entry = _track_cache.get(track_id)
    if entry and time.time() < entry["expires"]:
        return entry["data"]
    if entry:
        del _track_cache[track_id]
    return None


def buscar_canciones(query, limit=20):
    try:
        resp = requests.get(
            f"{API_BASE}/search/",
            headers=_headers(),
            params={"q": query, "type": "multi", "offset": 0, "limit": limit, "numberOfTopResults": 5},
            timeout=15,
        )
        if resp.status_code == 429:
            logger.warning("Rate limit de RapidAPI alcanzado")
            return None
        resp.raise_for_status()
        data = resp.json()
        tracks_container = data.get("tracks") or data.get("track") or {}
        items = tracks_container.get("items", [])
        resultados = []
        for item in items:
            track_data = item.get("data") if isinstance(item, dict) else item
            if track_data:
                parsed = _parsear_track(track_data)
                _cachear_track(parsed)
                resultados.append(parsed)
        return resultados
    except requests.RequestException as e:
        logger.error("Error en búsqueda Spotify vía RapidAPI: %s", e)
        return None


def obtener_detalle_track(track_id):
    cached = _obtener_de_cache(track_id)
    if cached:
        return cached
    try:
        resp = requests.get(
            f"{API_BASE}/track/",
            headers=_headers(),
            params={"id": track_id},
            timeout=15,
        )
        if resp.status_code == 429:
            logger.warning("Rate limit de RapidAPI alcanzado")
            return None
        resp.raise_for_status()
        data = resp.json()
        track_data = data.get("data") if isinstance(data, dict) else data
        if isinstance(track_data, dict) and track_data.get("id"):
            parsed = _parsear_track(track_data)
            _cachear_track(parsed)
            return parsed
        for key in ("tracks", "track"):
            group = data.get(key)
            if isinstance(group, list) and group:
                candidate = group[0].get("data") if isinstance(group[0], dict) else group[0]
                if isinstance(candidate, dict) and candidate.get("id"):
                    parsed = _parsear_track(candidate)
                    _cachear_track(parsed)
                    return parsed
            if isinstance(group, dict):
                items = group.get("items", [])
                if items:
                    candidate = items[0].get("data") if isinstance(items[0], dict) else items[0]
                    if isinstance(candidate, dict) and candidate.get("id"):
                        parsed = _parsear_track(candidate)
                        _cachear_track(parsed)
                        return parsed
        if isinstance(data, dict) and data.get("id"):
            parsed = _parsear_track(data)
            _cachear_track(parsed)
            return parsed
        logger.warning("Formato inesperado en detalle de track %s: %s", track_id, data)
        return None
    except requests.RequestException as e:
        logger.error("Error obteniendo detalle de track %s vía RapidAPI: %s", track_id, e)
        return None
