/* Tests for assets/js/repo-tree.js — run with:  node --test scripts/ */

const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');

const RepoTree = require(path.join(__dirname, '..', 'assets', 'js', 'repo-tree.js'));

const OPTS = { owner: 'swissmicros', repo: 'swissmicros-factorydefaults', branch: 'main' };

/* A slice of the real recursive-tree response shape. */
const TREE = [
  { path: 'README.md', type: 'blob', size: 2395 },
  { path: 'models.json', type: 'blob', size: 20778 },
  { path: 'Pioneer_Models', type: 'tree' },
  { path: 'Pioneer_Models/DM42_qspi_3.x.bin', type: 'blob', size: 1370864 },
  { path: 'Pioneer_Models/DMCP_HISTORY.md', type: 'blob', size: 3980 },
  { path: 'Pioneer_Models/DM32', type: 'tree' },
  { path: 'Pioneer_Models/DM32/HISTORY.md', type: 'blob', size: 6580 },
  { path: 'Pioneer_Models/DM32/programs', type: 'tree' },
  { path: 'Pioneer_Models/DM32/programs/demo.raw', type: 'blob', size: 12 },
  { path: 'Voyager_Models', type: 'tree' },
  { path: 'Voyager_Models/DM10_34.hex', type: 'blob', size: 98790 },
];

function names(entries) { return entries.map(e => e.name); }

test('root listing returns only top-level entries', () => {
  assert.deepStrictEqual(
    names(RepoTree.listDir(TREE, '', OPTS)).sort(),
    ['Pioneer_Models', 'README.md', 'Voyager_Models', 'models.json']);
});

test('nested listing returns only direct children', () => {
  assert.deepStrictEqual(
    names(RepoTree.listDir(TREE, 'Pioneer_Models', OPTS)).sort(),
    ['DM32', 'DM42_qspi_3.x.bin', 'DMCP_HISTORY.md']);
});

test('grandchildren do not leak into a shallow listing', () => {
  const got = names(RepoTree.listDir(TREE, 'Pioneer_Models', OPTS));
  assert.ok(!got.includes('HISTORY.md'), 'DM32/HISTORY.md leaked into Pioneer_Models');
  assert.ok(!got.includes('demo.raw'));
});

test('a tree entry becomes a dir with no size', () => {
  const [dm32] = RepoTree.listDir(TREE, 'Pioneer_Models', OPTS).filter(e => e.name === 'DM32');
  assert.strictEqual(dm32.type, 'dir');
  assert.strictEqual(dm32.path, 'Pioneer_Models/DM32');
  assert.strictEqual(dm32.size, undefined);
});

test('a blob entry becomes a file carrying its size', () => {
  const [h] = RepoTree.listDir(TREE, 'Pioneer_Models/DM32', OPTS).filter(e => e.name === 'HISTORY.md');
  assert.strictEqual(h.type, 'file');
  assert.strictEqual(h.size, 6580);
  assert.strictEqual(h.path, 'Pioneer_Models/DM32/HISTORY.md');
});

test('files get a raw download_url on the right branch', () => {
  const [h] = RepoTree.listDir(TREE, 'Pioneer_Models/DM32', OPTS).filter(e => e.name === 'HISTORY.md');
  assert.strictEqual(
    h.download_url,
    'https://raw.githubusercontent.com/swissmicros/swissmicros-factorydefaults/main/Pioneer_Models/DM32/HISTORY.md');
});

test('directories get no download_url', () => {
  const [dm32] = RepoTree.listDir(TREE, 'Pioneer_Models', OPTS).filter(e => e.name === 'DM32');
  assert.strictEqual(dm32.download_url, undefined);
});

test('path segments are url-encoded in download_url', () => {
  const tree = [{ path: 'Pioneer_Models/DM 42/a b&c.txt', type: 'blob', size: 1 }];
  const [f] = RepoTree.listDir(tree, 'Pioneer_Models/DM 42', OPTS);
  assert.strictEqual(
    f.download_url,
    'https://raw.githubusercontent.com/swissmicros/swissmicros-factorydefaults/main/Pioneer_Models/DM%2042/a%20b%26c.txt');
});

