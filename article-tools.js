// Het Open Vizier — versie-switch en audio-speler
(function() {
  'use strict';

  // ===== Versie-switch (Kort / Uitgebreid) =====
  function initVersionSwitch() {
    var container = document.querySelector('.version-content');
    if (!container) return;
    
    var buttons = document.querySelectorAll('.version-switch__btn');
    buttons.forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        var version = btn.dataset.version;
        if (!version) return;
        
        // Update content
        container.dataset.version = version;
        
        // Update buttons
        buttons.forEach(function(b) {
          b.classList.toggle('version-switch__btn--active', b.dataset.version === version);
        });
        
        // Update URL hash (zonder pagina-sprong)
        if (history && history.replaceState) {
          var url = new URL(window.location);
          if (version === 'kort') {
            url.searchParams.set('versie', 'kort');
          } else {
            url.searchParams.delete('versie');
          }
          history.replaceState({}, '', url);
        }
        
        // Scroll naar boven van het artikel
        window.scrollTo({ top: container.offsetTop - 80, behavior: 'smooth' });
      });
    });
    
    // Bij laden: check URL voor ?versie=kort
    var params = new URLSearchParams(window.location.search);
    if (params.get('versie') === 'kort') {
      container.dataset.version = 'kort';
      buttons.forEach(function(b) {
        b.classList.toggle('version-switch__btn--active', b.dataset.version === 'kort');
      });
    }
  }

  // ===== Audio-speler =====
  function initAudioPlayer() {
    var btn = document.querySelector('.audio-player__btn');
    var audio = document.querySelector('.audio-player__el');
    if (!btn || !audio) return;
    
    var labelEl = btn.querySelector('.audio-player__label-text');
    var defaultLabel = labelEl ? labelEl.textContent : 'Voorlezen';
    var pauseLabel = btn.dataset.pauseLabel || 'Pauzeren';
    var resumeLabel = btn.dataset.resumeLabel || 'Hervatten';
    
    var iconPlay = btn.querySelector('.icon-play');
    var iconPause = btn.querySelector('.icon-pause');
    function showPlayIcon() {
      if (iconPlay) iconPlay.style.display = '';
      if (iconPause) iconPause.style.display = 'none';
    }
    function showPauseIcon() {
      if (iconPlay) iconPlay.style.display = 'none';
      if (iconPause) iconPause.style.display = '';
    }
    
    btn.addEventListener('click', function() {
      if (audio.paused) {
        audio.play().then(function() {
          btn.classList.add('is-playing');
          showPauseIcon();
          if (labelEl) labelEl.textContent = pauseLabel;
        }).catch(function(err) {
          console.error('Audio kon niet starten:', err);
        });
      } else {
        audio.pause();
        btn.classList.remove('is-playing');
        showPlayIcon();
        if (labelEl) labelEl.textContent = resumeLabel;
      }
    });
    
    audio.addEventListener('ended', function() {
      btn.classList.remove('is-playing');
      showPlayIcon();
      if (labelEl) labelEl.textContent = defaultLabel;
    });
  }

  // Init bij DOM-ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initVersionSwitch();
      initAudioPlayer();
    });
  } else {
    initVersionSwitch();
    initAudioPlayer();
  }
})();
