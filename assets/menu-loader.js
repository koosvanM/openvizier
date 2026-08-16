/* ============================================================
   menu-loader.js — volledig dynamisch hoofdmenu
   
   Elke pagina heeft alleen:
     <div id="ov-nav-root"></div>
     <script src="/assets/menu-loader.js" defer></script>
   
   De loader:
   1. Leest <html lang="xx"> voor de taal
   2. Fetcht /nl/_data/tabellen/1_knopen.json (bevat alle talen)
   3. Filtert op eigen taal
   4. Bouwt menu — precies wat in de xlsx staat, in de volgorde uit de xlsx
   
   Geen fallbacks, geen prefix-berekening. Xlsx = bron van waarheid.
   ============================================================ */
(function() {
  'use strict';
  
  const TAAL_CODE = document.documentElement.lang || 'nl';
  const TAAL_PREFIX = {nl:'1',de:'2',en:'3',ru:'4',fr:'5',es:'6',it:'7',pt:'8'};
  const WORTEL = TAAL_PREFIX[TAAL_CODE] || '1';
  
  const JSON_URL = '/nl/_data/tabellen/1_knopen.json';
  
  async function loadJson(url) {
    try {
      const r = await fetch(url, {cache: 'no-store'});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch(e) {
      console.error('menu-loader:', url, e);
      return null;
    }
  }
  
  function esc(s) {
    return String(s || '')
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  
  /* Absolute URL vanuit xlsx-URL (relatief vanaf <taal>/) */
  function absUrl(taal, relUrl) {
    if (!relUrl) return null;
    if (relUrl === './') return '/' + taal + '/';
    let u = relUrl.replace(/^\/+/, '');
    const eerste = u.split('/')[0];
    if (['nl','de','en','ru','fr','es','it','pt'].includes(eerste)) {
      return '/' + u;
    }
    return '/' + taal + '/' + u;
  }
  
  async function build() {
    const root = document.getElementById('ov-nav-root');
    if (!root) return;
    
    const data = await loadJson(JSON_URL);
    if (!data || !data.rijen) {
      root.innerHTML = '<div class="ov-nav__inner"><a class="ov-nav__item" href="/' + TAAL_CODE + '/">Home</a></div>';
      root.className = 'ov-nav';
      return;
    }
    
    // Alleen deze taal
    const taalKnopen = data.rijen.filter(k => {
      const c = String(k.code || '');
      return c === WORTEL || c.startsWith(WORTEL + '.');
    });
    
    // Ingangen op niveau WORTEL.N
    const ingangen = taalKnopen
      .filter(k => {
        const c = String(k.code || '');
        return k.type === 'ingang' && c.split('.').length === 2;
      })
      .sort((a,b) => {
        const av = parseInt(String(a.code).split('.')[1]) || 0;
        const bv = parseInt(String(b.code).split('.')[1]) || 0;
        return av - bv;
      });
    
    // Kinderen van een ouder
    function kinderen(ouderCode) {
      const pfx = String(ouderCode) + '.';
      const diepte = ouderCode.split('.').length + 1;
      return taalKnopen
        .filter(k => {
          const c = String(k.code || '');
          return c.startsWith(pfx) && c.split('.').length === diepte;
        })
        .sort((a,b) => {
          const av = parseInt(String(a.code).split('.').pop()) || 0;
          const bv = parseInt(String(b.code).split('.').pop()) || 0;
          return av - bv;
        });
    }
    
    let html = '';
    
    for (const ing of ingangen) {
      const naam = ing.naam || '';
      const subs = kinderen(String(ing.code));
      
      if (subs.length === 0) {
        // Top-level link
        const href = ing.url ? absUrl(TAAL_CODE, ing.url) : ('/' + TAAL_CODE + '/');
        if (!href) continue;
        html += '<a class="ov-nav__item" href="' + esc(href) + '">' + esc(naam) + '</a>';
      } else {
        html += '<div class="ov-nav__dropdown">';
        html += '<a class="ov-nav__item" href="#" onclick="event.preventDefault()">' + esc(naam) + '<span class="ov-nav__caret">▾</span></a>';
        html += '<div class="ov-nav__submenu">';
        for (const sub of subs) {
          if (!sub.url) continue;  // Geen URL → toon niet
          const href = absUrl(TAAL_CODE, sub.url);
          if (!href) continue;
          html += '<a class="ov-nav__subitem" href="' + esc(href) + '">' + esc(sub.naam || '') + '</a>';
        }
        html += '</div></div>';
      }
    }
    
    // Taal-schakelaar
    const talen = [
      ['nl','Nederlands'], ['en','English'], ['de','Deutsch'], ['ru','Русский'],
      ['fr','Français'], ['es','Español'], ['it','Italiano'], ['pt','Português']
    ];
    html += '<div class="ov-nav__dropdown">';
    html += '<a class="ov-nav__item" href="#" onclick="event.preventDefault()">⌂<span class="ov-nav__caret">▾</span></a>';
    html += '<div class="ov-nav__submenu">';
    for (const [tc, tn] of talen) {
      html += '<a class="ov-nav__subitem" href="/' + tc + '/">' + esc(tn) + '</a>';
    }
    html += '</div></div>';
    
    root.className = 'ov-nav';
    root.innerHTML = '<div class="ov-nav__inner">' + html + '</div>';
    
    if (typeof window.initOvNavToggle === 'function') window.initOvNavToggle();
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
