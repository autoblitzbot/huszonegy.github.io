# HUSZONEGY Transcript Szépítés — Instrukciók

## ⚠️ ELSŐ LÉPÉS — MINDIG!
1. **Olvasd el a TRACKING.md-t** → ott van, hol tartasz
2. Ha van **"FOLYAMATBAN"** epizód → onnan folytasd (nézd meg mi van kész és mi nincs)
3. Ha nincs folyamatban semmi → vedd a következőt a "Még hátra" listáról
4. **Fork URL:** https://github.com/autoblitzbot/huszonegy.github.io
5. **Upstream:** https://github.com/huszonegy/huszonegy.github.io
6. **Lokális klón:** `/home/claw/huszonegy-repo/`

## Mi ez?
A HUSZONEGY Bitcoin podcast (huszonegy.github.io) epizódjainak átirat-szépítése.
Nyers `.txt` fájlokból szépített `.md` fájlokat készítünk.

## Repo
- **GitHub:** `huszonegy/huszonegy.github.io`
- **Lokális klón:** `/home/claw/huszonegy-repo/`
- **GitHub user:** `autoblitzbot`

## Fájlstruktúra
- `transcripts/epEXX_*.hu.srt` — eredeti SRT felirat fájlok
- `public/transcripts_clean/epEXX_*.txt` — nyers szöveg (SRT-ből kinyerve, már létezik)
- `public/transcripts_clean/epEXX_*.md` — **szépített markdown** (ezt készítem)

## Mit jelent a szépítés?
1. A `.txt` fájlból indulok ki
2. Bekezdéstörések javítása (beszélők váltása, logikai egységek)
3. Elírások, félrehallások javítása (speech-to-text hibák)
4. Markdown formázás (linkek, kiemelések ahol releváns)
5. `21` → `HUSZONEGY` ahol a podcast nevére utal
6. Eredmény: `.md` fájl ugyanabban a mappában, ugyanazzal a névvel

## Referencia
Meglévő szépített fájlok mintának (main branchen):
- `public/transcripts_clean/epE91_*.md` – `public/transcripts_clean/epE96_*.md`
- Nyitott PR-ekben lévő .md fájlok is jó minták (E21–E90)

## Gyakori javítások — gyűjtőlista (PR #348, #328 stb. alapján)

### Visszatérő névelírások (speech-to-text hibák)
- Peter Shiff → **Peter Schiff**
- Sailor → **Saylor** (Michael Saylor)
- Lagard → **Lagarde** (Christine Lagarde)
- Naib Bukele → **Nayib Bukele**
- Ludwig von Misses/Mizes → **Ludwig von Mises**
- André Kosztolányi → **André Kostolany**
- Max Skyer → **Max Keiser**
- Sveckytől → **Svetskitől** (Aleksandar Svetski)
- SFID → **Saifedean** (Ammous)
- Parker Lois → **Parker Lewis**
- Árti → **Árpi**

### Visszatérő márka/hely javítások
- Vangu Guard → **Vanguard**
- Micro Strategy → **MicroStrategy**
- Hotel & More → **Hotel Atlantis** / **Hotel Aurora** (kontextus szerint)
- Miskolctapolca (egy szó)
- El Salvador (egységesen)

### Szakkifejezések
- FAD → **FUD**
- FOMT → **FOMO**
- LTF → **ETF**
- CBD / CVDC → **CBDC**
- cyfer punk → **cypherpunk**
- praxzeológia / praxeológia → **praxeológia**
- tömegpsichológia → **tömegpszichológia**
- keynesi ideológia (helyes alak)

### Formázási szabályok
- **Bitcoin** nagy B-vel
- **HUSZONEGY** nagybetűvel ahol a podcast nevére utal (21 → HUSZONEGY)
- **Nostr-on** kötőjellel
- Mondatkezdések nagybetűvel
- Linkek kattinthatóvá: `[huszonegy.world](https://huszonegy.world)`, `[bitcoinmentor.hu](https://bitcoinmentor.hu)`, `[noszter.hu](https://noszter.hu)`, `[Köztér](https://jumble.social)` stb.
- „ne adjátok el a bitcoinotokat!" — felkiáltójellel
- böngésszétek (dupla sz)
- Akadozások/ismétlések eltávolítása (deduplikáció): „amíg amíg" → „amíg", „külső külső" → „külső" stb.

### pesz visszajelzés minták (PR #328 alapján)
- noszter.hu és magyarnostr.hu helyes alakok
- Hotel Aurora, Hotel Atlantis (NEM "Hotel & More")
- HUSZONEGY egységesítés — mindig ellenőrizd, minden előfordulást javíts
- Linkeket mindig tedd kattinthatóvá markdown-ban

## Munkafolyamat (epizódonként)
1. `git checkout main && git pull origin main`
2. `git checkout -b eXX-transcript-cleanup`
3. Olvasd el a `.txt` fájlt: `public/transcripts_clean/epEXX_*.txt`
4. Készítsd el a `.md` fájlt: `public/transcripts_clean/epEXX_*.md`
5. `git add public/transcripts_clean/epEXX_*.md`
6. `git commit -m "EXX: transcript szépítés"`
7. `git push -u origin eXX-transcript-cleanup`
8. `gh pr create --repo huszonegy/huszonegy.github.io --title "EXX: transcript szépítés" --body "..."`
9. TRACKING.md frissítése

## Haladási irány
**Csökkenő sorrendben** — a legmagasabb számú hiányzó epizódtól lefelé.

## Jelenlegi állapot (2026-03-07)
- **Main-en (mergelve):** E91–E96
- **Nyitott PR:** E21–E90 (70 db, pesz review-zza)
- **Nincs elkezdve:** E01–E20, R01–R07
- **E30 nem létezik** (nincs SRT fájl)
- **Következő:** E20, majd E19, E18... lefelé E01-ig, aztán R07–R01

## Munkamegosztás
- **Én (autoblitz):** szépítés, branch, commit, push, PR, TRACKING.md vezetése, review kommentek javítása
- **pesz:** PR-ok review-ja és merge-elése

## TRACKING.md
- Hely: `/home/claw/huszonegy-repo/TRACKING.md`
- Minden epizód után frissíteni!

## Review kommentek kezelése
- Ha pesz review kommentet ír → javítás, commit, push a meglévő branchre
- GitHub notifications ellenőrzése: `gh api notifications --jq '...'`
- Feldolgozás után olvasottnak jelölés: `gh api -X PATCH /notifications/threads/{thread_id}`

## Fontos szabályok
- Git config repo-szinten kell (user.name: autoblitzbot, email: autoblitzbot@users.noreply.github.com)
- Mindig main-ről indulj új branchcsel
- Egy PR = egy epizód
- Ha kétséges egy javítás, inkább hagyd az eredetit
- TRACKING.md-t MINDIG frissítsd (előtte és utána is)
- Hiba/session váltás után: ELŐSZÖR olvasd el ezt a fájlt + TRACKING.md!
