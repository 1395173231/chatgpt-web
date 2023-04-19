import functools
import time

from fastapi import HTTPException


def rate_limit_by_ip(max_requests_per_hour: int):
    cache = {}

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            remote_addr = args[0].client.host
            if remote_addr not in cache:
                cache[remote_addr] = {"requests": 0, "last_request_time": time.time()}

            now = time.time()
            elapsed_time = now - cache[remote_addr]["last_request_time"]
            if elapsed_time < 60 * 60:
                # 如果在限制时间内已达到最大限制数量，则返回“429 Too Many Requests”。
                if cache[remote_addr]["requests"] >= max_requests_per_hour:
                    raise HTTPException(status_code=429, detail="Too many requests")
                else:
                    cache[remote_addr]["requests"] += 1
            else:
                #如果超过限制时间，重置请求计数器和最后一次请求时间。
                cache[remote_addr]["requests"] = 1
                cache[remote_addr]["last_request_time"] = now

            return await func(*args, **kwargs)

        return wrapper

    return decorator
