# HUSZONEGY Transcript Szépítés — Instrukciók

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
- `public/transcripts_clean/epE91_*.md`
- `public/transcripts_clean/epE92_*.md`
- `public/transcripts_clean/epE93_*.md`
- `public/transcripts_clean/epE94_*.md`
- `public/transcripts_clean/epE95_*.md`
- `public/transcripts_clean/epE96_*.md`

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
