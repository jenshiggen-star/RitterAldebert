#!/usr/bin/env python3
"""Prüft alle Seiten in Handybreite (390 px) mit Headless-Chrome:
- seitliches Überlaufen (horizontales Scrollen)
- Schrift kleiner als 11 px
- zu kleine Tippflächen in Navigation und Fußzeile (< 24 px hoch)
Aufruf: python3 scripts/check_mobile.py      (benötigt google-chrome oder chromium)
"""
import html, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pages = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.html")
               if p.relative_to(ROOT).parts[0] not in ("RAW", "vorlagen", ".git"))
chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
if not chrome:
    sys.exit("Chrome/Chromium nicht gefunden.")

harness = """<!doctype html><html><body><pre id="out"></pre><script>
const pages=%s, root=%s; let res=[], i=0;
function next(){ if(i>=pages.length){document.getElementById('out').textContent=JSON.stringify(res);return;}
 const f=document.createElement('iframe'); f.style.width='390px'; f.style.height='800px'; f.src='file://'+root+'/'+pages[i];
 f.onload=()=>setTimeout(()=>{ try{ const d=f.contentDocument, w=d.documentElement.clientWidth, wide=[], small=[], taps=[];
   d.querySelectorAll('body *').forEach(el=>{const r=el.getBoundingClientRect(); if(r.width>0&&(r.right>w+1||r.left<-1)) wide.push(el.tagName+'.'+el.className)});
   d.querySelectorAll('p,li,a,span,figcaption,h1,h2,h3').forEach(el=>{const fs=parseFloat(getComputedStyle(el).fontSize); if(fs<11&&el.textContent.trim()&&getComputedStyle(el).display!=='none') small.push(el.textContent.trim().slice(0,30))});
   d.querySelectorAll('nav a,.footer a').forEach(a=>{const r=a.getBoundingClientRect(); if(r.height<24) taps.push(a.textContent.trim())});
   res.push({page:pages[i],overflow:d.documentElement.scrollWidth>w,wide:wide.slice(0,5),small:small.slice(0,5),taps:taps});
  }catch(e){res.push({page:pages[i],err:String(e)})} f.remove(); i++; next(); },1200);
 document.body.appendChild(f);}
next();</script></body></html>""" % (json.dumps(pages), json.dumps(str(ROOT)))

with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
    fh.write(harness)
out = subprocess.run([chrome, "--headless", "--disable-gpu", "--allow-file-access-from-files",
                      "--virtual-time-budget=60000", "--dump-dom", "file://" + fh.name],
                     capture_output=True, text=True, timeout=180).stdout
m = re.search(r'<pre id="out">(.*?)</pre>', out, re.S)
results = json.loads(html.unescape(m.group(1))) if m and m.group(1) else []
fehler = 0
for r in results:
    probleme = [k for k in ("overflow", "wide", "small", "taps", "err") if r.get(k)]
    fehler += bool(probleme)
    print(("FEHLER " if probleme else "OK     ") + r["page"] + ("" if not probleme else "  " + json.dumps({k: r[k] for k in probleme}, ensure_ascii=False)))
sys.exit(1 if fehler or not results else 0)
