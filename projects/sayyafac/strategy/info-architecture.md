# استراتيجية هندسة المعلومات وهيكل الروابط النظيفة (Information Architecture & Clean URLs)
**المشروع**: صَيّاف للتكييف (SayyafAC) - الطائف  
**المرحلة**: ترقية وتحديث معايير النظام (System Modernization & Alignment)  
**التاريخ**: 2026-10-21  

---

## 1. شجرة الروابط النظيفة القائمة على المجلدات (Flat Clean URLs - Option B)

وفقاً للقاعدة الصارمة للنظام، تم اعتماد نظام المجلدات النظيفة على الجذر المباشر للموقع التي تنتهي بصلة مائلة (`/`) دون تصدير ملفات `.html` مسطحة، مع ربط خدمات الشركة عبر فهرس مركزي `/services/` ومسار متخصص لفني تركيب السبليت:

```
sayyafac/
├── index.html                                        ➔ https://sayyafac.com/ (شركة فك وتركيب مكيفات)
├── split-ac-installation-technician/
│   └── index.html                                    ➔ https://sayyafac.com/split-ac-installation-technician/ (فني تركيب سبليت 100 ريال)
├── services/
│   └── index.html                                    ➔ https://sayyafac.com/services/ (دليل كافة الخدمات والأسعار)
├── maintenance/
│   └── index.html                                    ➔ https://sayyafac.com/maintenance/ (صيانة وتصليح وتعبئة فريون)
├── cleaning/
│   └── index.html                                    ➔ https://sayyafac.com/cleaning/ (تنظيف وغسيل مكيفات بالموقع)
├── copper-piping/
│   └── index.html                                    ➔ https://sayyafac.com/copper-piping/ (تأسيس وتمديد نحاس مكيفات)
├── about/
│   └── index.html                                    ➔ https://sayyafac.com/about/ (من نحن وقصة صَيّاف)
├── contact/
│   └── index.html                                    ➔ https://sayyafac.com/contact/ (تواصل معنا ومناطق التغطية)
├── terms/
│   └── index.html                                    ➔ https://sayyafac.com/terms/ (شروط الخدمة والضمان)
├── privacy/
│   └── index.html                                    ➔ https://sayyafac.com/privacy/ (سياسة الخصوصية)
├── installation/
│   └── index.html                                    ➔ https://sayyafac.com/installation/ (301 Redirect to /split-ac-installation-technician/)
├── articles/
│   ├── index.html                                    ➔ https://sayyafac.com/articles/ (مدونة التكييف بالطائف)
│   ├── split-ac-guide/
│   │   └── index.html                                ➔ https://sayyafac.com/articles/split-ac-guide/
│   ├── freon-types-guide/
│   │   └── index.html                                ➔ https://sayyafac.com/articles/freon-types-guide/
│   ├── deep-cleaning-guide/
│   │   └── index.html                                ➔ https://sayyafac.com/articles/deep-cleaning-guide/
│   ├── water-leakage-guide/
│   │   └── index.html                                ➔ https://sayyafac.com/articles/water-leakage-guide/
│   └── taif-winter-heating-guide/
│       └── index.html                                ➔ https://sayyafac.com/articles/taif-winter-heating-guide/
├── 404.html
├── llms.txt
├── robots.txt
└── sitemap.xml
```

---

## 2. جدول توزيع النوايا ودرع منع الالتهام الداخلي (Cannibalization Shield Matrix)

| الرابط القانوني (Canonical URL) | نوع الصفحة ونمطها | الكلمة المفتاحية المستهدفة والنية التجارية | نوع Schema |
| :--- | :--- | :--- | :--- |
| `/` | الصفحة الرئيسية (Brand & Multi-Unit Moving Hub) | شركة فك وتركيب مكيفات بالطائف، نقل مكيفات سبليت | LocalBusiness / HVACBusiness / Service |
| `/split-ac-installation-technician/` | صفحة هبوط تخصصية (Specific Task Landing Page) | فني تركيب مكيفات سبليت بالطائف، تركيب مكيفات 100 ريال | HVACBusiness / Service / FAQPage |
| `/services/` | دليل الفهرسة والخدمات (Catalog Hub) | خدمات تكييف الطائف، أسعار تركيب وصيانة التكييف | CollectionPage / HVACBusiness |
| `/maintenance/` | ركيزة الصيانة (Diagnostic & Repair) | صيانة مكيفات بالطائف، تصليح مكيفات، تعبئة فريون R410A | HVACBusiness / Service / FAQPage |
| `/cleaning/` | ركيزة الغسيل (On-Site Deep Cleaning) | تنظيف مكيفات بالطائف، غسيل مكيفات سبليت بالموقع | HVACBusiness / Service / FAQPage |
| `/copper-piping/` | ركيزة التأسيس (Infrastructure Piping) | تأسيس نحاس مكيفات بالطائف، تمديد نحاس مولر أمريكي | HVACBusiness / Service / FAQPage |
| `/contact/` | صفحة التواصل والأحياء | رقم فني تكييف بالطائف، تكييف أم العراد الطائف | ContactPage / HVACBusiness |
| `/about/` | صفحة الهوية والخبرة | من نحن صَيّاف للتكييف، خبرة فنيي التكييف بالطائف | AboutPage / HVACBusiness |
| `/articles/` | مركز الأدلة الفنية الاسترشادية | دليل التكييف بالطائف، نصائح تشغيل التكييف | CollectionPage |

---

## 3. معيار صناديق التوجيه التبادلي (Bidirectional Disambiguation Routing)

- توجد صناديق استرشادية واضحة في رأس المحتوى تربط بين:
  - **الصفحة الرئيسية (`/`)**: لمن يبحث عن فك ونقل أجهزة قديمة وإعادة تركيبها.
  - **صفحة الفني (`/split-ac-installation-technician/`)**: لمن يمتلك جهازاً جديداً ويريد فقط فني لتركيبه على نحاس المصنع أو تمديد جاهز بـ 100 ريال.
- هذا التوجيه يضمن وضوح تجربة المستخدم ويمنع التشتت والارتداد (Pogo-sticking) ويحسم مسألة التنافس الداخلي أمام محركات البحث.
