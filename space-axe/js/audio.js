let ctx = null;

function getCtx() {
  if (!ctx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    ctx = new AC();
  }
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}

function noiseBurst({ duration = 0.12, freq = 900, gain = 0.3 }) {
  const audioCtx = getCtx();
  const bufferSize = Math.max(1, Math.floor(audioCtx.sampleRate * duration));
  const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
  }

  const source = audioCtx.createBufferSource();
  source.buffer = buffer;

  const filter = audioCtx.createBiquadFilter();
  filter.type = 'bandpass';
  filter.frequency.value = freq;
  filter.Q.value = 0.9;

  const gainNode = audioCtx.createGain();
  gainNode.gain.setValueAtTime(gain, audioCtx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);

  source.connect(filter).connect(gainNode).connect(audioCtx.destination);
  source.start();
}

export function playChop() {
  try { noiseBurst({ duration: 0.09, freq: 1400, gain: 0.25 }); } catch (e) { /* audio unavailable */ }
}

export function playBreak() {
  try {
    noiseBurst({ duration: 0.28, freq: 500, gain: 0.4 });
    noiseBurst({ duration: 0.18, freq: 2200, gain: 0.2 });
  } catch (e) { /* audio unavailable */ }
}

export function playBlocked() {
  try { noiseBurst({ duration: 0.06, freq: 2600, gain: 0.15 }); } catch (e) { /* audio unavailable */ }
}
