import { getPlanet } from '../levels.js';
import { getTotalStars } from '../save.js';

export function renderPlanetComplete(root, navigate, { planetId }) {
  const planet = getPlanet(planetId);
  const total = getTotalStars(planetId, planet.sublevels.length);
  const max = planet.sublevels.length * 3;

  root.innerHTML = `
    <div class="screen complete-screen planet-complete">
      <div class="stars-bg"></div>
      <h2>${planet.name} cleared!</h2>
      <p class="stat">${total} / ${max} stars</p>
      <p class="tagline">More planets are on the way — the rest of the solar system awaits.</p>
      <div class="btn-col">
        <button class="btn primary" id="mapBtn">Back to Solar System</button>
      </div>
    </div>
  `;

  const mapBtn = root.querySelector('#mapBtn');
  const handler = () => navigate('map');
  mapBtn.addEventListener('click', handler);

  return () => mapBtn.removeEventListener('click', handler);
}
