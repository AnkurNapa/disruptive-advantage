/* Disruptive Advantage, site behaviour.
   Plain ES5-compatible DOM work, no dependencies. Everything here is
   progressive: with JS off, the pages still read and every link works. */
(function () {
  'use strict';

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* --- mobile menu ------------------------------------------------- */
  var burger = $('#menu');
  var nav = $('#sitenav');
  if (burger && nav) {
    var mq = window.matchMedia('(max-width: 980px)');
    var sync = function () {
      if (mq.matches) {
        nav.hidden = burger.getAttribute('aria-expanded') !== 'true';
      } else {
        nav.hidden = false;
        burger.setAttribute('aria-expanded', 'false');
      }
    };
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      burger.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      sync();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        burger.setAttribute('aria-expanded', 'false');
        sync();
        burger.focus();
      }
    });
    if (mq.addEventListener) { mq.addEventListener('change', sync); }
    else if (mq.addListener) { mq.addListener(sync); }
    sync();
  }

  /* --- case studies: filter by industry ---------------------------- */
  var chips = $$('.chip[data-filter]');
  if (chips.length) {
    var cards = $$('.csc[data-ind]');
    var count = $('#csCount');
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var want = chip.getAttribute('data-filter');
        chips.forEach(function (c) {
          var on = c === chip;
          c.classList.toggle('is-on', on);
          c.setAttribute('aria-pressed', String(on));
        });
        var shown = 0;
        cards.forEach(function (card) {
          var match = want === 'all' || card.getAttribute('data-ind') === want;
          card.hidden = !match;
          if (match) { shown++; }
        });
        if (count) { count.textContent = String(shown); }
      });
    });
  }

  /* --- contact: produce pills + a form that actually sends ---------- */
  var pills = $$('.pill[data-produce]');
  pills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      pills.forEach(function (p) {
        var on = p === pill;
        p.classList.toggle('is-on', on);
        p.setAttribute('aria-pressed', String(on));
      });
    });
  });

  var form = $('#enquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var val = function (id) { var el = $('#' + id); return el ? el.value.trim() : ''; };
      var note = $('#formnote');
      if (!val('e')) {
        if (note) { note.textContent = 'A work email address is needed so we can reply.'; note.className = 'formnote is-bad'; }
        var email = $('#e'); if (email) { email.focus(); }
        return;
      }
      var chosen = $('.pill.is-on');
      var lines = [
        'Name: ' + val('n'),
        'Company: ' + val('c'),
        'Role: ' + val('r'),
        'Produces: ' + (chosen ? chosen.textContent.trim() : 'not stated'),
        '',
        val('m') || '(no detail given)'
      ];
      window.location.href = 'mailto:info@disruptive-advantage.com'
        + '?subject=' + encodeURIComponent('Enquiry from ' + (val('c') || val('n') || 'the website'))
        + '&body=' + encodeURIComponent(lines.join('\n'));
      if (note) { note.textContent = 'Opening your email client with the message ready to send.'; note.className = 'formnote'; }
    });
  }

  /* --- newsletter sign-ups ----------------------------------------- */
  $$('.form button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var input = btn.parentNode.querySelector('input');
      var addr = input ? input.value.trim() : '';
      window.location.href = 'mailto:info@disruptive-advantage.com'
        + '?subject=' + encodeURIComponent('Subscribe to the monthly note')
        + '&body=' + encodeURIComponent('Please add ' + (addr || '[your email]') + ' to the monthly note.');
    });
  });

  /* --- careers: search the open roles ------------------------------ */
  var q = $('#jobq');
  if (q) {
    var jobs = $$('.job');
    var empty = $('#nojobs');
    var jobCount = $('#jobCount');
    var WORDS = ['No', 'One', 'Two', 'Three', 'Four', 'Five'];
    var run = function () {
      var term = q.value.trim().toLowerCase();
      var shown = 0;
      jobs.forEach(function (job) {
        var match = !term || job.textContent.toLowerCase().indexOf(term) !== -1;
        job.hidden = !match;
        if (match) { shown++; }
      });
      if (empty) { empty.hidden = shown !== 0; }
      if (jobCount) { jobCount.textContent = WORDS[shown] || String(shown); }
    };
    q.addEventListener('input', run);
    q.addEventListener('search', run);
    var go = $('#jobgo');
    if (go) { go.addEventListener('click', run); }
  }

  /* --- case study: copy link, print --------------------------------- */
  var copy = $('[data-share="copy"]');
  if (copy) {
    copy.addEventListener('click', function () {
      var done = function () {
        copy.classList.add('copied');
        setTimeout(function () { copy.classList.remove('copied'); }, 1600);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(window.location.href).then(done, done); }
      else { done(); }
    });
  }
  var printcs = $('#printcs');
  if (printcs) { printcs.addEventListener('click', function () { window.print(); }); }
})();
