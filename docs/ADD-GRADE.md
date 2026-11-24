# How to add a grade to Mthakarti (same method as Grade 10 Advanced)

Follow this exactly. It is how `g10a` (Grade 10 Advanced) and `g12g` were built. Reply to the owner in Gulf Arabic only.

## 1. Inputs (from the owner's laptop folder)
- The official Ministry exam structure (الهيكل) for Term 1 2026-2027, one per subject.
- The school material for that grade (book chapters, slides, summaries).
- Build ONLY what the structure covers. Do not invent topics, numbers, marks or exam dates.

## 2. Data format (one object per subject)
In `app.js`, grade data lives in blocks like `var DATA10A={};` followed by
`/* ---- data10a <subject>.js ---- */ try{ DATA10A["<subject>"] = {...} }catch(e){...}`.
For Grade 11 Advanced use `var DATA11A={};` (and `DATA11A_EN` for subjects taught in English).

Each subject object has these keys (copy the shape of `DATA10A["physics"]`):
- `name` (Arabic), `icon` (emoji), `tone` (pill class, e.g. `p-mint`), `desc`, `note`, `en` (true if taught in English), `summary` (plain-text summary of book units + official structure, used by the AI tutor)
- `exam`: `{n: <questions>, mins: <minutes>}` matching the official structure
- `T`: lessons, each `{id, t (title), q (one-line question/hook), html (the lesson: short, clear, with worked examples), deep (deeper explanation), say (text read aloud)}`. Grade 10 Advanced has 23-31 lessons per subject.
- `Q`: questions, each `[lessonNo, question, correct, wrong1, wrong2, wrong3, explanation]` (correct answer is always the 3rd element; the app shuffles). About 5-6 per lesson (135-166 per subject).
- Math uses `<span class="m">…</span>` for formulas. Science/Math/English that the school teaches in English must have an English version (`DATA11A_EN`) like `DATA10A_EN`.

## 3. Wire the grade in
- Add `g11a` to `const GR={…}` exactly like `g10a` (name `الصف الحادي عشر · متقدم`, short `11 متقدم`, icon 📘).
- Add an opener IIFE like the `G10A_SHARED` one: own subjects from `DATA11A`, shared subjects (Arabic, Islamic, Social, AI, PE) taken from the grade the owner says (ask her: Grade 10 or Grade 12 material).
- Open the grade only when its own subjects are all ready (same guard as g10a).
- Add `g11a` to `EXAMS` with the official exam timetable (ask the owner if not in the files).
- The sign-up form already lists Grade 11; once `GR.g11a.S` has subjects, the "coming soon" page disappears by itself.

## 4. Check before pushing
- `node --check app.js`
- Serve locally and open `#g11a`: every subject opens, every lesson renders, quizzes run, the final exam runs.
- Spot-check 10 questions per subject against the book: correct answer right, no duplicates.
- Run `bash tools/bump-app.sh`, then rebuild SEO pages: `python3 tools/seo/build.py` (adds /lessons and /exams pages for g11a).
- Commit and push to `main` (Render deploys automatically).

## 5. Tell the owner
In Gulf Arabic: which subjects are live, how many lessons and questions each, and anything missing from the files.
Also email the students already registered as `g11a` that their grade is ready (mailer, approved pink template).
