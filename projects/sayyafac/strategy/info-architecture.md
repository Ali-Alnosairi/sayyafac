# استراتيجية هندسة المعلومات وهيكل الروابط النظيفة (Information Architecture & Clean URLs)
**المشروع**: صَيّاف للتكييف (SayyafAC) - الطائف  
**المرحلة**: ترقية وتحديث معايير النظام (System Modernization & Alignment)  
**التاريخ**: 2026-10-23  
**الحالة**: معتمد ومطابق للحقيقة الميدانية 100%  

---

## 1. شجرة الروابط النظيفة القائمة على المجلدات (Flat Clean URLs - Option B)

وفقاً للقاعدة الصارمة للنظام، تم اعتماد نظام المجلدات النظيفة على الجذر المباشر للموقع التي تنتهي بصلة مائلة (`/`) دون تصدير ملفات `.html` مسطحة، مع توزيع خدمات الشركة عبر مسارات متخصصة مستقلة، وفهرس مركزي، ومركز للأدلة الفنية:

```
projects/sayyafac/website/
├── index.html                                        ➔ https://sayyafac.com/ (شركة فك وتركيب مكيفات)
├── split-ac-installation-technician/
│   └── index.html                                    ➔ https://sayyafac.com/split-ac-installation-technician/ (فني تركيب مكيفات سبليت 100 ريال)
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
│   └── index.html                                    ➔ https://sayyafac.com/privacy/ (سياسة الخصوصية PDPL)
├── installation/
│   └── index.html                                    ➔ https://sayyafac.com/installation/ (301 Permanent Redirect to /split-ac-installation-technician/)
├── articles/
│   ├── index.html                                    ➔ https://sayyafac.com/articles/ (مركز الأدلة الفنية للتكييف بالطائف)
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

| الرابط القانوني (Canonical URL) | نوع الصفحة ونمطها | الكلمة المفتاحية المستهدفة والنية التجارية | نوع Schema المعلق |
| :--- | :--- | :--- | :--- |
| `/` | الصفحة الرئيسية (Brand & Multi-Unit Moving Hub) | شركة فك وتركيب مكيفات بالطائف، نقل مكيفات سبليت | Organization / HVACBusiness / Service / ItemList |
| `/split-ac-installation-technician/` | صفحة هبوط تخصصية (Specific Task Landing Page) | فني تركيب مكيفات سبليت بالطائف، تركيب مكيفات 100 ريال | HVACBusiness / Service / FAQPage |
| `/services/` | دليل الفهرسة والخدمات (Catalog Hub) | خدمات تكييف الطائف، أسعار تركيب وصيانة التكييف | CollectionPage / HVACBusiness / ItemList |
| `/maintenance/` | ركيزة الصيانة (Diagnostic & Repair) | صيانة مكيفات بالطائف، تصليح مكيفات، تعبئة فريون R410A | HVACBusiness / Service / FAQPage |
| `/cleaning/` | ركيزة الغسيل (On-Site Deep Cleaning) | تنظيف مكيفات بالطائف، غسيل مكيفات سبليت بالموقع | HVACBusiness / Service / FAQPage |
| `/copper-piping/` | ركيزة التأسيس (Infrastructure Piping) | تأسيس نحاس مكيفات بالطائف، تمديد نحاس مولر أمريكي | HVACBusiness / Service / FAQPage |
| `/about/` | صفحة الهوية والخبرة (E-E-A-T Base) | من نحن صَيّاف للتكييف، خبرة فنيي التكييف بالطائف | AboutPage / HVACBusiness |
| `/contact/` | صفحة التواصل والأحياء (Local Citations) | رقم فني تكييف بالطائف، تكييف أم العراد الطائف | ContactPage / HVACBusiness |
| `/privacy/` | السياسة التنظيمية (PDPL Compliance) | سياسة الخصوصية صَيّاف للتكييف | WebPage |
| `/terms/` | الشروط والضمان (Field Warranty) | شروط خدمة صَيّاف للتكييف وضمان التركيب | WebPage |
| `/articles/` | مركز الأدلة الفنية الاسترشادية (Hub) | دليل التكييف بالطائف، نصائح تشغيل التكييف | CollectionPage |
| `/articles/split-ac-guide/` | دليل فني تخصصي (Technical Guide) | دليل تركيب مكيف سبليت، فاكيوم المكيف | TechArticle / Article |
| `/articles/water-leakage-guide/` | دليل فني تخصصي (Technical Guide) | علاج تنقيط ماء المكيف، تسليك صرف المكيف | TechArticle / Article |
| `/articles/freon-types-guide/` | دليل فني تخصصي (Technical Guide) | انواع فريون المكيفات، الفرق بين فريون 410 و 22 | TechArticle / Article |
| `/articles/deep-cleaning-guide/` | دليل فني تخصصي (Technical Guide) | غسيل مكيف سبليت بالموقع، كيس غسيل المكيف | TechArticle / Article |
| `/articles/taif-winter-heating-guide/`| دليل فني تخصصي (Technical Guide) | تشغيل مكيف سبليت حار في الشتاء، بلف العكس | TechArticle / Article |

---

## 3. قواعد التنقل والربط الداخلي المحققة (Navigation & Header/Footer Parity)

1. **توحيد اسم رابط الصفحة الرئيسية**:
   - تثبيت اسم الرابط للصفحة الرئيسية كـ **"الرئيسية"** دائماً في شريط التنقل العلوي لسطح المكتب وقائمة الجوال عبر كافة الصفحات الـ 12.
2. **تذييل موحد من 4 أعمدة (Unified 4-Column Footer)**:
   - العمود 1: هوية صَيّاف، العنوان الفعلي بشارع عور بحي أم العراد، ونبذة الاعتماد الميداني.
   - العمود 2: روابط خدمات التكييف الميدانية المباشرة (فك وتركيب، فني سبليت، صيانة وتعبئة فريون، غسيل عميق، تأسيس نحاس).
   - العمود 3: مركز الأدلة الفنية وروابط المقالات الاسترشادية والصفحات التنظيمية (من نحن، الشروط، الخصوصية).
   - العمود 4: قنوات الاتصال والواتساب، ساعات العمل المعتمدة (السبت-الخميس: 07:00-23:50 | الجمعة: 14:00-23:50)، وشبكات التواصل الموثقة (إنستغرام وفيسبوك).
3. **حفظ دافع النقر والفضول الإدراكي (Preserving Information Scent)**:
   - يُمنع إدراج الأسعار المجردة في نصوص الروابط الداخلية (مثل تجنب "فني سبليت (100 ريال)").
   - يُعرض نطاق الخدمة بوضوح ومهنية، ليترك للعميل دافع النقر والاستكشاف ومعاينة القيمة والضمان داخل صفحة الخدمة ذاتها.
4. **توجيه النية التبادلي الصامت (Intent Disambiguation Routing)**:
   - وضع صناديق توجيه واضحة في أسفل الصفحة الرئيسية وصفحة فني السبليت للفصل بين نية الفك والنقل الشامل ونية تركيب جهاز جديد على تأسيس جاهز.
