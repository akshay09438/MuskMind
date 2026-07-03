export function renderTitle(root, navigate) {
  root.innerHTML = `
    <div class="screen title-screen">
      <div class="stars-bg"></div>
      <h1 class="logo">SPACE<span>AXE</span></h1>
      <p class="tagline">Chop your way across the solar system</p>
      <button class="btn primary big" id="startBtn">Tap to Start</button>
    </div>
  `;

  const btn = root.querySelector('#startBtn');
  const onClick = () => navigate('map');
  btn.addEventListener('click', onClick);

  return () => btn.removeEventListener('click', onClick);
}
