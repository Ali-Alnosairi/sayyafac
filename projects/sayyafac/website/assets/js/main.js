/**
 * صَيّاف للتكييف - التفاعل البرمجي الموحد للجوال وسطح المكتب
 * يعمل بتوافق تام على الصفحة الرئيسية وجميع المسارات الفرعية (Mobile-First Parity)
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. إدارة القائمة الجانبية للجوال (Mobile Navigation Drawer & Gestures)
  const mobileToggleBtn = document.querySelector('.sayyaf-mobile-toggle');
  const drawer = document.querySelector('.sayyaf-drawer');
  const drawerBackdrop = document.querySelector('.sayyaf-drawer-backdrop');
  const drawerCloseBtn = document.querySelector('.sayyaf-drawer-close');
  const drawerLinks = document.querySelectorAll('.sayyaf-drawer-link');
  let savedScrollY = 0;

  function openDrawer() {
    if (drawer && drawerBackdrop) {
      savedScrollY = window.scrollY || window.pageYOffset;
      drawer.classList.add('is-open');
      drawerBackdrop.classList.add('is-open');
      
      // قفل التمرير الخلفي بدقة لمنع تسريب التمرير في متصفح Safari على iOS
      document.body.style.position = 'fixed';
      document.body.style.top = `-${savedScrollY}px`;
      document.body.style.width = '100%';
      document.body.style.overflow = 'hidden';

      if (mobileToggleBtn) {
        mobileToggleBtn.setAttribute('aria-expanded', 'true');
      }
    }
  }

  function closeDrawer() {
    if (drawer && drawerBackdrop) {
      drawer.classList.remove('is-open');
      drawerBackdrop.classList.remove('is-open');
      drawer.style.transform = '';

      // استعادة وضع التمرير الطبيعي وإعادة الصفحة لموضعها
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      document.body.style.overflow = '';
      window.scrollTo(0, savedScrollY);

      if (mobileToggleBtn) {
        mobileToggleBtn.setAttribute('aria-expanded', 'false');
      }
    }
  }

  if (mobileToggleBtn) {
    mobileToggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openDrawer();
    });
  }

  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener('click', (e) => {
      e.preventDefault();
      closeDrawer();
    });
  }

  if (drawerBackdrop) {
    drawerBackdrop.addEventListener('click', () => {
      closeDrawer();
    });
    // منع تمرير الخلفية عند لمس الستارة
    drawerBackdrop.addEventListener('touchmove', (e) => {
      e.preventDefault();
    }, { passive: false });
  }

  drawerLinks.forEach((link) => {
    link.addEventListener('click', () => {
      closeDrawer();
    });
  });

  // إغلاق الدرج بمفتاح Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) {
      closeDrawer();
    }
  });

  // دعم إيماءة السحب الطبيعية (Swipe to Dismiss) في واجهات اليمين لليسار (RTL)
  let touchStartX = 0;
  let touchCurrentX = 0;
  if (drawer) {
    drawer.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    drawer.addEventListener('touchmove', (e) => {
      touchCurrentX = e.touches[0].clientX;
      const diffX = touchCurrentX - touchStartX;
      // في بيئة RTL، السحب لليمين (diffX > 0) هو اتجاه الإغلاق الطبيعي
      if (diffX > 0) {
        drawer.style.transform = `translateX(${diffX}px)`;
      }
    }, { passive: true });

    drawer.addEventListener('touchend', () => {
      const diffX = touchCurrentX - touchStartX;
      drawer.style.transform = '';
      if (diffX > 65) {
        closeDrawer();
      }
      touchStartX = 0;
      touchCurrentX = 0;
    }, { passive: true });
  }

  // 2. تمييز الرابط النشط تلقائياً حسب المسار الحالي
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  const allNavLinks = document.querySelectorAll('.sayyaf-nav-link, .sayyaf-drawer-link');

  allNavLinks.forEach((link) => {
    const linkPath = (link.getAttribute('href') || '').replace(/\/$/, '') || '/';
    if (linkPath === currentPath) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // 3. التمرير السلس للروابط الداخلية
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  // 4. إدارة نموذج طلب تسعير الواتساب التفاعلي (Interactive WhatsApp Lead Generator)
  document.querySelectorAll('.sayyaf-quote-form').forEach((quoteForm) => {
    const gpsBtn = quoteForm.querySelector('.sayyaf-gps-btn');
    const locationInput = quoteForm.querySelector('.sayyaf-location-input');
    let detectedLocation = '';

    if (gpsBtn && locationInput) {
      gpsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (!navigator.geolocation) {
          gpsBtn.textContent = '❌ غير مدعوم بالجهاز';
          setTimeout(() => { gpsBtn.textContent = '📍 تحديد موقعي'; }, 3000);
          return;
        }
        gpsBtn.textContent = '⏳ جاري التحديد...';
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lat = position.coords.latitude.toFixed(6);
            const lng = position.coords.longitude.toFixed(6);
            detectedLocation = `https://maps.google.com/?q=${lat},${lng}`;
            gpsBtn.textContent = '✅ تم تحديد موقعك';
            gpsBtn.classList.add('is-active');
            if (!locationInput.value.trim()) {
              locationInput.value = 'موقعي على الخريطة (GPS)';
            }
          },
          (error) => {
            gpsBtn.textContent = '📍 تعذر التحديد (اكتب الحي)';
            setTimeout(() => { gpsBtn.textContent = '📍 تحديد موقعي'; }, 3500);
          },
          { timeout: 10000 }
        );
      });
    }

    quoteForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const serviceType = quoteForm.querySelector('[name="service_type"]')?.value || 'غير محدد';
      const acType = quoteForm.querySelector('[name="ac_type"]')?.value || 'سبليت جداري';
      const acCount = quoteForm.querySelector('[name="ac_count"]')?.value || '1';
      const district = locationInput?.value.trim() || 'الطائف';
      const notes = quoteForm.querySelector('[name="notes"]')?.value.trim() || '';

      let message = 'السلام عليكم ورحمة الله، أحتاج تسعير / حجز موعد مع صَيّاف للتكييف:\n';
      message += `• نوع الخدمة: ${serviceType}\n`;
      message += `• نوع المكيف: ${acType}\n`;
      message += `• العدد: ${acCount}\n`;
      message += `• الحي / الموقع في الطائف: ${district}\n`;
      if (detectedLocation) {
        message += `• رابط الموقع الجغرافي: ${detectedLocation}\n`;
      }
      if (notes) {
        message += `• تفاصيل إضافية: ${notes}\n`;
      }

      const encodedMsg = encodeURIComponent(message);
      const whatsappUrl = `https://wa.me/966538972324?text=${encodedMsg}`;

      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', {
          event_category: 'conversion',
          event_label: 'whatsapp_quote_builder',
          service_type: serviceType,
          district: district
        });
      }

      // توجيه ذكي مباشر على الهواتف لمنع اعتراض متصفحات الجوال للنوافذ المنبثقة
      const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      if (isMobile) {
        window.location.href = whatsappUrl;
      } else {
        window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
      }
    });
  });

  // 5. تتبع أحداث التحويل المباشر للاتصال والواتساب (Conversion Tracking Hooks)
  document.querySelectorAll('a[href^="tel:"]').forEach((link) => {
    link.addEventListener('click', () => {
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'contact', {
          event_category: 'conversion',
          event_label: 'phone_call'
        });
      }
    });
  });

  document.querySelectorAll('a[href*="wa.me"]').forEach((link) => {
    link.addEventListener('click', () => {
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'contact', {
          event_category: 'conversion',
          event_label: 'whatsapp_direct_click'
        });
      }
    });
  });
});
