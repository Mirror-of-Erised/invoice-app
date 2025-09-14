export function getRelays() {
  const raw = import.meta.env.VITE_NOSTR_RELAYS || "wss://relay.damus.io";
  return raw.split(",").map(s => s.trim());
}

export async function publish(kind: number, content: string, tags: string[][] = []) {
  // Browser stub – in real impl, use a Nostr lib (e.g., nostr-tools)
  return { ok: true, kind, content, relays: getRelays(), tags };
}
