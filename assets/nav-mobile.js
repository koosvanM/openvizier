/* Hamburger-menu voor Het Open Vizier — werkt op alle pagina's met <nav class="nav">.
   Onder 720px viewport: menu ingeklapt, opent met klik op ☰.
   Op desktop: volledig menu zichtbaar, hamburger verborgen via CSS. */
(function () {
  function init() {
    var nav = document.querySelector('nav.nav');
    if (!nav || nav.dataset.burgerInit === '1') return;
    nav.dataset.burgerInit = '1';

    // Voorkom dubbele injectie als er al een burger is
    if (nav.querySelector('.nav__burger')) return;

    // Maak de hamburger-knop
    var btn = document.createElement('button');
    btn.className = 'nav__burger';
    btn.setAttribute('aria-label', 'Menu');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<span class="nav__burger-icon"></span>';

    var inner = nav.querySelector('.nav__inner') || nav.firstElementChild;
    if (inner) inner.insertBefore(btn, inner.firstChild);

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = nav.classList.toggle('nav--open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    // Sluit als ergens anders wordt geklikt
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('nav--open') && !nav.contains(e.target)) {
        nav.classList.remove('nav--open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    // Sluit als de gebruiker een menu-item kiest
    nav.querySelectorAll('.nav__links a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('nav--open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });

    // Sluit bij Esc
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('nav--open')) {
        nav.classList.remove('nav--open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
