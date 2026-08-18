/* ov-deel v3 — deelmenu voor Het Open Vizier
 *
 * Vier acties op elk artikel (via het "Delen"-item in de hoofdnav):
 *   - PDF downloaden  → afgeschermd: klant moet een geldige toegangscode invoeren
 *   - Facebook delen  → vrij
 *   - Link kopiëren   → vrij
 *   - Per e-mail      → vrij (mailto)
 *
 * Toegangscodes:
 *   - Beheerd door Jacobus op /admin/deel-beheer.html
 *   - Opgeslagen als SHA-256 hashes in assets/deel-codes.json (repo)
 *   - Elke code heeft een 'verloopt' datum; verlopen codes worden genegeerd
 *   - Na een correcte invoer onthoudt de browser de code tot vervaldatum
 *
 * Geen server nodig. Alles client-side.
 */
(function() {
  'use strict';

  var HTML2PDF_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
  var STORAGE_KEY  = 'ov-deel-toegang';   // { hash, verloopt }
  var html2pdfLoading = null;
  var codesCache = null;

  // ---------- Helpers ----------
  function siteRootPrefix() {
    var path = window.location.pathname;
    var dirs = path.replace(/\/[^/]*$/, '').split('/').filter(Boolean);
    return dirs.length === 0 ? '' : '../'.repeat(dirs.length);
  }
  function canonicalUrl() {
    var link = document.querySelector('link[rel="canonical"]');
    if (link && link.href) return link.href;
    return window.location.href.split('#')[0];
  }
  function articleTitle() {
    var og = document.querySelector('meta[property="og:title"]');
    if (og && og.content) return og.content.trim();
    var h1 = document.querySelector('h1');
    if (h1) return h1.textContent.trim();
    return (document.title || 'Het Open Vizier').trim();
  }
  function articleDate() {
    var meta = document.querySelector('meta[property="article:published_time"]')
            || document.querySelector('meta[name="date"]')
            || document.querySelector('time[datetime]');
    if (meta) return meta.content || meta.getAttribute('datetime') || meta.textContent.trim();
    return '';
  }
  function slugify(s) {
    return (s || 'artikel').toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80);
  }
  function normaliseerCode(s) {
    // Uppercase, strip whitespace en verwijder streepjes voor de check
    return String(s || '').toUpperCase().replace(/\s+/g, '').replace(/-/g, '');
  }
  function sha256Hex(str) {
    var buf = new TextEncoder().encode(str);
    return crypto.subtle.digest('SHA-256', buf).then(function(hash) {
      return Array.from(new Uint8Array(hash))
        .map(function(b) { return b.toString(16).padStart(2, '0'); })
        .join('');
    });
  }
  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
      return { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c];
    });
  }
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'ov-deel-toast'; t.textContent = msg;
    document.body.appendChild(t);
    requestAnimationFrame(function() { t.classList.add('is-visible'); });
    setTimeout(function() {
      t.classList.remove('is-visible');
      setTimeout(function() { t.remove(); }, 400);
    }, 2400);
  }

  // ---------- Codes laden ----------
  function loadCodes() {
    if (codesCache) return Promise.resolve(codesCache);
    var url = siteRootPrefix() + 'assets/deel-codes.json';
    return fetch(url, { cache: 'no-cache' })
      .then(function(r) { return r.ok ? r.json() : Promise.reject(new Error('codes niet beschikbaar')); })
      .then(function(cfg) {
        codesCache = cfg;
        return cfg;
      });
  }

  // Zoek de code-invoer op in de lijst — geef het volledige record terug (met verloopt)
  function vindActieveCode(codes, hash) {
    var nu = new Date().toISOString();
    for (var i = 0; i < codes.length; i++) {
      if (codes[i].hash === hash && codes[i].verloopt > nu) return codes[i];
    }
    return null;
  }

  // ---------- Lokale opgeslagen toegang ----------
  function cachedToegang() {
    try {
      var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (saved && saved.verloopt && new Date().toISOString() < saved.verloopt) {
        return saved;
      }
    } catch (e) { /* negeer */ }
    return null;
  }
  function saveToegang(hash, verloopt) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ hash: hash, verloopt: verloopt })); }
    catch (e) { /* privaatvenster */ }
  }

  // ---------- Modal: toegangscode invoeren ----------
  function promptCode(config) {
    return new Promise(function(resolve, reject) {
      var overlay = document.createElement('div');
      overlay.className = 'ov-deel-gate-overlay';
      overlay.innerHTML = ''
        + '<div class="ov-deel-gate" role="dialog" aria-modal="true">'
        + '  <h3>' + escapeHtml(config.gateTitle || 'Toegangscode') + '</h3>'
        + '  <p>' + escapeHtml(config.gateBody || 'Voer uw toegangscode in om deze PDF te downloaden.') + '</p>'
        + '  <input type="text" class="ov-deel-gate-input ov-deel-code-input" placeholder="XXXX-XXXX" autocomplete="off" spellcheck="false" autocapitalize="characters">'
        + '  <div class="ov-deel-gate-error" hidden></div>'
        + '  <div class="ov-deel-gate-actions">'
        + '    <button type="button" class="ov-deel-gate-cancel">' + escapeHtml(config.gateCancel || 'Annuleren') + '</button>'
        + '    <button type="button" class="ov-deel-gate-submit">' + escapeHtml(config.gateSubmit || 'Ontgrendelen') + '</button>'
        + '  </div>'
        + '  <p class="ov-deel-gate-note">' + escapeHtml(config.gateNote || 'Nog geen code? Neem contact op met Het Open Vizier.') + '</p>'
        + '</div>';
      document.body.appendChild(overlay);

      var input     = overlay.querySelector('.ov-deel-gate-input');
      var err       = overlay.querySelector('.ov-deel-gate-error');
      var submitBtn = overlay.querySelector('.ov-deel-gate-submit');
      var cancelBtn = overlay.querySelector('.ov-deel-gate-cancel');
      setTimeout(function() { input.focus(); }, 50);

      // Live formatting: XXXX-XXXX
      input.addEventListener('input', function() {
        var raw = normaliseerCode(input.value);
        if (raw.length > 4) input.value = raw.slice(0, 4) + '-' + raw.slice(4, 8);
        else input.value = raw;
      });

      function showError(msg) {
        err.textContent = msg; err.hidden = false;
        submitBtn.disabled = false; submitBtn.textContent = config.gateSubmit || 'Ontgrendelen';
        input.focus(); input.select();
      }
      function close(record) { overlay.remove(); resolve(record); }
      function cancel() { overlay.remove(); reject(new Error('cancelled')); }

      function submit() {
        var raw = normaliseerCode(input.value);
        if (raw.length < 4) {
          showError(config.gateInvalid || 'Voer een geldige code in.');
          return;
        }
        err.hidden = true;
        submitBtn.disabled = true;
        submitBtn.textContent = config.gateChecking || 'Bezig…';

        // Bereken hash van genormaliseerde code (dezelfde normalisatie als bij genereren)
        // Codes worden gegenereerd als XXXX-XXXX; opgeslagen hash is van XXXX-XXXX letterlijk
        var codeMetStreepje = raw.length > 4 ? raw.slice(0, 4) + '-' + raw.slice(4, 8) : raw;
        sha256Hex(codeMetStreepje).then(function(hash) {
          loadCodes().then(function(cfg) {
            var record = vindActieveCode(cfg.codes || [], hash);
            if (record) {
              saveToegang(hash, record.verloopt);
              close(record);
            } else {
              // Controleer ook zonder streepje voor het geval iemand een andere generator gebruikte
              sha256Hex(raw).then(function(h2) {
                var rec2 = vindActieveCode(cfg.codes || [], h2);
                if (rec2) {
                  saveToegang(h2, rec2.verloopt);
                  close(rec2);
                } else {
                  showError(config.gateWrong || 'Onjuiste of verlopen code.');
                }
              });
            }
          }).catch(function() {
            showError(config.gateServerError || 'Kon codes niet raadplegen.');
          });
        });
      }

      submitBtn.addEventListener('click', submit);
      cancelBtn.addEventListener('click', cancel);
      input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') submit();
        if (e.key === 'Escape') cancel();
      });
      overlay.addEventListener('click', function(e) { if (e.target === overlay) cancel(); });
    });
  }

  // ---------- Vrije acties ----------
  function actionCopy(config) {
    var url = canonicalUrl();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(
        function() { toast(config.msgCopied || 'Link gekopieerd'); },
        function() { fallbackCopy(url, config); }
      );
    } else { fallbackCopy(url, config); }
  }
  function fallbackCopy(url, config) {
    var ta = document.createElement('textarea');
    ta.value = url; ta.style.position='fixed'; ta.style.left='-9999px';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); toast(config.msgCopied || 'Link gekopieerd'); }
    catch (e) { window.prompt(config.msgCopyPrompt || 'Kopieer deze link:', url); }
    ta.remove();
  }
  // Generieke popup-opener met fallback naar nieuwe tab bij blokkade.
  // GEEN noopener/noreferrer — die verbreken sessie-cookies op deel-diensten.
  function openSharePopup(url, name, w, h) {
    var win = window.open(url, name || '_blank',
                'width=' + (w || 626) + ',height=' + (h || 520) +
                ',menubar=no,toolbar=no,resizable=yes,scrollbars=yes,status=no');
    if (!win || win.closed || typeof win.closed === 'undefined') {
      window.open(url, '_blank');
    } else {
      win.focus();
    }
  }

  // ---- Facebook ----
  function actionFacebook() {
    var url = 'https://www.facebook.com/sharer/sharer.php?u='
            + encodeURIComponent(canonicalUrl())
            + '&display=popup';
    openSharePopup(url, 'ov-fb-share', 626, 436);
  }

  // ---- X (Twitter) ----
  function actionX(config) {
    var text = articleTitle();
    var url = 'https://twitter.com/intent/tweet'
            + '?text=' + encodeURIComponent(text)
            + '&url='  + encodeURIComponent(canonicalUrl())
            + '&via='  + encodeURIComponent(config.xVia || 'KMerksteij62968');
    openSharePopup(url, 'ov-x-share', 550, 420);
  }

  // ---- LinkedIn ----
  function actionLinkedIn() {
    // LinkedIn haalt titel/preview zelf op via Open Graph van de canonical URL.
    var url = 'https://www.linkedin.com/sharing/share-offsite/?url='
            + encodeURIComponent(canonicalUrl());
    openSharePopup(url, 'ov-li-share', 640, 580);
  }

  // ---- WhatsApp ----
  function actionWhatsApp() {
    // wa.me werkt zowel op desktop (opent web.whatsapp.com) als mobiel (opent app).
    var text = articleTitle() + ' \u2014 ' + canonicalUrl();
    var url = 'https://wa.me/?text=' + encodeURIComponent(text);
    // Op mobiel: gewone navigatie (opent WhatsApp app); op desktop: popup.
    var isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    if (isMobile) {
      window.location.href = url;
    } else {
      openSharePopup(url, 'ov-wa-share', 720, 640);
    }
  }

  // ---- Telegram ----
  function actionTelegram() {
    var url = 'https://t.me/share/url'
            + '?url='  + encodeURIComponent(canonicalUrl())
            + '&text=' + encodeURIComponent(articleTitle());
    openSharePopup(url, 'ov-tg-share', 640, 580);
  }

  // ---- Instagram (kopieer + open) ----
  function actionInstagram(config) {
    // Instagram accepteert geen externe deelbare URL's. We kopiëren de link
    // naar het klembord en openen Instagram, zodat de gebruiker de link
    // handmatig in bio, Story of DM kan plakken.
    var url = canonicalUrl();
    var doCopy = navigator.clipboard && navigator.clipboard.writeText
      ? navigator.clipboard.writeText(url)
      : Promise.resolve();
    doCopy.finally(function() {
      toast(config.msgInstagramCopied || 'Link gekopieerd — plak in Instagram');
      var isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
      var target = isMobile ? 'instagram://user?username=openvizier' : 'https://www.instagram.com/';
      setTimeout(function() { window.open(target, '_blank'); }, 900);
    });
  }

  // ---- TikTok (kopieer + open) ----
  function actionTikTok(config) {
    // TikTok heeft ook geen externe share-URL. Zelfde patroon als Instagram:
    // link kopiëren + app/site openen zodat gebruiker het kan doorplaatsen.
    var url = canonicalUrl();
    var doCopy = navigator.clipboard && navigator.clipboard.writeText
      ? navigator.clipboard.writeText(url)
      : Promise.resolve();
    doCopy.finally(function() {
      toast(config.msgTikTokCopied || 'Link gekopieerd — plak in TikTok');
      setTimeout(function() { window.open('https://www.tiktok.com/', '_blank'); }, 900);
    });
  }
  function actionEmail(config) {
    var subject = (config.mailSubject || 'Artikel van Het Open Vizier: ') + articleTitle();
    var body = articleTitle() + '\n\n' + canonicalUrl() + '\n\n— ' + (config.mailFooter || 'Gedeeld via openvizier.org');
    window.location.href = 'mailto:?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  // ---------- PDF ----------
  function loadHtml2pdf() {
    if (window.html2pdf) return Promise.resolve(window.html2pdf);
    if (html2pdfLoading) return html2pdfLoading;
    html2pdfLoading = new Promise(function(resolve, reject) {
      var s = document.createElement('script');
      s.src = HTML2PDF_CDN;
      s.onload = function() { resolve(window.html2pdf); };
      s.onerror = function() { reject(new Error('html2pdf laden mislukt')); };
      document.head.appendChild(s);
    });
    return html2pdfLoading;
  }
  function buildPdfWorkspace(config) {
    var ws = document.createElement('div');
    ws.className = 'ov-deel-pdf-workspace';
    var cover = document.createElement('div');
    cover.className = 'ov-pdf-cover';
    var h1 = document.createElement('h1'); h1.textContent = articleTitle();
    cover.appendChild(h1);
    var meta = document.createElement('p'); meta.className = 'ov-pdf-meta';
    var date = articleDate();
    meta.textContent = 'Het Open Vizier · openvizier.org' + (date ? ' · ' + date : '');
    cover.appendChild(meta);
    ws.appendChild(cover);

    var body = document.createElement('div'); body.className = 'ov-pdf-body';
    var source = document.querySelector('article')
              || document.querySelector('main')
              || document.querySelector('.artikel')
              || document.querySelector('.content');
    if (source) {
      var clone = source.cloneNode(true);
      clone.querySelectorAll('nav, script, .ov-nav, .audio-player, .version-switch, .ov-deel-toast, .ov-deel-gate-overlay')
        .forEach(function(el) { el.remove(); });
      var firstH1 = clone.querySelector('h1'); if (firstH1) firstH1.remove();
      body.appendChild(clone);
    } else {
      body.textContent = document.body.innerText;
    }
    ws.appendChild(body);

    var footer = document.createElement('div'); footer.className = 'ov-pdf-footer';
    footer.innerHTML = '<strong>' + escapeHtml(config.pdfSource || 'Bron') + ':</strong> '
      + '<a href="' + escapeHtml(canonicalUrl()) + '">' + escapeHtml(canonicalUrl()) + '</a><br>'
      + escapeHtml(config.pdfNote || 'Gedeeld via openvizier.org.');
    ws.appendChild(footer);
    return ws;
  }
  function renderPdf(config, btn) {
    var labelEl = btn.querySelector('.ov-deel-label');
    var origLabel = labelEl ? labelEl.textContent : '';
    if (labelEl) labelEl.textContent = config.pdfBuilding || 'PDF wordt gemaakt…';
    btn.style.pointerEvents = 'none';

    return loadHtml2pdf().then(function(html2pdf) {
      var ws = buildPdfWorkspace(config);
      document.body.appendChild(ws);
      var filename = 'openvizier-' + slugify(articleTitle()) + '.pdf';
      var opt = {
        margin: [10, 10, 12, 10],
        filename: filename,
        image: { type: 'jpeg', quality: 0.94 },
        html2canvas: { scale: 2, useCORS: true, logging: false },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
      };
      return html2pdf().set(opt).from(ws).save().then(function() {
        ws.remove(); toast(config.pdfDone || 'PDF gedownload');
      });
    }).catch(function(err) {
      console.error('[ov-deel] PDF-fout:', err);
      toast(config.pdfFail || 'PDF maken mislukte — probeer Cmd+P');
    }).finally(function() {
      if (labelEl) labelEl.textContent = origLabel;
      btn.style.pointerEvents = '';
    });
  }
  function actionPdf(config, btn) {
    // Cached toegang? Direct renderen.
    if (cachedToegang()) {
      // Extra check: is de code nog steeds in de repo-lijst? (kan zijn ingetrokken)
      loadCodes().then(function(cfg) {
        var cached = cachedToegang();
        if (cached && vindActieveCode(cfg.codes || [], cached.hash)) {
          renderPdf(config, btn);
        } else {
          // Ingetrokken of niet meer geldig → vraag opnieuw
          try { localStorage.removeItem(STORAGE_KEY); } catch(e) {}
          promptCode(config).then(function() { renderPdf(config, btn); }).catch(function() {});
        }
      }).catch(function() {
        // Geen codes-lijst → weiger stil
        toast(config.gateServerError || 'Kon codes niet raadplegen.');
      });
      return;
    }
    promptCode(config).then(function() { renderPdf(config, btn); }).catch(function() { /* geannuleerd */ });
  }

  // ---------- Auto-generate submenu voor kale triggers ----------
  var LABELS = {
    nl: {copy:'Link kopi\u00ebren', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'Per e-mail', pdf:'PDF downloaden'},
    en: {copy:'Copy link', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'Send by email', pdf:'Download PDF'},
    de: {copy:'Link kopieren', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'Per E-Mail', pdf:'PDF herunterladen'},
    ru: {copy:'\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u0441\u044b\u043b\u043a\u0443', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'\u041f\u043e e-mail', pdf:'\u0421\u043a\u0430\u0447\u0430\u0442\u044c PDF'},
    fr: {copy:'Copier le lien', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'Par e-mail', pdf:'T\u00e9l\u00e9charger le PDF'},
    es: {copy:'Copiar enlace', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'Por correo', pdf:'Descargar PDF'},
    it: {copy:'Copia link', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'Per e-mail', pdf:'Scarica PDF'},
    pt: {copy:'Copiar liga\u00e7\u00e3o', whatsapp:'WhatsApp', x:'X (Twitter)', linkedin:'LinkedIn', facebook:'Facebook', email:'Por e-mail', pdf:'Descarregar PDF'}
  };
  function detectLang() {
    var m = window.location.pathname.match(/^\/([a-z]{2})\//);
    return (m && LABELS[m[1]]) ? m[1] : 'nl';
  }
  function autogenerate() {
    var triggers = document.querySelectorAll('[data-ov-deel-trigger]');
    triggers.forEach(function(trg) {
      if (trg.parentNode.querySelector('[data-ov-deel]')) return;
      var lang = detectLang();
      var lab = LABELS[lang];
      var acts = ['copy','whatsapp','x','linkedin','facebook','email','pdf'];
      var menu = document.createElement('div');
      menu.className = 'ov-nav__submenu';
      menu.setAttribute('data-ov-deel', '');
      acts.forEach(function(a) {
        var link = document.createElement('a');
        link.className = 'ov-nav__subitem';
        link.href = '#';
        link.setAttribute('data-ov-deel-action', a);
        link.textContent = lab[a] || a;
        menu.appendChild(link);
      });
      // Insert direct na trigger
      if (trg.nextSibling) trg.parentNode.insertBefore(menu, trg.nextSibling);
      else trg.parentNode.appendChild(menu);
      // Wrap trigger + menu in ov-nav__dropdown zodat hover/tap-toggle werkt
      if (trg.parentNode.classList && !trg.parentNode.classList.contains('ov-nav__dropdown')) {
        var wrapper = document.createElement('div');
        wrapper.className = 'ov-nav__dropdown';
        trg.parentNode.insertBefore(wrapper, trg);
        wrapper.appendChild(trg);
        wrapper.appendChild(menu);
      }
    });
  }

  // ---------- Init ----------
  function init() {
    autogenerate();
    // Extra: als menu-loader.js heeft al data-ov-deel-action op subitems gezet zonder [data-ov-deel]-wrapper, wrap ze
    document.querySelectorAll('[data-ov-deel-trigger]').forEach(function(trg) {
      var dropdown = trg.closest('.ov-nav__dropdown');
      if (dropdown) {
        var submenu = dropdown.querySelector('.ov-nav__submenu');
        if (submenu && !submenu.hasAttribute('data-ov-deel')) {
          submenu.setAttribute('data-ov-deel', '');
        }
      }
    });
    document.querySelectorAll('[data-ov-deel]').forEach(function(menu) {
      var config = {};
      Object.keys(menu.dataset).forEach(function(k) { config[k] = menu.dataset[k]; });
      menu.querySelectorAll('[data-ov-deel-action]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          var action = btn.dataset.ovDeelAction;
          if      (action === 'copy')      actionCopy(config);
          else if (action === 'facebook')  actionFacebook();
          else if (action === 'x')         actionX(config);
          else if (action === 'linkedin')  actionLinkedIn();
          else if (action === 'whatsapp')  actionWhatsApp();
          else if (action === 'telegram')  actionTelegram();
          else if (action === 'instagram') actionInstagram(config);
          else if (action === 'tiktok')    actionTikTok(config);
          else if (action === 'email')     actionEmail(config);
          else if (action === 'pdf')       actionPdf(config, btn);
        });
      });
    });
  }
  // Ook luisteren op menu-loader.js dat via CustomEvent aangeeft dat de nav klaar is
  document.addEventListener('ov-nav-ready', init);
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
