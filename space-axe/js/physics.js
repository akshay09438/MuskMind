export function springStep(state, dt, { restX, restY, gravityScale, motion, t }) {
  const springK = 60 * gravityScale;
  const damping = 9 * Math.sqrt(gravityScale);

  let targetX = restX;
  let targetY = restY;

  if (motion === 'static') {
    targetY = restY + Math.sin(t * 1.6) * 5;
  } else if (motion === 'drift') {
    targetX = restX + Math.sin(t * 1.1) * 30;
    targetY = restY + Math.sin(t * 0.8) * 14;
  } else if (motion === 'swing') {
    targetX = restX + Math.sin(t * 2.1) * 46;
    targetY = restY + Math.cos(t * 1.6) * 18;
  }

  const ax = (targetX - state.x) * springK - state.vx * damping;
  const ay = (targetY - state.y) * springK - state.vy * damping;

  state.vx += ax * dt;
  state.vy += ay * dt;
  state.x += state.vx * dt;
  state.y += state.vy * dt;
}

export function applyImpulse(state, ix, iy) {
  state.vx += ix;
  state.vy += iy;
}
