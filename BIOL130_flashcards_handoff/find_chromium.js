// Find a Chromium/Chrome binary for Playwright, so the browser checks work
// without downloading a browser.
//
// Search order:
//   1. the CHROMIUM_PATH environment variable;
//   2. Playwright browsers already on disk ($PLAYWRIGHT_BROWSERS_PATH,
//      /opt/pw-browsers, ~/.cache/ms-playwright);
//   3. common system installs.
// Returns undefined when nothing is found. Playwright then uses its own
// download (`npx playwright install chromium`), which some networks block.
const fs = require('fs');
const os = require('os');
const path = require('path');

module.exports = function findChromium() {
  const candidates = [];
  if (process.env.CHROMIUM_PATH) candidates.push(process.env.CHROMIUM_PATH);
  const roots = [process.env.PLAYWRIGHT_BROWSERS_PATH, '/opt/pw-browsers', path.join(os.homedir(), '.cache', 'ms-playwright')];
  for (const root of roots.filter(Boolean)) {
    let dirs = [];
    try { dirs = fs.readdirSync(root).filter(d => /^chromium-\d+$/.test(d)).sort().reverse(); } catch (e) { /* no such dir */ }
    for (const d of dirs) {
      candidates.push(path.join(root, d, 'chrome-linux', 'chrome'), path.join(root, d, 'chrome-linux64', 'chrome'));
    }
  }
  candidates.push('/usr/bin/chromium', '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/opt/google/chrome/chrome');
  return candidates.find(p => { try { return fs.statSync(p).isFile(); } catch (e) { return false; } });
};
