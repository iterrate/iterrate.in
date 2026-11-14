// Draws the logo's loop around the home page headline, sized to the box.
// Same parts as the logo: sky line over the top ending in a half arrowhead,
// green uprights (the t and the a), earth line underneath kicking up into the
// right upright, and the green exit arrow carrying on out to the right.
(function () {
  var hero = document.querySelector('.hero');
  if (!hero) return;
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'loop draw');
  svg.setAttribute('aria-hidden', 'true');
  hero.insertBefore(svg, hero.firstChild);

  var parts = [
    ['earth', 0], ['leaf', 0.35], ['sky', 0.55], ['leaf', 0.9], ['leaf', 1.1]
  ];
  var paths = parts.map(function (p) {
    var el = document.createElementNS(NS, 'path');
    el.setAttribute('class', p[0]);
    el.style.setProperty('--delay', p[1] + 's');
    svg.appendChild(el);
    return el;
  });

  function draw() {
    var w = hero.clientWidth, h = hero.clientHeight;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    var small = w < 520;
    var xl = small ? 12 : 30;            // left upright (the t)
    var xr = w - (small ? 24 : 70);      // right upright (the a)
    var top = 4, bot = h - 16;           // sky line, earth line
    var r = 14, a = small ? 10 : 13;     // corner radius, arrowhead size
    var kick = small ? 22 : 30;          // earth line's diagonal kick

    // Gaps where lines meet, as in the logo. Distances are between line centres,
    // so the visible gap is that minus the line width (5px).
    var g = 15;   // 10px gaps where the loop's lines meet
    var gb = 7;   // 2px breaks in the earth line around the green corner

    // earth: from outside the loop on the left, breaking around the green corner,
    // then under everything, kicking up into the right upright
    var kx = xr - 6, ky = bot - kick;
    paths[0].setAttribute('d',
      'M0 ' + bot + ' H' + (xl - gb) + ' M' + (xl + r + gb) + ' ' + bot +
      ' H' + (kx - kick) + ' L' + kx + ' ' + ky + ' M' + kx + ' ' + ky + ' H' + (kx - a - 4));
    // left upright: down from the sky line, curving round to become the bottom line for a moment
    var skyEnd = top + 26;
    paths[1].setAttribute('d', 'M' + xl + ' ' + (skyEnd + g) + ' V' + (bot - r) +
      ' Q' + xl + ' ' + bot + ' ' + (xl + r) + ' ' + bot);
    // sky: up from the right upright, across the top, down towards the left upright with a half arrowhead
    var skyStart = top + 34;
    paths[2].setAttribute('d',
      'M' + xr + ' ' + skyStart + ' V' + (top + r) + ' Q' + xr + ' ' + top + ' ' + (xr - r) + ' ' + top +
      ' H' + (xl + r) + ' Q' + xl + ' ' + top + ' ' + xl + ' ' + (top + r) + ' V' + skyEnd +
      ' L' + (xl + a) + ' ' + (skyEnd - a));
    // right upright
    paths[3].setAttribute('d', 'M' + xr + ' ' + (skyStart + g) + ' V' + (ky - g));
    // exit arrow: starts g away (at right angles) from the earth line's diagonal kick
    var ex = w - 4, exStart = kx - kick + g * Math.SQRT2;
    paths[4].setAttribute('d',
      'M' + exStart + ' ' + bot + ' H' + ex + ' M' + (ex - a) + ' ' + (bot - a) + ' L' + ex + ' ' + bot + ' L' + (ex - a) + ' ' + (bot + a));

    paths.forEach(function (p) {
      p.style.setProperty('--len', Math.ceil(p.getTotalLength()) + 1);
    });
  }
  draw();
  // Redraw whenever the box changes size (fonts loading, window resizing).
  var first = true;
  new ResizeObserver(function () {
    if (first) { first = false; return; }
    draw();
  }).observe(hero);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { draw(); });
  }
})();
