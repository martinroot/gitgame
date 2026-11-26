# GitGame

Каталог HTML5-игр с готовыми веб-сборками и исходниками. Сайт: https://gitgame.live

**288 игр** с ручной оценкой, отсортированы как на сайте: по звёздам, затем по цене и названию.

## Скрипты

- `scripts/game_crawler.py` — поиск и обогащение игр с GitHub (`--discover`, `--enrich`), БД `games.db`
- `scripts/auto_deploy.py` — клон → сборка → деплой в каталог fapa.io/dsgame, `--n 20`
- `scripts/daily.sh` — ежедневный цикл: discover → enrich → deploy (cron 09:30)
- `scripts/junk_purge.py`, `scripts/catalog_*.py` — чистка и проверка каталога (headless Chrome)
- `scripts/gitgame_gen.py` — генератор витрины gitgame.live (EN/DE/KR/RU/AR)
- `scripts/gen_gitgame_prices.py` — цены из каталога в `api/prices.json` (источник для checkout)
- `web/api/*.php` — оплата через DV-merchant: checkout, webhook, статус заказа
- `scripts/gen_readme_catalog.py` — пересборка этого README из `catalog.json`, `ratings.json` и цен

Запуск: `python3 scripts/gen_readme_catalog.py` (пути переопределяются через `CATALOG_JSON`, `RATINGS_JSON`, `PRICES_JSON`, `SITE_THUMBS`). Секреты берутся из окружения (`FAPA_PASS`, `GITHUB_TOKEN`), в репозитории их нет.

## Каталог игр

### ★★★★★ Deep Blue — Fishing — $1.65

