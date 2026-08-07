/* ov-nav mobile tap-toggle — v1
   Op mobiel (viewport < 720px): tap op dropdown-trigger toggle't de submenu via .is-open klasse.
   Op desktop blijft :hover werken.
*/
(function() {
  if (typeof document === 'undefined') return;
  
  function init() {
    var dropdowns = document.querySelectorAll('.ov-nav__dropdown');
    dropdowns.forEach(function(dd) {
      var trigger = dd.querySelector(':scope > .ov-nav__item, :scope > a');
      if (!trigger) return;
      trigger.addEventListener('click', function(e) {
        // Alleen actief op smalle schermen
        if (window.innerWidth > 720) return;
        // Voorkom navigeren naar #
        e.preventDefault();
        // Sluit andere open dropdowns
        dropdowns.forEach(function(other) {
          if (other !== dd) other.classList.remove('is-open');
        });
        // Toggle deze
        dd.classList.toggle('is-open');
      });
    });
    
    // Sluit alles bij tap buiten menu
    document.addEventListener('click', function(e) {
      if (window.innerWidth > 720) return;
      if (!e.target.closest('.ov-nav')) {
        dropdowns.forEach(function(dd) { dd.classList.remove('is-open'); });
      }
    });
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
