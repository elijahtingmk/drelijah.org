// main.js - Global interactive behaviors for Dr. Elijah website

document.addEventListener('DOMContentLoaded', () => {
  // ── 1. Sticky Navigation Scroll Effect ──
  const nav = document.getElementById('nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    });
    // Check initial scroll position on load
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }

  // ── 2. Responsive Mobile Hamburger Menu ──
  const hamburger = document.querySelector('.nav-hamburger');
  const navLinks = document.querySelector('.nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navLinks.classList.toggle('open');
      const open = navLinks.classList.contains('open');
      hamburger.setAttribute('aria-expanded', open);
      hamburger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });

    // Close menu when a link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navLinks.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.setAttribute('aria-label', 'Open menu');
      });
    });
  }

  // ── 3. Scroll Reveal Animation Observer ──
  const revealSelectors = [
    '.role-card',
    '.framework-item',
    '.cred-item',
    '.wte-card',
    '.tier-card',
    '.journey-phase',
    '.credential',
    '.scope-box',
    '.fit-criteria',
    '.buyer-strip-inner',
    '.stage-block',
    '.cta-protocol',
    '.pr6-card',
    '.outcome-card',
    '.hrd-box',
    '.boundary-inner',
    '.crosslink-inner'
  ].join(', ');

  const revealElements = document.querySelectorAll(revealSelectors);

  if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    revealElements.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = 'opacity 0.7s ease, transform 0.7s cubic-bezier(0.16, 1, 0.3, 1)';
      revealObserver.observe(el);
    });
  }
});
