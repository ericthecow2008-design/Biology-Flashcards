// Find a Chromium that Playwright can drive, without downloading one if any is already on disk.
// Order: $CHROMIUM_PATH, Playwright's own default, then common install locations.
// Returns a path, or undefined to let Playwright use its default (which may need `npx playwright install chromium`).
const fs = require('fs');
const path = require('path');
const os = require('os');

module.exports = function findChromium() {
  const cands = [];
  if (process.env.CHROMIUM_PATH) cands.push(process.env.CHROMIUM_PATH);
  try { cands.push(require('playwright').chromium.executablePath()); } catch (e) { /* not installed yet */ }
  const roots = ['/opt/pw-browsers', path.join(os.homedir(), '.cache', 'ms-playwright'), '/ms-playwright'];
  for (const r of roots) {
    let entries = [];
    try { entries = fs.readdirSync(r); } catch (e) { continue; }
    for (const e of entries.filter(x => /^chromium/.test(x)).sort().reverse()) {
      for (const sub of ['chrome-linux64/chrome', 'chrome-linux/chrome', 'chrome-linux64/headless_shell',
                         'chrome-linux/headless_shell', 'chrome-headless-shell-linux64/chrome-headless-shell']) {
        cands.push(path.join(r, e, sub));
      }
    }
  }
  cands.push('/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable');
  for (const c of cands) {
    try { if (c && fs.statSync(c).isFile()) return c; } catch (e) { /* keep looking */ }
  }
  return undefined;
};

if (require.main === module) {
  const p = module.exports();
  console.log(p ? `Chromium: ${p}` : 'No Chromium found: run  npx playwright install chromium');
  process.exit(p ? 0 : 1);
}
