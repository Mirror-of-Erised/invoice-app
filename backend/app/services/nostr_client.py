"""Minimal Nostr client stub (Python)"""
import os
import json


class NostrClient:
    def __init__(self, relays: list[str] | None = None):
        self.relays = relays or os.getenv("NOSTR_RELAYS", "wss://relay.damus.io").split(",")


def publish_event(self, kind: int, content: str, tags: list[list[str]] | None = None):
# TODO: sign and send over websockets
    return {"relay_count": len(self.relays), "kind": kind, "content": content, "tags": tags or []}
