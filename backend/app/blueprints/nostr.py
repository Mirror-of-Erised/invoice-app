from flask import Blueprint, request
from ..services.nostr_client import NostrClient


nostr_bp = Blueprint("nostr", __name__)


@nostr_bp.post("/publish")
def publish():
    payload = request.json or {}
    client = NostrClient()
    result = client.publish_event(kind=payload.get("kind", 1),
            content=payload.get("content", ""),
            tags=payload.get("tags", []))
    return {"ok": True, "result": result}
