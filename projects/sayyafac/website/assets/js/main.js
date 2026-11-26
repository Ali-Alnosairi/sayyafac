/**
 * صياف للتكييف - التفاعل البرمجي الموحد للجوال وسطح المكتب
 * يعمل بتوافق تام على الصفحة الرئيسية وجميع المسارات الفرعية (Mobile-First Parity)
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. إدارة القائمة الجانبية للجوال (Mobile Navigation Drawer, Focus Trap & Gestures)
  const mobileToggleBtn = document.querySelector('.sayyaf-mobile-toggle');
  const drawer = document.querySelector('.sayyaf-drawer');
  const drawerBackdrop = document.querySelector('.sayyaf-drawer-backdrop');
  const drawerCloseBtn = document.querySelector('.sayyaf-drawer-close');
  const drawerLinks = document.querySelectorAll('.sayyaf-drawer-link');
  let savedScrollY = 0;
  let lastFocusedEl = null;

  if (drawer) {
    drawer.setAttribute('aria-hidden', 'true');
  }

  function getDrawerFocusable() {
    if (!drawer) return [];
    return Array.from(
      drawer.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')
    );
  }

  function openDrawer() {
    if (drawer && drawerBackdrop) {
      lastFocusedEl = document.activeElement;
      savedScrollY = window.scrollY || window.pageYOffset;
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      drawerBackdrop.classList.add('is-open');
      document.body.classList.add('drawer-open');

      // قفل التمرير الخلفي بدقة لمنع تسريب التمرير في متصفح Safari على iOS
      document.body.style.position = 'fixed';
      document.body.style.top = `-${savedScrollY}px`;
      document.body.style.width = '100%';
      document.body.style.overflow = 'hidden';

      if (mobileToggleBtn) {
        mobileToggleBtn.setAttribute('aria-expanded', 'true');
      }

      window.requestAnimationFrame(() => {
        if (drawerCloseBtn) {
          drawerCloseBtn.focus();
        } else {
          const focusables = getDrawerFocusable();
          if (focusables.length) focusables[0].focus();
        }
      });
    }
  }

  function closeDrawer() {
    if (drawer && drawerBackdrop) {
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      drawerBackdrop.classList.remove('is-open');
      document.body.classList.remove('drawer-open');
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

      if (lastFocusedEl && typeof lastFocusedEl.focus === 'function') {
        lastFocusedEl.focus();
      } else if (mobileToggleBtn) {
        mobileToggleBtn.focus();
      }
      lastFocusedEl = null;
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

  // إغلاق الدرج بمفتاح Escape وحصر التنقل بلوحة المفاتيح داخله (Focus Trap)
  document.addEventListener('keydown', (e) => {
    if (!drawer || !drawer.classList.contains('is-open')) return;

    if (e.key === 'Escape') {
      closeDrawer();
      return;
    }

    if (e.key === 'Tab') {
      const focusables = getDrawerFocusable();
      if (!focusables.length) return;
      const firstEl = focusables[0];
      const lastEl = focusables[focusables.length - 1];

      if (e.shiftKey && document.activeElement === firstEl) {
        e.preventDefault();
        lastEl.focus();
      } else if (!e.shiftKey && document.activeElement === lastEl) {
        e.preventDefault();
        firstEl.focus();
      }
    }
  });

  // دعم إيماءة السحب الطبيعية (Swipe to Dismiss) في واجهات اليمين لليسار (RTL)
  let touchStartX = 0;
  let touchCurrentX = 0;
  if (drawer) {
    drawer.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
      touchCurrentX = touchStartX;
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
      link.setAttribute('aria-current', 'page');
    } else {
      link.classList.remove('active');
      link.removeAttribute('aria-current');
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

  function openWhatsAppUrl(whatsappUrl) {
    const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    if (isMobile) {
      window.location.href = whatsappUrl;
    } else {
      window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
    }
  }

  function trackEvent(eventName, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
  }

  // 4. إدارة نموذج طلب تسعير الواتساب التفاعلي (Interactive WhatsApp Lead Generator)
  document.querySelectorAll('.sayyaf-quote-form').forEach((quoteForm) => {
    const gpsBtn = quoteForm.querySelector('.sayyaf-gps-btn');
    const locationInput = quoteForm.querySelector('.sayyaf-location-input');
    let detectedLocation = '';

    if (gpsBtn && locationInput) {
      const gpsLabel = gpsBtn.querySelector('span') || gpsBtn;
      const defaultGpsText = gpsLabel.textContent.trim() || 'موقعي';

      gpsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (!navigator.geolocation) {
          gpsLabel.textContent = 'غير مدعوم';
          setTimeout(() => { gpsLabel.textContent = defaultGpsText; }, 3000);
          return;
        }
        gpsLabel.textContent = 'جاري التحديد...';
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lat = position.coords.latitude.toFixed(6);
            const lng = position.coords.longitude.toFixed(6);
            detectedLocation = `https://maps.google.com/?q=${lat},${lng}`;
            gpsLabel.textContent = 'تم تحديد موقعك';
            gpsBtn.classList.add('is-active');
            if (!locationInput.value.trim()) {
              locationInput.value = 'موقعي على الخريطة (GPS)';
            }
          },
          () => {
            gpsLabel.textContent = 'اكتب الحي يدوياً';
            setTimeout(() => { gpsLabel.textContent = defaultGpsText; }, 3500);
          },
          { timeout: 10000 }
        );
      });
    }

    quoteForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const serviceType = quoteForm.querySelector('[name="service_type"]')?.value || 'غير محدد';
      const acTypeEl = quoteForm.querySelector('[name="ac_type"]');
      const acCount = quoteForm.querySelector('[name="ac_count"]')?.value || '1';
      const district = locationInput?.value.trim() || 'الطائف';
      const notes = quoteForm.querySelector('[name="notes"]')?.value.trim() || '';

      let message = 'السلام عليكم ورحمة الله، أحتاج تسعير / حجز موعد مع صياف للتكييف:\n';
      message += `• نوع الخدمة: ${serviceType}\n`;
      if (acTypeEl && acTypeEl.value) {
        message += `• نوع المكيف: ${acTypeEl.value}\n`;
      }
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

      trackEvent('generate_lead', {
        event_category: 'conversion',
        event_label: 'whatsapp_quote_builder',
        service_type: serviceType,
        district: district
      });

      openWhatsAppUrl(whatsappUrl);
    });
  });

  // 5. تتبع أحداث التحويل المباشر للاتصال والواتساب (Conversion Tracking Hooks)
  document.querySelectorAll('a[href^="tel:"]').forEach((link) => {
    link.addEventListener('click', () => {
      trackEvent('contact', {
        event_category: 'conversion',
        event_label: 'phone_call'
      });
    });
  });

  document.querySelectorAll('a[href*="wa.me"]').forEach((link) => {
    link.addEventListener('click', () => {
      trackEvent('contact', {
        event_category: 'conversion',
        event_label: 'whatsapp_direct_click'
      });
    });
  });

  // 6. زر الرجوع إلى أعلى الصفحة (Back to Top FAB - Ultra Mobile-First)
  let backToTopBtn = document.getElementById('sayyafBackToTop');
  if (!backToTopBtn) {
    backToTopBtn = document.createElement('button');
    backToTopBtn.type = 'button';
    backToTopBtn.id = 'sayyafBackToTop';
    backToTopBtn.className = 'sayyaf-back-to-top';
    backToTopBtn.setAttribute('aria-label', 'الرجوع إلى أعلى الصفحة');
    backToTopBtn.setAttribute('title', 'الرجوع لأعلى الصفحة');
    backToTopBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 15l-6-6-6 6"/></svg>';
    document.body.appendChild(backToTopBtn);
  }

  let scrollTicking = false;
  window.addEventListener('scroll', () => {
    if (!scrollTicking) {
      window.requestAnimationFrame(() => {
        if (window.scrollY > 350) {
          backToTopBtn.classList.add('is-visible');
        } else {
          backToTopBtn.classList.remove('is-visible');
        }
        scrollTicking = false;
      });
      scrollTicking = true;
    }
  }, { passive: true });

  backToTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  // 7. رقاقات الأحياء التفاعلية (تعبئة النموذج بالرئيسية أو فتح واتساب مباشر بالخدمة والحي في الصفحات الفرعية)
  const pathServiceMap = {
    '/split-ac-installation-technician': 'تركيب مكيفات سبليت',
    '/maintenance': 'صيانة مكيفات وتعبئة فريون',
    '/cleaning': 'تنظيف وغسيل مكيفات بالموقع',
    '/copper-piping': 'تأسيس وتمديد مواسير النحاس'
  };
  const pageServiceName = pathServiceMap[currentPath] || 'خدمات التكييف';

  document.querySelectorAll('.taif-district-chip').forEach((chip) => {
    const rawText = chip.textContent.trim();
    const locationInput = document.querySelector('.sayyaf-location-input');
    const quoteSection = document.getElementById('quick-quote');

    chip.setAttribute('role', 'button');
    chip.setAttribute('tabindex', '0');
    chip.style.cursor = 'pointer';
    chip.setAttribute(
      'aria-label',
      locationInput
        ? `اختيار ${rawText} في نموذج التسعير`
        : `طلب ${pageServiceName} في ${rawText} عبر واتساب`
    );

    chip.addEventListener('click', () => {
      if (locationInput) {
        locationInput.value = rawText;
        if (quoteSection) {
          quoteSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        locationInput.focus();
      } else {
        const msg = `السلام عليكم ورحمة الله، أحتاج خدمة ${pageServiceName} في ${rawText} (الطائف).`;
        const whatsappUrl = `https://wa.me/966538972324?text=${encodeURIComponent(msg)}`;
        trackEvent('generate_lead', {
          event_category: 'conversion',
          event_label: 'district_chip_whatsapp',
          service_type: pageServiceName,
          district: rawText
        });
        openWhatsAppUrl(whatsappUrl);
      }
    });

    chip.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        chip.click();
      }
    });
  });

  // 8. إيقاف شريط الأخبار المتحرك عند اللمس على شاشات الجوال لحماية البطارية وتسهيل النقر
  const tickerBar = document.querySelector('.sayyaf-ticker-bar');
  const tickerTrack = document.querySelector('.sayyaf-ticker-track');
  if (tickerBar && tickerTrack) {
    tickerBar.addEventListener('touchstart', () => {
      tickerTrack.style.animationPlayState = 'paused';
    }, { passive: true });

    tickerBar.addEventListener('touchend', () => {
      tickerTrack.style.animationPlayState = 'running';
    }, { passive: true });
  }
});
