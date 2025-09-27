#!/usr/bin/env python3
import argparse, os, re, sys, time, hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

UA = "ImgGrabber/1.0 (+your@email)"

def safe_name(name: str) -> str:
    name = re.sub(r"[^\w.\-]+", "_", name)
    return name[:120] or "image"

def guess_ext(ct: str, url: str) -> str:
    if ct:
        ct = ct.lower().split(";")[0].strip()
        mapping = {
            "image/jpeg": ".jpg", "image/jpg": ".jpg",
            "image/png": ".png", "image/webp": ".webp",
            "image/gif": ".gif", "image/svg+xml": ".svg",
            "image/bmp": ".bmp", "image/tiff": ".tif", "image/x-icon": ".ico",
            "image/avif": ".avif", "image/heic": ".heic", "image/heif": ".heif",
        }
        if ct in mapping: return mapping[ct]
    # fallback to URL path
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    return ext if ext in {".jpg",".jpeg",".png",".webp",".gif",".svg",".bmp",".tif",".tiff",".ico",".avif",".heic",".heif"} else ""

def collect_image_urls(page_url: str, html: str):
    soup = BeautifulSoup(html, "html.parser")
    urls = set()

    # <img src> and srcset variants
    for img in soup.find_all("img"):
        src = img.get("src") or ""
        if src:
            urls.add(urljoin(page_url, src))
        srcset = img.get("srcset") or ""
        for part in srcset.split(","):
            cand = part.strip().split(" ")[0]
            if cand:
                urls.add(urljoin(page_url, cand))

    # common meta/og images
    for sel in ('meta[property="og:image"]', 'meta[name="twitter:image"]', 'link[rel="image_src"]'):
        for tag in soup.select(sel):
            content = tag.get("content") or tag.get("href")
            if content:
                urls.add(urljoin(page_url, content))

    # CSS background-images in inline styles (simple catch)
    for tag in soup.select("[style*='background']"):
        style = tag.get("style") or ""
        m = re.findall(r"url\((['\"]?)(.+?)\1\)", style)
        for _, u in m:
            urls.add(urljoin(page_url, u))

    # basic filtering: only likely image extensions or will be verified by HEAD/GET
    return list(urls)

def head_or_get(url: str, session: requests.Session, timeout=20):
    try:
        r = session.head(url, allow_redirects=True, timeout=timeout)
        if r.status_code >= 400 or not r.headers.get("Content-Type", "").startswith("image"):
            # some servers don't support HEAD properly
            r = session.get(url, stream=True, allow_redirects=True, timeout=timeout)
        return r
    except Exception:
        return None

def download(url: str, outdir: Path, session: requests.Session, min_bytes: int, same_origin: bool, origin_netloc: str):
    if same_origin and urlparse(url).netloc and urlparse(url).netloc != origin_netloc:
        return None

    r = head_or_get(url, session)
    if not r or r.status_code >= 400:
        return None
    ct = r.headers.get("Content-Type", "").lower()
    if not ct.startswith("image"):
        # try to sniff by extension; if not image, skip
        if not guess_ext("", url):
            return None

    # decide filename
    ext = guess_ext(ct, url) or ".bin"
    url_path_name = os.path.basename(urlparse(url).path) or hashlib.sha1(url.encode()).hexdigest()[:10] + ext
    base = safe_name(os.path.splitext(url_path_name)[0]) + ext
    dest = outdir / base
    # avoid clobber
    i = 1
    while dest.exists():
        dest = outdir / f"{safe_name(os.path.splitext(url_path_name)[0])}_{i}{ext}"
        i += 1

    # stream to disk
    try:
        with session.get(r.url, stream=True, timeout=60) as resp:
            resp.raise_for_status()
            size = 0
            dest_tmp = dest.with_suffix(dest.suffix + ".part")
            with open(dest_tmp, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if not chunk: continue
                    f.write(chunk)
                    size += len(chunk)
            if size < min_bytes:
                dest_tmp.unlink(missing_ok=True)
                return None
            dest_tmp.rename(dest)
            return dest
    except Exception:
        try:
            dest.unlink(missing_ok=True)
            (dest.with_suffix(dest.suffix + ".part")).unlink(missing_ok=True)
        except Exception:
            pass
        return None

def main():
    ap = argparse.ArgumentParser(description="Download all images found on a webpage.")
    ap.add_argument("url", help="Page URL")
    ap.add_argument("-o","--out", default="images", help="Output folder (default: images)")
    ap.add_argument("--min-bytes", type=int, default=2048, help="Skip images smaller than this (default: 2048)")
    ap.add_argument("--same-origin", action="store_true", help="Only download images from the same domain")
    ap.add_argument("--delay", type=float, default=0.0, help="Delay between downloads in seconds")
    args = ap.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "*/*"})
    session.max_redirects = 5

    # fetch page
    resp = session.get(args.url, timeout=30)
    resp.raise_for_status()

    origin_netloc = urlparse(args.url).netloc
    candidates = collect_image_urls(args.url, resp.text)

    seen = set()
    saved = []
    for u in candidates:
        u = u.split("#")[0]
        if u in seen: continue
        seen.add(u)
        dest = download(u, outdir, session, args.min_bytes, args.same_origin, origin_netloc)
        if dest:
            saved.append(dest.name)
            if args.delay: time.sleep(args.delay)

    print(f"Found {len(candidates)} candidates; saved {len(saved)} files in '{outdir}'.")
    if saved:
        for name in saved:
            print(" -", name)

if __name__ == "__main__":
    # Basic ToS/robots courte