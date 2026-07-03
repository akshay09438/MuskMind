import { springStep, applyImpulse } from './physics.js';

export class BreakableObject {
  constructor(config, canvasWidth, canvasHeight) {
    this.config = config;
    this.maxHp = config.hp;
    this.hp = config.hp;
    this.radius = config.radius;
    this.restX = canvasWidth / 2;
    this.restY = canvasHeight * 0.42;
    this.x = this.restX;
    this.y = this.restY;
    this.vx = 0;
    this.vy = 0;
    this.t = Math.random() * 10;
    this.broken = false;
    this.motion = config.motion;
    this.hasGuard = !!config.guard;
    this.guardOpenDuration = config.guardOpenDuration || 1.4;
    this.guardClosedDuration = config.guardClosedDuration || 0.6;
    this.guardTimer = 0;
    this.guardActive = false;
  }

  update(dt, gravityScale) {
    if (this.broken) return;
    this.t += dt;
    springStep(this, dt, {
      restX: this.restX,
      restY: this.restY,
      gravityScale,
      motion: this.motion,
      t: this.t
    });

    if (this.hasGuard) {
      this.guardTimer += dt;
      const cycle = this.guardOpenDuration + this.guardClosedDuration;
      const phase = this.guardTimer % cycle;
      this.guardActive = phase >= this.guardOpenDuration;
    }
  }

  containsPoint(px, py) {
    return Math.hypot(px - this.x, py - this.y) <= this.radius;
  }

  hit(damage, impulseX, impulseY) {
    if (this.broken) return { blocked: false, broke: false };
    if (this.guardActive) return { blocked: true, broke: false };

    this.hp -= damage;
    applyImpulse(this, impulseX, impulseY);

    if (this.hp <= 0) {
      this.hp = 0;
      this.broken = true;
      return { blocked: false, broke: true };
    }
    return { blocked: false, broke: false };
  }
}