test('slashes in the path are not encoded away', () => {
  const [f] = RepoTree.listDir(TREE, 'Pioneer_Models/DM32', OPTS);
  assert.ok(f.download_url.includes('/main/Pioneer_Models/DM32/'), f.download_url);
});

test('an unknown directory lists nothing', () => {
  assert.deepStrictEqual(RepoTree.listDir(TREE, 'Nope/Missing', OPTS), []);
});

test('a trailing slash on the path is tolerated', () => {
  assert.deepStrictEqual(
    names(RepoTree.listDir(TREE, 'Pioneer_Models/', OPTS)).sort(),
    ['DM32', 'DM42_qspi_3.x.bin', 'DMCP_HISTORY.md']);
});

test('source order is preserved', () => {
  assert.deepStrictEqual(
    names(RepoTree.listDir(TREE, 'Pioneer_Models', OPTS)),
    ['DM42_qspi_3.x.bin', 'DMCP_HISTORY.md', 'DM32']);
});

test('a path that is a prefix of a sibling does not capture it', () => {
  const tree = [
    { path: 'DM4', type: 'tree' },
    { path: 'DM4/a.txt', type: 'blob', size: 1 },
    { path: 'DM42', type: 'tree' },
    { path: 'DM42/b.txt', type: 'blob', size: 1 },
  ];
  assert.deepStrictEqual(names(RepoTree.listDir(tree, 'DM4', OPTS)), ['a.txt']);
  assert.deepStrictEqual(names(RepoTree.listDir(tree, 'DM42', OPTS)), ['b.txt']);
});

test('entries missing a size are tolerated', () => {
  const tree = [{ path: 'x.bin', type: 'blob' }];
  const [f] = RepoTree.listDir(tree, '', OPTS);
  assert.strictEqual(f.type, 'file');
  assert.strictEqual(f.size, undefined);
});

test('commit entries (submodules) are skipped', () => {
  const tree = [
    { path: 'sub', type: 'commit' },
    { path: 'keep.txt', type: 'blob', size: 3 },
  ];
  assert.deepStrictEqual(names(RepoTree.listDir(tree, '', OPTS)), ['keep.txt']);
});

/* ── error messages ──────────────────────────────────────────────── */

function hdrs(obj) { return { get: k => (k.toLowerCase() in obj ? obj[k.toLowerCase()] : null) }; }

const NOW = 1757849000; // fixed clock, seconds

test('exhausted rate limit is named, not shown as a bare 403', () => {
  const msg = RepoTree.describeHttpError(403,
    hdrs({ 'x-ratelimit-remaining': '0', 'x-ratelimit-limit': '60',
           'x-ratelimit-reset': String(NOW + 22 * 60) }), NOW * 1000);
  assert.match(msg, /rate limit/i);
  assert.match(msg, /60 requests/);
  assert.match(msg, /22 minutes/);
  assert.doesNotMatch(msg, /HTTP 403/);
});

test('rate limit message rounds a sub-minute reset sensibly', () => {
  const msg = RepoTree.describeHttpError(403,
    hdrs({ 'x-ratelimit-remaining': '0', 'x-ratelimit-reset': String(NOW + 20) }), NOW * 1000);
  assert.match(msg, /less than a minute/i);
});

test('rate limit message uses singular for one minute', () => {
  const msg = RepoTree.describeHttpError(403,
    hdrs({ 'x-ratelimit-remaining': '0', 'x-ratelimit-reset': String(NOW + 70) }), NOW * 1000);
  assert.match(msg, /\b1 minute\b/);
  assert.doesNotMatch(msg, /1 minutes/);
});

test('a 403 that is not a rate limit stays a plain forbidden', () => {
  const msg = RepoTree.describeHttpError(403, hdrs({}), NOW * 1000);
  assert.doesNotMatch(msg, /rate limit/i);
  assert.match(msg, /403/);
});

test('a rate-limited 403 with no reset header still explains itself', () => {
  const msg = RepoTree.describeHttpError(403,
    hdrs({ 'x-ratelimit-remaining': '0' }), NOW * 1000);
  assert.match(msg, /rate limit/i);
  assert.doesNotMatch(msg, /NaN/);
});

test('404 reads as not found', () => {
  assert.match(RepoTree.describeHttpError(404, hdrs({}), NOW * 1000), /not found/i);
});

