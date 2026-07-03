import { getPlanet } from '../levels.js';

export function renderSublevelComplete(root, navigate, { planetId, sublevelIndex, stars, elapsed }) {
  const planet = getPlanet(planetId);
  const subConfig = planet.sublevels[sublevelIndex];
  const isLast = sublevelIndex === planet.sublevels.length - 1;
  const starIcons = [0, 1, 2].map((i) => `<span class="star big ${i < stars ? 'filled' : ''}">★</span>`).join('');

  root.innerHTML = `
    <div class="screen complete-screen">
      <div class="stars-bg"></div>
      <h2>${subConfig.name} chopped!</h2>
      <div class="stars-row">${starIcons}</div>
      <p class="stat">Time: ${elapsed.toFixed(1)}s</p>
      <div class="btn-col">
        <button class="btn primary" id="nextBtn">${isLast ? 'Finish Planet' : 'Next Sublevel'}</button>
        <button class="btn" id="retryBtn">Retry</button>
        <button class="btn" id="mapBtn">Map</button>
      </div>
    </div>
  `;

  const nextBtn = root.querySelector('#nextBtn');
  const nextHandler = () => {
    if (isLast) {
      navigate('planetComplete', { planetId });
    } else {
      navigate('gameplay', { planetId, sublevelIndex: sublevelIndex + 1 });
    }
  };
  nextBtn.addEventListener('click', nextHandler);

  const retryBtn = root.querySelector('#retryBtn');
  const retryHandler = () => navigate('gameplay', { planetId, sublevelIndex });
  retryBtn.addEventListener('click', retryHandler);

  const mapBtn = root.querySelector('#mapBtn');
  const mapHandler = () => navigate('sublevelSelect', { planetId });
  mapBtn.addEventListener('click', mapHandler);

  return () => {
    nextBtn.removeEventListener('click', nextHandler);
    retryBtn.removeEventListener('click', retryHandler);
    mapBtn.removeEventListener('click', mapHandler);
  };
}
