export class SwipeTracker {
  constructor(canvas, { onSegment, minSegmentDist = 6 }) {
    this.canvas = canvas;
    this.onSegment = onSegment;
    this.minSegmentDist = minSegmentDist;
    this.active = false;
    this.last = null;

    this.handlePointerDown = this.handlePointerDown.bind(this);
    this.handlePointerMove = this.handlePointerMove.bind(this);
    this.handlePointerUp = this.handlePointerUp.bind(this);

    canvas.addEventListener('pointerdown', this.handlePointerDown);
    canvas.addEventListener('pointermove', this.handlePointerMove);
    window.addEventListener('pointerup', this.handlePointerUp);
    window.addEventListener('pointercancel', this.handlePointerUp);
  }

  getPos(e) {
    const rect = this.canvas.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      time: performance.now() / 1000
    };
  }

  handlePointerDown(e) {
    this.active = true;
    this.last = this.getPos(e);
    try { this.canvas.setPointerCapture(e.pointerId); } catch (err) {}
  }

  handlePointerMove(e) {
    if (!this.active || !this.last) return;
    const pos = this.getPos(e);
    const dx = pos.x - this.last.x;
    const dy = pos.y - this.last.y;
    const dist = Math.hypot(dx, dy);
    if (dist < this.minSegmentDist) return;

    const dt = Math.max(pos.time - this.last.time, 1 / 240);
    const speed = dist / dt;

    this.onSegment({
      x1: this.last.x,
      y1: this.last.y,
      x2: pos.x,
      y2: pos.y,
      dist,
      dt,
      speed
    });

    this.last = pos;
  }

  handlePointerUp() {
    this.active = false;
    this.last = null;
  }

  destroy() {
    this.canvas.removeEventListener('pointerdown', this.handlePointerDown);
    this.canvas.removeEventListener('pointermove', this.handlePointerMove);
    window.removeEventListener('pointerup', this.handlePointerUp);
    window.removeEventListener('pointercancel', this.handlePointerUp);
  }
}
