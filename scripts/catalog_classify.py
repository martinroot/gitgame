#!/usr/bin/env python3
"""
catalog_classify.py — сводит результаты проверок в решение по каждому слагу.

Правила (в порядке приоритета):
  404 / 403 / no-index / empty-dir      -> BROKEN   (снос)
  blank + DOM пустой (403/404 в DOM)     -> BROKEN   (снос)
  blank + DOM живой (текст/canvas)       -> OK       (оставить: тёмный кадр = ложное срабатывание)
  no-shot после ретрая                    -> SUSPECT  (решает DOM-зонд)
  http ok / render ok                     -> OK

Вход: catalog_render.json (основной), catalog_http.json (http), catalog_retry.json (ретрай no-shot),
      noshot_probe.log (DOM-зонд no-shot).
Выход: catalog_decision.json + текстовый список.
"""
import json
import os
import re

BUILD = '/home/drogame/build'


def load(name):
    p = os.path.join(BUILD, name)
    if not os.path.isfile(p):
        return {}
    try:
        with open(p, encoding='utf-8') as fh:
            d = json.load(fh)
    except Exception:
        return {}
    return {r.get('slug'): r for r in d.get('results', [])}


def main():
    render = load('catalog_render.json')
    http = load('catalog_http.json')
    retry = load('catalog_retry.json')

    # DOM-зонд: slug -> (dom_bytes, text)
    dom = {}
    p = os.path.join(BUILD, 'noshot_probe.log')
    if os.path.isfile(p):
        cur = None
        for line in open(p, encoding='utf-8', errors='ignore'):
            m = re.match(r'---\s+(\S+)', line)
            if m:
                cur = m.group(1)
                dom.setdefault(cur, {'bytes': 0, 'text': ''})
                continue
            if cur is None:
                continue
            if 'dom=' in line:
                mb = re.search(r'dom=(\d+)B', line)
                if mb:
                    dom[cur]['bytes'] = int(mb.group(1))
            elif 'text:' in line:
                dom[cur]['text'] = line.split('text:', 1)[1].strip()

    slugs = set(render) | set(http)
    decision = {}
    for s in slugs:
        probs = list(render.get(s, {}).get('problems') or [])
        hprobs = list(http.get(s, {}).get('problems') or [])
        rprobs = list(retry.get(s, {}).get('problems') or [])
        if s in retry:
            # слаги из ретрая: его вердикт authoritative, даже если пустой (выздоровели)
            probs = rprobs
        hard = [p for p in probs + hprobs
                if p.startswith(('http-', 'no-index', 'no-dir', 'empty-dir'))]
        verdict, why = 'OK', 'ok'
        if hard:
            verdict, why = 'BROKEN', ','.join(sorted(set(hard)))
        elif 'blank' in probs:
            d = dom.get(s)
            if d and d['bytes'] > 0 and '403 Forbidden' not in d.get('text', '') \
                    and '404' not in d.get('text', '')[:40]:
                verdict, why = 'OK', 'blank-but-live-dom'
            else:
                verdict, why = 'BROKEN', 'blank-empty-dom'
        elif 'no-shot' in probs:
            d = dom.get(s)
            if d and d['bytes'] > 0 and 'Forbidden' not in d.get('text', '') \
                    and 'Not Found' not in d.get('text', ''):
                verdict, why = 'OK', 'no-shot-but-live-dom'
            elif d:
                verdict, why = 'BROKEN', 'no-shot:' + d.get('text', '')[:40]
            else:
                verdict, why = 'SUSPECT', 'no-shot-no-probe'
        decision[s] = {'verdict': verdict, 'why': why,
                       'render': probs, 'http': hprobs}

    from collections import Counter
    c = Counter(v['verdict'] for v in decision.values())
    print('=== сводка:', dict(c))
    for verdict in ('BROKEN', 'SUSPECT'):
        sel = [s for s, v in decision.items() if v['verdict'] == verdict]
        print('\n--- %s (%d):' % (verdict, len(sel)))
        for s in sorted(sel):
            v = decision[s]
            print('   %-40s %s' % (s, v['why']))
    ok = [s for s, v in decision.items() if v['verdict'] == 'OK']
    print('\nOK: %d' % len(ok))

    with open(os.path.join(BUILD, 'catalog_decision.json'), 'w', encoding='utf-8') as fh:
        json.dump(decision, fh, ensure_ascii=False, indent=1)
    broken = sorted(s for s, v in decision.items() if v['verdict'] == 'BROKEN')
    with open(os.path.join(BUILD, 'catalog_broken.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(broken))
    print('\nсписок на снос (%d) -> catalog_broken.txt' % len(broken))


if __name__ == '__main__':
    main()
