import { renderTitle } from './screens/title.js';
import { renderMap } from './screens/map.js';
import { renderSublevelSelect } from './screens/sublevelSelect.js';
import { renderGameplay } from './screens/gameplay.js';
import { renderSublevelComplete } from './screens/sublevelComplete.js';
import { renderPlanetComplete } from './screens/planetComplete.js';

const root = document.getElementById('app');
let cleanup = null;

const screens = {
  title: renderTitle,
  map: renderMap,
  sublevelSelect: renderSublevelSelect,
  gameplay: renderGameplay,
  sublevelComplete: renderSublevelComplete,
  planetComplete: renderPlanetComplete
};

function navigate(screenName, params = {}) {
  if (cleanup) {
    cleanup();
    cleanup = null;
  }
  root.innerHTML = '';
  const renderFn = screens[screenName];
  if (!renderFn) {
    console.error('Unknown screen:', screenName);
    return;
  }
  cleanup = renderFn(root, navigate, params) || null;
}

navigate('title');
