---
name: GSAP + SVG rotation pivot — the fix that works
description: Use svgOrigin (viewBox coords) in GSAP tweens; CSS transform-box is ignored for SVG.
type: reference
---

## The gotcha

Animating a `<g>` element in GSAP so it rotates **around its own viewBox
origin** (not its bounding-box centre) is a well-known trap.

## What does NOT work

```css
/* CSS alone — GSAP writes to the SVG transform attribute and ignores this */
#platform {
  transform-box: view-box;
  transform-origin: 0 0;          /* or 50% 50% */
}
```

GSAP sees an SVG element and switches to native SVG `transform="matrix(...)"`
attribute writes, which bypass CSS `transform-box` entirely.

Also wasted an iteration: proxy-object + onUpdate setting `transform`
attribute manually. Works during *playback* but `onUpdate` doesn't fire
reliably when the timeline is paused+seeked for screenshotting.

## What DOES work

```js
gsap.set('#platform',   { rotation: -90, svgOrigin: '0 0' });
gsap.to ('#platform',   { rotation:  90, svgOrigin: '0 0',
                          duration: 3.6, ease: 'power3.inOut' });
```

- `svgOrigin` is in **viewBox user-space coordinates**, not pixels.
- With `viewBox="-450 -450 900 900"` the centre of the SVG is `0 0`.
- `svgOrigin` must be supplied on **every** tween that touches this
  element — re-setting only in the `set` isn't inherited.

## Why this matters for Australian Turntables

Scene 3 of `trailer.html` has a platform + car silhouette that sweeps
0° → 180° around the dial centre. Without `svgOrigin: '0 0'` the group
orbits around its bounding-box centre, which drifts off-axis as the car
silhouette is asymmetric.

**How to apply:** any time you write GSAP rotations against an SVG `<g>`
whose children are authored centred on the user-space origin, add
`svgOrigin: '0 0'` to both the `set` and the `to`.
