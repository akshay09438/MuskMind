import { PLANETS } from '../levels.js';
import { getTotalStars } from '../save.js';

export function renderMap(root, navigate) {
  const cards = PLANETS.map((planet) => {
    const totalSublevels = planet.sublevels.length || 5;
    const locked = !planet.available;
    const stars = locked ? 0 : getTotalStars(planet.id, totalSublevels);
    return `
      <button class="planet-card ${locked ? 'locked' : ''}" data-id="${planet.id}" ${locked ? 'disabled' : ''} style="--planet-color:${planet.color}">
        <div class="planet-dot"></div>
        <div class="planet-info">
          <div class="planet-name">${planet.name}</div>
          <div class="planet-sub">${locked ? 'Coming soon' : `${stars} / ${totalSublevels * 3} stars`}</div>
        </div>
        ${locked ? '<div class="lock">LOCKED</div>' : '<div class="chevron">›</div>'}
      </button>
    `;
  }).join('');

  root.innerHTML = `
    <div class="screen map-screen">
      <div class="stars-bg"></div>
      <header class="screen-header">
        <h2>Solar System</h2>
        <p>Select a planet to begin</p>
      </header>
      <div class="planet-list">${cards}</div>
    </div>
  `;

  const buttons = [...root.querySelectorAll('.planet-card:not(.locked)')];
  const handler = (e) => {
    const id = e.currentTarget.dataset.id;
    navigate('sublevelSelect', { planetId: id });
  };
  buttons.forEach((b) => b.addEventListener('click', handler));

  return () => buttons.forEach((b) => b.removeEventListener('click', handler));
}