![Deep Blue — Fishing](https://gitgame.live/thumbs/fishing-game.jpg)

Рыбалка в тёмной глубине: закинь снасть, поймай что клюнет, собери 22 вида. Tap/drag.

[Игра на GitGame](https://gitgame.live/game/fishing-game/) · [Репозиторий](https://github.com/ctbot000/fishing-game)

### ★★★★★ Jamblob Sandbox — $1.65

![Jamblob Sandbox](https://gitgame.live/thumbs/jamblob-sandbox.jpg)

Browser physics sandbox: fling 12 musical ragdoll characters into traps and props, then start a Web Audio jam.

[Игра на GitGame](https://gitgame.live/game/jamblob-sandbox/) · [Репозиторий](https://github.com/brepre109/jamblob-sandbox)

### ★★★★★ Knight Duel — $1.65

![Knight Duel](https://gitgame.live/thumbs/knight-duel.jpg)

武士圓舞曲 Knight's Waltz — 俯視角物理甩劍決鬥(Three.js+Rapier+TS,無引擎)。Play: satsumacreative.tw/kw 或 saomin.itch.io/knightswaltz

[Игра на GitGame](https://gitgame.live/game/knight-duel/) · [Репозиторий](https://github.com/saomin0317/knight-duel)

### ★★★★★ Ragdoll Drop — $1.65

![Ragdoll Drop](https://gitgame.live/thumbs/ragdoll-drop.jpg)

A 3D ragdoll game built for Henry: tower drops, a slice lab, a colosseum and a story with eighteen endings. Installable PWA.

[Игра на GitGame](https://gitgame.live/game/ragdoll-drop/) · [Репозиторий](https://github.com/aussiescupper/ragdoll-drop)

### ★★★★★ Touchline — Arcade Soccer — $1.65

![Touchline — Arcade Soccer](https://gitgame.live/thumbs/soccer-game.jpg)

Аркадный футбол: выбор команд, сложность, длина тайма. Canvas-2D, pointer-управление (тач из коробки).

[Игра на GitGame](https://gitgame.live/game/soccer-game/) · [Репозиторий](https://github.com/ctbot000/soccer-game)

### ★★★★★ Gpt 6 Astra Test — $1.60

![Gpt 6 Astra Test](https://gitgame.live/thumbs/gpt-6_astra_test.jpg)

Retro Game!

[Игра на GitGame](https://gitgame.live/game/gpt-6_astra_test/) · [Репозиторий](https://github.com/padmashri23/gpt-6_Astra_test)

### ★★★★★ Smash Karts Arena · GPT-6 Astra — $1.60

![Smash Karts Arena · GPT-6 Astra](https://gitgame.live/thumbs/astra-smash-karts.jpg)

3D кар-баттл-арена: боты, 11 видов оружия, выбор карта. Standalone-сборка (без сервера, одиночка с ботами).

[Игра на GitGame](https://gitgame.live/game/astra-smash-karts/) · [Репозиторий](https://github.com/amsminn/gpt-6-astra-smash-karts)

### ★★★★★ Elevator Town — $1.55

![Elevator Town](https://gitgame.live/thumbs/elevator-town.jpg)

A simple 3D elevator game for young kids: ride glass and solid elevators in a hotel, parking garage and mall.

[Игра на GitGame](https://gitgame.live/game/elevator-town/) · [Репозиторий](https://github.com/aiden-azarnoush/elevator-town)

### ★★★★★ Fablexiangqi — $1.55

楚汉争霸 — a 3D xiangqi game in gongbi heavy-color style; every mesh, texture, animation, glyph and note generated from code (300KB gzip)

[Игра на GitGame](https://gitgame.live/game/fablexiangqi/) · [Репозиторий](https://github.com/dittowang/fablexiangqi)

### ★★★★★ Game Barrel Shooter — $1.55

![Game Barrel Shooter](https://gitgame.live/thumbs/game-barrel-shooter.jpg)

Barrel Blast — a browser-based 3D physics shooting game (three.js + cannon-es)

[Игра на GitGame](https://gitgame.live/game/game-barrel-shooter/) · [Репозиторий](https://github.com/freaxnx01/game-barrel-shooter)

### ★★★★★ H5 Pvz Mahjong — $1.55

![H5 Pvz Mahjong](https://gitgame.live/thumbs/h5-pvz-mahjong.jpg)

植物麻将 · 肉鸽塔防：用麻将凑牌代替阳光的 H5 塔防，AWS AI-DLC 学习展示项目

[Игра на GitGame](https://gitgame.live/game/h5-pvz-mahjong/) · [Репозиторий](https://github.com/Severn17/h5-pvz-mahjong)

### ★★★★★ Hallowmere — $1.55

![Hallowmere](https://gitgame.live/thumbs/hallowmere.jpg)

A dark fantasy action RPG game made w/ Astra

[Игра на GitGame](https://gitgame.live/game/hallowmere/) · [Репозиторий](https://github.com/miguelsolorio/hallowmere)

### ★★★★★ Magiccarpetwizard — $1.55

![Magiccarpetwizard](https://gitgame.live/thumbs/magiccarpetwizard.jpg)

Video Game made with GPT 6 Astra

[Игра на GitGame](https://gitgame.live/game/magiccarpetwizard/) · [Репозиторий](https://github.com/threapchills/MagicCarpetWizard)

### ★★★★★ Magnets — $1.55

![Magnets](https://gitgame.live/thumbs/magnets.jpg)

POLAR — magnet physics puzzle game. Flip polarity to pull and push iron cores.

[Игра на GitGame](https://gitgame.live/game/magnets/) · [Репозиторий](https://github.com/Sirchanced/Magnets)

### ★★★★★ Soccer Car — $1.55

![Soccer Car](https://gitgame.live/thumbs/soccer-car.jpg)

Jogo autoral de futebol com carros no navegador: TypeScript, Three.js, bot, garagem, controle e modo 2D leve

[Игра на GitGame](https://gitgame.live/game/soccer-car/) · [Репозиторий](https://github.com/enzozon/soccer-car)

### ★★★★★ Timbertrail — $1.55

![Timbertrail](https://gitgame.live/thumbs/timbertrail.jpg)

Survival game with amazing pixel graphics. Entirely made with ChatGPT

[Игра на GitGame](https://gitgame.live/game/timbertrail/) · [Репозиторий](https://github.com/jonivainio/Timbertrail)

### ★★★★★ Afterlight — $1.50

![Afterlight](https://gitgame.live/thumbs/afterlight.jpg)

A Three.js planet destruction sandbox: nine weapons, five worlds, ice-shatter combos, and slow-motion chaos.

[Игра на GitGame](https://gitgame.live/game/afterlight/) · [Репозиторий](https://github.com/tokenmaxxing-ai/afterlight)

### ★★★★★ Andersonigarashi.Github.Io — $1.50

![Andersonigarashi.Github.Io](https://gitgame.live/thumbs/andersonigarashi.github.io.jpg)

Portfolio site: playable ads you can play in the browser

[Игра на GitGame](https://gitgame.live/game/andersonigarashi.github.io/) · [Репозиторий](https://github.com/AndersonIgarashi/AndersonIgarashi.github.io)

### ★★★★★ Bubble Shooter. — $1.50

![Bubble Shooter.](https://gitgame.live/thumbs/bubble-shooter..jpg)

Gemini 3 Flash is your intelligent game companion, analyzing the bubble board in real time and helping you choose the smartest shots. Use your webcam to aim, match…

[Игра на GitGame](https://gitgame.live/game/bubble-shooter./) · [Репозиторий](https://github.com/surajkumar661380-netizen/bubble-shooter.)

### ★★★★★ Bunbetsu Beat — $1.50

![Bunbetsu Beat](https://gitgame.live/thumbs/bunbetsu-beat.jpg)

流れてくるゴミを、音楽のリズムに合わせて 4 方向のゴミ箱へ投げ分ける、ブラウザで遊べる 3D リズムゲーム。 / A browser 3D rhythm game about sorting trash to the beat.

[Игра на GitGame](https://gitgame.live/game/bunbetsu-beat/) · [Репозиторий](https://github.com/tanuu5/bunbetsu-beat)

### ★★★★★ Crayon Contraptions — $1.50

![Crayon Contraptions](https://gitgame.live/thumbs/crayon-contraptions.jpg)

A Rube Goldberg puzzle game drawn in crayon: 100 levels, seven crayons with their own physics, live levels and boss monsters.

[Игра на GitGame](https://gitgame.live/game/crayon-contraptions/) · [Репозиторий](https://github.com/winchxyz/crayon-contraptions)

### ★★★★★ Duckies Pop — $1.50

![Duckies Pop](https://gitgame.live/thumbs/duckies-pop.jpg)

Playable HTML5 physics game — slingshot duck launching with a custom foam simulation, built on Matter.js

[Игра на GitGame](https://gitgame.live/game/duckies-pop/) · [Репозиторий](https://github.com/daniellesasi/duckies-pop)

### ★★★★★ Dunekeep Rts — $1.50

![Dunekeep Rts](https://gitgame.live/thumbs/dunekeep-rts.jpg)

A procedural Three.js castle-building strategy game with a six-mission campaign, production chains, fortifications and siege combat. Built with TypeScript.

[Игра на GitGame](https://gitgame.live/game/dunekeep-rts/) · [Репозиторий](https://github.com/andreashxc/dunekeep-rts)

### ★★★★★ Fellswoop — $1.50

![Fellswoop](https://gitgame.live/thumbs/fellswoop.jpg)

FELLSWOOP: a little forest, a very busy axe. Idle chopping game on a floating island (Three.js, one HTML file).

[Игра на GitGame](https://gitgame.live/game/fellswoop/) · [Репозиторий](https://github.com/TrentSterling/fellswoop)

### ★★★★★ Hill Climbing Race — $1.50

![Hill Climbing Race](https://gitgame.live/thumbs/hill-climbing-race.jpg)

Hill Climbing Race is a 2D physics-based driving game where players explore endless terrain, collect rewards, upgrade vehicles, unlock new stages, and achieve record…

[Игра на GitGame](https://gitgame.live/game/hill-climbing-race/) · [Репозиторий](https://github.com/aryankumar-04/Hill-Climbing-Race)

### ★★★★★ Iris — $1.50

![Iris](https://gitgame.live/thumbs/iris.jpg)

An isometric real-time strategy game in 13kb, for js13kGames 2026

[Игра на GitGame](https://gitgame.live/game/iris/) · [Репозиторий](https://github.com/TheAxeC/iris)

### ★★★★★ Kata Rube Goldberg Game Gpt 6 Luna Extra High — $1.50

![Kata Rube Goldberg Game Gpt 6 Luna Extra High](https://gitgame.live/thumbs/kata-rube-goldberg-game-gpt-6-luna-extra-high.jpg)

Игра из парсера, авто-деплой.

[Игра на GitGame](https://gitgame.live/game/kata-rube-goldberg-game-gpt-6-luna-extra-high/) · [Репозиторий](https://github.com/intrepion/kata-rube-goldberg-game-gpt-6-luna-extra-high)

### ★★★★★ Lucky Bastard Astra — $1.50

![Lucky Bastard Astra](https://gitgame.live/thumbs/lucky-bastard-astra.jpg)

Lucky Bastard Astra — an original offline-compatible HTML5 cartoon auto-fighting survival game. Build a fighter and survive 25 rounds.

[Игра на GitGame](https://gitgame.live/game/lucky-bastard-astra/) · [Репозиторий](https://github.com/barryklaus/Lucky-Bastard-Astra)

### ★★★★★ Peel Out — $1.50

Peel Out: drop banana peels, cause chaos. A slapstick physics game you can play in the browser.

[Игра на GitGame](https://gitgame.live/game/peel-out/) · [Репозиторий](https://github.com/SwiftReason/peel-out)

### ★★★★★ Ricochet Rush — $1.50

![Ricochet Rush](https://gitgame.live/thumbs/ricochet-rush.jpg)

Ricochet Rush - a self-contained offline physics puzzle game

[Игра на GitGame](https://gitgame.live/game/ricochet-rush/) · [Репозиторий](https://github.com/dannyking6/ricochet-rush)

### ★★★★★ Sundrift — $1.50

![Sundrift](https://gitgame.live/thumbs/sundrift.jpg)

MINIDRIFT: night drifting in Japan (a cherry-blossom mountain pass, or NEO TOKYO). Every drift you bank moves the clock toward dawn. Every 3D object is Three.js code…

[Игра на GitGame](https://gitgame.live/game/sundrift/) · [Репозиторий](https://github.com/lkruer/sundrift)

### ★★★★★ Swarmlings — $1.50

![Swarmlings](https://gitgame.live/thumbs/swarmlings.jpg)

A pixel-art virtual-pet sim that grows into a civilization — and then starts watching you. Single HTML file, zero dependencies. 像素風養成模擬。

[Игра на GitGame](https://gitgame.live/game/swarmlings/) · [Репозиторий](https://github.com/shanchiehchiu/swarmlings)

### ★★★★★ Tokken — $1.50

![Tokken](https://gitgame.live/thumbs/tokken.jpg)

AI models fight. HP is tokens. A 90s arcade fighting game parodying the AI industry — browser, PWA, rollback netcode. Play: tokken.win

[Игра на GitGame](https://gitgame.live/game/tokken/) · [Репозиторий](https://github.com/lexdoudkin/tokken)

### ★★★★★ Wobble Wheels — $1.50

![Wobble Wheels](https://gitgame.live/thumbs/wobble-wheels.jpg)

Build wobbly physics cars from hinged beams, wheels,springs and rockets, then drive them across 30 maps.Plays on phones. Plain JS + planck.js.

[Игра на GitGame](https://gitgame.live/game/wobble-wheels/) · [Репозиторий](https://github.com/mister-giga/wobble-wheels)

### ★★★★☆ 380 Game Civilization Road — $1.15

文明之路 · 借鉴《文明6》的网页回合制策略游戏：程序化六边形地图、8 个文明、科技与市政树、电脑对手与外交，科技/文化/征服/分数四种胜利。纯 HTML + JS + Canvas，零依赖。

[Игра на GitGame](https://gitgame.live/game/380_game-civilization-road/) · [Репозиторий](https://github.com/Liyucheng1997/380_game-civilization-road)

### ★★★★☆ Angry Birds Html — $1.15

![Angry Birds Html](https://gitgame.live/thumbs/angry-birds-html.jpg)

A playable Angry Birds-style HTML physics game

[Игра на GitGame](https://gitgame.live/game/angry-birds-html/) · [Репозиторий](https://github.com/wangzhiqiang-ccc/angry-birds-html)

### ★★★★☆ Backgammon — $1.15

![Backgammon](https://gitgame.live/thumbs/backgammon.jpg)

⚅ Backgammon in your browser against four AI opponents — including an Expert neural network trained from scratch by self-play. Single-click moves, a coach you can switch…

[Игра на GitGame](https://gitgame.live/game/backgammon/) · [Репозиторий](https://github.com/WilburFort/backgammon)

### ★★★★☆ Blind Spot — $1.15

![Blind Spot](https://gitgame.live/thumbs/blind-spot.jpg)

Blind Spot Region 1: standalone physics puzzle game, source and tests.

[Игра на GitGame](https://gitgame.live/game/blind-spot/) · [Репозиторий](https://github.com/Dumb-Tony/blind-spot)

### ★★★★☆ Crossy Fish — $1.15

![Crossy Fish](https://gitgame.live/thumbs/crossy-fish.jpg)

🎣 Crossy Fish - 3D Voxel Crossy Road style fishing game built with Three.js, dynamic weather, multi-stage biomes, mobile support, AI auto-play & serverless leaderboard!

[Игра на GitGame](https://gitgame.live/game/crossy-fish/) · [Репозиторий](https://github.com/jeiel85/crossy-fish)

### ★★★★☆ Crush Factory — $1.15

![Crush Factory](https://gitgame.live/thumbs/crush-factory.jpg)

Idle clicker where the crusher actually crushes — chunks fall through spinning drums on real Matter.js physics. Skins, achievements, 10 languages.

[Игра на GitGame](https://gitgame.live/game/crush-factory/) · [Репозиторий](https://github.com/JohnInWork/crush-factory)

### ★★★★☆ Ctrl Slash — $1.15

![Ctrl Slash](https://gitgame.live/thumbs/ctrl-slash.jpg)

Unofficial fan art: a Fruit Ninja-style slicer starring VS Code's Buddy pet and its 17 hats. Mobile-first, confetti gore.

[Игра на GitGame](https://gitgame.live/game/ctrl-slash/) · [Репозиторий](https://github.com/digitarald/ctrl-slash)

### ★★★★☆ Fly Lab — $1.15

![Fly Lab](https://gitgame.live/thumbs/fly-lab.jpg)

Small brain. Strange worlds. Seven interactive fruit-fly games with a research-derived 3D brain atlas, live simulated activity, and five languages.

[Игра на GitGame](https://gitgame.live/game/fly-lab/) · [Репозиторий](https://github.com/LeeHueeng/fly-lab)

### ★★★★☆ Hole City — $1.15

Hole City · 16 张地图、4 种模式、106 款免费皮肤的三维黑洞吞噬游戏。仅发布构建后的浏览器运行版本。

[Игра на GitGame](https://gitgame.live/game/hole-city/) · [Репозиторий](https://github.com/seiya058904/Hole-City)

### ★★★★☆ Klondike Solitaire — $1.15

![Klondike Solitaire](https://gitgame.live/thumbs/klondike-solitaire.jpg)

A web-based Klondike solitaire game featuring a built-in timer and a personal record tracker for your fastest finishes.

[Игра на GitGame](https://gitgame.live/game/klondike-solitaire/) · [Репозиторий](https://github.com/johnnyheggelund/klondike-solitaire)

### ★★★★☆ Operation Ironhold — $1.15

![Operation Ironhold](https://gitgame.live/thumbs/operation-ironhold.jpg)

Браузерный FPS на Three.js: зачистить 10 целей на складе за 3 минуты. Портирован, добавлено мобильное управление.

[Игра на GitGame](https://gitgame.live/game/operation-ironhold/) · [Репозиторий](https://github.com/StarKnightt/operation-ironhold)

### ★★★★☆ Physics Sandbox 2D — $1.15

![Physics Sandbox 2D](https://gitgame.live/thumbs/physics-sandbox-2d.jpg)

A simple game who you play whit physics

[Игра на GitGame](https://gitgame.live/game/physics-sandbox-2d/) · [Репозиторий](https://github.com/matteovanegas2014-cpu/physics-sandbox-2d)

### ★★★★☆ Red Sand Rally — $1.15

![Red Sand Rally](https://gitgame.live/thumbs/red-sand-rally.jpg)

赤沙狂飙 · Red Sand Rally — 浏览器里可玩的 3D 战斗赛车（TypeScript + Three.js）

[Игра на GitGame](https://gitgame.live/game/red-sand-rally/) · [Репозиторий](https://github.com/Tao716/red-sand-rally)

### ★★★★☆ Rhythm Game — $1.15

![Rhythm Game](https://gitgame.live/thumbs/rhythm-game.jpg)

A four-lane browser rhythm game with zero audio files — every note is synthesized with the Web Audio API, and the charts are derived from the music itself.

[Игра на GitGame](https://gitgame.live/game/rhythm-game/) · [Репозиторий](https://github.com/ctbot000/rhythm-game)

### ★★★★☆ Soccer Slingshot — $1.15

![Soccer Slingshot](https://gitgame.live/thumbs/soccer-slingshot.jpg)

Slingshot Soccer game with Webcam Computer Vision + Gemini 3 Flash tactical co-pilot

[Игра на GitGame](https://gitgame.live/game/soccer-slingshot/) · [Репозиторий](https://github.com/robot3-track/soccer-slingshot)

### ★★★★☆ Table Tower — $1.15

![Table Tower](https://gitgame.live/thumbs/table-tower.jpg)

A 3D physics-based block tower game built with JavaScript, Three.js and cannon-es.

[Игра на GitGame](https://gitgame.live/game/table-tower/) · [Репозиторий](https://github.com/adharv-afk/TABLE-TOWER)

### ★★★★☆ Wwb — $1.15

![Wwb](https://gitgame.live/thumbs/wwb.jpg)

World War B: Bugfront. High-octane, style-ranked 3D browser FPS built with Three.js, Rapier physics, and Supabase.

[Игра на GitGame](https://gitgame.live/game/wwb/) · [Репозиторий](https://github.com/jeevesh2515/WWB)

### ★★★★☆ Battle Of The Bots — $1.10

![Battle Of The Bots](https://gitgame.live/thumbs/battle-of-the-bots.jpg)

A battleship simulation game built by Devin

[Игра на GitGame](https://gitgame.live/game/battle-of-the-bots/) · [Репозиторий](https://github.com/ashima-jain/battle-of-the-bots)

### ★★★★☆ Bloquebots — $1.10

![Bloquebots](https://gitgame.live/thumbs/bloquebots.jpg)

Juego 3D de robots hechos de bloques, con física y partidas en red. Three.js + cannon-es.

[Игра на GitGame](https://gitgame.live/game/bloquebots/) · [Репозиторий](https://github.com/germancsaid/bloquebots)

### ★★★★☆ Brick Mart — $1.10

![Brick Mart](https://gitgame.live/thumbs/brick-mart.jpg)

Kids' browser game: shop a toy aisle, then build the brick set you bought step by step. Canvas isometric renderer.

[Игра на GitGame](https://gitgame.live/game/brick-mart/) · [Репозиторий](https://github.com/brepre109/brick-mart)

### ★★★★☆ Game Ocean Racing — $1.10

대항해시대 레이싱 : 바다를 향한 당신의 꿈이 지금, 시작됩니다. 브라우저에서 바로 즐기는 3D 범선 레이싱 웹 게임

[Игра на GitGame](https://gitgame.live/game/game-ocean-racing/) · [Репозиторий](https://github.com/leaf-kit/game-ocean-racing)

### ★★★★☆ Hungrykatz — $1.10

![Hungrykatz](https://gitgame.live/thumbs/hungrykatz.jpg)

🐱 HungryKatz: a cute cat café game. Feed hungry cats, unlock new foods and fix up your café. Free to play on your phone, works offline.

[Игра на GitGame](https://gitgame.live/game/hungrykatz/) · [Репозиторий](https://github.com/icewinds/HungryKatz)

### ★★★★☆ Jet Arena — $1.10

![Jet Arena](https://gitgame.live/thumbs/jet-arena.jpg)

Jetpack deathmatch you play in a browser — solo against bots, or with friends over a Wi-Fi hotspot. No installs, no accounts, no dependencies.

[Игра на GitGame](https://gitgame.live/game/jet-arena/) · [Репозиторий](https://github.com/rishabcv-eng/jet-arena)

### ★★★★☆ Lighthouse Fishing Game — $1.10

![Lighthouse Fishing Game](https://gitgame.live/thumbs/lighthouse-fishing-game.jpg)

Three.js로 만든 로우폴리 등대섬 항해·낚시 게임

[Игра на GitGame](https://gitgame.live/game/lighthouse-fishing-game/) · [Репозиторий](https://github.com/freeboxwork/lighthouse-fishing-game)

### ★★★★☆ Magic Pencil Kingdoms — $1.10

![Magic Pencil Kingdoms](https://gitgame.live/thumbs/magic-pencil-kingdoms.jpg)

Whatever you draw comes alive. A free open-source browser game: draw it, name it, it fights for you. The limit is your imagination.

[Игра на GitGame](https://gitgame.live/game/magic-pencil-kingdoms/) · [Репозиторий](https://github.com/devkancheti4-design/magic-pencil-kingdoms)

### ★★★★☆ Mykonos Island Voxels — $1.10

![Mykonos Island Voxels](https://gitgame.live/thumbs/mykonos-island-voxels.jpg)

Изометрический воксельный город-билдер: строй средиземноморский остров. Canvas-2D, адаптив под тач.

[Игра на GitGame](https://gitgame.live/game/mykonos-island-voxels/) · [Репозиторий](https://github.com/boona13/mykonos-island-voxels)

### ★★★★☆ Neonplay Arcade Game Website — $1.10

![Neonplay Arcade Game Website](https://gitgame.live/thumbs/neonplay-arcade-game-website.jpg)

Arcade website that has many mini offline games created by claude

[Игра на GitGame](https://gitgame.live/game/neonplay-arcade-game-website/) · [Репозиторий](https://github.com/Agar19/Neonplay-Arcade-game-website)

### ★★★★☆ Night City — $1.10

![Night City](https://gitgame.live/thumbs/night-city.jpg)

An endless ASCII cyberpunk city and interactive tech demo. Reveal the 3D renderer, watch neighborhoods stream, scan buildings, and explore their interiors.

[Игра на GitGame](https://gitgame.live/game/night-city/) · [Репозиторий](https://github.com/willzjc/night-city)

### ★★★★☆ Road Physics Game Live — $1.10

![Road Physics Game Live](https://gitgame.live/thumbs/road-physics-game-live.jpg)

Игра из парсера, авто-деплой.

[Игра на GitGame](https://gitgame.live/game/road-physics-game-live/) · [Репозиторий](https://github.com/Iraq-project-baghdad/road-physics-game-live)

### ★★★★☆ Rumble Arena — $1.10

![Rumble Arena](https://gitgame.live/thumbs/rumble-arena.jpg)

Flashy 1v1 One Piece fan fighting game for kids: 25 chibi fighters, arcade mode with boss Imu, plain HTML5 canvas + JS

[Игра на GitGame](https://gitgame.live/game/rumble-arena/) · [Репозиторий](https://github.com/NGJHD/rumble-arena)

### ★★★★☆ Surf Nos Trilhos — $1.10

Surf nos Trilhos — jogo de corrida infinita 3D grátis no navegador (Three.js, PWA). Estilo endless runner, cenário de Maceió.

[Игра на GitGame](https://gitgame.live/game/surf-nos-trilhos/) · [Репозиторий](https://github.com/alequizao/surf-nos-trilhos)

### ★★★★☆ Thelegendoftrump — $1.10

![Thelegendoftrump](https://gitgame.live/thumbs/thelegendoftrump.jpg)

The Legend of Trump · 白宫奇遇记 — AI-assisted 3D browser action-adventure (React/Three.js/R3F). Playable WebGL game by jammyfu. Not the White House X video; not an OoT…

[Игра на GitGame](https://gitgame.live/game/thelegendoftrump/) · [Репозиторий](https://github.com/jammyfu/TheLegendOfTrump)

### ★★★★☆ Vixe — $1.10

An ASCII platformer that doesn't play fair. ~180 KB, no images, no libraries.

[Игра на GitGame](https://gitgame.live/game/vixe/) · [Репозиторий](https://github.com/thiagorodriguesdutra/vixe)

### ★★★★☆ Wanted Infinity — $1.10

![Wanted Infinity](https://gitgame.live/thumbs/wanted-infinity.jpg)

수배 레벨에 상한은 없다 — Three.js 단일 HTML로 만든 무한 경찰 추격 아케이드 게임. 별이 늘수록 SWAT, 헬기, 전차, 공습, UFO까지. An endless police-chase browser game.

[Игра на GitGame](https://gitgame.live/game/wanted-infinity/) · [Репозиторий](https://github.com/jeiel85/wanted-infinity)

### ★★★★☆ Ashen Throne — $1.05

![Ashen Throne](https://gitgame.live/thumbs/ashen-throne.jpg)

灰烬王座 · 原创浏览器卡牌肉鸽 Demo：单文件、零依赖、点开即玩

[Игра на GitGame](https://gitgame.live/game/ashen-throne/) · [Репозиторий](https://github.com/xierwanasijiang/ashen-throne)

### ★★★★☆ Chesself — $1.05

![Chesself](https://gitgame.live/thumbs/chesself.jpg)

A complete chess game with 7 AI opponents, each with unique play styles. Built with JavaScript and Minimax alpha-beta pruning.

[Игра на GitGame](https://gitgame.live/game/chesself/) · [Репозиторий](https://github.com/katzzero/Chesself)

### ★★★★☆ Counter Strike In Browser — $1.05

![Counter Strike In Browser](https://gitgame.live/thumbs/counter-strike-in-browser.jpg)

A CS2-style Dust2 A-site FPS running in the browser: Three.js, procedurally built in Blender, bots, bomb, HUD

[Игра на GitGame](https://gitgame.live/game/counter-strike-in-browser/) · [Репозиторий](https://github.com/StarKnightt/counter-strike-in-browser)

### ★★★★☆ Doodle Game — $1.05

![Doodle Game](https://gitgame.live/thumbs/doodle-game.jpg)

used claude-fable-5.1-max to build this

[Игра на GitGame](https://gitgame.live/game/doodle-game/) · [Репозиторий](https://github.com/dbestvarun/doodle-game)

### ★★★★☆ Doodle Rock — $1.05

![Doodle Rock](https://gitgame.live/thumbs/doodle-rock.jpg)

A stationery FPS drawn in ballpoint on notebook paper: a Will Rock-style campaign built on Doodle District (three.js)

[Игра на GitGame](https://gitgame.live/game/doodle-rock/) · [Репозиторий](https://github.com/mesutpiskin/doodle-rock)

### ★★★★☆ Fluid Physics Game — $1.05

![Fluid Physics Game](https://gitgame.live/thumbs/fluid-physics-game.jpg)

Игра из парсера, авто-деплой.

[Игра на GitGame](https://gitgame.live/game/fluid-physics-game/) · [Репозиторий](https://github.com/ryouf1430-creator/fluid-physics-game)

### ★★★★☆ Fowl Fortress — $1.05

![Fowl Fortress](https://gitgame.live/thumbs/fowl-fortress.jpg)

3D Angry Birds-style slingshot physics game in one HTML file. 8 levels, 4 birds, real physics.

[Игра на GitGame](https://gitgame.live/game/fowl-fortress/) · [Репозиторий](https://github.com/LearnPrompt/fowl-fortress)

### ★★★★☆ Geometric Battle Sandbox — $1.05

![Geometric Battle Sandbox](https://gitgame.live/thumbs/geometric-battle-sandbox.jpg)

Offline 2D auto-battle sandbox with 36 unit types, reversible army editing and seeded combat.

[Игра на GitGame](https://gitgame.live/game/geometric-battle-sandbox/) · [Репозиторий](https://github.com/seiya058904/GEOMETRIC-BATTLE-SANDBOX)

### ★★★★☆ Kernel Keep — $1.05

![Kernel Keep](https://gitgame.live/thumbs/kernel-keep.jpg)

Kernel Keep (provisional title): an original offline fortress-building RTS in a luminous digital world. Deterministic TypeScript sim, isometric renderer, React HUD.…

[Игра на GitGame](https://gitgame.live/game/kernel-keep/) · [Репозиторий](https://github.com/subfrecuency-png/kernel-keep)

### ★★★★☆ Moss Atlas — $1.05

![Moss Atlas](https://gitgame.live/thumbs/moss-atlas.jpg)

A 3D miniature ecosystem strategy game. Build a living garden in 22 choices.

[Игра на GitGame](https://gitgame.live/game/moss-atlas/) · [Репозиторий](https://github.com/chendahe666/moss-atlas)

### ★★★★☆ Pvz Myanmar Game — $1.05

![Pvz Myanmar Game](https://gitgame.live/thumbs/pvz-myanmar-game.jpg)

🌻 အပင်များ vs ဖုတ်များ 🧟 — Plants vs Zombies Myanmar Edition. HTML5 canvas tower defense, 10 levels + endless mode, pure Burmese UI.

[Игра на GitGame](https://gitgame.live/game/pvz-myanmar-game/) · [Репозиторий](https://github.com/mymyanmarland/pvz-myanmar-game)

### ★★★★☆ Ragdoll Riot — $1.05

![Ragdoll Riot](https://gitgame.live/thumbs/ragdoll-riot.jpg)

Ragdoll Riot: website, playable game and privacy policy

[Игра на GitGame](https://gitgame.live/game/ragdoll-riot/) · [Репозиторий](https://github.com/dallingbell23-ui/ragdoll-riot)

### ★★★★☆ Slowmo Fps — $1.05

![Slowmo Fps](https://gitgame.live/thumbs/slowmo-fps.jpg)

Endless runner for phones on Three.js: three lanes, wireframe world, time you can slow down. Playable in the browser.

[Игра на GitGame](https://gitgame.live/game/slowmo-fps/) · [Репозиторий](https://github.com/JohnInWork/slowmo-fps)

### ★★★★☆ Sumo Bounce — $1.05

![Sumo Bounce](https://gitgame.live/thumbs/sumo-bounce.jpg)

Charge, aim, shove your rival out of the shrinking ring. 2P local.

[Игра на GitGame](https://gitgame.live/game/sumo-bounce/) · [Репозиторий](https://github.com/Rainforest-0305/sumo-bounce)

### ★★★★☆ Void Serpent 3D — $1.05

VOID SERPENT // 虚空蛇核 — a neon 3D snake roguelite with incremental progression, built with Three.js. 真 XYZ 三维空间 · 肉鸽进化 · 增量机库。

[Игра на GitGame](https://gitgame.live/game/void-serpent-3d/) · [Репозиторий](https://github.com/EnderBull/void-serpent-3d)

### ★★★★☆ 3D Minesweeper Game By Fable 5 — $1.00

![3D Minesweeper Game By Fable 5](https://gitgame.live/thumbs/3d-minesweeper-game-by-fable-5.jpg)

Remix of xoau79/3D-Minesweeper-Game-by-Fable-5

[Игра на GitGame](https://gitgame.live/game/3d-minesweeper-game-by-fable-5/) · [Репозиторий](https://github.com/agents-dev/3D-Minesweeper-Game-by-Fable-5)

### ★★★★☆ Agezim — $1.00

![Agezim](https://gitgame.live/thumbs/agezim.jpg)

Agezim - clone isometrico de Age of Empires em HTML5 Canvas (JavaScript puro, graficos procedurais)

[Игра на GitGame](https://gitgame.live/game/agezim/) · [Репозиторий](https://github.com/MQZGAMES/Agezim)

### ★★★★☆ Ai Horror Games — $1.00

Three AI models (Claude Opus 5.5, Gemini 4 Argon, Kimi K3.1) got $25 and 3 hours each to make a horror game that scares one person. Play them in your browser.

[Игра на GitGame](https://gitgame.live/game/ai-horror-games/) · [Репозиторий](https://github.com/KostiKoNeuro/ai-horror-games)

### ★★★★☆ Alderhoard — $1.00

![Alderhoard](https://gitgame.live/thumbs/alderhoard.jpg)

An arcade universe in one HTML page — 20+ interlocking games on one map with one save. Vanilla JS + Canvas, zero dependencies, no build. Play it live.

[Игра на GitGame](https://gitgame.live/game/alderhoard/) · [Репозиторий](https://github.com/scottcovert/alderhoard)

### ★★★★☆ Arcade — $1.00

![Arcade](https://gitgame.live/thumbs/arcade.jpg)

A small arcade of quiet browser games. No ads, no accounts, no timers, nothing to install. Free and MIT.

[Игра на GitGame](https://gitgame.live/game/arcade/) · [Репозиторий](https://github.com/markfriedlander/arcade)

### ★★★★☆ Astra Game 2 — $1.00

![Astra Game 2](https://gitgame.live/thumbs/astra-game-2.jpg)

Игра из парсера, авто-деплой.

[Игра на GitGame](https://gitgame.live/game/astra-game-2/) · [Репозиторий](https://github.com/AV-Vignesh/astra-game-2)

### ★★★★☆ Backlog Arcade — $1.00

![Backlog Arcade](https://gitgame.live/thumbs/backlog-arcade.jpg)

Three tiny browser games about life in product teams — padel, toy-car sprints and backlog monsters. Plain JS, no build step, MIT.

[Игра на GitGame](https://gitgame.live/game/backlog-arcade/) · [Репозиторий](https://github.com/fisieek/backlog-arcade)

### ★★★★☆ Biecuewo — $1.00

![Biecuewo](https://gitgame.live/thumbs/biecuewo.jpg)

别Cue我: a one-file mobile web game about surviving the National Day holiday by leaving everyone on read, plus the Douyin video pipeline (headless recording, Qwen3-TTS,…

[Игра на GitGame](https://gitgame.live/game/biecuewo/) · [Репозиторий](https://github.com/syydaniel/biecuewo)

### ★★★★☆ Blob Brawl — $1.00

![Blob Brawl](https://gitgame.live/thumbs/blob-brawl.jpg)

吞吞大乱斗：吞噬成长类网页游戏，单机 + 多人联机大厅与排行榜。Node 服务端 + Docker/Caddy 一键部署

[Игра на GitGame](https://gitgame.live/game/blob-brawl/) · [Репозиторий](https://github.com/FuzzyLogic112/blob-brawl)

### ★★★★☆ Bubble Party — $1.00

泡泡堂·深海大乱斗：Canvas 单文件水泡对战游戏，支持单人 1v3、双人同屏和 GitHub Pages 在线游玩

[Игра на GitGame](https://gitgame.live/game/bubble-party/) · [Репозиторий](https://github.com/LJYIC/bubble-party)

### ★★★★☆ Campus Smash — $1.00

캠퍼스 부수기 — 브라우저에서 바로 하는 캠퍼스 파괴 게임 (three.js)

[Игра на GitGame](https://gitgame.live/game/campus-smash/) · [Репозиторий](https://github.com/elliott-json-park/campus-smash)

### ★★★★☆ Cathedral Builder — $1.00

![Cathedral Builder](https://gitgame.live/thumbs/cathedral-builder.jpg)

Dig rock, cut stone and raise a Gothic cathedral stone by stone before the 13th century ends in this free incremental game in your browser.

[Игра на GitGame](https://gitgame.live/game/cathedral-builder/) · [Репозиторий](https://github.com/pewplay/cathedral-builder)

### ★★★★☆ Chess Game — $1.00

![Chess Game](https://gitgame.live/thumbs/chess_game.jpg)

A browser-based chess game where you play as White against an AI (Black), built with React 19, TypeScript, and Vite. Uses chess.js for all rules—check, checkmate,…

[Игра на GitGame](https://gitgame.live/game/chess_game/) · [Репозиторий](https://github.com/santhosh220z/chess_game)

### ★★★★☆ Darkness Slot Game — $1.00

![Darkness Slot Game](https://gitgame.live/thumbs/darkness-slot-game.jpg)

🦇 DARKNESS — A browser-based 5-reel slot game with 20 paylines, multiplier streak mechanics, bat collection bonus wheel, and free spins. Pure HTML/CSS/JS, no…

[Игра на GitGame](https://gitgame.live/game/darkness-slot-game/) · [Репозиторий](https://github.com/DinkoTrendafilov/Darkness-Slot-Game)

### ★★★★☆ Dogs Of War — $1.00

![Dogs Of War](https://gitgame.live/thumbs/dogs-of-war.jpg)

AI-game, testing qwen3.8 27B vs Claude Opus 5 Max

[Игра на GitGame](https://gitgame.live/game/dogs-of-war/) · [Репозиторий](https://github.com/slampunk/dogs-of-war)

### ★★★★☆ Firebreak Minimax Game — $1.00

![Firebreak Minimax Game](https://gitgame.live/thumbs/firebreak-minimax-game.jpg)

A tactical forest-control strategy game featuring Minimax AI with Alpha-Beta pruning.

[Игра на GitGame](https://gitgame.live/game/firebreak-minimax-game/) · [Репозиторий](https://github.com/SM-Hussain08/firebreak-minimax-game)

### ★★★★☆ Fruit Drop — $1.00

![Fruit Drop](https://gitgame.live/thumbs/fruit-drop.jpg)

Fruit Drop — drop-and-merge physics puzzle game (JS + Matter.js + Capacitor)

[Игра на GitGame](https://gitgame.live/game/fruit-drop/) · [Репозиторий](https://github.com/larsbars/fruit-drop)

### ★★★★☆ Grand Tour — $1.00

![Grand Tour](https://gitgame.live/thumbs/grand-tour.jpg)

Unofficial single-file browser cycling game with one-stage races, a 21-stage Grand Tour, team tactics, drafting, and sprint and mountain competitions.

[Игра на GitGame](https://gitgame.live/game/grand-tour/) · [Репозиторий](https://github.com/seiya058904/Grand-Tour)

### ★★★★☆ Grok Bot Poker Game — $1.00

![Grok Bot Poker Game](https://gitgame.live/thumbs/grok-bot-poker-game.jpg)

Playable Texas Hold'em website

[Игра на GitGame](https://gitgame.live/game/grok-bot-poker-game/) · [Репозиторий](https://github.com/Eric-Cart/grok-bot-poker-game)

### ★★★★☆ Howitzer Duel — $1.00

![Howitzer Duel](https://gitgame.live/thumbs/howitzer-duel.jpg)

An artillery physics game.

[Игра на GitGame](https://gitgame.live/game/howitzer-duel/) · [Репозиторий](https://github.com/dustinrjo/howitzer-duel)

### ★★★★☆ Ink Drop — $1.00

![Ink Drop](https://gitgame.live/thumbs/ink-drop.jpg)

Draw lines, drop the ball, land it in the cup — browser physics game

[Игра на GitGame](https://gitgame.live/game/ink-drop/) · [Репозиторий](https://github.com/shaybergman3-collab/ink-drop)

### ★★★★☆ Klubok — $1.00

![Klubok](https://gitgame.live/thumbs/klubok.jpg)

Klubok: untangle the snakes. Tap a snake and it slithers off the board. Endless procedural levels, offline PWA, no build step.

[Игра на GitGame](https://gitgame.live/game/klubok/) · [Репозиторий](https://github.com/0fuz/klubok)

### ★★★★☆ Kludgeworks — $1.00

![Kludgeworks](https://gitgame.live/thumbs/kludgeworks.jpg)

Steampunk chain-reaction puzzle game (Matter.js + three.js)

[Игра на GitGame](https://gitgame.live/game/kludgeworks/) · [Репозиторий](https://github.com/SITC/Kludgeworks)

### ★★★★☆ Lander — $1.00

![Lander](https://gitgame.live/thumbs/lander.jpg)

Lander Rescue Mission is a browser-based game blending the classics Lunar Lander and Choplifter, set to an ASMR-inspired soundtrack.

[Игра на GitGame](https://gitgame.live/game/lander/) · [Репозиторий](https://github.com/johnnyheggelund/lander)

### ★★★★☆ Mahjong Game — $1.00

![Mahjong Game](https://gitgame.live/thumbs/mahjong-game.jpg)

Mahjong solitaire in the browser — six boards, every deal guaranteed solvable, no build step and no dependencies.

[Игра на GitGame](https://gitgame.live/game/mahjong-game/) · [Репозиторий](https://github.com/ctbot000/mahjong-game)

### ★★★★☆ Match Architect — $1.00

![Match Architect](https://gitgame.live/thumbs/match-architect.jpg)

火柴建築師 Match Architect — 接下世界各地的委託，用最少的火柴搭出建築骨架，撐過 10 秒大地震。AI Browser Game Jam 5

[Игра на GitGame](https://gitgame.live/game/match-architect/) · [Репозиторий](https://github.com/brycekuo-proj/match-architect)

### ★★★★☆ Melon Pals Playground — $1.00

![Melon Pals Playground](https://gitgame.live/thumbs/melon-pals-playground.jpg)

Melon Pals Playground - a kids' physics sandbox game

[Игра на GitGame](https://gitgame.live/game/melon-pals-playground/) · [Репозиторий](https://github.com/nancicatalan-ctrl/melon-pals-playground)

### ★★★★☆ Moonlight English — $1.00

![Moonlight English](https://gitgame.live/thumbs/moonlight-english.jpg)

深夜来客：用英语对话、收集线索、改变结局的两章浏览器剧情游戏。

[Игра на GitGame](https://gitgame.live/game/moonlight-english/) · [Репозиторий](https://github.com/SuperLeilei2026/moonlight-english)

### ★★★★☆ My First Ai Game1 — $1.00

![My First Ai Game1](https://gitgame.live/thumbs/my-first-ai-game1.jpg)

My first game that i made by AI. Thanks, ChatGPT, hope one day i will be able to make a game by myself.1

[Игра на GitGame](https://gitgame.live/game/my-first-ai-game1/) · [Репозиторий](https://github.com/Vickytoria21/my-first-ai-game1)

### ★★★★☆ Office Bonk — $1.00

![Office Bonk](https://gitgame.live/thumbs/office-bonk.jpg)

Annoying coworker? I've got a solution! A ragdoll stress-relief game where you get to bonk your (fully customizable) office nemesis with a bat, fish, or plunger — no HR…

[Игра на GitGame](https://gitgame.live/game/office-bonk/) · [Репозиторий](https://github.com/YukiHarris/office-bonk)

### ★★★★☆ Old Mountain Works — $1.00

![Old Mountain Works](https://gitgame.live/thumbs/old-mountain-works.jpg)

Old Mountain Works - Physics-driven 2.5D mountain climbing and destruction driving game built with Matter.js & Three.js

[Игра на GitGame](https://gitgame.live/game/old-mountain-works/) · [Репозиторий](https://github.com/LetMeCodex/old-mountain-works)

### ★★★★☆ Openroad — $1.00

![Openroad](https://gitgame.live/thumbs/openroad.jpg)

An open-world driving game that runs in a browser. Tarmac, gravel, dust and damage — procedurally generated, no build step.

[Игра на GitGame](https://gitgame.live/game/openroad/) · [Репозиторий](https://github.com/gravityst/OpenRoad)

### ★★★★☆ Orbound — $1.00

![Orbound](https://gitgame.live/thumbs/orbound.jpg)

ORBOUND - a GunBound-inspired turn-based multiplayer artillery game. Vanilla Canvas+JS, real WebSocket multiplayer, Nostr integration, AI-generated art via ComfyUI.

[Игра на GitGame](https://gitgame.live/game/orbound/) · [Репозиторий](https://github.com/ttiiggss/orbound)

### ★★★★☆ Pindou — $1.00

![Pindou](https://gitgame.live/thumbs/pindou.jpg)

拼豆工坊：网页版拼豆，摆豆 + 手动熨烫融合模拟、12 关图纸、图片转拼豆（Lab 最近色匹配）。原生 JS + Canvas 单文件

[Игра на GitGame](https://gitgame.live/game/pindou/) · [Репозиторий](https://github.com/FuzzyLogic112/pindou)

### ★★★★☆ Plinko — $1.00

![Plinko](https://gitgame.live/thumbs/plinko.jpg)

A Plinko game I made with AI

[Игра на GitGame](https://gitgame.live/game/plinko/) · [Репозиторий](https://github.com/MrBlawckss/plinko)

### ★★★★☆ Reconnect — $1.00

![Reconnect](https://gitgame.live/thumbs/reconnect.jpg)

Guide a computer and a mirrored Wi-Fi signal together past firewalls and Ice Walkers in this free puzzle game you play in your browser.

[Игра на GitGame](https://gitgame.live/game/reconnect/) · [Репозиторий](https://github.com/pewplay/reconnect)

### ★★★★☆ Rekt Game — $1.00

![Rekt Game](https://gitgame.live/thumbs/rekt-game.jpg)

REKT — Beat the Crypto Bosses. A single-file browser game: 8 bosses, 6 weapons, hand-written 2D ragdoll, zero dependencies.

[Игра на GitGame](https://gitgame.live/game/rekt-game/) · [Репозиторий](https://github.com/TokenPost/rekt-game)

### ★★★★☆ Rex Chase — $1.00

![Rex Chase](https://gitgame.live/thumbs/rex-chase.jpg)

Игра из парсера, авто-деплой.

[Игра на GitGame](https://gitgame.live/game/rex-chase/) · [Репозиторий](https://github.com/SwikrutD/rex-chase)

### ★★★★☆ Rishu Key Jutsu — $1.00

![Rishu Key Jutsu](https://gitgame.live/thumbs/rishu-key-jutsu.jpg)

Action Martial Arts Touch Typing Combat Game for Web and Windows PC • 100 Levels, 11 Arenas, 60 FPS Canvas Engine

[Игра на GitGame](https://gitgame.live/game/rishu-key-jutsu/) · [Репозиторий](https://github.com/rishu-builds/rishu-key-jutsu)

### ★★★★☆ Robofight — $1.00

![Robofight](https://gitgame.live/thumbs/robofight.jpg)

robofight é uma arena de combate local para dois robôs programados em JavaScript. Cada competidor possui seu próprio editor, console, barra de integridade e placar;…

[Игра на GitGame](https://gitgame.live/game/robofight/) · [Репозиторий](https://github.com/n8nfelipe/robofight)

### ★★★★☆ Save The Dog Shiba — $1.00

![Save The Dog Shiba](https://gitgame.live/thumbs/save-the-dog-shiba.jpg)

Save the Dog — Draw lines to protect your Shiba Inu from angry bees! A fun physics puzzle game.

[Игра на GitGame](https://gitgame.live/game/save-the-dog-shiba/) · [Репозиторий](https://github.com/song3431928081-rgb/save-the-dog-shiba)

### ★★★★☆ Serpent.Io — $1.00

![Serpent.Io](https://gitgame.live/thumbs/serpent.io.jpg)

Open-Source slither.io-style snake game in your browser. Features include 60 AI snakes, Web Assembly, WebGPU or WebGL one HTML file, no download

[Игра на GitGame](https://gitgame.live/game/serpent.io/) · [Репозиторий](https://github.com/CatanCats/Serpent.io)

### ★★★★☆ Threshold Fable 5 1 — $1.00

![Threshold Fable 5 1](https://gitgame.live/thumbs/threshold-fable-5-1.jpg)

A game by fable 5.1 that cost $60 to build. Here's hoping it doesn't suck.

[Игра на GitGame](https://gitgame.live/game/threshold-fable-5-1/) · [Репозиторий](https://github.com/CantankerousPotatomancer/threshold-fable-5-1)

### ★★★★☆ Tidemill — $1.00

![Tidemill](https://gitgame.live/thumbs/tidemill.jpg)

A calm procedural toy-town builder for the browser.

[Игра на GitGame](https://gitgame.live/game/tidemill/) · [Репозиторий](https://github.com/aeiouvcode/tidemill)

### ★★★★☆ Turbo Hills — $1.00

![Turbo Hills](https://gitgame.live/thumbs/turbo-hills.jpg)

Turbo Hills — A 2D physics-based arcade hill climb racing game built with JavaScript, Matter.js, and p5.js.

[Игра на GitGame](https://gitgame.live/game/turbo-hills/) · [Репозиторий](https://github.com/saahiyo/turbo-hills)

### ★★★★☆ Uar Tower Defence — $1.00

![Uar Tower Defence](https://gitgame.live/thumbs/uar-tower-defence.jpg)

Небесний Щит — браузерний tower defense про протиповітряну оборону України

[Игра на GitGame](https://gitgame.live/game/uar-tower-defence/) · [Репозиторий](https://github.com/andrew-shumylo/uar-tower-defence)

### ★★★★☆ Zombie Game — $1.00

![Zombie Game](https://gitgame.live/thumbs/zombie_game.jpg)

just a simple web game made by gemini 3.7 flash

[Игра на GitGame](https://gitgame.live/game/zombie_game/) · [Репозиторий](https://github.com/buxuele/zombie_game)

### ★★★☆☆ 0051 Pochadraw — $0.85

![0051 Pochadraw](https://gitgame.live/thumbs/0051-pochadraw.jpg)

A crayon physics puzzle game with 100 levels and a visual editor to make, test, save, and share contraptions.

[Игра на GitGame](https://gitgame.live/game/0051-pochadraw/) · [Репозиторий](https://github.com/confusionlab/0051-pochadraw)

### ★★★☆☆ Aether Front — $0.85

A polished, dependency-free browser RTS: gather aether, build a strike force, and destroy the corruption core.

[Игра на GitGame](https://gitgame.live/game/aether-front/) · [Репозиторий](https://github.com/ZhuangHT-1201/aether-front)

### ★★★☆☆ After The Sirens — $0.85

![After The Sirens](https://gitgame.live/thumbs/after-the-sirens.jpg)

Original offline open world zombie survival game with driving, multi-floor buildings, survivors, 212 items and 61 recipes.

[Игра на GitGame](https://gitgame.live/game/after-the-sirens/) · [Репозиторий](https://github.com/ChaseHendrick/After-the-Sirens)

### ★★★☆☆ Backcountry 4X4 — $0.85

![Backcountry 4X4](https://gitgame.live/thumbs/backcountry-4x4.jpg)

Free-roam 4x4 wheeling game in a single HTML file — Three.js + Rapier physics

[Игра на GitGame](https://gitgame.live/game/backcountry-4x4/) · [Репозиторий](https://github.com/cmitt23/backcountry-4x4)

### ★★★☆☆ Balance Stack — $0.85

![Balance Stack](https://gitgame.live/thumbs/balance-stack.jpg)

​A zero-dependency HTML5 Canvas physics engine and PWA. Simulates real-time torque, center-of-mass dynamics, and discrete block-locking mechanics for a responsive…

[Игра на GitGame](https://gitgame.live/game/balance-stack/) · [Репозиторий](https://github.com/Thanshika2012/Balance-Stack)

### ★★★☆☆ Bouncy Ball — $0.85

![Bouncy Ball](https://gitgame.live/thumbs/bouncy-ball.jpg)

Launch-and-bounce physics puzzle with trampolines, fans and spikes, plus a built-in level editor.

[Игра на GitGame](https://gitgame.live/game/bouncy-ball/) · [Репозиторий](https://github.com/TimothyHadfield/bouncy-ball)

### ★★★☆☆ Castle Crash — $0.85

![Castle Crash](https://gitgame.live/thumbs/castle-crash.jpg)

Castle Crash: an original physics puzzle game for iPhone. Aim, fire, topple the castle.

[Игра на GitGame](https://gitgame.live/game/castle-crash/) · [Репозиторий](https://github.com/fparro-netizen/castle-crash)

### ★★★☆☆ Chess Master — $0.85

![Chess Master](https://gitgame.live/thumbs/chess-master.jpg)

国际象棋 AI 网页版 · Stockfish 18（WASM/NNUE）全部跑在浏览器本地 · 六档难度 · 复盘分析与评估曲线 · PGN 导入导出 · ECO 开局识别（3810 条）· 纯前端零后端，静态托管即可部署

[Игра на GitGame](https://gitgame.live/game/chess-master/) · [Репозиторий](https://github.com/justa-cai/chess-master)

### ★★★☆☆ Cold Call Crew — $0.85

![Cold Call Crew](https://gitgame.live/thumbs/cold-call-crew.jpg)

A co-op comedy browser game: run the worst call center on Earth against live AI callers.

[Игра на GitGame](https://gitgame.live/game/cold-call-crew/) · [Репозиторий](https://github.com/NaorX/cold-call-crew)

### ★★★☆☆ Inkwave — $0.85

Splatoon-style 4v4 turf-war shooter for the browser, built on three.js. No build step.

[Игра на GitGame](https://gitgame.live/game/inkwave/) · [Репозиторий](https://github.com/jaydendavisnc/inkwave)

### ★★★☆☆ Michi-Neko · Cat's Path — $0.85

![Michi-Neko · Cat's Path](https://gitgame.live/thumbs/michi-neko.jpg)

3D-игра про кота-философа (Three.js, модули с CDN).

[Игра на GitGame](https://gitgame.live/game/michi-neko/) · [Репозиторий](https://github.com/c1t1zen1/Michi-Neko-The-Cat-Philosophers-Path)

### ★★★☆☆ Neon Ledger — $0.85

![Neon Ledger](https://gitgame.live/thumbs/neon-ledger.jpg)

🌃 사이버펑크 트레이딩 타이쿤 — 20개 가상 기업 실시간 캔들차트, 레버리지 롱/숏, 다크웹, M&A, 규제 게이지. 단일 HTML 파일, 외부 의존성 0 | Single-file cyberpunk stock-trading tycoon browser game

[Игра на GitGame](https://gitgame.live/game/neon-ledger/) · [Репозиторий](https://github.com/jeiel85/neon-ledger)

### ★★★☆☆ Neon Tetris — $0.85

![Neon Tetris](https://gitgame.live/thumbs/neon-tetris.jpg)

霓虹方块 · Neon Tetris — 单文件网页版 + Kotlin/Jetpack Compose 安卓原生版

[Игра на GitGame](https://gitgame.live/game/neon-tetris/) · [Репозиторий](https://github.com/longwei3/neon-tetris)

### ★★★☆☆ Poker Game — $0.85

![Poker Game](https://gitgame.live/thumbs/poker-game.jpg)

No-Limit Texas Hold'em in the browser: three AI opponents, real side pots, no build step.

[Игра на GitGame](https://gitgame.live/game/poker-game/) · [Репозиторий](https://github.com/ctbot000/poker-game)

### ★★★☆☆ Sea Battle — $0.85

![Sea Battle](https://gitgame.live/thumbs/sea-battle.jpg)

Classic naval combat game with tactical AI and realtime online multiplayer

[Игра на GitGame](https://gitgame.live/game/sea-battle/) · [Репозиторий](https://github.com/abi4ka/Sea-Battle)

### ★★★☆☆ Seventh Archive — $0.85

![Seventh Archive](https://gitgame.live/thumbs/seventh-archive.jpg)

第七号档案：Three.js 第三人称 3D 雨夜密室逃脱，五道连环机关、手电与碰撞、自动存档；WebGL2 不可用时回退软件渲染

[Игра на GitGame](https://gitgame.live/game/seventh-archive/) · [Репозиторий](https://github.com/FuzzyLogic112/seventh-archive)

### ★★★☆☆ Super Nobooth — $0.85

![Super Nobooth](https://gitgame.live/thumbs/super-nobooth.jpg)

Retro arcade game about booking meetings at a conference with no booth. Cast invented live by Claude Fable 5.1.

[Игра на GitGame](https://gitgame.live/game/super-nobooth/) · [Репозиторий](https://github.com/dennis-noah/super-nobooth)

### ★★★☆☆ Zero G Playground — $0.85

![Zero G Playground](https://gitgame.live/thumbs/zero-g-playground.jpg)

8-bit zero-gravity arcade game (무중력 놀이터)

[Игра на GitGame](https://gitgame.live/game/zero-g-playground/) · [Репозиторий](https://github.com/Brandon-Jun/zero-g-playground)

### ★★★☆☆ All In Texas — $0.80

![All In Texas](https://gitgame.live/thumbs/all-in-texas.jpg)

All in TEXAS — 勝率・アウツ・必要勝率が見える、初心者のためのテキサスホールデム。通信なし・1ファイル・打ち筋の違う5人のCPU

[Игра на GitGame](https://gitgame.live/game/all-in-texas/) · [Репозиторий](https://github.com/pikaring/all-in-texas)

### ★★★☆☆ Bo Cui Chill Game — $0.80

![Bo Cui Chill Game](https://gitgame.live/thumbs/bo-cui-chill-game.jpg)

🌲 Game bổ củi 3D chill guy - Three.js. Tạo bởi DeepSeek Harness

[Игра на GitGame](https://gitgame.live/game/bo-cui-chill-game/) · [Репозиторий](https://github.com/OdinHoang03/bo-cui-chill-game)

### ★★★☆☆ Bogaz Vapuru — $0.80

Bosphorus ferry captain in 3D: dock at 6 piers against current and wind, keep the timetable. Browser game built by Claude Fable 5.1 · Boğaz'da vapur kaptanlığı: akıntıya…

[Игра на GitGame](https://gitgame.live/game/bogaz-vapuru/) · [Репозиторий](https://github.com/Furkiozknn/bogaz-vapuru)

### ★★★☆☆ Cacador — $0.80

![Cacador](https://gitgame.live/thumbs/cacador.jpg)

🎯 Caçador — jogo de caçada visto de cima no navegador (celular e PC): recriação do clássico Flash com arte, sons e código próprios. Ranking, PWA.

[Игра на GitGame](https://gitgame.live/game/cacador/) · [Репозиторий](https://github.com/alequizao/cacador)

### ★★★☆☆ Crab Dash — $0.80

![Crab Dash](https://gitgame.live/thumbs/crab-dash.jpg)

A one-button rhythm platformer starring a crab. Six levels, practice mode, an icon kit and a level editor.

[Игра на GitGame](https://gitgame.live/game/crab-dash/) · [Репозиторий](https://github.com/itsdannyt/crab-dash)

### ★★★☆☆ Floppy Knight — $0.80

![Floppy Knight](https://gitgame.live/thumbs/floppy-knight.jpg)

Floppy Knight - HTML5 ragdoll-knight escort game for Cloudflare Pages

[Игра на GitGame](https://gitgame.live/game/floppy-knight/) · [Репозиторий](https://github.com/ZaneyP/floppy-knight)

### ★★★☆☆ Gangho — $0.80

![Gangho](https://gitgame.live/thumbs/gangho.jpg)

무림 고수 22명이 3대3으로 영단을 쟁탈하는 브라우저 무협 대전 게임 — Three.js

[Игра на GitGame](https://gitgame.live/game/gangho/) · [Репозиторий](https://github.com/NuclearPunch/gangho)

### ★★★☆☆ Hexablox Sorting Game — $0.80

![Hexablox Sorting Game](https://gitgame.live/thumbs/hexablox-sorting-game.jpg)

A color sorting game where you play in a hive

[Игра на GitGame](https://gitgame.live/game/hexablox-sorting-game/) · [Репозиторий](https://github.com/abraham-ny/HexaBlox-Sorting-Game)

### ★★★☆☆ Infanti Grok — $0.80

![Infanti Grok](https://gitgame.live/thumbs/infanti-grok.jpg)

Infanti Grok — low-poly music stage game (Jelly Band style)

[Игра на GitGame](https://gitgame.live/game/infanti-grok/) · [Репозиторий](https://github.com/pulananave/infanti-grok)

### ★★★☆☆ Kids Games — $0.80

Free, quietly educational browser games for kids. Make the characters look like your own family.

[Игра на GitGame](https://gitgame.live/game/kids-games/) · [Репозиторий](https://github.com/GarySto/kids-games)

### ★★★☆☆ Lifesim — $0.80

![Lifesim](https://gitgame.live/thumbs/lifesim.jpg)

Life Sim: free life simulator game on Telegram. Live a whole life year by year, make choices, reach life goals and earn your life title. AI-written stories, 11 languages.

[Игра на GitGame](https://gitgame.live/game/lifesim/) · [Репозиторий](https://github.com/jeremstyke/lifesim)

### ★★★☆☆ Little Flock · 小羊慢慢 — $0.80

![Little Flock · 小羊慢慢](https://gitgame.live/thumbs/little-flock.jpg)

Уютная ферма: расти овечек и обустраивай остров. Собрано из исходника. ⚠ интерфейс на китайском.

[Игра на GitGame](https://gitgame.live/game/little-flock/) · [Репозиторий](https://github.com/songkeys/little-flock)

### ★★★☆☆ Magnetic Courier — $0.80

![Magnetic Courier](https://gitgame.live/thumbs/magnetic-courier.jpg)

A neon one-touch physics game about magnetic momentum and precision delivery.

[Игра на GitGame](https://gitgame.live/game/magnetic-courier/) · [Репозиторий](https://github.com/maple-xin/magnetic-courier)

### ★★★☆☆ Texas Holdem Trainer — $0.80

单文件、零依赖的德州扑克练习器：内置 GTO 翻前表、七种性格 AI、三档难度、蒙特卡洛实时胜率、复盘讲评、牌谱回放、统计成就与挑战模式，支持手机竖屏/横屏

[Игра на GitGame](https://gitgame.live/game/texas-holdem-trainer/) · [Репозиторий](https://github.com/InoriMutsumi/texas-holdem-trainer)

### ★★★☆☆ Alone Star — $0.75

![Alone Star](https://gitgame.live/thumbs/alone-star.jpg)

created in 2 hours. just enjoy this peak game

[Игра на GitGame](https://gitgame.live/game/alone-star/) · [Репозиторий](https://github.com/monkedDev/alone-star)

### ★★★☆☆ Ball Physics Game — $0.75

![Ball Physics Game](https://gitgame.live/thumbs/ball-physics-game.jpg)

Игра из парсера, авто-деплой.

[Игра на GitGame](https://gitgame.live/game/ball-physics-game/) · [Репозиторий](https://github.com/Brandon-Valley/ball-physics-game)

### ★★★☆☆ Blackwater Dock — $0.75

![Blackwater Dock](https://gitgame.live/thumbs/blackwater-dock.jpg)

BLACKWATER DOCK — klimatyczna gra przeglądarkowa o łodzi podwodnej: sonar echo-pulse, sztormy, precyzyjne dokowanie. Jeden plik index.html, vanilla JS + canvas 2D +…

[Игра на GitGame](https://gitgame.live/game/blackwater-dock/) · [Репозиторий](https://github.com/Trochim86/blackwater-dock)

### ★★★☆☆ Claude of Legends — $0.75

![Claude of Legends](https://gitgame.live/thumbs/claude-of-legends.jpg)

Браузерная 5v5 MOBA: 3 линии, 10 чемпионов, лес, туман войны. Лендинг задеплоен; для полной игры нужен серверный бэкенд.

[Игра на GitGame](https://gitgame.live/game/claude-of-legends/) · [Репозиторий](https://github.com/killian01/claude-of-legends)

### ★★★☆☆ Cosmic Vanguard — $0.75

![Cosmic Vanguard](https://gitgame.live/thumbs/cosmic-vanguard.jpg)

Original 2D arcade beat ’em up built with HTML5 Canvas and JavaScript. Choose your hero, fight the forces of the Void, recruit new Vanguard members and play solo or in…

[Игра на GitGame](https://gitgame.live/game/cosmic-vanguard/) · [Репозиторий](https://github.com/MrPowerUp82/cosmic-vanguard)

### ★★★☆☆ Game Sample Corner Mart — $0.75

![Game Sample Corner Mart](https://gitgame.live/thumbs/game-sample-corner-mart.jpg)

A browser-based 3D convenience store game built with GPT-6 Astra, Blender, and Three.js.

[Игра на GitGame](https://gitgame.live/game/game-sample-corner-mart/) · [Репозиторий](https://github.com/ericyanpek/game-sample-corner-mart)

### ★★★☆☆ Game With Ai Starter Pack — $0.75

![Game With Ai Starter Pack](https://gitgame.live/thumbs/game-with-ai-starter-pack.jpg)

Prompts that move: an Opus 5.5 field guide for games, art, animation, 3D and coded video

[Игра на GitGame](https://gitgame.live/game/game-with-ai-starter-pack/) · [Репозиторий](https://github.com/2600th/game-with-ai-starter-pack)

### ★★★☆☆ Gravity — $0.75

![Gravity](https://gitgame.live/thumbs/gravity.jpg)

gravity game

[Игра на GitGame](https://gitgame.live/game/gravity/) · [Репозиторий](https://github.com/nikhilkrajput/gravity)

### ★★★☆☆ Hold Please — $0.75

![Hold Please](https://gitgame.live/thumbs/hold-please.jpg)

A fast portrait physics game about staying on the call while the office falls apart.

[Игра на GitGame](https://gitgame.live/game/hold-please/) · [Репозиторий](https://github.com/smithmw7/hold-please)

### ★★★☆☆ Icy Climb — $0.75

![Icy Climb](https://gitgame.live/thumbs/icy-climb.jpg)

Run, jump and combo your way up an endless frozen tower. An arcade climber for Android, Windows and the browser, inspired by Icy Tower.

[Игра на GitGame](https://gitgame.live/game/icy-climb/) · [Репозиторий](https://github.com/Wolklaw/icy-climb)

### ★★★☆☆ Low Tide Letters — $0.75

![Low Tide Letters](https://gitgame.live/thumbs/low-tide-letters.jpg)

Low Tide Letters: a small hand-drawn browser JRPG about a fishing town going quiet, and the things nobody said

[Игра на GitGame](https://gitgame.live/game/low-tide-letters/) · [Репозиторий](https://github.com/m1omg/Low-Tide-Letters)

### ★★★☆☆ Pen Flick — $0.75

Pen Flick: Desk Duel, a top-down pen-flicking browser game (HTML5 Canvas + Matter.js) with 6 pens and 3 AI difficulty levels

[Игра на GitGame](https://gitgame.live/game/pen-flick/) · [Репозиторий](https://github.com/shahriarahi/pen-flick)

### ★★★☆☆ Puchiworkshop — $0.75

![Puchiworkshop](https://gitgame.live/thumbs/puchiworkshop.jpg)

A playful browser physics sandbox for grabbing, stretching, slicing and smashing colorful objects.

[Игра на GitGame](https://gitgame.live/game/puchiworkshop/) · [Репозиторий](https://github.com/cabal312512/puchiworkshop)

### ★★★☆☆ Qwen3.8 27B 3D Snake — $0.75

![Qwen3.8 27B 3D Snake](https://gitgame.live/thumbs/qwen3.8-27b-3d-snake.jpg)

3d snake game, generated from single prompt by local model qwen3.8-27b

[Игра на GitGame](https://gitgame.live/game/qwen3.8-27b-3d-snake/) · [Репозиторий](https://github.com/Armofast/qwen3.8-27b-3d-snake)

### ★★★☆☆ Range — $0.75

![Range](https://gitgame.live/thumbs/range.jpg)

A realistic, single-player, first-person pistol training simulator that runs entirely in the browser.

[Игра на GitGame](https://gitgame.live/game/range/) · [Репозиторий](https://github.com/zrnge/range)

### ★★★☆☆ Richman 3D — $0.75

![Richman 3D](https://gitgame.live/thumbs/richman-3d.jpg)

🎲 大富翁3D —— 完全复刻经典大富翁核心玩法的 3D 网页游戏：52 格中国城市棋盘、16 色组×2 城、掷骰买地盖房收租、机会/事件翻牌盲选、道具卡，全部素材代码绘制，支持 2-4 人同屏对战与 AI。

[Игра на GitGame](https://gitgame.live/game/richman-3d/) · [Репозиторий](https://github.com/Yakamozli/richman-3d)

### ★★★☆☆ 000051 Pochadraw — $0.70

A crayon physics puzzle game with 100 levels and a visual editor to make, test, save, and share contraptions.

[Игра на GitGame](https://gitgame.live/game/000051-pochadraw/) · [Репозиторий](https://github.com/confusionlab/000051-pochadraw)

### ★★★☆☆ 1010 Game Physics — $0.70

![1010 Game Physics](https://gitgame.live/thumbs/1010-game-physics.jpg)

1010 PHYSICS — 1010! with real Matter.js physics: tumbling blocks, 16 chaos events, 4 weapons, 8 themes, 7 languages. React + Vite + Tailwind, single-file build.

[Игра на GitGame](https://gitgame.live/game/1010-game-physics/) · [Репозиторий](https://github.com/l10yd/1010-game-physics)

### ★★★☆☆ Amyra Ind Usa Export — $0.70

![Amyra Ind Usa Export](https://gitgame.live/thumbs/amyra-ind-usa-export.jpg)

The Journey of One Box: a pixel-art game that teaches anyone in India to export a product and sell it on Amazon USA, in plain words.

[Игра на GitGame](https://gitgame.live/game/amyra-ind-usa-export/) · [Репозиторий](https://github.com/edock-in/amyra-ind-usa-export)

### ★★★☆☆ Amyra Ind Usa Export 2 — $0.70

![Amyra Ind Usa Export 2](https://gitgame.live/thumbs/amyra-ind-usa-export-2.jpg)

Goods Out, Money Home: an interactive globe that shows anyone in India how one product travels to an Amazon customer in America, and how the money comes back, in plain…

[Игра на GitGame](https://gitgame.live/game/amyra-ind-usa-export-2/) · [Репозиторий](https://github.com/edock-in/amyra-ind-usa-export-2)

### ★★★☆☆ Angkor Architecture — $0.70

![Angkor Architecture](https://gitgame.live/thumbs/angkor-architecture.jpg)

Browser-based isometric city-building game in pre-production, inspired by the hydraulic engineering of the medieval Khmer Empire. Built with TypeScript, PixiJS, and…

[Игра на GitGame](https://gitgame.live/game/angkor-architecture/) · [Репозиторий](https://github.com/RithyBondeth/Angkor-Architecture)

### ★★★☆☆ Angry Raven — $0.70

![Angry Raven](https://gitgame.live/thumbs/angry-raven.jpg)

Angry Raven: a small physics game made for the Raven showcase (English and Chinese)

[Игра на GitGame](https://gitgame.live/game/angry-raven/) · [Репозиторий](https://github.com/LivXue/angry-raven)

### ★★★☆☆ Beat Me — $0.70

![Beat Me](https://gitgame.live/thumbs/beat-me.jpg)

A browser punching-bag game in vanilla JavaScript and Canvas. No dependencies and no build step: throw physics, a combo system, and sound effects synthesised with Web…

[Игра на GitGame](https://gitgame.live/game/beat-me/) · [Репозиторий](https://github.com/ne-he/beat-me)

### ★★★☆☆ Bounce Synth — $0.70

![Bounce Synth](https://gitgame.live/thumbs/bounce-synth.jpg)

A neon physics puzzle game where you draw musical bounce lines to guide orbs into a portal. Features procedural music, interactive physics, 6 challenging levels,…

[Игра на GitGame](https://gitgame.live/game/bounce-synth/) · [Репозиторий](https://github.com/vigneshwarann901-art/bounce-synth)

### ★★★☆☆ Bricklab — $0.70

![Bricklab](https://gitgame.live/thumbs/bricklab.jpg)

A free 3D brick workshop that runs in your browser. No build step, no account.

[Игра на GitGame](https://gitgame.live/game/bricklab/) · [Репозиторий](https://github.com/swiftugandan/bricklab)

### ★★★☆☆ Cinderbelt — $0.70

A top-down 3D space game in your browser: mine asteroids, trade, fight pirates and build your ship from parts. Made with Claude Code agents.

[Игра на GitGame](https://gitgame.live/game/cinderbelt/) · [Репозиторий](https://github.com/amoreo140/cinderbelt)

### ★★★☆☆ Cla Go — $0.70

![Cla Go](https://gitgame.live/thumbs/cla-go.jpg)

网页版战术射击游戏：拟真射击手感 + 爆发式滑铲。纯静态 three.js，双击 index.html 即玩。

[Игра на GitGame](https://gitgame.live/game/cla-go/) · [Репозиторий](https://github.com/Kwusv55/Cla-Go)

### ★★★☆☆ Claw Friends — $0.70

![Claw Friends](https://gitgame.live/thumbs/claw-friends.jpg)

A cozy 3D anime-style claw machine arcade for the browser: physics claws, plush collecting and dress-up, built with Three.js and Rapier.

[Игра на GitGame](https://gitgame.live/game/claw-friends/) · [Репозиторий](https://github.com/GianneAngely/claw-friends)

### ★★★☆☆ Darkness Elements Slot Game — $0.70

![Darkness Elements Slot Game](https://gitgame.live/thumbs/darkness-elements-slot-game.jpg)

🧛 Darkness Elements — 8-symbol, 40-line horror-themed slot game with Full Screen Bonus, multipliers, progressive jackpot, and Rare Collection. Includes HTML/JS playable…

[Игра на GitGame](https://gitgame.live/game/darkness-elements-slot-game/) · [Репозиторий](https://github.com/DinkoTrendafilov/Darkness-Elements-Slot-Game)

### ★★★☆☆ Deathstar — $0.70

![Deathstar](https://gitgame.live/thumbs/deathstar.jpg)

A browser-based 3D space combat game built with Babylon.js, TypeScript, and Vite, featuring arcade flight controls, enemy squadrons, procedural visuals, progressive…

[Игра на GitGame](https://gitgame.live/game/deathstar/) · [Репозиторий](https://github.com/jeffotoni/deathstar)

### ★★★☆☆ Defend The Dog — $0.70

A two-level H5 drawing-defense game built with Phaser 3 and Matter.js.

[Игра на GitGame](https://gitgame.live/game/defend-the-dog/) · [Репозиторий](https://github.com/tanglong-1/defend-the-dog)

### ★★★☆☆ GPT-6 City Crisis — $0.70

![GPT-6 City Crisis](https://gitgame.live/thumbs/gpt6-city-crisis.jpg)

Кризис-менеджмент города на Three.js. Собрано из исходника (Vite).

[Игра на GitGame](https://gitgame.live/game/gpt6-city-crisis/) · [Репозиторий](https://github.com/hlforever11/gpt6-city-crisis)

### ★★★☆☆ Gengling — $0.70

![Gengling](https://gitgame.live/thumbs/gengling.jpg)

梗灵大陆 GengLing Continent — 三消+RPG 解压小游戏 | Match-3 + RPG casual game. Pure H5 (Canvas + WebAudio, zero assets), packaged as Android APK

[Игра на GitGame](https://gitgame.live/game/gengling/) · [Репозиторий](https://github.com/wuliao00/gengling)

### ★★★☆☆ Hagashi Master — $0.70

![Hagashi Master](https://gitgame.live/thumbs/hagashi-master.jpg)

アイドル握手会の「剥がし」になって、握手の秒数を心の中で数えてピッタリで剥がすブラウザゲーム

[Игра на GitGame](https://gitgame.live/game/hagashi-master/) · [Репозиторий](https://github.com/yabon3/hagashi-master)

### ★★★☆☆ Hallenlegenden — $0.70

![Hallenlegenden](https://gitgame.live/thumbs/hallenlegenden.jpg)

Retro-Handball im Pixel-Look: 7 gegen 7, 36 Vereine, Karriere mit Transfers und Pokal. Kostenloses Browsergame mit Tastatur-, Gamepad- und Touch-Steuerung.

[Игра на GitGame](https://gitgame.live/game/hallenlegenden/) · [Репозиторий](https://github.com/tobwil/HallenLegenden)

### ★★★☆☆ Havana22 Game — $0.70

![Havana22 Game](https://gitgame.live/thumbs/havana22-game.jpg)

HAVANA 22 — Večernja smjena: a night-shift game about the Havana 22 cigar lounge in Zagreb

[Игра на GitGame](https://gitgame.live/game/havana22-game/) · [Репозиторий](https://github.com/Zheruel/havana22-game)

### ★★★☆☆ Honey Line — $0.70

Honey Line: draw one line of honey, save your buddy from the bees.

[Игра на GitGame](https://gitgame.live/game/honey-line/) · [Репозиторий](https://github.com/bishojbk/honey-line)

### ★★★☆☆ Huecorn — $0.70

![Huecorn](https://gitgame.live/thumbs/huecorn.jpg)

Guide a unicorn through seven rainbow platforming levels, collecting colour crystals that reshape the world. Free to play in your browser.

[Игра на GitGame](https://gitgame.live/game/huecorn/) · [Репозиторий](https://github.com/pewplay/huecorn)

### ★★★☆☆ Iron Tide Submarine — $0.70

![Iron Tide Submarine](https://gitgame.live/thumbs/iron-tide-submarine.jpg)

WWII-inspired 3D submarine patrol game. Hunt convoys, fire torpedoes, and evade destroyers in your browser. Inspired by Silent Hunter; built with Three.js.

[Игра на GitGame](https://gitgame.live/game/iron-tide-submarine/) · [Репозиторий](https://github.com/eforus-overseer/iron-tide-submarine)

### ★★★☆☆ Lemmingsvc — $0.70

![Lemmingsvc](https://gitgame.live/thumbs/lemmingsvc.jpg)

Lemmings, but they're VCs. A browser tribute to the 1991 classic — guide the herd into your round before they follow each other off a cliff.

[Игра на GitGame](https://gitgame.live/game/lemmingsvc/) · [Репозиторий](https://github.com/brettgoldstein3/lemmingsvc)

### ★★★☆☆ Linefold — $0.70

![Linefold](https://gitgame.live/thumbs/linefold.jpg)

A small city, moving - an original browser subway design game.

[Игра на GitGame](https://gitgame.live/game/linefold/) · [Репозиторий](https://github.com/aeiouvcode/linefold)

### ★★★☆☆ Malandrins — $0.70

![Malandrins](https://gitgame.live/thumbs/malandrins.jpg)

Testing GPT Astra for web game development.

[Игра на GitGame](https://gitgame.live/game/malandrins/) · [Репозиторий](https://github.com/dani-beltran/malandrins)

### ★★★☆☆ Modernjet Dogfight — $0.70

![Modernjet Dogfight](https://gitgame.live/thumbs/modernjet-dogfight.jpg)

브라우저에서 바로 돌아가는 한반도 상공 F-22A 도그파이팅 시뮬레이터 · 3D 클릭커블 콕핏 · KC-135R 공중급유

[Игра на GitGame](https://gitgame.live/game/modernjet-dogfight/) · [Репозиторий](https://github.com/salmonashimi3/modernjet-dogfight)

### ★★★☆☆ Monopoly — $0.70

![Monopoly](https://gitgame.live/thumbs/monopoly.jpg)

Experience a Monopoly board game featuring options to compete against the computer or challenge a friend in local multiplayer mode.

[Игра на GitGame](https://gitgame.live/game/monopoly/) · [Репозиторий](https://github.com/johnnyheggelund/monopoly)

### ★★★☆☆ Musical Chairs — $0.70

![Musical Chairs](https://gitgame.live/thumbs/musical-chairs.jpg)

Musical Chairs: when the music stops, grab a chair. A party game on Onceworlds.

[Игра на GitGame](https://gitgame.live/game/musical-chairs/) · [Репозиторий](https://github.com/onceworlds-games/musical-chairs)

### ★★★☆☆ Necrotris — $0.70

![Necrotris](https://gitgame.live/thumbs/necrotris.jpg)

Tetris, except what you stack is alive. Settled blocks replicate; tidy stacking is what kills you.

[Игра на GitGame](https://gitgame.live/game/necrotris/) · [Репозиторий](https://github.com/parttimediarybehavior/necrotris)

### ★★★☆☆ Neon Astra — $0.70

![Neon Astra](https://gitgame.live/thumbs/neon-astra.jpg)

NEON ASTRA browser game — compiled static GitHub Pages deployment

[Игра на GitGame](https://gitgame.live/game/neon-astra/) · [Репозиторий](https://github.com/stevenflyai/neon-astra)

### ★★★☆☆ Neon Ball — $0.70

![Neon Ball](https://gitgame.live/thumbs/neon-ball.jpg)

Neon Ball - browser physics game with level constructor and community levels

[Игра на GitGame](https://gitgame.live/game/neon-ball/) · [Репозиторий](https://github.com/NikolaiGorovikov/Neon-ball)

### ★★★☆☆ Neon Grid — $0.70

![Neon Grid](https://gitgame.live/thumbs/neon-grid.jpg)

⚡ Neon circuit-connection puzzle. 100 levels + daily puzzles. Offline. Single HTML file, zero dependencies.

[Игра на GitGame](https://gitgame.live/game/neon-grid/) · [Репозиторий](https://github.com/sakibsheikho69252-netizen/neon-grid)

### ★★★☆☆ Pacman Clone — $0.70

![Pacman Clone](https://gitgame.live/thumbs/pacman-clone.jpg)

AI-generated Pac-Man style arcade game for desktop and mobile browsers, offline-capable, written by Claude Code

[Игра на GitGame](https://gitgame.live/game/pacman-clone/) · [Репозиторий](https://github.com/boromisp/pacman-clone)

### ★★★☆☆ Pass The Bomb — $0.70

![Pass The Bomb](https://gitgame.live/thumbs/pass-the-bomb.jpg)

Pass the Bomb: tag someone before it blows. A party game on Onceworlds.

[Игра на GitGame](https://gitgame.live/game/pass-the-bomb/) · [Репозиторий](https://github.com/onceworlds-games/pass-the-bomb)

### ★★★☆☆ PegSort — $0.70

![PegSort](https://gitgame.live/thumbs/pegsort.jpg)

3D-головоломка: сортируй цветные кольца по столбикам. Язык-независимая, тач.

[Игра на GitGame](https://gitgame.live/game/pegsort/) · [Репозиторий](https://github.com/WheatFordTide/PegSort)

### ★★★☆☆ Poker — $0.70

![Poker](https://gitgame.live/thumbs/poker.jpg)

Little vibecoded Texas hold-em game

[Игра на GitGame](https://gitgame.live/game/poker/) · [Репозиторий](https://github.com/Winteractiv/Poker)

### ★★★☆☆ Prism Relay — $0.70

A neon light-routing puzzle game: rotate mirrors and splitters, fold beams through portals, and charge every receiver across three episodes. Free personal play under…

[Игра на GitGame](https://gitgame.live/game/prism-relay/) · [Репозиторий](https://github.com/AegeanWorks/Prism-Relay)

### ★★★☆☆ Privateers — $0.70

俯視角海盜海戰網頁遊戲 · A top-down pirate naval battle browser game built with Phaser 3

[Игра на GitGame](https://gitgame.live/game/privateers/) · [Репозиторий](https://github.com/howwmingnew/Privateers)

### ★★★☆☆ Ragdollshooter Webgl — $0.70

![Ragdollshooter Webgl](https://gitgame.live/thumbs/ragdollshooter-webgl.jpg)

Playable WebGL build of Ragdoll Gun Shooter. Compiled game only.

[Игра на GitGame](https://gitgame.live/game/ragdollshooter-webgl/) · [Репозиторий](https://github.com/aillmdevel-tech/RagdollShooter-WebGL)

### ★★★☆☆ Rewind Heist — $0.70

![Rewind Heist](https://gitgame.live/thumbs/rewind-heist.jpg)

Time-loop stealth heist game: every loop you play becomes a ghost. Custom WebGL 3D engine, no build step.

[Игра на GitGame](https://gitgame.live/game/rewind-heist/) · [Репозиторий](https://github.com/rohitpatil9121/rewind-heist)

### ★★★☆☆ Rink Rivals — $0.70

![Rink Rivals](https://gitgame.live/thumbs/rink-rivals.jpg)

Real-time multiplayer ice hockey for mobile browsers, built from scratch with Canvas 2D, custom physics and Firebase.

[Игра на GitGame](https://gitgame.live/game/rink-rivals/) · [Репозиторий](https://github.com/MGanoub/rink-rivals)

### ★★★☆☆ Rpg Car Game — $0.70

![Rpg Car Game](https://gitgame.live/thumbs/rpg-car-game.jpg)

A browser-based 3D off-road driving simulation built with Three.js WebGPU and Rapier 3D physics. Features procedural terrain, multiple biomes, destructible environments,…

[Игра на GitGame](https://gitgame.live/game/rpg-car-game/) · [Репозиторий](https://github.com/rsamwilson2323-cloud/rpg-car-game)

### ★★★☆☆ Runecraft Playable — $0.70

![Runecraft Playable](https://gitgame.live/thumbs/runecraft-playable.jpg)

Playable ad для RuneCraft Survivor: roguelite-survivor с крафтом заклинаний из рун. Чистый JavaScript + Canvas, один HTML на 1,6 МБ, спрайты из 3D-моделей игры, MRAID /…

[Игра на GitGame](https://gitgame.live/game/runecraft-playable/) · [Репозиторий](https://github.com/Shark26-reg/runecraft-playable)

### ★★★☆☆ Sallu Theft Auto — $0.70

![Sallu Theft Auto](https://gitgame.live/thumbs/sallu-theft-auto.jpg)

GTA-стайл открытый мир: неоновый город, машины, погони. WASD+мышь. Three.js. Все текстуры/модели AI-сгенерены.

[Игра на GitGame](https://gitgame.live/game/sallu-theft-auto/) · [Репозиторий](https://github.com/salmannawaz786/sallu-theft-auto)

### ★★★☆☆ Singularity Online — $0.70

![Singularity Online](https://gitgame.live/thumbs/singularity-online.jpg)

Code-only browser MMORPG parody: e/acc vs EA champions, procedural three.js world, WebSocket realm with bots, quests and a Moloch raid.

[Игра на GitGame](https://gitgame.live/game/singularity-online/) · [Репозиторий](https://github.com/peterxing/singularity-online)

### ★★★☆☆ Skate Park — $0.70

![Skate Park](https://gitgame.live/thumbs/skate-park.jpg)

A painterly third-person skateboarding game for the browser: a beachside park at golden hour, built with three.js, TypeScript and Vite.

[Игра на GitGame](https://gitgame.live/game/skate-park/) · [Репозиторий](https://github.com/StarKnightt/skate-park)

### ★★★☆☆ Skyhook — $0.70

![Skyhook](https://gitgame.live/thumbs/skyhook.jpg)

Цепляйся тросом, раскачивайся и лезь вверх; золото толкает разлом назад. Tap/Space.

[Игра на GitGame](https://gitgame.live/game/skyhook/) · [Репозиторий](https://github.com/leopechnicki/skyhook)

### ★★★☆☆ Sobosuba — $0.70

![Sobosuba](https://gitgame.live/thumbs/sobosuba.jpg)

Browser fan remake of the squishy merge game sobosuba (soft-body physics in plain JS)

[Игра на GitGame](https://gitgame.live/game/sobosuba/) · [Репозиторий](https://github.com/Noam-Elisha/sobosuba)

### ★★★☆☆ Sonar Maze — $0.70

![Sonar Maze](https://gitgame.live/thumbs/sonar-maze.jpg)

Ты слеп в лабиринте — каждый импульс сонара на миг освещает стены, батареи и охотников. 5 уровней. Встроенный мобильный стик + тап.

[Игра на GitGame](https://gitgame.live/game/sonar-maze/) · [Репозиторий](https://github.com/endurovojta173/Sonar_Maze_Profiq_Contest)

### ★★★☆☆ Squid Game Using Gemini 3.8 Flash Model — $0.70

![Squid Game Using Gemini 3.8 Flash Model](https://gitgame.live/thumbs/squid-game-using-gemini-3.8-flash-model.jpg)

Learning How The Ai Agents Actually Builds A Product End To End. Testing The Capabilities Of Gemini New Model 3.8 Flash

[Игра на GitGame](https://gitgame.live/game/squid-game-using-gemini-3.8-flash-model/) · [Репозиторий](https://github.com/RehanShaikh23/Squid-Game-Using-Gemini-3.8-Flash-Model)

### ★★★☆☆ Starloom — $0.70

![Starloom](https://gitgame.live/thumbs/starloom.jpg)

STARLOOM: a browser arcade game where you draw loops of light to trap enemies. Single-file HTML, CSS and canvas JavaScript, mobile-friendly.

[Игра на GitGame](https://gitgame.live/game/starloom/) · [Репозиторий](https://github.com/yash262626/starloom)

### ★★★☆☆ Stormglass — $0.70

![Stormglass](https://gitgame.live/thumbs/stormglass.jpg)

A third-person 3D elemental physics game by Dirty Boy Devs.

[Игра на GitGame](https://gitgame.live/game/stormglass/) · [Репозиторий](https://github.com/kylefriesmarketing/stormglass)

### ★★★☆☆ Tentakel Toast — $0.70

![Tentakel Toast](https://gitgame.live/thumbs/tentakel-toast.jpg)

Tentakel-Toast – ein inoffizielles Day-of-the-Tentacle-Fanspiel im Browser (Point & Click, 3 Zeitebenen)

[Игра на GitGame](https://gitgame.live/game/tentakel-toast/) · [Репозиторий](https://github.com/madd1in/tentakel-toast)

### ★★★☆☆ Tesla Roadster Simulation — $0.70

Tesla Roadster Simulation: 3D browser simulator with PS5 controller and keyboard support, runs on Windows and macOS

[Игра на GitGame](https://gitgame.live/game/tesla_roadster_simulation/) · [Репозиторий](https://github.com/francesco2011-source/tesla_roadster_simulation)

### ★★★☆☆ Tinker Physics — $0.70

![Tinker Physics](https://gitgame.live/thumbs/tinker-physics.jpg)

Physics Sandbox Game

[Игра на GitGame](https://gitgame.live/game/tinker-physics/) · [Репозиторий](https://github.com/L0nE-F0x/tinker-physics)

### ★★★☆☆ Trickshot Sandbox — $0.70

![Trickshot Sandbox](https://gitgame.live/thumbs/trickshot_sandbox.jpg)

Browser FPS built on three.js: chain slides, bunnyhops and wall bounces to build speed, then land trickshots for stacking score multipliers. No install.

[Игра на GitGame](https://gitgame.live/game/trickshot_sandbox/) · [Репозиторий](https://github.com/cubicobelus/trickshot_sandbox)

### ★★★☆☆ Vivienne — $0.70

Vivienne: a browser game with an original soundtrack

[Игра на GitGame](https://gitgame.live/game/vivienne/) · [Репозиторий](https://github.com/yousefabuyaseen/vivienne)

### ★★★☆☆ Voidfront — $0.70

![Voidfront](https://gitgame.live/thumbs/voidfront.jpg)

a vibe coding rts game

[Игра на GitGame](https://gitgame.live/game/voidfront/) · [Репозиторий](https://github.com/w94206229-crypto/voidfront)

### ★★★☆☆ Wordstrata — $0.70

![Wordstrata](https://gitgame.live/thumbs/wordstrata.jpg)

Word game about excavation, gravity and digging through increasingly valuable geological strata.

[Игра на GitGame](https://gitgame.live/game/wordstrata/) · [Репозиторий](https://github.com/splargdotcom/wordstrata)

### ★★☆☆☆ Angry Birds — $0.45

![Angry Birds](https://gitgame.live/thumbs/angry-birds.jpg)

A physics-based Angry Birds inspired game built with JavaScript, p5.js, and Matter.js.

[Игра на GitGame](https://gitgame.live/game/angry-birds/) · [Репозиторий](https://github.com/dslord/Angry-Birds)

### ★★☆☆☆ Dust2 Web — $0.45

![Dust2 Web](https://gitgame.live/thumbs/dust2-web.jpg)

在浏览器中重返 Dust II：实时房间联机、机器人对战、原版武器动作与可选皮肤。Three.js + Node.js / WebSocket。

[Игра на GitGame](https://gitgame.live/game/dust2-web/) · [Репозиторий](https://github.com/ETO-ze/dust2-web)

### ★★☆☆☆ Edge50 — $0.45

![Edge50](https://gitgame.live/thumbs/edge50.jpg)

Survive 50 seconds on the edge. A single-file HTML5 dodging game with daily challenges, endless mode, instant replays, and shareable score cards. Play offline with…

[Игра на GitGame](https://gitgame.live/game/edge50/) · [Репозиторий](https://github.com/CARL-JOSEPH-LEE/edge50)

### ★★☆☆☆ Glush Game — $0.45

![Glush Game](https://gitgame.live/thumbs/glush-game.jpg)

Atmospheric procedural pixel expedition through fog, fading roads and distant signals.

[Игра на GitGame](https://gitgame.live/game/glush-game/) · [Репозиторий](https://github.com/Likemiens/glush-game)

### ★★☆☆☆ Kilnheart — $0.45

![Kilnheart](https://gitgame.live/thumbs/kilnheart.jpg)

A clay-toy isometric action RPG that runs in the browser, plain ES modules on Three.js. MIT licensed. Play live: https://kilnheart.bles-software.com

[Игра на GitGame](https://gitgame.live/game/kilnheart/) · [Репозиторий](https://github.com/stas4000/kilnheart)

### ★★☆☆☆ Little Red Flower Game — $0.45

![Little Red Flower Game](https://gitgame.live/thumbs/little-red-flower-game.jpg)

公益应急科普 HTML 游戏：台风隐患排查与厨房油锅起火处置训练

[Игра на GitGame](https://gitgame.live/game/little-red-flower-game/) · [Репозиторий](https://github.com/KeepingMoving/little-red-flower-game)

### ★★☆☆☆ Mox2 — $0.45

![Mox2](https://gitgame.live/thumbs/mox2.jpg)

Shanhe Wending - Ancient Chinese 3D strategy game. Six kingdoms fight for control of the realm.

[Игра на GitGame](https://gitgame.live/game/mox2/) · [Репозиторий](https://github.com/yanyu473/mox2)

### ★★☆☆☆ Quickrush — $0.45

![Quickrush](https://gitgame.live/thumbs/quickrush.jpg)

🛵 QuickRush: Delivery Wars — 3D web-based delivery arcade and racing game built with Three.js, Web Audio & HTML5.

[Игра на GitGame](https://gitgame.live/game/quickrush/) · [Репозиторий](https://github.com/Jatinnn-ui/QuickRush)

### ★★☆☆☆ Tahu Tak — $0.45

![Tahu Tak](https://gitgame.live/thumbs/tahu-tak.jpg)

A Malaysia trivia game you can eat: win hawker dishes, sell them, buy hints. Three.js + vanilla JS.

[Игра на GitGame](https://gitgame.live/game/tahu-tak/) · [Репозиторий](https://github.com/markinko202-sys/tahu-tak)

### ★★☆☆☆ Compound Ball — $0.40

![Compound Ball](https://gitgame.live/thumbs/compound-ball.jpg)

🎮 合成球球（南林特别版）· B 站 Toy 版 —— 竖屏休闲合成类 H5 小游戏（单文件 HTML5 + Canvas，零依赖零后端）/ Suika Ball (Nanlin Edition), a portrait HTML5 merging game on Bilibili Toy

[Игра на GitGame](https://gitgame.live/game/compound-ball/) · [Репозиторий](https://github.com/Kazuha233/compound-ball)

### ★★☆☆☆ Ice37Outlaw Html5 Game — $0.40

Native HTML5 game porting & preservation of Outlaw by ICE37 (Phaser 3 Engine)

[Игра на GitGame](https://gitgame.live/game/ice37outlaw-html5-game/) · [Репозиторий](https://github.com/DannyWhyze/ice37outlaw-html5-game)

### ★★☆☆☆ Rabbit City — $0.40

![Rabbit City](https://gitgame.live/thumbs/rabbit-city.jpg)

A PS1-style survival horror game starring Cevdet. 12 zombies, fixed cameras and procedural rain-soaked streets in one offline-ready HTML file.

[Игра на GitGame](https://gitgame.live/game/rabbit-city/) · [Репозиторий](https://github.com/torunum/rabbit-city)

### ★★☆☆☆ Smallscope — $0.40

![Smallscope](https://gitgame.live/thumbs/smallscope.jpg)

Faithful with little, faithful with much.

[Игра на GitGame](https://gitgame.live/game/smallscope/) · [Репозиторий](https://github.com/Aptyll/SmallScope)

### ★★☆☆☆ Stick Fight Game — $0.40

![Stick Fight Game](https://gitgame.live/thumbs/stick-fight-game.jpg)

Игра из парсера, авто-деплой.

[Игра на GitGame](https://gitgame.live/game/stick-fight-game/) · [Репозиторий](https://github.com/barubarubbq86-coder/stick-fight-game)

### ★★☆☆☆ Sticklab — $0.40

Physics game

[Игра на GitGame](https://gitgame.live/game/sticklab/) · [Репозиторий](https://github.com/matthagersenior/StickLab)

### ★★☆☆☆ The Game Name Is Feed Fish — $0.40

![The Game Name Is Feed Fish](https://gitgame.live/thumbs/the-game-name-is-feed-fish.jpg)

FEED-FISH is a fast-paced, minimalist HTML5 arcade survival game built entirely in a single file with zero dependencies. Balance gravity, hunt golden insect swarms, and…

[Игра на GitGame](https://gitgame.live/game/the-game-name-is-feed-fish/) · [Репозиторий](https://github.com/pradeep-vishnu/The-Game-Name-is-FEED-FISH)

### ★★☆☆☆ Waterslide Game Astra — $0.40

![Waterslide Game Astra](https://gitgame.live/thumbs/waterslide-game-astra.jpg)

a test to see how AI 0-shot performs against a game I have various models. This version is using GPT 6 Astra with EXTRA HIGH effort.

[Игра на GitGame](https://gitgame.live/game/waterslide-game-astra/) · [Репозиторий](https://github.com/KJLKurt/waterslide-game-astra)

### ★★☆☆☆ Lumen Isles — $0.35

![Lumen Isles](https://gitgame.live/thumbs/lumen-isles.jpg)

A tiny explorable world of floating islands at dusk, in one HTML file plus Three.js. MIT licensed. Play live: https://lumen-isles.bles-software.com

[Игра на GitGame](https://gitgame.live/game/lumen-isles/) · [Репозиторий](https://github.com/stas4000/lumen-isles)

### ★★☆☆☆ Recoil Foundry — $0.35

![Recoil Foundry](https://gitgame.live/thumbs/recoil-foundry.jpg)

One gun. Sixteen stages. A physics roguelike with recoil movement, evolving builds, and optional challenge rooms.

[Игра на GitGame](https://gitgame.live/game/recoil-foundry/) · [Репозиторий](https://github.com/Caleb-Guyer/recoil-foundry)

### ★★☆☆☆ Rocky Grid — $0.35

![Rocky Grid](https://gitgame.live/thumbs/rocky-grid.jpg)

A neon light-cycle arena duel, built by an AI and hardened through a gauntlet loop. Play in your browser.

[Игра на GitGame](https://gitgame.live/game/rocky-grid/) · [Репозиторий](https://github.com/ExtremeAI-Labs/rocky-grid)

### ★★☆☆☆ Strikearena — $0.35

![Strikearena](https://gitgame.live/thumbs/strikearena.jpg)

3D Mobile Optimized FPS Shooter Game (Perfect Bunny Hop and Ragdoll)

[Игра на GitGame](https://gitgame.live/game/strikearena/) · [Репозиторий](https://github.com/harun-aksoy/strikearena)

### ★★☆☆☆ Wolf Sheep Game — $0.35

![Wolf Sheep Game](https://gitgame.live/thumbs/wolf-sheep-game.jpg)

A browser implementation of the Battanian tavern Wolf & Sheep game with deterministic minimax AI.

[Игра на GitGame](https://gitgame.live/game/wolf-sheep-game/) · [Репозиторий](https://github.com/wangsunyan777/Wolf-Sheep-Game)

### ★★☆☆☆ Yoru No Gakko — $0.35

![Yoru No Gakko](https://gitgame.live/thumbs/yoru-no-gakko.jpg)

夜の学校 — a retro fixed-camera survival-horror game in a Japanese school at night. Plays in the browser.

[Игра на GitGame](https://gitgame.live/game/yoru-no-gakko/) · [Репозиторий](https://github.com/KantLex/yoru-no-gakko)

### ★★☆☆☆ A Combat Game — $0.30

![A Combat Game](https://gitgame.live/thumbs/a_combat_game.jpg)

一个有趣的3D WebGL制作的小游戏，无需复杂部署流程，即开即玩。 线上预览项目地址👇

[Игра на GitGame](https://gitgame.live/game/a_combat_game/) · [Репозиторий](https://github.com/Kevinlaptop/A_combat_game)

### ★★☆☆☆ Ai Trainer Simulator — $0.30

![Ai Trainer Simulator](https://gitgame.live/thumbs/ai-trainer-simulator.jpg)

3D IT Trainer Simulator - retro pixel-art career/business sim with WebMCP for AI Agents to join the game!

[Игра на GitGame](https://gitgame.live/game/ai-trainer-simulator/) · [Репозиторий](https://github.com/LucasMatuszewski/ai-trainer-simulator)

### ★★☆☆☆ Airhockey Gamelab — $0.30

![Airhockey Gamelab](https://gitgame.live/thumbs/airhockey-gamelab.jpg)

Air Hockey futurista Player vs CPU com física, IA, SMASH, diferentes dificuldades e controles por mouse ou teclado. Desenvolvido em HTML, CSS e JavaScript — GameLab…

[Игра на GitGame](https://gitgame.live/game/airhockey-gamelab/) · [Репозиторий](https://github.com/sammyfreitas/airhockey-gamelab)

### ★★☆☆☆ Artifact Web — $0.30

![Artifact Web](https://gitgame.live/thumbs/artifact_web.jpg)

rebuild dota2 card game Artifact with Astra, play in browser http://101.43.178.127/

[Игра на GitGame](https://gitgame.live/game/artifact_web/) · [Репозиторий](https://github.com/NigelYao/Artifact_Web)

### ★★☆☆☆ Astramc — $0.30

A browser-based 3D voxel wilderness sandbox: explore, build, craft and survive with dynamic weather, wildlife and fishing. Built with JavaScript and Three.js.

[Игра на GitGame](https://gitgame.live/game/astramc/) · [Репозиторий](https://github.com/LeVraiMattokDev/AstraMC)

### ★★☆☆☆ Battleship Ai — $0.30

![Battleship Ai](https://gitgame.live/thumbs/battleship-ai.jpg)

Battleship game Devin

[Игра на GitGame](https://gitgame.live/game/battleship-ai/) · [Репозиторий](https://github.com/aronh-ui/battleship-ai)

### ★★☆☆☆ Blocks Openworld — $0.30

![Blocks Openworld](https://gitgame.live/thumbs/blocks-openworld.jpg)

An open-world game built overnight by Claude Fable 5.1 — drive, shoot, get chased. Includes every brief, gate and measurement.

[Игра на GitGame](https://gitgame.live/game/blocks-openworld/) · [Репозиторий](https://github.com/Nipale-ai/blocks-openworld)

### ★★☆☆☆ Business Tycoon — $0.30

![Business Tycoon](https://gitgame.live/thumbs/business-tycoon.jpg)

Построй компанию с $10k до $1M: офисы, найм агентов, кампании, стратегия. Клавиши B/H + мышь.

[Игра на GitGame](https://gitgame.live/game/business-tycoon/) · [Репозиторий](https://github.com/TeamDay-AI/business-tycoon)

### ★★☆☆☆ Cadle — $0.30

![Cadle](https://gitgame.live/thumbs/cadle.jpg)

A Destiny-grade FPS-RPG that runs in a browser tab: ten walkable regions, 65 quests, 25 creatures, and every sound synthesised in code. three.js, no install, no account.

[Игра на GitGame](https://gitgame.live/game/cadle/) · [Репозиторий](https://github.com/Humpalumps/Cadle)

### ★★☆☆☆ Chicago Rush Home — $0.30

![Chicago Rush Home](https://gitgame.live/thumbs/chicago-rush-home.jpg)

A browser-based arcade driving game inspired by Chicago rush-hour traffic, designed to turn commuting frustration into fun while introducing players to the city’s…

[Игра на GitGame](https://gitgame.live/game/chicago-rush-home/) · [Репозиторий](https://github.com/Mmmarkw/Chicago-Rush-Home)

### ★★☆☆☆ Chronica — $0.30

![Chronica](https://gitgame.live/thumbs/chronica.jpg)

A living ASCII civilization simulator: an emergent world that writes its own history, in one HTML file

[Игра на GitGame](https://gitgame.live/game/chronica/) · [Репозиторий](https://github.com/Eeman1113/chronica)

### ★★☆☆☆ Claude of Duty · Vibe Slops II — $0.30

![Claude of Duty · Vibe Slops II](https://gitgame.live/thumbs/claude-of-duty.jpg)

Браузерный COD-стайл шутер, реконструкция. Tap/click to load. Процедурная графика.

[Игра на GitGame](https://gitgame.live/game/claude-of-duty/) · [Репозиторий](https://github.com/luckeyfaraday/claude-of-duty)

### ★★☆☆☆ Dctd Public — $0.30

![Dctd Public](https://gitgame.live/thumbs/dctd_public.jpg)

Datacenter Shield — tower defense against drones

[Игра на GitGame](https://gitgame.live/game/dctd_public/) · [Репозиторий](https://github.com/EpicDima/dctd_public)

### ★★☆☆☆ Dominion — $0.30

![Dominion](https://gitgame.live/thumbs/dominion.jpg)

Browser-based real-time strategy game built with Three.js, with AI opponents, diplomacy, and territory control

[Игра на GitGame](https://gitgame.live/game/dominion/) · [Репозиторий](https://github.com/amithey/dominion)

### ★★☆☆☆ Game Noir Walking Simulator — $0.30

![Game Noir Walking Simulator](https://gitgame.live/thumbs/game-noir-walking-simulator.jpg)

Noir 3D walking simulator in three.js

[Игра на GitGame](https://gitgame.live/game/game-noir-walking-simulator/) · [Репозиторий](https://github.com/dvhx/game-noir-walking-simulator)

### ★★☆☆☆ Lockedworld — $0.30

A ten-level top-down shooter that runs in the browser. Lockware has locked the city: free it with the Solid Geeks crew. In French.

[Игра на GitGame](https://gitgame.live/game/lockedworld/) · [Репозиторий](https://github.com/SolidGeeks/lockedworld)

### ★★☆☆☆ Neon Drop — $0.30

![Neon Drop](https://gitgame.live/thumbs/neon-drop.jpg)

Neon Drop — a free, zero-dependency HTML5 drop-and-merge puzzle game with a landing page, legal pages and a multi-network ad adapter.

[Игра на GitGame](https://gitgame.live/game/neon-drop/) · [Репозиторий](https://github.com/darkgambit/neon-drop)

### ★★☆☆☆ S Game — $0.30

![S Game](https://gitgame.live/thumbs/s-game.jpg)

公益环境教育动作肉鸽：战胜污染外壳，找回材料价值

[Игра на GitGame](https://gitgame.live/game/s-game/) · [Репозиторий](https://github.com/xingchenyd/S-game)

### ★★☆☆☆ Stella Ball — $0.30

![Stella Ball](https://gitgame.live/thumbs/stella-ball.jpg)

Stella Ball — a browser action-strategy prototype: roll a meteor and three starkeepers around a top-down billiards battlefield, then choose each shot whether the…

[Игра на GitGame](https://gitgame.live/game/stella-ball/) · [Репозиторий](https://github.com/8rulerstar/stella-ball)

### ★★☆☆☆ Stick Fight — $0.30

![Stick Fight](https://gitgame.live/thumbs/stick-fight.jpg)

Stick figure fighting game built with pure HTML5 Canvas (zero dependencies, single file)

[Игра на GitGame](https://gitgame.live/game/stick-fight/) · [Репозиторий](https://github.com/LinyaoyuSS/stick-fight)

### ★★☆☆☆ Stickman Vs Geometry — $0.30

![Stickman Vs Geometry](https://gitgame.live/thumbs/stickman-vs-geometry.jpg)

Stickman vs Geometry — a 16-chapter physics and maths web game

[Игра на GitGame](https://gitgame.live/game/stickman-vs-geometry/) · [Репозиторий](https://github.com/PerryAgbo/stickman-vs-geometry)

### ★★☆☆☆ The Last Ember — $0.30

![The Last Ember](https://gitgame.live/thumbs/the-last-ember.jpg)

A glowing, story-driven HTML5 adventure game built for touch screens. Six realms, dynamic lighting, synthesised audio, zero dependencies.

[Игра на GitGame](https://gitgame.live/game/the-last-ember/) · [Репозиторий](https://github.com/Mr-vero/the-last-ember)

### ★☆☆☆☆ Mg Oyun Klubu — $0.25

![Mg Oyun Klubu](https://gitgame.live/thumbs/mg-oyun-klubu.jpg)

MG Oyun Klübü — minik oyuncular için tarayıcı oyunları

[Игра на GitGame](https://gitgame.live/game/mg-oyun-klubu/) · [Репозиторий](https://github.com/MetinGulerce/mg-oyun-klubu)

### ★☆☆☆☆ On Time Off — $0.15

![On Time Off](https://gitgame.live/thumbs/on-time-off.jpg)

一个 60 秒的俯视角潜行小游戏：从工位走到打卡机，别被同事和领导看见

[Игра на GitGame](https://gitgame.live/game/on-time-off/) · [Репозиторий](https://github.com/xiajingg/on-time-off)

### ★☆☆☆☆ Tilt Marble Labyrinth Game — $0.15

![Tilt Marble Labyrinth Game](https://gitgame.live/thumbs/tilt-marble-labyrinth-game.jpg)

A 3D-tilted marble physics puzzle game built with React, TypeScript, Canvas, and Vite

[Игра на GitGame](https://gitgame.live/game/tilt-marble-labyrinth-game/) · [Репозиторий](https://github.com/Shivansh-HITK/tilt-marble-labyrinth-game)

### ★☆☆☆☆ Harvest Heat — $0.10

![Harvest Heat](https://gitgame.live/thumbs/harvest-heat.jpg)

A browser racing game made with GPT-6 Astra.

[Игра на GitGame](https://gitgame.live/game/harvest-heat/) · [Репозиторий](https://github.com/gabeashah/Harvest-Heat)

### ★☆☆☆☆ Wake Rider — $0.10

![Wake Rider](https://gitgame.live/thumbs/wake-rider.jpg)

A 2.5D boat and tube physics game with a shared lake, rideable wakes, optional bots, and solo open water.

[Игра на GitGame](https://gitgame.live/game/wake-rider/) · [Репозиторий](https://github.com/sagan246/wake-rider)

