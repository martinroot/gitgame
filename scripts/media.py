import base64,json,os,re,requests,sys
API="https://api.github.com"; T=os.environ["GITHUB_TOKEN"]
H={"Accept":"application/vnd.github+json","Authorization":f"Bearer {T}"}
def gh(p):
    r=requests.get(API+p,headers=H,timeout=30)
    return r.json() if r.status_code==200 else None
def readme(fn):
    d=gh(f"/repos/{fn}/readme")
    if not d or "content" not in d: return ""
    return base64.b64decode(d["content"]).decode("utf-8","ignore")
cands=json.load(open("out.json"))[:10]
res={}
for c in cands:
    fn=c["full_name"]; rm=readme(fn)
    media=[]
    # markdown + html images/video
    for m in re.findall(r'!\[[^\]]*\]\(([^)\s]+)',rm): media.append(m)
    for m in re.findall(r'<img[^>]+src=["\']([^"\']+)',rm): media.append(m)
    for m in re.findall(r'<video[^>]+src=["\']([^"\']+)',rm): media.append(m)
    for m in re.findall(r'<source[^>]+src=["\']([^"\']+)',rm): media.append(m)
    # bare links to media / youtube / demos
    for m in re.findall(r'https?://[^\s)\]"\'<>]+',rm):
        if re.search(r'\.(gif|mp4|webm|png|jpg|jpeg|webp)(\?|$)|youtu\.be|youtube\.com/watch|itch\.io|vimeo',m,re.I):
            media.append(m)
    # normalize relative -> github raw HEAD
    norm=[]
    for u in media:
        if u.startswith("http"): norm.append(u)
        elif u.startswith("/"): norm.append(f"https://github.com/{fn}/raw/HEAD{u}")
        else: norm.append(f"https://github.com/{fn}/raw/HEAD/{u.lstrip('./')}")
    # dedup keep order
    seen=set(); out=[]
    for u in norm:
        if u not in seen: seen.add(u); out.append(u)
    res[fn]={"repo":c["url"],"demo":c.get("homepage") or "","media":out[:6]}
json.dump(res,open("media.json","w"),ensure_ascii=False,indent=2)
for fn,d in res.items():
    print(f"\n### {fn}")
    print("repo:",d["repo"])
    if d["demo"]: print("demo:",d["demo"])
    for m in d["media"]: print("  media:",m)
