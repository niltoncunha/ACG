import { matrixScenes } from "./tesserus-data.js";

const canvas = document.getElementById("stage");
const ctx = canvas.getContext("2d");
const matrixRail = document.getElementById("matrixRail");
const codeEl = document.getElementById("code");
const titleEl = document.getElementById("title");
const statementEl = document.getElementById("statement");
const centerLabelEl = document.getElementById("centerLabel");
const detailLabelEl = document.getElementById("detailLabel");
const mapLabelEl = document.getElementById("mapLabel");
const excerptEl = document.getElementById("excerpt");
const planesEl = document.getElementById("planes");
const autoplayButton = document.getElementById("autoplay");
const modeButtons = [...document.querySelectorAll("[data-mode]")];

const state = {
  width: 0,
  height: 0,
  time: 0,
  mode: "pulse",
  dragging: false,
  yaw: -0.85,
  pitch: -0.32,
  pointerX: 0,
  pointerY: 0,
  activeScene: 0,
  autoplay: true,
  lastSwitch: 0,
};

function resize() {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(window.innerWidth * ratio);
  canvas.height = Math.round(window.innerHeight * ratio);
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  state.width = window.innerWidth;
  state.height = window.innerHeight;
}
function lerp(a, b, t) { return a + (b - a) * t; }
function rotateY(point, angle) {
  const c = Math.cos(angle); const s = Math.sin(angle);
  return { x: point.x * c + point.z * s, y: point.y, z: -point.x * s + point.z * c };
}
function rotateX(point, angle) {
  const c = Math.cos(angle); const s = Math.sin(angle);
  return { x: point.x, y: point.y * c - point.z * s, z: point.y * s + point.z * c };
}
function project(point) {
  const rotated = rotateX(rotateY(point, state.yaw), state.pitch);
  const depth = rotated.z + 18;
  const scale = 1100 / depth;
  return { x: rotated.x * scale + state.width * 0.56, y: rotated.y * scale + state.height * 0.56, scale, depth };
}
function line(a, b, color, width = 1, alpha = 1) {
  const pa = project(a); const pb = project(b);
  ctx.save(); ctx.globalAlpha = alpha; ctx.strokeStyle = color; ctx.lineWidth = width;
  ctx.beginPath(); ctx.moveTo(pa.x, pa.y); ctx.lineTo(pb.x, pb.y); ctx.stroke(); ctx.restore();
}
function polygon(points, fill, stroke, alpha = 1, width = 1) {
  const projected = points.map(project);
  ctx.save(); ctx.globalAlpha = alpha; ctx.beginPath(); ctx.moveTo(projected[0].x, projected[0].y);
  for (let i = 1; i < projected.length; i += 1) ctx.lineTo(projected[i].x, projected[i].y);
  ctx.closePath();
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.lineWidth = width; ctx.strokeStyle = stroke; ctx.stroke(); }
  ctx.restore();
}
function dot(point, radius, color, glow = 0, alpha = 1) {
  const p = project(point);
  ctx.save(); ctx.globalAlpha = alpha; ctx.fillStyle = color; ctx.shadowBlur = glow; ctx.shadowColor = color;
  ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(radius * p.scale * 0.06, 2), 0, Math.PI * 2); ctx.fill(); ctx.restore();
}
function label(text, point, color, align = "center") {
  const p = project(point);
  ctx.save(); ctx.fillStyle = color; ctx.font = "600 12px Segoe UI, sans-serif"; ctx.textAlign = align; ctx.fillText(text, p.x, p.y); ctx.restore();
}
function backdrop(scene) {
  const gradient = ctx.createRadialGradient(state.width * 0.6, state.height * 0.5, 50, state.width * 0.6, state.height * 0.5, state.width * 0.55);
  gradient.addColorStop(0, `${scene.palette.center}22`); gradient.addColorStop(0.35, `${scene.palette.detail}12`); gradient.addColorStop(1, "#04060b");
  ctx.fillStyle = gradient; ctx.fillRect(0, 0, state.width, state.height);
  ctx.save(); ctx.strokeStyle = "rgba(113, 145, 204, 0.08)"; ctx.lineWidth = 1;
  for (let x = 0; x < state.width; x += 36) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, state.height); ctx.stroke(); }
  for (let y = 0; y < state.height; y += 36) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(state.width, y); ctx.stroke(); }
  ctx.restore();
}
function drawPlanes(scene, phase) {
  const bands = [{ x: -7.4, y: 3.1, z: -3.3 }, { x: -7.4, y: 0.1, z: -0.3 }, { x: -7.4, y: -2.9, z: 2.7 }];
  bands.forEach((band, index) => {
    const wobble = state.mode === "drift" ? Math.sin(phase + index * 0.9) * 0.3 : 0;
    const plane = [
      { x: band.x, y: band.y - 1.6 + wobble, z: band.z - 3.1 },
      { x: band.x, y: band.y - 1.6 + wobble, z: band.z + 3.1 },
      { x: band.x, y: band.y + 1.6 + wobble, z: band.z + 3.1 },
      { x: band.x, y: band.y + 1.6 + wobble, z: band.z - 3.1 },
    ];
    polygon(plane, `${scene.palette.plane}14`, `${scene.palette.plane}aa`, 0.8, 1.15);
    label(scene.planes[index].name, { x: band.x, y: band.y + 2.25, z: band.z }, scene.palette.plane, "left");
  });
}
function drawMap(scene, phase) {
  const points = []; const total = scene.nodes.length;
  for (let i = 0; i < total; i += 1) {
    const t = total === 1 ? 0 : i / (total - 1); const bend = Math.sin(phase + t * Math.PI * 1.5) * 0.6;
    points.push({ x: 7.2 - t * 12.6, y: 4.4 - t * 5.1 + bend, z: -4.4 + t * 8.7 });
  }
  for (let i = 0; i < points.length - 1; i += 1) line(points[i], points[i + 1], scene.palette.map, 2.2, 0.9 - i * 0.08);
  points.forEach((point, index) => {
    dot(point, 8 - index * 0.6, scene.palette.map, 22, 0.95 - index * 0.08);
    label(scene.nodes[index], { x: point.x, y: point.y + 0.55, z: point.z }, scene.palette.map, "left");
  });
}
function drawStackCenter(scene, beat) {
  for (let i = 0; i < 4; i += 1) {
    const y = 2.4 - i * 1.45; const width = 3.6 - i * 0.18 + beat * 0.06; const depth = 3.4 - i * 0.12;
    polygon([{ x: -width, y, z: -depth }, { x: width, y, z: -depth }, { x: width, y, z: depth }, { x: -width, y, z: depth }], `${scene.palette.center}${i === 1 ? "3c" : "18"}`, `${scene.palette.center}aa`, 0.95, 1.1);
  }
  line({ x: 0, y: -2.4, z: 0 }, { x: 0, y: 2.8, z: 0 }, scene.palette.detail, 1.3, 0.7);
  dot({ x: 0, y: 1.0, z: 0 }, 12 + beat * 2, scene.palette.detail, 26, 1);
  label(scene.centerLabel, { x: 0, y: 3.4, z: 0 }, scene.palette.center);
}
function drawTowerCenter(scene, beat) {
  const levels = [{ y: 2.8, w: 3.4, d: 1.2 }, { y: 1.0, w: 2.9, d: 1.2 }, { y: -0.8, w: 2.4, d: 1.2 }, { y: -2.6, w: 1.9, d: 1.2 }];
  levels.forEach((level, index) => {
    const pulse = beat * (0.14 - index * 0.02);
    polygon([{ x: -level.w - pulse, y: level.y - 0.58, z: -level.d }, { x: level.w + pulse, y: level.y - 0.58, z: -level.d }, { x: level.w + pulse, y: level.y + 0.58, z: level.d }, { x: -level.w - pulse, y: level.y + 0.58, z: level.d }], `${scene.palette.center}${index === 0 ? "38" : "16"}`, `${scene.palette.center}aa`, 0.96, 1.1);
  });
  label(scene.centerLabel, { x: 0, y: 4.1, z: 0 }, scene.palette.center);
}
function drawPortalCenter(scene, beat) {
  const half = 3.3 + beat * 0.1;
  polygon([{ x: -half, y: -half, z: 0 }, { x: half, y: -half, z: 0 }, { x: half, y: half, z: 0 }, { x: -half, y: half, z: 0 }], `${scene.palette.center}12`, `${scene.palette.center}aa`, 0.95, 1.2);
  for (let row = 0; row < 8; row += 1) {
    for (let col = 0; col < 8; col += 1) {
      const x = lerp(-2.7, 2.7, col / 7); const y = lerp(-2.7, 2.7, row / 7); const active = row === 4 && col === 3;
      dot({ x, y, z: 0 }, active ? 14 : 8, active ? scene.palette.detail : scene.palette.center, active ? 30 : 16, active ? 1 : 0.72);
    }
  }
  label(scene.centerLabel, { x: 0, y: 4.2, z: 0 }, scene.palette.center);
}
function drawCubeGridCenter(scene, beat) {
  const size = 2.8 + beat * 0.12;
  const corners = [
    { x: -size, y: -size, z: -size }, { x: size, y: -size, z: -size }, { x: size, y: size, z: -size }, { x: -size, y: size, z: -size },
    { x: -size, y: -size, z: size }, { x: size, y: -size, z: size }, { x: size, y: size, z: size }, { x: -size, y: size, z: size },
  ];
  const edges = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
  polygon([corners[0], corners[1], corners[2], corners[3]], `${scene.palette.center}10`, `${scene.palette.center}aa`, 0.9, 1.05);
  polygon([corners[4], corners[5], corners[6], corners[7]], `${scene.palette.center}20`, `${scene.palette.center}aa`, 0.88, 1.05);
  edges.forEach(([a, b]) => line(corners[a], corners[b], scene.palette.center, 1.1, 0.88));
  for (let i = 0; i < 8; i += 1) {
    const z = lerp(-2.3, 2.3, i / 7);
    for (let j = 0; j < 8; j += 1) dot({ x: lerp(-2.1, 2.1, j / 7), y: 0.3, z }, j === 4 && i === 3 ? 10 : 5, j === 4 && i === 3 ? scene.palette.detail : scene.palette.center, 18, 0.7);
  }
  label(scene.centerLabel, { x: 0, y: 4, z: 0 }, scene.palette.center);
}
function drawTriangleCenter(scene, beat) {
  const top = { x: 0, y: 3.4 + beat * 0.08, z: 0 }; const left = { x: -3.6, y: -2.5, z: -1.2 }; const right = { x: 3.6, y: -2.5, z: 1.2 };
  polygon([top, right, left], `${scene.palette.center}12`, `${scene.palette.center}cc`, 0.96, 1.3);
  dot(top, 14, scene.palette.detail, 28, 1); dot(left, 12, scene.palette.map, 24, 0.9); dot(right, 12, scene.palette.plane, 24, 0.9);
  label(scene.centerLabel, { x: 0, y: 4.3, z: 0 }, scene.palette.center);
}
function drawBusCenter(scene, phase) {
  const labels = ["A", "B", "C", "D", "E", "F", "G"];
  labels.forEach((axis, index) => {
    const x = -4.2 + index * 1.4; const flicker = Math.sin(phase * 2 + index * 0.6) * 0.25;
    line({ x, y: -3.2, z: 0 }, { x, y: 3.2, z: 0 }, scene.palette.center, axis === "D" ? 2 : 1.1, 0.75 + index * 0.02);
    dot({ x, y: flicker, z: 0 }, axis === "D" ? 16 : 8, axis === "D" ? scene.palette.detail : scene.palette.center, axis === "D" ? 30 : 16, 0.92);
    label(axis, { x, y: 4.0, z: 0 }, scene.palette.center);
  });
  label(scene.centerLabel, { x: 0, y: 5.0, z: 0 }, scene.palette.center);
}
function drawDetail(scene, phase) {
  const p = { x: 4.25 + Math.cos(phase) * 0.45, y: 1.8 + (state.mode === "drift" ? Math.sin(phase * 1.8) * 0.45 : 0), z: 2.8 + Math.sin(phase) * 0.45 };
  const screen = project(p); const width = 120 + screen.scale * 0.9; const height = 86 + screen.scale * 0.55;
  ctx.save(); ctx.translate(screen.x - width / 2, screen.y - height / 2); ctx.fillStyle = "rgba(7, 11, 18, 0.86)"; ctx.strokeStyle = `${scene.palette.detail}aa`; ctx.lineWidth = 1.2; ctx.shadowBlur = 30; ctx.shadowColor = scene.palette.detail;
  ctx.beginPath(); ctx.roundRect(0, 0, width, height, 14); ctx.fill(); ctx.stroke(); ctx.shadowBlur = 0; ctx.strokeStyle = `${scene.palette.detail}55`;
  for (let i = 0; i < 8; i += 1) { const x = 18 + i * ((width - 36) / 7); ctx.beginPath(); ctx.moveTo(x, 16); ctx.lineTo(x, height - 16); ctx.stroke(); }
  for (let i = 0; i < 6; i += 1) { const y = 16 + i * ((height - 32) / 5); ctx.beginPath(); ctx.moveTo(18, y); ctx.lineTo(width - 18, y); ctx.stroke(); }
  ctx.fillStyle = scene.palette.detail; ctx.font = "600 11px Segoe UI, sans-serif"; ctx.fillText(scene.detailLabel, 16, height - 12); ctx.restore();
  line({ x: 0, y: 0, z: 0 }, p, `${scene.palette.detail}99`, 1.2, 0.75);
}
function drawCenter(scene, beat, phase) {
  switch (scene.centerType) {
    case "tower": drawTowerCenter(scene, beat); break;
    case "portal": drawPortalCenter(scene, beat); break;
    case "cube-grid": drawCubeGridCenter(scene, beat); break;
    case "triangle": drawTriangleCenter(scene, beat); break;
    case "bus": drawBusCenter(scene, phase); break;
    default: drawStackCenter(scene, beat); break;
  }
}
function drawAxis() {
  line({ x: -9, y: 0, z: 0 }, { x: 9, y: 0, z: 0 }, "rgba(120, 152, 214, 0.3)", 1, 0.45);
  line({ x: 0, y: -7, z: 0 }, { x: 0, y: 7, z: 0 }, "rgba(120, 152, 214, 0.22)", 1, 0.25);
}
function updateInfo(scene) {
  codeEl.textContent = scene.code; titleEl.textContent = scene.title; statementEl.textContent = scene.statement;
  centerLabelEl.textContent = scene.centerLabel; detailLabelEl.textContent = scene.detailLabel; mapLabelEl.textContent = scene.mapLabel; excerptEl.textContent = scene.excerpt;
  planesEl.innerHTML = scene.planes.map((plane) => `\n        <article class="plane-chip">\n          <strong>${plane.name}</strong>\n          <span>${plane.note}</span>\n        </article>\n      `).join("");
  [...matrixRail.querySelectorAll(".matrix-button")].forEach((button, index) => button.classList.toggle("active", index === state.activeScene));
}
function buildRail() {
  matrixRail.innerHTML = matrixScenes.map((scene, index) => `\n        <button class="matrix-button${index === 0 ? " active" : ""}" data-scene="${index}">\n          <strong>${scene.code}</strong>\n          <span>${scene.title}</span>\n        </button>\n      `).join("");
  matrixRail.addEventListener("click", (event) => {
    const target = event.target.closest("[data-scene]"); if (!target) return;
    state.activeScene = Number(target.dataset.scene); state.lastSwitch = state.time; updateInfo(matrixScenes[state.activeScene]);
  });
}
function advanceScene() { state.activeScene = (state.activeScene + 1) % matrixScenes.length; updateInfo(matrixScenes[state.activeScene]); }
function frame(ms) {
  state.time = ms * 0.001; const scene = matrixScenes[state.activeScene]; const beat = (Math.sin(state.time * 2) + 1) / 2;
  const phase = state.mode === "pulse" ? state.time * 0.78 : state.mode === "drift" ? state.time * 0.42 : state.time * 0.58;
  if (state.autoplay && state.time - state.lastSwitch > 7.5) { advanceScene(); state.lastSwitch = state.time; }
  backdrop(scene); drawAxis(); drawPlanes(scene, phase); drawMap(scene, phase); drawCenter(scene, beat, phase); drawDetail(scene, phase + 0.35);
  requestAnimationFrame(frame);
}
canvas.addEventListener("pointerdown", (event) => { state.dragging = true; state.pointerX = event.clientX; state.pointerY = event.clientY; canvas.setPointerCapture(event.pointerId); });
canvas.addEventListener("pointermove", (event) => {
  if (!state.dragging) return;
  const dx = event.clientX - state.pointerX; const dy = event.clientY - state.pointerY; state.pointerX = event.clientX; state.pointerY = event.clientY;
  state.yaw += dx * 0.0048; state.pitch = Math.max(-1.05, Math.min(0.32, state.pitch + dy * 0.0038));
});
canvas.addEventListener("pointerup", () => { state.dragging = false; });
canvas.addEventListener("pointerleave", () => { state.dragging = false; });
autoplayButton.addEventListener("click", () => {
  state.autoplay = !state.autoplay; autoplayButton.setAttribute("aria-pressed", String(state.autoplay)); autoplayButton.textContent = state.autoplay ? "Autoplay on" : "Autoplay off"; state.lastSwitch = state.time;
});
modeButtons.forEach((button) => {
  button.addEventListener("click", () => { modeButtons.forEach((item) => item.classList.remove("active")); button.classList.add("active"); state.mode = button.dataset.mode; });
});
window.addEventListener("resize", resize);
resize(); buildRail(); updateInfo(matrixScenes[0]); requestAnimationFrame(frame);
