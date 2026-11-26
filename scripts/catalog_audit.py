#!/usr/bin/env python3
"""catalog_audit.py — audit of the fapa.io/dsgame/catalog catalog.

Looks for:
  * game folders without a card in catalog.json (unmarked);
  * cards without a folder;
  * previews without a card;
  * cards without a preview / without path.

Read-only, deletes nothing. The path to the catalog JSON is an argument."""
import json
import os
import sys

CAT = sys.argv[1] if len(sys.argv) > 1 else '/var/www/fapa.io/dsgame/catalog'
SKIP_DIRS = {'thumbs'}


def main():
    with open(os.path.join(CAT, 'catalog.json'), encoding='utf-8') as fh:
        cat = json.load(fh)

    slugs = []
    for g in cat:
        slugs.append(g.get('slug', ''))
    slug_set = set(slugs)

    dirs = set()
    for name in os.listdir(CAT):
        if name in SKIP_DIRS:
            continue
        if os.path.isdir(os.path.join(CAT, name)):
            dirs.add(name)

    unmarked = sorted(dirs - slug_set)
    missing_dir = sorted(slug_set - dirs)

    no_thumb = [g.get('slug', '') for g in cat if not g.get('thumb')]
    with_path = [(g.get('slug', ''), g.get('path')) for g in cat if g.get('path')]

    thumbs_dir = os.path.join(CAT, 'thumbs')
    thumbs = set()
    if os.path.isdir(thumbs_dir):
        thumbs = {n[:-4] for n in os.listdir(thumbs_dir) if n.endswith('.jpg')}
    orphan_thumbs = sorted(thumbs - slug_set)
    missing_thumb_file = sorted(
        g.get('slug', '') for g in cat
        if g.get('thumb') and not os.path.isfile(os.path.join(CAT, g['thumb']))
    )

    print('catalog.json entries: %d (unique slugs: %d)' % (len(cat), len(slug_set)))
    print('game dirs on disk:    %d' % len(dirs))
    print()
    print('UNMARKED dirs (no card in catalog.json): %d' % len(unmarked))
    for s in unmarked:
        print('   ', s)
    print()
    print('cards without dir:     %d' % len(missing_dir))
    for s in missing_dir:
        print('   ', s)
    print()
    print('cards without thumb:   %d' % len(no_thumb))
    print('cards with path:       %d' % len(with_path))
    for s, p in with_path[:20]:
        print('    %s -> %s' % (s, p))
    print()
    print('orphan thumbs (file, no card): %d' % len(orphan_thumbs))
    for s in orphan_thumbs[:20]:
        print('   ', s)
    print('cards whose thumb file is missing: %d' % len(missing_thumb_file))
    for s in missing_thumb_file[:20]:
        print('   ', s)


if __name__ == '__main__':
    main()
