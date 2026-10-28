(() => {
  'use strict';
  const language = document.querySelector('#language');
  language?.addEventListener('change', () => { window.location.assign(language.value); });

  const preview = document.querySelector('.preview');
  if (!preview) return;
  const sprite = preview.querySelector('.hero-pet');
  const speech = preview.querySelector('.speech');
  const toggle = preview.querySelector('.motion-toggle');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const choices = [...document.querySelectorAll('.pet-choice')];
  let kind = 'cat', pose = 'idle', name = choices[0].dataset.name;
  let frame = 0, timer = null, resetTimer = null, paused = false;

  function paint() {
    sprite.src = `${preview.dataset.assetBase}${kind}-${pose}-${frame}.png`;
  }
  function stop() {
    if (timer !== null) window.clearInterval(timer);
    timer = null;
  }
  function animate() {
    stop();
    frame = 0;
    paint();
    if (paused || reducedMotion.matches || document.hidden) return;
    timer = window.setInterval(() => {
      frame = (frame + 1) % (pose === 'walk' ? 6 : 4);
      paint();
    }, 320);
  }
  function setPose(next) {
    window.clearTimeout(resetTimer);
    pose = next;
    animate();
    if (next !== 'idle') resetTimer = window.setTimeout(() => { pose = 'idle'; animate(); }, 3800);
  }
  choices.forEach(button => button.addEventListener('click', () => {
    kind = button.dataset.pet;
    name = button.dataset.name;
    choices.forEach(choice => choice.setAttribute('aria-pressed', String(choice === button)));
    speech.textContent = name;
    setPose('idle');
  }));
  preview.querySelectorAll('[data-action]').forEach(button => button.addEventListener('click', () => {
    const playing = button.dataset.action === 'play';
    speech.textContent = `${name}: ${playing ? preview.dataset.playing : preview.dataset.greeting}`;
    setPose(playing ? 'play' : 'greet');
  }));
  toggle.addEventListener('click', () => {
    paused = !paused;
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.setAttribute('aria-label', paused ? toggle.dataset.resume : toggle.dataset.pause);
    toggle.firstElementChild.textContent = paused ? '▷' : 'Ⅱ';
    animate();
  });
  document.addEventListener('visibilitychange', animate);
  reducedMotion.addEventListener('change', animate);
  window.addEventListener('pagehide', () => { stop(); window.clearTimeout(resetTimer); });
  animate();
})();
