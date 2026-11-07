# ريلات موقع الأعمال (المنشورات 13 و14 و15)

تسجيل للموقع `docs/index.html` بعرض هاتف 405×720 (1080×1920، 30 إطاراً) على ساعة افتراضية، مع تعليق صوتي بصوت Sola من Gemini (AI Studio).

| المنشور | المفتاح في `site_reels.py` | الأخذة |
|---|---|---|
| 13، الجولة (الإعلان الممول) | `B` | `vo-src/take-13-tour-sola.wav` |
| 14، الجسر | `A` | `vo-src/take-14-bridge-sola.wav` |
| 15، الموقع التفاعلي | `C` | `vo-src/take-15-website-sola.wav` |

التشغيل (المسارات في `rig.js` مطلقة: المستودع في `/home/claude/shwani-media`، والمكتبات في `/home/claude/vendor` بـ `npm i gsap@3.12.5 lenis@1.1.13`):

    python3 site_reels.py B vo-src/take-13-tour-sola.wav [--preview]

التفاصيل في ملف المشروع `claude/site-reels.md`.
