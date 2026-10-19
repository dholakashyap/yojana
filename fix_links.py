"""Replaces dead or broken government links in the v2 feeds with working official pages (checked 19 Oct 2026)."""
import json

FIX = {
    # RTE admission portal is only up during the April admission window; Samagra Shiksha Gujarat runs RTE admissions.
    "https://rte.orpgujarat.com/": "https://www.ssagujarat.org/",
    "www.rte.orpgujarat.com": "https://www.ssagujarat.org/",
    "https://mysy.guj.nic.in/Noticeboard/Self%20declaration%20for%20Non%20IT%20Returns1920.pdf": "https://mysy.gujarat.gov.in/",
    "https://mysy.guj.nic.in/Noticeboard/Format%20of%20Self%20declaration%20form%201920.pdf": "https://mysy.gujarat.gov.in/",
    "https://mysy.guj.nic.in/": "https://mysy.gujarat.gov.in/",
    "https://mera.pmjay.gov.in/search/login": "https://beneficiary.nha.gov.in/",
    "https://gueedc.apphost.in/": "https://gueedc.gujarat.gov.in/",
    "https://esamajkalyan.gujarat.gov.in/index.aspx?HodID=3": "https://esamajkalyan.gujarat.gov.in/",
    "https://esamajkalyan.gujarat.gov.in/index.aspx?HodID=2": "https://esamajkalyan.gujarat.gov.in/",
    "https://www.jansuraksha.gov.in/Files/PMJJBY/Gujarati/ApplicationForm.pdf": "https://jansuraksha.gov.in/Files/PMJJBY/Gujarati/ApplicationForm.pdf",
    "http://www.cottage.gujarat.gov.in/FileExplorer/Document/SUBSIDY-Form.pdf": "https://cottage.gujarat.gov.in/FileExplorer/Document/SUBSIDY-Form.pdf",
    "http://www.cottage.gujarat.gov.in/FileExplorer/Branch/DTAISY.pdf": "https://cottage.gujarat.gov.in/FileExplorer/Branch/DTAISY.pdf",
    "http://www.cottage.gujarat.gov.in/FileExplorer/Bank-Certificate.pdf": "https://cottage.gujarat.gov.in/FileExplorer/Bank-Certificate.pdf",
    "www.cottage.gujarat.gov.in/FileExplorer/Document/SUBSIDY-Form.pdf": "https://cottage.gujarat.gov.in/FileExplorer/Document/SUBSIDY-Form.pdf",
    "www.cottage.gujarat.gov.in/FileExplorer/Branch/DTAISY.pdf": "https://cottage.gujarat.gov.in/FileExplorer/Branch/DTAISY.pdf",
    "www.cottage.gujarat.gov.in/FileExplorer/Bank-Certificate.pdf": "https://cottage.gujarat.gov.in/FileExplorer/Bank-Certificate.pdf",
    "www.jansuraksha.gov.in/Files/PMJJBY/Gujarati/ApplicationForm.pdf": "https://jansuraksha.gov.in/Files/PMJJBY/Gujarati/ApplicationForm.pdf",
    "http://pmkisan.gov.in/Documents/Kcc.pdf": "https://pmkisan.gov.in/Documents/Kcc.pdf",
    # Google Drive copies of forms were deleted: link the department that issues the form.
    "https://drive.google.com/file/d/1jp8osVkebbQA8P6DO-gAxBrwy3vrQcwx/view?usp=sharing": "https://wcd.gujarat.gov.in/",
    "https://drive.google.com/file/d/1FfFTVX7WuAqF6TWFInNc8RIyXhfc51Nn/view?usp=sharing": "https://e-kutir.gujarat.gov.in/",
    "https://drive.google.com/file/d/18OU0_FxCDQwTBH0OAN_LIhoGDiQgdr_f/view?usp=sharing": "https://e-kutir.gujarat.gov.in/",
    "https://drive.google.com/file/d/1bB2KuwOlsc9Pph5RfzJsoXWCjdDXsE8b/view?usp=sharing": "https://sje.gujarat.gov.in/",
    "https://drive.google.com/file/d/1KNxMMqLnufKv4tVG7JV6MeYnZaMkL8CI/view?usp=sharing": "https://sje.gujarat.gov.in/",
    "https://drive.google.com/file/d/145W1ImJ-Uj38sEAMvTaXjG01mgSc7IQb/view?usp=sharing": "https://sje.gujarat.gov.in/",
}

# The RTE "where to apply" line ran into the next scheme's name, which the app linked as one broken URL.
TEXT = {
    "hi": ("वेबसाइट www.rte.orpgujarat.com.-Mukhyamantri Yuva Swavalaman Yojana पर भरना होगा",
           "वेबसाइट https://www.ssagujarat.org/ पर भरना होगा (प्रवेश हर साल अप्रैल में खुलते हैं)"),
    "gu": ("વેબસાઈટ www.rte.orpgujarat.com પર ઓનલાઈન ફોર્મ ભરવાનું રહેશે.-મુખ્યમંત્રી યુવા સ્વાવલંબન યોજના",
           "વેબસાઈટ https://www.ssagujarat.org/ પર ઓનલાઈન ફોર્મ ભરવાનું રહેશે (પ્રવેશ દર વર્ષે એપ્રિલમાં ખુલે છે)."),
}

for lang in ("gu", "hi"):
    p = f"v2/{lang}/content.json"
    raw = open(p, encoding="utf-8").read()
    old, new = TEXT[lang]
    assert old in raw, (lang, "RTE text not found")
    raw = raw.replace(old, new)
    # Longest first so a full URL is replaced before a shorter form inside it.
    for a in sorted(FIX, key=len, reverse=True):
        raw = raw.replace(a, FIX[a]) if a.startswith("http") else raw.replace(a, FIX[a]) if f"//{a}" not in raw else raw
    json.loads(raw)  # still valid JSON
    open(p, "w", encoding="utf-8").write(raw)
    print(lang, "ok")
