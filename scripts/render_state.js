// Renders analysis/model-state.svg to a PNG: node scripts/render_state.js $PWD/analysis/model-state.svg $PWD/analysis/model-state.png
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1320, height: 1030 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.argv[2]);
  await p.screenshot({ path: process.argv[3] });
  await b.close();
})();