test('other statuses fall back to the status code', () => {
  assert.match(RepoTree.describeHttpError(500, hdrs({}), NOW * 1000), /500/);
});

test('missing headers object does not throw', () => {
  assert.doesNotThrow(() => RepoTree.describeHttpError(403, null, NOW * 1000));
});

/* ── fromFileIndex: tree.json carries files only, dirs are derived ── */

function paths(entries) { return entries.map(e => e.path + ':' + e.type); }

test('a nested file creates every ancestor directory', () => {
  assert.deepStrictEqual(
    paths(RepoTree.fromFileIndex([{ path: 'a/b/c.txt', size: 1 }])),
    ['a:tree', 'a/b:tree', 'a/b/c.txt:blob']);
});

test('sibling files do not duplicate their shared directory', () => {
  assert.deepStrictEqual(
    paths(RepoTree.fromFileIndex([
      { path: 'a/one.txt', size: 1 },
      { path: 'a/two.txt', size: 2 },
    ])),
    ['a:tree', 'a/one.txt:blob', 'a/two.txt:blob']);
});

test('a root-level file creates no directories', () => {
  assert.deepStrictEqual(
    paths(RepoTree.fromFileIndex([{ path: 'README.md', size: 9 }])),
    ['README.md:blob']);
});

test('blob sizes survive, directories have none', () => {
  const out = RepoTree.fromFileIndex([{ path: 'a/c.txt', size: 42 }]);
  assert.strictEqual(out.find(e => e.path === 'a/c.txt').size, 42);
  assert.strictEqual(out.find(e => e.path === 'a').size, undefined);
});

test('output is sorted by path, so the artifact order cannot leak through', () => {
  const out = RepoTree.fromFileIndex([
    { path: 'z.txt', size: 1 },
    { path: 'a/b.txt', size: 1 },
    { path: 'README.md', size: 1 },
  ]);
  assert.deepStrictEqual(out.map(e => e.path), ['README.md', 'a', 'a/b.txt', 'z.txt']);
});

test('empty input yields an empty tree', () => {
  assert.deepStrictEqual(RepoTree.fromFileIndex([]), []);
});

test('the derived tree feeds listDir unchanged', () => {
  const tree = RepoTree.fromFileIndex([
    { path: 'Pioneer_Models/DM32/HISTORY.md', size: 6580 },
    { path: 'Pioneer_Models/DMCP_HISTORY.md', size: 3980 },
    { path: 'README.md', size: 2395 },
  ]);
  assert.deepStrictEqual(
    RepoTree.listDir(tree, '', OPTS).map(e => e.name).sort(),
    ['Pioneer_Models', 'README.md']);
  const dm32 = RepoTree.listDir(tree, 'Pioneer_Models', OPTS).find(e => e.name === 'DM32');
  assert.strictEqual(dm32.type, 'dir');
  const hist = RepoTree.listDir(tree, 'Pioneer_Models/DM32', OPTS)[0];
  assert.strictEqual(hist.size, 6580);
  assert.strictEqual(hist.download_url,
    'https://raw.githubusercontent.com/swissmicros/swissmicros-factorydefaults/main/Pioneer_Models/DM32/HISTORY.md');
});

test('a directory that is also a path prefix of a file name is distinct', () => {
  const tree = RepoTree.fromFileIndex([
    { path: 'DM4/a.txt', size: 1 },
    { path: 'DM42.txt', size: 1 },
  ]);
  assert.deepStrictEqual(paths(tree), ['DM4:tree', 'DM4/a.txt:blob', 'DM42.txt:blob']);
  assert.deepStrictEqual(RepoTree.listDir(tree, '', OPTS).map(e => e.name), ['DM4', 'DM42.txt']);
});

test('malformed artifact entries are skipped, not rendered as blanks', () => {
  const out = RepoTree.fromFileIndex([
    { path: '', size: 1 },
    { path: '/', size: 1 },
    { size: 1 },
    { path: 'good.txt', size: 2 },
  ]);
  assert.deepStrictEqual(out.map(e => e.path), ['good.txt']);
});

test('leading and trailing slashes in an artifact path are normalised', () => {
  assert.deepStrictEqual(
    RepoTree.fromFileIndex([{ path: '/a/b.txt', size: 1 }]).map(e => e.path),
    ['a', 'a/b.txt']);
});
