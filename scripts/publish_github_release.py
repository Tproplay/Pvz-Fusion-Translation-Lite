#!/usr/bin/env python3
"""Publish PvZ Fusion 4.0.5 English Release to GitHub.

Creates or updates the GitHub release for tag v4.0.5 and uploads:
1. PvZ-Fusion-4.0.5-English-PC.zip
2. PvZ-Fusion-4.0.5-English-Android.apk
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def get_github_token() -> str:
    # 1. Environment variable
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token

    # 2. Git credential helper
    try:
        p = subprocess.Popen(
            ["git", "credential", "fill"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        out, _ = p.communicate("protocol=https\nhost=github.com\n\n")
        data = dict(line.split("=", 1) for line in out.strip().splitlines() if "=" in line)
        if data.get("password"):
            return data["password"]
    except Exception as e:
        print(f"Warning: git credential fill failed: {e}")

    raise RuntimeError("Could not obtain GitHub token. Set GITHUB_TOKEN environment variable.")


def api_request(
    url: str,
    token: str,
    method: str = "GET",
    data: dict | None = None,
) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "PvZ-Fusion-Release-Builder",
    }
    payload = None
    if data is not None:
        payload = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        if resp.status == 204:
            return {}
        return json.loads(resp.read().decode("utf-8"))


def upload_asset_with_curl(
    upload_url_base: str,
    token: str,
    file_path: Path,
    asset_name: str,
) -> None:
    encoded_name = urllib.parse.quote(asset_name)
    target_url = f"{upload_url_base}?name={encoded_name}"
    size_mb = file_path.stat().st_size / (1024 * 1024)
    print(f"\n--> Uploading {asset_name} ({size_mb:.2f} MB) via curl...")

    cmd = [
        "curl.exe",
        "-L",
        "-X", "POST",
        "-H", f"Authorization: Bearer {token}",
        "-H", "Content-Type: application/octet-stream",
        "-H", "Accept: application/vnd.github+json",
        "--upload-file", str(file_path),
        "--progress-bar",
        target_url,
    ]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        raise RuntimeError(f"curl upload failed with code {res.returncode}")
    print(f"\nUploaded {asset_name} successfully.")


def publish_release(
    owner: str = "Tproplay",
    repo: str = "Pvz-Fusion-Translation-Lite",
    tag: str = "v4.0.5",
    name: str = "PvZ: Fusion v4.0.5 — English Release (PC & Android)",
    notes_file: Path | None = None,
    pc_zip: Path | None = None,
    android_apk: Path | None = None,
) -> int:
    token = get_github_token()

    if notes_file and notes_file.exists():
        body = notes_file.read_text(encoding="utf-8")
    else:
        body = f"# PvZ Fusion {tag} English Release\n\nDual-platform release for Windows PC and Android."

    repo_url = f"https://api.github.com/repos/{owner}/{repo}"

    print(f"Checking existing release for tag {tag} in {owner}/{repo}...")
    release_info = None
    try:
        release_info = api_request(f"{repo_url}/releases/tags/{tag}", token)
        print(f"Found existing release: ID {release_info['id']} ({release_info['html_url']})")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"No release found for {tag}. Creating new release...")
        else:
            raise

    if release_info is None:
        create_data = {
            "tag_name": tag,
            "target_commitish": "main",
            "name": name,
            "body": body,
            "draft": False,
            "prerelease": False,
        }
        release_info = api_request(f"{repo_url}/releases", token, method="POST", data=create_data)
        print(f"Created release: ID {release_info['id']} ({release_info['html_url']})")
    else:
        # Update existing release body and title
        update_data = {
            "name": name,
            "body": body,
        }
        release_info = api_request(
            f"{repo_url}/releases/{release_info['id']}",
            token,
            method="PATCH",
            data=update_data,
        )
        print(f"Updated release metadata for ID {release_info['id']}")

    # Clean upload_url (remove template "{?name,label}")
    raw_upload_url = release_info["upload_url"]
    upload_url_base = raw_upload_url.split("{")[0]

    # Check existing assets to delete if replacing
    existing_assets = {a["name"]: a["id"] for a in release_info.get("assets", [])}

    assets_to_upload = []
    if pc_zip and pc_zip.exists():
        assets_to_upload.append((pc_zip, pc_zip.name))
    if android_apk and android_apk.exists():
        assets_to_upload.append((android_apk, android_apk.name))

    for path, asset_name in assets_to_upload:
        if asset_name in existing_assets:
            asset_id = existing_assets[asset_name]
            print(f"Deleting existing asset {asset_name} (ID: {asset_id})...")
            api_request(f"{repo_url}/releases/assets/{asset_id}", token, method="DELETE")
        upload_asset_with_curl(upload_url_base, token, path, asset_name)

    # Fetch final release details
    final_info = api_request(f"{repo_url}/releases/{release_info['id']}", token)
    print("\n" + "=" * 70)
    print("RELEASE PUBLISHED SUCCESSFULLY!")
    print(f"Release URL: {final_info['html_url']}")
    print("Assets:")
    for a in final_info.get("assets", []):
        size_mb = a["size"] / (1024 * 1024)
        print(f"  - {a['name']} ({size_mb:.2f} MB): {a['browser_download_url']}")
    print("=" * 70)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="Tproplay", help="GitHub repo owner")
    parser.add_argument("--repo", default="Pvz-Fusion-Translation-Lite", help="GitHub repo name")
    parser.add_argument("--tag", default="v4.0.5", help="Git tag name")
    parser.add_argument("--name", default="PvZ: Fusion v4.0.5 — English Release (PC & Android)", help="Release title")
    parser.add_argument("--notes", type=Path, default=Path("docs/RELEASE-4.0.5-EN.md"), help="Path to release notes")
    parser.add_argument(
        "--pc-zip",
        type=Path,
        default=Path("build/PvZ-Fusion-4.0.5-English-PC.zip"),
        help="Path to PC zip asset",
    )
    parser.add_argument(
        "--android-apk",
        type=Path,
        default=Path("build/android-405/PvZ-Fusion-4.0.5-English-Android.apk"),
        help="Path to Android APK asset",
    )

    args = parser.parse_args()
    try:
        return publish_release(
            owner=args.owner,
            repo=args.repo,
            tag=args.tag,
            name=args.name,
            notes_file=args.notes,
            pc_zip=args.pc_zip,
            android_apk=args.android_apk,
        )
    except Exception as exc:
        print(f"Failed to publish release: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
