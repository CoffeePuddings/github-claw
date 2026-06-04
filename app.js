// === Chart Data ===
const growthData = [124, 139, 153, 171, 198, 216, 238, 267, 301, 338, 390, 452];
const svgWidth = 620;
const svgHeight = 220;
const padding = 18;
const min = Math.min(...growthData);
const max = Math.max(...growthData);

const points = growthData
  .map((value, index) => {
    const x =
      padding + (index * (svgWidth - padding * 2)) / (growthData.length - 1);
    const y =
      svgHeight -
      padding -
      ((value - min) / Math.max(max - min, 1)) * (svgHeight - padding * 2);
    return `${x.toFixed(2)},${y.toFixed(2)}`;
  })
  .join(" ");

const trendLine = document.getElementById("trendLine");
const trendValue = document.getElementById("trendValue");
const weekRow = document.getElementById("weekRow");
const starTotal = document.getElementById("starTotal");
const weeklyAvg = document.getElementById("weeklyAvg");
const growthSlope = document.getElementById("growthSlope");

if (trendLine) trendLine.setAttribute("points", points);

if (trendValue) {
  const first = growthData[0];
  const last = growthData[growthData.length - 1];
  const ratio = (((last - first) / first) * 100).toFixed(1);
  trendValue.textContent = `+${ratio}%`;
}

if (weekRow) {
  growthData.forEach((_, i) => {
    const span = document.createElement("span");
    span.textContent = `W${i + 1}`;
    weekRow.appendChild(span);
  });
}

const first = growthData[0];
const last = growthData[growthData.length - 1];
const avgIncrease = ((last - first) / (growthData.length - 1)).toFixed(1);
const slope = (growthData[growthData.length - 1] - growthData[growthData.length - 4]) / 3;

if (starTotal) starTotal.textContent = `${last}+`;
if (weeklyAvg) weeklyAvg.textContent = `+${avgIncrease}`;
if (growthSlope) growthSlope.textContent = slope.toFixed(1);

// === Scroll Progress Bar ===
const scrollProgress = document.querySelector(".scroll-progress");
function updateScrollProgress() {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  if (scrollProgress) scrollProgress.style.width = progress + "%";
}

// === Scroll-to-Top Button ===
const scrollTopBtn = document.getElementById("scrollTopBtn");
function updateScrollTopBtn() {
  if (!scrollTopBtn) return;
  if (window.scrollY > 400) {
    scrollTopBtn.classList.add("visible");
  } else {
    scrollTopBtn.classList.remove("visible");
  }
}

if (scrollTopBtn) {
  scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

// === Scroll-driven Entrance Animations ===
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function initFadeInObserver() {
  if (prefersReducedMotion) {
    document.querySelectorAll(".fade-in").forEach((el) => {
      el.classList.add("visible");
    });
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
  );
  document.querySelectorAll(".fade-in").forEach((el) => observer.observe(el));
}

// Add fade-in class to sections
document.querySelectorAll(".section:not(.hero)").forEach((section) => {
  section.classList.add("fade-in");
});

// Scroll event (throttled via rAF)
let ticking = false;
window.addEventListener("scroll", () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      updateScrollProgress();
      updateScrollTopBtn();
      ticking = false;
    });
    ticking = true;
  }
});

// Initialize
updateScrollProgress();
updateScrollTopBtn();
initFadeInObserver();
