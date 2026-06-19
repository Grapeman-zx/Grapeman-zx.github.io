const likeButtons = [
  {
    button: document.querySelector("#support-like-button"),
    count: document.querySelector("#support-like-count"),
    countKey: "grapeman_support_like_count",
    likedKey: "grapeman_support_has_liked",
  },
];

function readCount(key) {
  return Number.parseInt(localStorage.getItem(key) || "0", 10);
}

function renderLike(item) {
  if (!item.button || !item.count) {
    return;
  }

  const count = readCount(item.countKey);
  const liked = localStorage.getItem(item.likedKey) === "true";
  item.count.textContent = String(count);
  item.button.classList.toggle("is-liked", liked);
  item.button.setAttribute("aria-pressed", String(liked));
}

function toggleLike(item) {
  const count = readCount(item.countKey);
  const liked = localStorage.getItem(item.likedKey) === "true";
  const nextLiked = !liked;
  const nextCount = Math.max(0, count + (nextLiked ? 1 : -1));

  localStorage.setItem(item.countKey, String(nextCount));
  localStorage.setItem(item.likedKey, String(nextLiked));
  renderLike(item);
}

likeButtons.forEach((item) => {
  renderLike(item);
  item.button?.addEventListener("click", () => toggleLike(item));
});

const mailModal = document.querySelector("#mail-modal");
const mailTriggers = document.querySelectorAll(".mail-trigger");
const mailCloseButtons = document.querySelectorAll("[data-mail-close]");

function openMailModal() {
  if (!mailModal) {
    return;
  }

  mailModal.hidden = false;
  document.body.classList.add("modal-open");
  mailModal.querySelector("[data-mail-close]")?.focus();
}

function closeMailModal() {
  if (!mailModal) {
    return;
  }

  mailModal.hidden = true;
  document.body.classList.remove("modal-open");
}

mailTriggers.forEach((trigger) => {
  trigger.addEventListener("click", openMailModal);
});

mailCloseButtons.forEach((button) => {
  button.addEventListener("click", closeMailModal);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeMailModal();
  }
});

const siteRibbon = document.querySelector(".site-ribbon");
const hero = document.querySelector(".hero");

function layoutSiteRibbon() {
  if (!siteRibbon || !hero) {
    return;
  }

  const heroRect = hero.getBoundingClientRect();
  const mainRect = document.querySelector("main")?.getBoundingClientRect();
  const ribbonTop = Math.max(0, heroRect.bottom + window.scrollY - (mainRect?.top + window.scrollY || 0) - 0.5);
  const ribbonHeight = Math.max(1, (mainRect?.height || document.documentElement.scrollHeight) - ribbonTop);
  const supportRect = document.querySelector("#support")?.getBoundingClientRect();
  const supportBottom = supportRect ? supportRect.bottom + window.scrollY - (mainRect?.top + window.scrollY || 0) - ribbonTop : ribbonHeight * 0.78;
  const heroWidth = heroRect.width;
  const heroHeight = heroRect.height;
  const pageLeft = Math.max(16, (window.innerWidth - heroWidth) / 2);
  const angle = 128 * Math.PI / 180;
  const ux = Math.sin(angle);
  const uy = -Math.cos(angle);
  const gradientLength = heroWidth * Math.abs(ux) + heroHeight * Math.abs(uy);
  const qMin = -gradientLength / 2;
  const bottomProjection = (heroHeight / 2) * uy;
  const stripeWidth = (0.05 * gradientLength) / ux;
  const stripeGap = (0.02 * gradientLength) / ux;
  const pitch = stripeWidth + stripeGap;
  const baseStops = [53.5, 60.5, 67.5, 74.5, 81.5];
  const startCenters = baseStops.map((stop) => {
    const stopProjection = (stop / 100) * gradientLength + qMin;
    return ((stopProjection - bottomProjection) / ux) + heroWidth / 2;
  });
  const turnStepY = pitch;
  const bottomBoundFirstExitY = ribbonHeight + stripeWidth * 1.2;
  const preferredFirstExitY = supportBottom + stripeWidth * 3.4;
  const firstExitY = Math.max(preferredFirstExitY, bottomBoundFirstExitY);
  const turnSlope = Math.abs(Math.cos(angle) / Math.sin(angle));
  const turnStartY = firstExitY - stripeWidth * 1.5;
  const exitLeft = -heroWidth * 0.34;

  siteRibbon.style.top = `${ribbonTop}px`;
  siteRibbon.style.left = `${pageLeft}px`;
  siteRibbon.style.width = `${heroWidth}px`;
  siteRibbon.style.height = `${ribbonHeight}px`;
  siteRibbon.style.setProperty("--ribbon-stroke", `${stripeWidth}px`);
  siteRibbon.setAttribute("viewBox", `0 0 ${heroWidth} ${ribbonHeight}`);

  siteRibbon.querySelectorAll("polyline").forEach((line, index) => {
    const x = startCenters[index];
    const exitY = firstExitY + index * turnStepY;
    const turnRise = exitY - turnStartY;
    const elbowX = x - turnSlope * turnRise;
    line.setAttribute("points", `${x},0 ${x},${turnStartY} ${elbowX},${exitY} ${exitLeft},${exitY}`);
  });
}

layoutSiteRibbon();
window.addEventListener("resize", layoutSiteRibbon);
window.addEventListener("load", layoutSiteRibbon);
