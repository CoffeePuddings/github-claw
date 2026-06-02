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
