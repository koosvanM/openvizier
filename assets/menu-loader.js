/* ============================================================
   MENU-LOADER — dynamisch hoofdmenu uit vizier.xlsx
   
   Bij elke pagina-load:
   1. Detecteert taal uit <html lang="xx">
   2. Fetcht knopen, routes, teksten uit /nl/_data/tabellen/
   3. Bouwt hoofdmenu (16 ingangen + Taal-schakelaar)
   4. Injecteert in <nav id="ov-nav-root">
   ============================================================ */
(function() {
  'use strict';
  
  const TAAL_CODE = document.documentElement.lang || 'nl';
  const TAAL_PREFIX = {nl:'1',de:'2',en:'3',ru:'4',fr:'5',es:'6',it:'7',pt:'8'};
  const WORTEL = TAAL_PREFIX[TAAL_CODE] || '1';
  
  // Pad naar JSON-tabellen (NL-map is canoniek)
  // We bepalen relatief pad op basis van huidige URL
  function jsonBase() {
    const path = window.location.pathname;
    // /nl/xxx.html of /nl/ → _data/tabellen/
    // /nl/wat-opkomt/xxx.html → ../_data/tabellen/
    // /de/xxx.html → ../nl/_data/tabellen/
    // /de/ausgabe-3/xxx.html → ../../nl/_data/tabellen/
    const parts = path.split('/').filter(p => p);
    // Eerste segment = taal, daarna N segmenten waarvan de laatste bestand of leeg
    const isFile = path.endsWith('.html');
    const depth = isFile ? parts.length - 1 : parts.length; // aantal directories vanaf root
    // Taal-directory zelf telt niet als "diep in map"
    const inTaal = depth; // vanaf root
    const opNiveauInTaal = Math.max(0, depth - 1); // hoe diep binnen taal-map
    
    let prefix = '';
    for (let i = 0; i < opNiveauInTaal; i++) prefix += '../';
    
    if (TAAL_CODE === 'nl') {
      return prefix + '_data/tabellen/';
    } else {
      return prefix + '../nl/_data/tabellen/';
    }
  }
  
  // URL-prefix voor menu-links (relatief vanaf huidige pagina)
  function urlPrefix() {
    const path = window.location.pathname;
    const parts = path.split('/').filter(p => p);
    const isFile = path.endsWith('.html');
    const depth = isFile ? parts.length - 1 : parts.length;
    const opNiveauInTaal = Math.max(0, depth - 1);
    
    let prefix = '';
    for (let i = 0; i < opNiveauInTaal; i++) prefix += '../';
    return prefix;
  }
  
  async function loadJson(url) {
    try {
      const r = await fetch(url, {cache: 'no-store'});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch(e) {
      console.error('menu-loader: kon niet laden', url, e);
      return null;
    }
  }
  
  function esc(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  
  async function build() {
    const nav = document.getElementById('ov-nav-root');
    if (!nav) return;
    
    const base = jsonBase();
    const [knopenData, routesData, ...rest] = await Promise.all([
      loadJson(base + '1_knopen.json'),
      loadJson(base + '2_routes_' + TAAL_CODE + '.json'),
    ]);
    
    if (!knopenData || !routesData) {
      // Fallback: toon minimaal menu met alleen taal-schakelaar
      nav.innerHTML = '<a class="ov-nav__item" href="/' + TAAL_CODE + '/">Home</a>';
      return;
    }
    
    const knopen = knopenData.rijen || [];
    const routes = routesData.rijen || [];
    
    // Filter knopen voor deze taal (code begint met WORTEL)
    const taalKnopen = knopen.filter(k => {
      const c = String(k.code || '');
      return c.startsWith(WORTEL + '.') || c === WORTEL;
    });
    
    // Routes indexeren op code
    const routesByCode = {};
    for (const r of routes) {
      routesByCode[String(r.code)] = r;
    }
    
    // Fallback naar NL-routes als deze taal geen route heeft
    let nlRoutes = null;
    async function ensureNlRoutes() {
      if (nlRoutes !== null) return nlRoutes;
      const nlData = await loadJson(base + '2_routes_nl.json');
      const map = {};
      for (const r of (nlData?.rijen || [])) map[String(r.code)] = r;
      nlRoutes = map;
      return map;
    }
    
    // Groep-items: type=ingang met code op niveau WORTEL.N (dus 2 segmenten)
    const ingangen = taalKnopen.filter(k => {
      const c = String(k.code);
      const parts = c.split('.');
      return k.type === 'ingang' && parts.length === 2;
    }).sort((a,b) => {
      const av = parseInt(String(a.code).split('.')[1]) || 0;
      const bv = parseInt(String(b.code).split('.')[1]) || 0;
      return av - bv;
    });
    
    // Voor elke ingang: alle kinderen (code = WORTEL.N.X)
    function kinderen(ouderCode) {
      const prefix = String(ouderCode) + '.';
      return taalKnopen.filter(k => {
        const c = String(k.code);
        return c.startsWith(prefix) && c.split('.').length === ouderCode.split('.').length + 1;
      }).sort((a,b) => {
        const av = parseInt(String(a.code).split('.').pop()) || 0;
        const bv = parseInt(String(b.code).split('.').pop()) || 0;
        return av - bv;
      });
    }
    
    // Build HTML
    let html = '';
    const pfx = urlPrefix();
    
    for (const ing of ingangen) {
      const code = String(ing.code);
      const naam = ing.naam || '';
      const subs = kinderen(code);
      
      if (subs.length === 0 && !ing.url) {
        // Geen submenu en geen eigen URL — sla over (behalve Voorpagina)
        if (code !== WORTEL + '.1') continue;
      }
      
      if (subs.length === 0) {
        // Top-level link zonder dropdown (bijv. Voorpagina)
        const url = pfx + (ing.url === './' || !ing.url ? '' : ing.url);
        html += '<a class="ov-nav__item" href="' + esc(url || pfx) + '">' + esc(naam) + '</a>';
      } else {
        // Dropdown
        html += '<div class="ov-nav__dropdown">';
        html += '<a class="ov-nav__item" href="#" onclick="event.preventDefault()">' + esc(naam) + '<span class="ov-nav__caret">▾</span></a>';
        html += '<div class="ov-nav__submenu">';
        for (const sub of subs) {
          let subUrl = sub.url;
          let fallbackClass = '';
          if (!subUrl && TAAL_CODE !== 'nl') {
            // Fallback naar NL — zoek NL-code
            const nlCode = '1' + String(sub.code).slice(WORTEL.length);
            await ensureNlRoutes();
            const nlRoute = nlRoutes[nlCode];
            if (nlRoute && nlRoute.url) {
              subUrl = pfx + '../nl/' + nlRoute.url;
              fallbackClass = ' ov-nav__subitem--fallback';
            }
          } else if (subUrl) {
            // Eigen URL
            subUrl = pfx + subUrl;
          }
          if (!subUrl) continue;
          html += '<a class="ov-nav__subitem' + fallbackClass + '" href="' + esc(subUrl) + '">' + esc(sub.naam || '') + '</a>';
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
    html += '<a class="ov-nav__item" href="#" onclick="event.preventDefault()">⌂ ' + esc('Taal') + '<span class="ov-nav__caret">▾</span></a>';
    html += '<div class="ov-nav__submenu">';
    for (const [tc, tn] of talen) {
      html += '<a class="ov-nav__subitem" href="' + pfx + '../' + tc + '/">' + esc(tn) + '</a>';
    }
    html += '</div></div>';
    
    nav.className = 'ov-nav';
    nav.innerHTML = '<div class="ov-nav__inner">' + html + '</div>';
    
    // Init mobile-toggle als aanwezig
    if (typeof window.initOvNavToggle === 'function') window.initOvNavToggle();
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
