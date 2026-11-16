# mthakarti.com

- `index.html`: الصفحة الرئيسية (خفيفة، 27KB). فيها الهيدر والستايل وصفحة تحميل بسيطة تقراها قوقل.
- `app.js`: كود التطبيق كامل، وفيه كل الدروس والأسئلة. **أي تعديل على التطبيق يصير هني.**
  - بعد أي تعديل على app.js شغّل: `tools/bump-app.sh`. هذا يحدّث رقم النسخة في index.html، عشان المتصفحات تحمّل النسخة الجديدة.
- `/lessons`، `/exams`، `/exam-structure`، `/about` و`sitemap.xml`: صفحات قوقل (SEO). يبنيها `tools/seo/build.py` من بيانات الدروس.
  - `node tools/seo/export.js`: يقرا الدروس من الموقع وهو شغال محليًا على المنفذ 8765.
  - `python3 tools/seo/build.py lessons.json`: يبني الصفحات.
- `reels/`: ريلز إنستغرام المعتمدة (ينشر منها النشر التلقائي).
- `googlec709c437d3029474.html`: تحقق Google Search Console. **لا تمسحه.**
