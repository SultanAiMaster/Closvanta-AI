import time
from collections import defaultdict, deque

from fastapi import HTTPException


class InMemoryRateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] > self.window_seconds:
            q.popleft()
        if len(q) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        q.append(now)


rate_limiter = InMemoryRateLimiter()
