import argparse
import asyncio
import os
from typing import List

import aiofiles
import aiohttp


LIST_URL = "https://picsum.photos/v2/list"


async def fetch_image_list(session: aiohttp.ClientSession, limit: int) -> List[dict]:
    images = []
    page = 1
    while len(images) < limit:
        per_page = min(limit - len(images), 100)
        async with session.get(LIST_URL, params={"page": page, "limit": per_page}) as resp:
            resp.raise_for_status()
            data = await resp.json()
        if not data:
            break
        images.extend(data[: limit - len(images)])
        if len(data) < per_page:
            break
        page += 1
    return images[:limit]


async def download_one(
    session: aiohttp.ClientSession,
    url: str,
    path: str,
) -> str:
    async with session.get(url) as resp:
        resp.raise_for_status()
        body = await resp.read()
    async with aiofiles.open(path, "wb") as f:
        await f.write(body)
    return path


async def download_all(count: int, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        images = await fetch_image_list(session, count)
        if len(images) < count:
            raise RuntimeError(
                f"Requested {count} images, got only {len(images)} from API"
            )
        tasks = [
            download_one(
                session,
                img["download_url"],
                os.path.join(out_dir, f"image_{i}.jpg"),
            )
            for i, img in enumerate(images)
        ]
        await asyncio.gather(*tasks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Async download images from picsum.photos")
    parser.add_argument(
        "count",
        type=int,
        help="Number of different images to download",
    )
    parser.add_argument(
        "out_dir",
        nargs="?",
        default="artifacts",
        help="Output directory (default: artifacts)",
    )
    args = parser.parse_args()
    if args.count < 1:
        parser.error("count must be >= 1")
    asyncio.run(download_all(args.count, args.out_dir))
    print(f"Downloaded {args.count} images to {args.out_dir}")


if __name__ == "__main__":
    main()
