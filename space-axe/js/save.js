const SAVE_KEY = 'spaceAxeSave_v1';

function defaultSave() {
  return {
    planets: {
      earth: { stars: [0, 0, 0, 0, 0] }
    }
  };
}

export function loadSave() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return defaultSave();
    const parsed = JSON.parse(raw);
    return { planets: { ...defaultSave().planets, ...parsed.planets } };
  } catch (e) {
    return defaultSave();
  }
}

export function writeSave(save) {
  localStorage.setItem(SAVE_KEY, JSON.stringify(save));
}

export function setSublevelStars(planetId, sublevelIndex, stars) {
  const save = loadSave();
  if (!save.planets[planetId]) save.planets[planetId] = { stars: [] };
  const current = save.planets[planetId].stars[sublevelIndex] || 0;
  save.planets[planetId].stars[sublevelIndex] = Math.max(current, stars);
  writeSave(save);
  return save;
}

export function getStars(planetId, sublevelIndex) {
  const save = loadSave();
  return save.planets[planetId]?.stars?.[sublevelIndex] || 0;
}

export function isSublevelUnlocked(planetId, sublevelIndex) {
  if (sublevelIndex === 0) return true;
  return getStars(planetId, sublevelIndex - 1) > 0;
}

export function getTotalStars(planetId, totalSublevels) {
  const save = loadSave();
  const stars = save.planets[planetId]?.stars || [];
  let total = 0;
  for (let i = 0; i < totalSublevels; i++) total += stars[i] || 0;
  return total;
}
