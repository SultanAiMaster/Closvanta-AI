import asyncio
from datetime import datetime, timezone

import httpx

from app.models import Lead


REDDIT_BASE = "https://www.reddit.com/r/{subreddit}/new.json"


class RedditScraper:
    def __init__(self, user_agent: str, timeout: float = 15.0, min_request_gap: float = 1.0):
        self.user_agent = user_agent
        self.timeout = timeout
        self.min_request_gap = min_request_gap
        self._last_request = 0.0

    async def _throttle(self) -> None:
        now = asyncio.get_running_loop().time()
        wait = self.min_request_gap - (now - self._last_request)
        if wait > 0:
            await asyncio.sleep(wait)
        self._last_request = asyncio.get_running_loop().time()

    async def fetch_subreddit(self, subreddit: str, limit: int = 25) -> list[Lead]:
        await self._throttle()
        headers = {"User-Agent": self.user_agent, "Accept": "application/json"}
        params = {"limit": min(max(limit, 1), 100), "raw_json": 1}
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            response = await client.get(REDDIT_BASE.format(subreddit=subreddit), headers=headers, params=params)
            response.raise_for_status()
            payload = response.json()

        leads: list[Lead] = []
        for child in payload.get("data", {}).get("children", []):
            data = child.get("data", {})
            if not data.get("id"):
                continue
            created = data.get("created_utc")
            created_at = datetime.fromtimestamp(created, tz=timezone.utc).isoformat() if created else None
            leads.append(
                Lead(
                    source="reddit",
                    external_id=data["id"],
                    url=(f"https://www.reddit.com{data['permalink']}" if data.get("permalink") else None),
                    author=data.get("author"),
                    title=data.get("title", ""),
                    body=data.get("selftext", ""),
                    created_at=created_at,
                )
            )
        return leads

    async def fetch_many(self, subreddits: list[str], limit: int = 25) -> list[Lead]:
        results: list[Lead] = []
        for subreddit in subreddits:
            results.extend(await self.fetch_subreddit(subreddit, limit))
        return results
