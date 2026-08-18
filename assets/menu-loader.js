/* ============================================================
   menu-loader.js — volledig dynamisch hoofdmenu
   Vraagt aan 3 JSONs: knopen (structuur), routes (URLs per taal),
   teksten (namen per taal). Bouwt menu voor huidige <html lang>.
   ============================================================ */
(function() {
  'use strict';
  
  const TAAL_CODE = document.documentElement.lang || 'nl';
  const TAAL_PREFIX = {nl:'1',de:'2',en:'3',ru:'4',fr:'5',es:'6',it:'7',pt:'8'};
  const WORTEL = TAAL_PREFIX[TAAL_CODE] || '1';
  
  const JSON_BASE = '/nl/_data/tabellen/';
  
  const FALLBACK = {
    nl: {home:'Voorpagina', menu:[['/nl/','Voorpagina'],['/nl/verkennen.html','Overzicht'],['/nl/onderzoek/','Onderzoek'],['/nl/wat-opkomt/','Wat opkomt'],['/nl/dossiers/','Dossiers']]},
    de: {home:'Titelseite', menu:[['/de/','Titelseite'],['/de/uebersicht.html','Übersicht'],['/de/forschung/','Forschung']]},
    en: {home:'Front page', menu:[['/en/','Front page'],['/en/overview.html','Overview'],['/en/research/','Research']]},
    ru: {home:'Главная', menu:[['/ru/','Главная']]},
    fr: {home:'Une', menu:[['/fr/','Une']]},
    es: {home:'Portada', menu:[['/es/','Portada']]},
    it: {home:'Copertina', menu:[['/it/','Copertina']]},
    pt: {home:'Capa', menu:[['/pt/','Capa']]},
  };
  
  async function loadJson(url) {
    try {
      const r = await fetch(url, {cache: 'no-store'});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch(e) { return null; }
  }
  
  function esc(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  
  function absUrl(taal, relUrl) {
    if (!relUrl) return null;
    if (relUrl === './') return '/' + taal + '/';
    let u = relUrl.replace(/^\/+/, '');
    const eerste = u.split('/')[0];
    if (['nl','de','en','ru','fr','es','it','pt'].includes(eerste)) return '/' + u;
    return '/' + taal + '/' + u;
  }
  
  function renderFallback(root) {
    const fb = FALLBACK[TAAL_CODE] || FALLBACK.nl;
    let html = '<div class="ov-nav__inner">';
    for (const [url, tekst] of fb.menu) {
      html += '<a class="ov-nav__item" href="' + esc(url) + '">' + esc(tekst) + '</a>';
    }
    // Taal-schakelaar
    const talen = [['nl','NL'],['en','EN'],['de','DE'],['ru','RU'],['fr','FR'],['es','ES'],['it','IT'],['pt','PT']];
    html += '<div class="ov-nav__dropdown"><a class="ov-nav__item" href="#" onclick="event.preventDefault()">⌂<span class="ov-nav__caret">▾</span></a><div class="ov-nav__submenu">';
    for (const [tc, tn] of talen) html += '<a class="ov-nav__subitem" href="/' + tc + '/">' + tn + '</a>';
    html += '</div></div></div>';
    root.className = 'ov-nav';
    root.innerHTML = html;
  }
  
  async function build() {
    const root = document.getElementById('ov-nav-root');
    if (!root) return;
    
    const [knopenData, routesData, tekstenData] = await Promise.all([
      loadJson(JSON_BASE + '1_knopen.json'),
      loadJson(JSON_BASE + '2_routes.json'),  // Gecombineerd, alle codes
      loadJson(JSON_BASE + '4_teksten_' + TAAL_CODE + '.json'),
    ]);
    
    if (!knopenData || !knopenData.rijen) {
      renderFallback(root);
      return;
    }
    
    // Bouw indexen
    const routeByCode = {};
    for (const r of (routesData?.rijen || [])) routeByCode[String(r.code)] = r;
    const tekstByCode = {};
    for (const r of (tekstenData?.rijen || [])) tekstByCode[String(r.code)] = r;
    
    // Voor deze taal: knopen waarvan code met WORTEL begint
    const taalKnopen = knopenData.rijen.filter(k => {
      const c = String(k.code || '');
      return c === WORTEL || c.startsWith(WORTEL + '.');
    });
    
    // Filter actief=true, status=live
    const actief = taalKnopen.filter(k => k.actief !== false && (k.status || 'live') === 'live');
    
    // Ingangen op niveau WORTEL.N
    const ingangen = actief
      .filter(k => k.type === 'ingang' && String(k.code).split('.').length === 2)
      .sort((a,b) => {
        const av = parseInt(String(a.volgorde || a.code.split('.')[1])) || 0;
        const bv = parseInt(String(b.volgorde || b.code.split('.')[1])) || 0;
        return av - bv;
      });
    
    if (ingangen.length === 0) {
      renderFallback(root);
      return;
    }
    
    function kinderen(ouderCode) {
      const pfx = String(ouderCode) + '.';
      const diepte = ouderCode.split('.').length + 1;
      return actief
        .filter(k => {
          const c = String(k.code || '');
          return c.startsWith(pfx) && c.split('.').length === diepte;
        })
        .sort((a,b) => {
          const av = parseInt(String(a.volgorde || a.code.split('.').pop())) || 0;
          const bv = parseInt(String(b.volgorde || b.code.split('.').pop())) || 0;
          return av - bv;
        });
    }
    
    let html = '';
    
    for (const ing of ingangen) {
      const code = String(ing.code);
      const tekst = tekstByCode[code];
      const naam = tekst?.naam || '';
      if (!naam) continue;
      
      const subs = kinderen(code);
      const DELEN_NAMEN = ['delen','teilen','share','поделиться','partager','compartir','condividi','partilhar'];
      const isDelen = DELEN_NAMEN.includes((naam || '').toLowerCase().trim());
      
      if (subs.length === 0 && !isDelen) {
        // Top-level link
        const route = routeByCode[code];
        const href = route?.url ? absUrl(TAAL_CODE, route.url) : ('/' + TAAL_CODE + '/');
        html += '<a class="ov-nav__item" href="' + esc(href) + '">' + esc(naam) + '</a>';
      } else {
        html += '<div class="ov-nav__dropdown">';
        const delenAttr = isDelen ? ' data-ov-deel-trigger' : '';
        html += '<a class="ov-nav__item" href="#"' + delenAttr + ' onclick="event.preventDefault()">' + esc(naam) + '<span class="ov-nav__caret">▾</span></a>';
        // Submenu: als Delen, markeer als data-ov-deel zodat deel-menu.js niet dupliceert
        html += '<div class="ov-nav__submenu"' + (isDelen ? ' data-ov-deel' : '') + '>';
        let subCount = 0;
        for (const sub of subs) {
          const subCode = String(sub.code);
          const subTekst = tekstByCode[subCode];
          const subRoute = routeByCode[subCode];
          const subNaam = subTekst?.naam || '';
          const subUrl = subRoute?.url || '';
          if (!subNaam || !subUrl) continue;
          const href = absUrl(TAAL_CODE, subUrl);
          if (!href) continue;
          // Delen-acties: href="#action-xxx" wordt data-ov-deel-action="xxx"
          const actionMatch = String(subUrl).match(/^#action-(.+)$/);
          if (actionMatch) {
            html += '<a class="ov-nav__subitem" href="#" data-ov-deel-action="' + esc(actionMatch[1]) + '" onclick="event.preventDefault()">' + esc(subNaam) + '</a>';
          } else {
            html += '<a class="ov-nav__subitem" href="' + esc(href) + '">' + esc(subNaam) + '</a>';
          }
          subCount++;
        }
        html += '</div></div>';
        // Verwijder lege dropdowns
        if (subCount === 0) {
          const dropdownStart = html.lastIndexOf('<div class="ov-nav__dropdown">');
          html = html.substring(0, dropdownStart);
        }
      }
    }
    
    // Taal-schakelaar komt uit xlsx (1.17)
    
    root.className = 'ov-nav';
    root.innerHTML = '<div class="ov-nav__inner">' + html + '</div>';
    
    // Signaleer aan deel-menu.js dat de nav klaar is
    document.dispatchEvent(new CustomEvent('ov-nav-ready'));
    
    if (typeof window.initOvNavToggle === 'function') window.initOvNavToggle();
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
