// Mobile navigation
(function () {
  var btn = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Email links are assembled here so the address isn't sitting in the HTML for spam bots.
  var user = 'rverver', host = 'canon-lawyer.ca';
  var addr = user + '@' + host;
  document.querySelectorAll('[data-email]').forEach(function (a) {
    a.href = 'mailto:' + addr;
    if (a.hasAttribute('data-email-show')) a.textContent = addr;
  });
})();
