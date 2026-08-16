/* ============================================================
   menu-loader.js — volledig dynamisch hoofdmenu
   
   Elke pagina heeft:
     <div id="ov-nav-root"></div>
     <script src="/assets/menu-loader.js" defer></script>
   
   De loader:
   1. Leest <html lang="xx"> voor de taal
   2. Fetcht /nl/_data/tabellen/1_knopen.json + 2_routes_<taal>.json
   3. Bouwt menu (16 ingangen + Taal-schakelaar)
   4. Fallback: geen vertaalde URL → link naar NL met .ov-nav__subitem--fallback
   
   Geen relatieve paden, geen prefix-berekening — alles absoluut vanaf site-root.
   ============================================================ */
(function() {
  'use strict';
  
  const TAAL_CODE = document.documentElement.lang || 'nl';
  const TAAL_PREFIX = {nl:'1',de:'2',en:'3',ru:'4',fr:'5',es:'6',it:'7',pt:'8'};
  const WORTEL = TAAL_PREFIX[TAAL_CODE] || '1';
  
  const JSON_BASE = '/nl/_data/tabellen/';
  
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
  
  /* Bouw een absolute URL vanuit een xlsx-URL (relatief vanaf <taal>/) */
  function absUrl(taal, relUrl) {
    if (!relUrl) return null;
    if (relUrl === './') return '/' + taal + '/';
    // Kap eventuele leading /
    let u = relUrl.replace(/^\/+/, '');
    // Als de URL al met een taal-directory begint, gebruik zoals-is
    const eersteSegment = u.split('/')[0];
    if (['nl','de','en','ru','fr','es','it','pt'].includes(eersteSegment)) {
      return '/' + u;
    }
    return '/' + taal + '/' + u;
  }
  
  async function build() {
    const root = document.getElementById('ov-nav-root');
    if (!root) return;
    
    const [knopenData, routesData] = await Promise.all([
      loadJson(JSON_BASE + '1_knopen.json'),
      loadJson(JSON_BASE + '2_routes_' + TAAL_CODE + '.json'),
    ]);
    
    if (!knopenData || !knopenData.rijen) {
      root.innerHTML = '<div class="ov-nav__inner"><a class="ov-nav__item" href="/' + TAAL_CODE + '/">Home</a></div>';
      root.className = 'ov-nav';
      return;
    }
    
    const knopen = knopenData.rijen;
    
    // Knopen voor deze taal
    const taalKnopen = knopen.filter(k => {
      const c = String(k.code || '');
      return c === WORTEL || c.startsWith(WORTEL + '.');
    });
    
    // Ingangen op niveau WORTEL.N (2 segmenten)
    const ingangen = taalKnopen
      .filter(k => {
        const c = String(k.code || '');
        const parts = c.split('.');
        return k.type === 'ingang' && parts.length === 2;
      })
      .sort((a,b) => {
        const av = parseInt(String(a.code).split('.')[1]) || 0;
        const bv = parseInt(String(b.code).split('.')[1]) || 0;
        return av - bv;
      });
    
    // Kinderen op niveau ouder + 1 segment
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
    
    // NL-route-index voor fallback bij lege URLs
    let nlKnopenIdx = null;
    function nlLookup(taalCode) {
      if (nlKnopenIdx === null) {
        nlKnopenIdx = {};
        for (const k of knopen) {
          if (String(k.code || '').startsWith('1')) nlKnopenIdx[String(k.code)] = k;
        }
      }
      // taalCode "2.5.3" → NL "1.5.3"
      const nlCode = '1' + String(taalCode).slice(WORTEL.length);
      return nlKnopenIdx[nlCode] || null;
    }
    
    let html = '';
    
    for (const ing of ingangen) {
      const code = String(ing.code);
      const naam = ing.naam || '';
      const subs = kinderen(code);
      
      if (subs.length === 0) {
        // Top-level link (bijv. Voorpagina)
        const href = ing.url ? absUrl(TAAL_CODE, ing.url) : ('/' + TAAL_CODE + '/');
        if (!href) continue;
        html += '<a class="ov-nav__item" href="' + esc(href) + '">' + esc(naam) + '</a>';
      } else {
        // Dropdown
        html += '<div class="ov-nav__dropdown">';
        html += '<a class="ov-nav__item" href="#" onclick="event.preventDefault()">' + esc(naam) + '<span class="ov-nav__caret">▾</span></a>';
        html += '<div class="ov-nav__submenu">';
        for (const sub of subs) {
          let href = null;
          let cls = 'ov-nav__subitem';
          
          if (sub.url) {
            href = absUrl(TAAL_CODE, sub.url);
          } else if (TAAL_CODE !== 'nl') {
            // Fallback naar NL
            const nlKnoop = nlLookup(sub.code);
            if (nlKnoop && nlKnoop.url) {
              href = absUrl('nl', nlKnoop.url);
              cls += ' ov-nav__subitem--fallback';
            }
          }
          
          if (!href) continue;
          html += '<a class="' + cls + '" href="' + esc(href) + '">' + esc(sub.naam || '') + '</a>';
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
