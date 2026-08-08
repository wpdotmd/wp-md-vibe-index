#!/usr/bin/env python3
"""Validate every record in data/ against the schema and the derivation rules.

Deliberately dependency-free so CI needs no install step and a contributor can
run it before opening a PR.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
TAGS = {"data", "service", "ai", "network", "compliance", "updates", "support", "library"}
BUILDS = {"sitting", "weekend", "weekends", "months"}

def verdict_for(moat):
    if moat <= 33:  return "yes"
    if moat <= 57:  return "kinda"
    if moat <= 74:  return "no"
    return "never"

errors = []
files = sorted(p for p in (ROOT / "data").glob("*.json") if p.name != "schema.json")

for path in files:
    def err(msg):
        errors.append(f"{path.name}: {msg}")
    try:
        rec = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        err(f"invalid JSON — {e}")
        continue

    for field in ("slug", "name", "moat", "moatTags", "verdict", "build",
                  "upkeepHoursPerYear", "couldBuild", "stillMissing", "requirements"):
        if field not in rec:
            err(f"missing required field '{field}'")

    if rec.get("slug") != path.stem:
        err(f"slug '{rec.get('slug')}' does not match filename")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(rec.get("slug", ""))):
        err("slug must be lowercase with hyphens")

    moat = rec.get("moat")
    if not isinstance(moat, int) or not 0 <= moat <= 100:
        err("moat must be an integer 0-100")
    else:
        expected = verdict_for(moat)
        if rec.get("verdict") != expected:
            err(f"verdict '{rec.get('verdict')}' contradicts moat {moat} — should be '{expected}'")
        derived = rec.get("derived") or {}
        if "codeShare" in derived and derived["codeShare"] != 100 - moat:
            err(f"derived.codeShare {derived['codeShare']} != 100 - moat ({100 - moat})")

    tags = rec.get("moatTags") or []
    if not 1 <= len(tags) <= 4:
        err("moatTags must have 1-4 entries")
    for t in tags:
        if t not in TAGS:
            err(f"unknown moat tag '{t}'")
    if len(set(tags)) != len(tags):
        err("duplicate moat tags")

    if rec.get("build") not in BUILDS:
        err(f"build must be one of {sorted(BUILDS)}")

    up = rec.get("upkeepHoursPerYear")
    if not isinstance(up, int) or not 0 <= up <= 400:
        err("upkeepHoursPerYear must be an integer 0-400")

    reqs = rec.get("requirements") or []
    if not 3 <= len(reqs) <= 8:
        err("requirements must have 3-8 entries")

    for f in ("couldBuild", "stillMissing"):
        if len(str(rec.get(f, ""))) < 20:
            err(f"{f} is too short to be useful")

    if rec.get("reviewedOn") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", rec["reviewedOn"]):
        err("reviewedOn must be YYYY-MM-DD")

print(f"checked {len(files)} records")
if errors:
    print(f"\n{len(errors)} problem(s):\n")
    for e in errors:
        print("  " + e)
    sys.exit(1)
print("all good")
