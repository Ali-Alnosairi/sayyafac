# استراتيجية هندسة المعلومات وهيكل الروابط (Information Architecture & Clean URL Strategy)
**المشروع**: صَيّاف للتكييف (SayyafAC) - الطائف
**المرحلة**: المرحلة الثانية (Phase 2: Strategy)
**التاريخ**: 2026-10-11

---

## 1. تطبيق مبدأ تكلفة المعمارية والتناسب مع الطلب المحلي (Architecture Cost Principle & Demand Proportionality)

بناءً على نتائج أبحاث السوق المحلي بالطائف:
- **خدمة تركيب المكيفات** تمثل أكثر من 58% من إجمالي الطلب التجاري المباشر.
- **خدمة صيانة وإصلاح المكيفات وتعبئة الفريون** تمثل نحو 25-30% من الطلب.
- بناءً عليه، تم تخصيص عمودين رئيسيين مستقلين في شريط التنقل الأساسي للموقع يمثلان هذه النسبة الواقعية، مع تجنب تشتيت الموقع بصفحات رقيقة أو صفحات أبواب (Doorway Pages).

---

## 2. هيكلية الروابط النظيفة القائمة على المجلدات (Directory-Based Clean URLs - Option B)

وفقاً للقاعدة الصارمة للنظام، تم اعتماد نظام المجلدات النظيفة الذي ينتهي بصلة مائلة (`/`) دون تصدير ملفات `.html` مسطحة:

```
sayyafac/
├── index.html                                        ➔ https://sayyafac.com/
├── installation/
│   └── index.html                                    ➔ https://sayyafac.com/installation/
├── maintenance/
│   └── index.html                                    ➔ https://sayyafac.com/maintenance/
├── contact/
│   └── index.html                                    ➔ https://sayyafac.com/contact/
├── articles/
│   ├── index.html                                    ➔ https://sayyafac.com/articles/
│   └── split-ac-installation-taif/
│       └── index.html                                ➔ https://sayyafac.com/articles/split-ac-installation-taif/
├── assets/
│   ├── css/
│   │   ├── style.css
│   │   └── fonts.css
│   ├── fonts/
│   │   ├── cairo-v35-arabic-400.woff2
│   │   ├── cairo-v35-arabic-600.woff2
│   │   ├── cairo-v35-arabic-700.woff2
│   │   └── cairo-v35-arabic-800.woff2
│   ├── images/
│   │   ├── install-after-aston-indoor.webp
│   │   ├── install-aston-cantilever-bracket.webp
│   │   ├── install-aston-outdoor-facade.webp
│   │   ├── install-before-majlis.webp
│   │   ├── install-commercial-midea-stacked.webp
│   │   ├── install-commercial-york-cabinet.webp
│   │   ├── install-facade-tornado-nikai.webp
│   │   ├── install-rooftop-koolen-piping-loop.webp
│   │   ├── install-rooftop-koolen-rubber-mounts.webp
│   │   └── logo.svg
│   └── js/
│       └── main.js
├── llms.txt
├── robots.txt
└── sitemap.xml
```

---

## 3. خريطة التنقل وشجرة الصفحات المعتمدة

| الرابط القانوني (Canonical URL) | الهدف ونوع الصفحة | الكلمة المفتاحية المستهدفة | نوع Schema | نوع Open Graph |
| :--- | :--- | :--- | :--- | :--- |
| `/` | الصفحة الرئيسية (Brand & HVAC Hub) | شركة تكييف بالطائف، تركيب وصيانة مكيفات | LocalBusiness / HVACBusiness | `website` |
| `/installation/` | ركيزة الخدمة الأولى (Service Landing Page) | تركيب مكيفات سبليت بالطائف، فني تركيب مكيفات | Service / HVACBusiness | `website` |
| `/maintenance/` | ركيزة الخدمة الثانية (Service Landing Page) | صيانة مكيفات بالطائف، تصليح وتعبئة فريون | Service / HVACBusiness | `website` |
| `/contact/` | صفحة التواصل والأحياء وطلب الخدمة | رقم فني تكييف بالطائف، تكييف أم العراد الطائف | ContactPage / LocalBusiness | `website` |
| `/articles/` | مركز الأدلة الفنية والإرشادية (Hub) | دليل التكييف بالطائف، نصائح تركيب وصيانة | CollectionPage | `website` |
| `/articles/split-ac-installation-taif/` | دليل فني متخصص ذو سلطة تشغيلية عميقة | خطوات تركيب مكيف سبليت بالطائف وتأسيس النحاس | Article | `article` |
