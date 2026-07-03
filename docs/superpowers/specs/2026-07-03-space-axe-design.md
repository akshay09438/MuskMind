# Space Axe — Design Spec (v1: Earth Slice)

## Concept
A mobile-first, touch-controlled arcade game. The solar system is the level map — each planet is a level, each level has 5 sublevels, each sublevel presents one breakable object that the player destroys by swiping an axe across it. Planets differ in gravity, which changes object physics (drift, fall speed, swing) and therefore the timing/skill needed to land hits.

## Scope of this build
Full solar-system data model and engine, but only **Earth** (level 1) is populated with real sublevel content for now. The architecture supports adding further planets purely as data (theme + gravity + object list) without new code.

## Tech stack
- Static site: plain HTML5 Canvas + vanilla JS (ES modules), no build step, no framework, no external assets beyond code.
- Runs by opening `index.html` or serving the folder statically. Works on both touch (mobile) and mouse (desktop, for dev/testing).
- Custom lightweight 2D physics (position/velocity/gravity accel) — no physics engine dependency.
- Persistence via `localStorage` (stars per sublevel, unlocked levels).
- Location: new top-level folder `space-axe/` in the repo, fully standalone from the MindMusk chatbot app.

## Screens
1. **Title screen** — "SPACE AXE" logo, tap to start, shows solar system map.
2. **Solar system map** — planets rendered in a scroll/orbit row. Locked planets are dimmed with a lock icon. Tap unlocked planet → sublevel select for that planet.
3. **Sublevel select** — 5 nodes on a path (like a level trail) showing stars earned (0-3) and lock state (must clear sublevel N to unlock N+1).
4. **Gameplay screen** — the object in the center, HUD (planet name, sublevel #, HP bar for the object, combo counter, pause button). Swipe gestures chop the object.
5. **Sublevel complete screen** — stars earned, damage-efficiency stat, "Next" / "Retry" / "Map" buttons.
6. **Planet complete screen** — shown after sublevel 5/5 cleared, congratulates player, unlocks next planet (locked/"coming soon" for now beyond Earth), returns to map.

## Core mechanic: the swipe-axe
- Player performs a drag gesture (touchstart → touchmove → touchend, mouse equivalent for desktop) across the canvas.
- A swipe only counts as a "chop" if:
  - It crosses over the object's current hitbox (a circle/polygon that may be moving due to gravity/physics).
  - Its length exceeds a minimum distance threshold (prevents accidental taps from counting as swipes) — this also fulfills "tap to break" naturally: a short deliberate tap-drag still works if it crosses the object, just does less damage.
- Damage dealt = f(swipe speed, swipe length, angle-vs-object alignment). Faster + longer + more perpendicular-to-the-object's long axis = more damage. This rewards a real "slicing" motion over random flailing.
- Each chop spawns particle chips flying off in the swipe's perpendicular direction, plus a brief screen shake scaled to damage on the killing blow.
- A combo counter increments on consecutive chops within a short time window (0.8s) and resets on miss or timeout; combo adds a small damage multiplier, encouraging rhythm.
- Object HP hits 0 → break animation (particle burst + fade) → auto-advance to sublevel-complete screen after a short delay.

## Gravity system
- Each planet defines a `gravityScale` (Earth = 1.0, baseline).
- The breakable object is subject to gravity: it sits in a "rest zone" but on being hit takes knockback velocity, then gravity pulls it back to rest. Higher gravity = faster fall-back and shorter hover window (must chop quickly in bursts); lower gravity = slow drift, floats longer after a hit, but travels further off the "sweet spot" so the player must track it and adjust their swipe target — reads as genuinely different game-feel rather than pure difficulty knob.
- On Earth (this build) gravityScale = 1.0, object behavior: gentle bob/sway idle animation, moderate knockback-and-settle after each hit.

## Difficulty ramp within Earth (5 sublevels)
Sublevel 1 → 5 increases:
- Object HP (more chops needed).
- Reduces the swipe-timing window that keeps the combo alive.
- Introduces object motion: sublevel 1-2 objects are stationary (idle bob only); sublevel 3 introduces slow drift/swing; sublevel 4-5 add faster swing + brief invulnerability "guard" windows where a spinning knot/branch must be avoided or timed around.
- Object theming for Earth: 5 wood-based objects of increasing toughness — Twig, Branch, Log, Knotted Trunk, Ironwood Stump (flavor names, visual = different size/color logs).

## Scoring / stars
- 3 stars: break the object within a target time AND with high average damage-efficiency (few wasted/weak swipes).
- 2 stars: break within a looser time limit.
- 1 star: break with no time limit (completion only).
- Stars stored per sublevel in localStorage; total stars shown on planet-complete and map screens.

## Out of scope for this build (explicitly deferred)
- Planets beyond Earth (Mercury, Venus, Mars, ... Neptune) — map UI will show them locked/"coming soon".
- Sound/music assets (simple Web Audio synthesized thud/crack sound effects are in-scope since they require no external files; music is deferred).
- Backend, accounts, cloud save, monetization — all deferred, localStorage only.
- Orientation lock / native app wrapper — deferred; build as responsive web page, portrait-oriented layout.

## File layout
```
space-axe/
  index.html
  css/style.css
  js/
    main.js          # boot, screen router
    input.js         # swipe/touch gesture tracking
    physics.js        # gravity/knockback sim for the breakable object
    object.js         # breakable object model (HP, hitbox, damage calc)
    levels.js         # planet + sublevel data (Earth populated, rest stubbed)
    screens/
      title.js
      map.js
      sublevelSelect.js
      gameplay.js
      sublevelComplete.js
      planetComplete.js
    save.js           # localStorage read/write
    audio.js           # tiny WebAudio synth sfx
```

## Testing approach
Manual verification via the preview tool: load the page, confirm swipe gestures register as damage on the object, confirm object breaks and advances through all 5 Earth sublevels, confirm stars/localStorage persist across reload, confirm mobile viewport (375x812) layout and touch events work via preview_resize + simulated touch/mouse events.
