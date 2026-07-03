import { getPlanet } from '../levels.js';
import { BreakableObject } from '../object.js';
import { SwipeTracker } from '../input.js';
import { setSublevelStars } from '../save.js';
import { playChop, playBreak, playBlocked } from '../audio.js';

const REF_SPEED = 900;

function segmentCircleDistance(x1, y1, x2, y2, cx, cy) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const lenSq = dx * dx + dy * dy;
  let t = lenSq === 0 ? 0 : ((cx - x1) * dx + (cy - y1) * dy) / lenSq;
  t = Math.max(0, Math.min(1, t));
  const px = x1 + t * dx;
  const py = y1 + t * dy;
  return Math.hypot(cx - px, cy - py);
}

export function renderGameplay(root, navigate, { planetId, sublevelIndex }) {
  const planet = getPlanet(planetId);
  const subConfig = planet.sublevels[sublevelIndex];

  root.innerHTML = `
    <div class="screen gameplay-screen">
      <div class="hud">
        <button class="btn back small" id="backBtn">‹</button>
        <div class="hud-center">
          <div class="hud-title">${planet.name} · ${subConfig.name}</div>
          <div class="hp-bar-track"><div class="hp-bar-fill" id="hpFill"></div></div>
        </div>
        <div class="combo" id="comboDisplay"></div>
      </div>
      <div class="canvas-wrap" id="canvasWrap">
        <canvas id="gameCanvas"></canvas>
      </div>
      <div class="hint" id="hint">Swipe across the object to chop it!</div>
    </div>
  `;

  const canvas = root.querySelector('#gameCanvas');
  const wrap = root.querySelector('#canvasWrap');
  const ctx = canvas.getContext('2d');
  const hpFill = root.querySelector('#hpFill');
  const comboDisplay = root.querySelector('#comboDisplay');
  const hint = root.querySelector('#hint');

  let width = 0;
  let height = 0;
  const obj = new BreakableObject(subConfig, 300, 500);

  function resize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = wrap.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    obj.restX = width / 2;
    obj.restY = height * 0.42;
    obj.x = obj.restX;
    obj.y = obj.restY;
    obj.vx = 0;
    obj.vy = 0;
  }
  resize();
  window.addEventListener('resize', resize);

  let particles = [];
  let shakeTime = 0;
  let shakeMag = 0;
  let combo = 0;
  let comboTimer = 0;
  const comboWindow = subConfig.comboWindow;
  let finished = false;
  const startTime = performance.now() / 1000;
  let goodHits = 0;
  let totalHits = 0;

  function spawnParticles(x, y, color, count, dirX, dirY) {
    for (let i = 0; i < count; i++) {
      const angle = Math.atan2(dirY, dirX) + (Math.random() - 0.5) * 2.2;
      const speed = 60 + Math.random() * 160;
      const life = 0.4 + Math.random() * 0.4;
      particles.push({
        x, y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life,
        maxLife: life,
        color,
        size: 2 + Math.random() * 3
      });
    }
  }

  function triggerShake(mag) {
    shakeTime = 0.25;
    shakeMag = mag;
  }

  function finishSublevel() {
    finished = true;
    const elapsed = performance.now() / 1000 - startTime;
    const efficiency = totalHits > 0 ? goodHits / totalHits : 1;
    let stars = 1;
    if (elapsed <= subConfig.timeTarget3 && efficiency > 0.75) stars = 3;
    else if (elapsed <= subConfig.timeTarget2) stars = 2;

    setSublevelStars(planetId, sublevelIndex, stars);

    setTimeout(() => {
      navigate('sublevelComplete', { planetId, sublevelIndex, stars, elapsed });
    }, 900);
  }

  function handleSegment(seg) {
    if (finished || obj.broken) return;
    const dist = segmentCircleDistance(seg.x1, seg.y1, seg.x2, seg.y2, obj.x, obj.y);
    if (dist > obj.radius) return;

    const now = performance.now() / 1000;
    combo = comboTimer > 0 && now - comboTimer < comboWindow ? combo + 1 : 1;
    comboTimer = now;

    const speedFactor = Math.min(Math.max(seg.speed / REF_SPEED, 0.35), 2.4);
    const comboMult = 1 + Math.min(combo - 1, 8) * 0.08;
    const damage = speedFactor * comboMult;

    const dirX = seg.x2 - seg.x1;
    const dirY = seg.y2 - seg.y1;
    const midX = (seg.x1 + seg.x2) / 2;
    const midY = (seg.y1 + seg.y2) / 2;

    const result = obj.hit(damage, dirX * 0.4, dirY * 0.4);
    totalHits++;

    if (result.blocked) {
      playBlocked();
      spawnParticles(midX, midY, '#ffffff', 6, dirX, dirY);
      combo = 0;
      return;
    }

    goodHits++;
    hint.style.opacity = '0';
    spawnParticles(midX, midY, subConfig.color, 10 + combo, dirX, dirY);

    if (result.broke) {
      playBreak();
      triggerShake(14);
      spawnParticles(obj.x, obj.y, subConfig.color, 40, 0, -1);
      finishSublevel();
    } else {
      playChop();
      triggerShake(4 + Math.min(combo, 6));
    }
  }

  const tracker = new SwipeTracker(canvas, { onSegment: handleSegment });

  let raf = null;
  let lastTime = performance.now();

  function loop() {
    const now = performance.now();
    const dt = Math.min((now - lastTime) / 1000, 0.033);
    lastTime = now;
    const t = now / 1000;

    if (!finished) {
      if (comboTimer > 0 && t - comboTimer > comboWindow) combo = 0;
      obj.update(dt, planet.gravityScale);
    }

    particles = particles.filter((p) => p.life > 0);
    particles.forEach((p) => {
      p.life -= dt;
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.vy += 220 * dt;
      p.vx *= 0.98;
    });

    if (shakeTime > 0) shakeTime -= dt;

    ctx.clearRect(0, 0, width, height);
    ctx.save();

    if (shakeTime > 0) {
      const decay = shakeTime / 0.25;
      ctx.translate((Math.random() - 0.5) * shakeMag * decay, (Math.random() - 0.5) * shakeMag * decay);
    }

    if (!obj.broken) {
      ctx.save();
      if (obj.hasGuard && obj.guardActive) {
        ctx.globalAlpha = 0.55 + Math.sin(now / 60) * 0.15;
        ctx.fillStyle = '#ffffff';
      } else {
        ctx.fillStyle = subConfig.color;
      }
      ctx.beginPath();
      ctx.arc(obj.x, obj.y, obj.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.lineWidth = 4;
      ctx.strokeStyle = 'rgba(0,0,0,0.35)';
      ctx.stroke();
      ctx.restore();
    }

    particles.forEach((p) => {
      ctx.globalAlpha = Math.max(p.life / p.maxLife, 0);
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalAlpha = 1;

    ctx.restore();

    hpFill.style.width = `${Math.max(obj.hp / obj.maxHp, 0) * 100}%`;
    comboDisplay.textContent = combo > 1 ? `x${combo}` : '';

    raf = requestAnimationFrame(loop);
  }
  raf = requestAnimationFrame(loop);

  const backBtn = root.querySelector('#backBtn');
  const backHandler = () => navigate('sublevelSelect', { planetId });
  backBtn.addEventListener('click', backHandler);

  return () => {
    cancelAnimationFrame(raf);
    window.removeEventListener('resize', resize);
    tracker.destroy();
    backBtn.removeEventListener('click', backHandler);
  };
}
