import { getPlanet } from '../levels.js';
import { getStars, isSublevelUnlocked } from '../save.js';

export function renderSublevelSelect(root, navigate, { planetId }) {
  const planet = getPlanet(planetId);

  const nodes = planet.sublevels.map((sub, idx) => {
    const unlocked = isSublevelUnlocked(planetId, idx);
    const stars = getStars(planetId, idx);
    const starIcons = [0, 1, 2].map((i) => `<span class="star ${i < stars ? 'filled' : ''}">★</span>`).join('');
    return `
      <button class="sublevel-node ${unlocked ? '' : 'locked'}" data-idx="${idx}" ${unlocked ? '' : 'disabled'}>
        <div class="sublevel-num">${idx + 1}</div>
        <div class="sublevel-name">${sub.name}</div>
        <div class="sublevel-stars">${unlocked ? starIcons : '🔒'}</div>
      </button>
    `;
  }).join('');

  root.innerHTML = `
    <div class="screen sublevel-screen">
      <div class="stars-bg"></div>
      <header class="screen-header">
        <button class="btn back small" id="backBtn">‹ Map</button>
        <h2>${planet.name}</h2>
        <p>Choose a sublevel</p>
      </header>
      <div class="sublevel-path">${nodes}</div>
    </div>
  `;

  const backBtn = root.querySelector('#backBtn');
  const backHandler = () => navigate('map');
  backBtn.addEventListener('click', backHandler);

  const nodeButtons = [...root.querySelectorAll('.sublevel-node:not(.locked)')];
  const nodeHandler = (e) => {
    const idx = parseInt(e.currentTarget.dataset.idx, 10);
    navigate('gameplay', { planetId, sublevelIndex: idx });
  };
  nodeButtons.forEach((b) => b.addEventListener('click', nodeHandler));

  return () => {
    backBtn.removeEventListener('click', backHandler);
    nodeButtons.forEach((b) => b.removeEventListener('click', nodeHandler));
  };
}
