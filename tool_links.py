"""Lists schemes that use given link fragments: python tool_links.py drive.google.com gueedc"""
import json
import re
import sys

for lang in ("gu", "hi"):
    d = json.load(open(f"v2/{lang}/content.json", encoding="utf-8"))
    for s in d["schemes"]:
        blob = json.dumps(s, ensure_ascii=False)
        urls = re.findall(r"https?://[^\s\"\\]+", blob)
        hits = [u for u in urls if any(k in u for k in sys.argv[1:])]
        if hits:
            print(lang, s.get("id"), "|", str(s.get("title", ""))[:45], "|", hits)
