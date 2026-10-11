/**
 * صَيّاف للتكييف (SayyafAC) - التفاعل البرمجي الموحد
 * يعمل بتوافق تام على الصفحة الرئيسية وجميع المسارات الفرعية (Subpage Script Parity)
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. إدارة القائمة الجانبية للجوال (Mobile Navigation Drawer)
  const mobileToggleBtn = document.querySelector('.sayyaf-mobile-toggle');
  const drawer = document.querySelector('.sayyaf-drawer');
  const drawerBackdrop = document.querySelector('.sayyaf-drawer-backdrop');
  const drawerCloseBtn = document.querySelector('.sayyaf-drawer-close');
  const drawerLinks = document.querySelectorAll('.sayyaf-drawer-link');

  function openDrawer() {
    if (drawer && drawerBackdrop) {
      drawer.classList.add('is-open');
      drawerBackdrop.classList.add('is-open');
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
      document.body.style.overflow = '';
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

  // 2. تمييز الرابط النشط تلقائياً حسب المسار الحالي
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  const allNavLinks = document.querySelectorAll('.sayyaf-nav-link, .sayyaf-drawer-link');

  allNavLinks.forEach((link) => {
    const linkPath = link.getAttribute('href').replace(/\/$/, '') || '/';
    if (linkPath === currentPath) {
      link.classList.add('active');
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
});
