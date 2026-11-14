# التعليق الصوتي: ريل المنشور 17

وُلّد في Google AI Studio (صفحة generate-speech، Gemini TTS) من Chrome على جهاز مروة، 14 نوفمبر 2026. الصوت: **Sola**.
تعليمات الأسلوب (Style): `Read in Arabic, warm, calm and confident, at a natural, unhurried pace.`
بين الجمل `<long pause> <long pause>` (الوسم المفرد أعطى وقفات قصيرة كالوقفة بعد السؤال).

الأخذة: `vo-src/take-sola.wav`. المقدمة 5.3 ث، والمدة 33.94 ث.

النص كما لُصق (مشكول، والوقفات بالسكون):

```
تُذاكِرُ وَحْدَكَ بِلا أُسْتاذْ؟ هٰذِهِ المَلازِمُ لَكْ، مَجّاناً. <long pause>
الرِّياضِيّاتْ. <long pause>
الطَّبِيعِيّاتْ. <long pause>
قَواعِدُ اللُّغَةِ العَرَبِيَّةْ. <long pause>
وَصِيانَةُ الحاسُوبْ. <long pause>
اكْتُبِ اسْمَ المادَّةِ في التَّعْلِيقاتْ، وَنُرْسِلُ لَكَ المَلْزَمَةَ في الرَّسائِلْ، مَجّاناً. <long pause>
وَأَرْسِلْهُ لِزَمِيلِكَ في الصَّفّْ.
```

التركيب:

```
python3 vo.py 17 posts/17/vo-src/take-sola.wav
python3 posts/17/build.py
```

يُنشر بملف `reel-vo.mp4` (مرفوع باسم `reel.mp4`).
