/* Turn one recursive git-trees response into per-directory listings.
 *
 * The directory browser used to call the GitHub contents API once per folder.
 * That API allows 60 requests an hour to anonymous callers, so a few minutes of
 * clicking around exhausted it and every folder then failed with a bare 403.
 * Fetching the whole tree once and slicing it here costs a single request no
 * matter how much browsing follows.
 *
 * Loaded as a plain script in the browser (window.RepoTree) and required from
 * node by the tests. No dependencies either way.
 */
(function (root, factory) {
    if (typeof module === 'object' && module.exports) module.exports = factory();
    else root.RepoTree = factory();
}(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    function rawUrl(opts, path) {
        var encoded = path.split('/').map(encodeURIComponent).join('/');
        return 'https://raw.githubusercontent.com/' + opts.owner + '/' + opts.repo +
               '/' + opts.branch + '/' + encoded;
    }

    /* Direct children of `dir`, shaped like the contents API entries the table
     * already renders: {name, path, type: 'dir'|'file', size, download_url}. */
    function listDir(tree, dir, opts) {
        var base = String(dir == null ? '' : dir).replace(/^\/+|\/+$/g, '');
        var prefix = base ? base + '/' : '';
        var out = [];

        for (var i = 0; i < tree.length; i++) {
            var entry = tree[i];
            if (entry.type !== 'blob' && entry.type !== 'tree') continue;  // submodules
            if (entry.path.slice(0, prefix.length) !== prefix) continue;

            var rest = entry.path.slice(prefix.length);
            if (!rest || rest.indexOf('/') !== -1) continue;               // not a direct child

            var isDir = entry.type === 'tree';
            out.push({
                name: rest,
                path: entry.path,
                type: isDir ? 'dir' : 'file',
                size: isDir ? undefined : entry.size,
                download_url: isDir ? undefined : rawUrl(opts, entry.path)
            });
        }
        return out;
    }

    /* Every file anywhere below `dir`, for zipping a folder: {path, relPath,
     * size, download_url}, where relPath is relative to `dir`. */
    function filesUnder(tree, dir, opts) {
        var base = String(dir == null ? '' : dir).replace(/^\/+|\/+$/g, '');
        var prefix = base ? base + '/' : '';
        var out = [];

        for (var i = 0; i < tree.length; i++) {
            var entry = tree[i];
            if (entry.type !== 'blob') continue;
            if (entry.path.slice(0, prefix.length) !== prefix) continue;
            out.push({
                path: entry.path,
                relPath: entry.path.slice(prefix.length),
                size: entry.size,
                download_url: rawUrl(opts, entry.path)
            });
        }
        return out;
    }

    /* tree.json lists tracked files only — git has no standalone directory
     * objects — so derive the directories their paths imply. Sorted by path so
     * the artifact's own ordering cannot affect what the page renders. */
    function fromFileIndex(files) {
        var dirs = {};
        var out = [];

        for (var i = 0; i < files.length; i++) {
            var path = String(files[i].path || '').replace(/^\/+|\/+$/g, '');
            if (!path) continue;

            var parts = path.split('/');
            for (var j = 0; j < parts.length - 1; j++) {
                var dir = parts.slice(0, j + 1).join('/');
                if (!dirs[dir]) {
                    dirs[dir] = true;
                    out.push({ path: dir, type: 'tree' });
                }
            }
            out.push({ path: path, type: 'blob', size: files[i].size });
        }

        out.sort(function (a, b) { return a.path < b.path ? -1 : a.path > b.path ? 1 : 0; });
        return out;
    }

    /* Every folder from the root ('') down to and including `path` — the
     * nodes the folder tree must expand for `path` to be visible. */
    function ancestorPaths(path) {
        var parts = String(path == null ? '' : path).replace(/^\/+|\/+$/g, '').split('/');
        var out = [''];
        for (var i = 0; i < parts.length; i++) {
            if (parts[i]) out.push(parts.slice(0, i + 1).join('/'));
        }
        return out;
    }

    /* Where a link inside a repository file points: {path, hash} relative to
     * the repository root, or null for links that are not into the repository
     * (other sites, mailto:, in-page #anchors, paths climbing above the root). */
    function resolveLink(fromPath, href) {
        href = String(href == null ? '' : href).trim();
        if (!href || href.charAt(0) === '#' || href.slice(0, 2) === '//' ||
            /^[a-z][a-z0-9+.-]*:/i.test(href)) return null;

        var hashAt = href.search(/[?#]/);
        var hash = hashAt === -1 ? '' : href.slice(hashAt).replace(/^\?[^#]*/, '');
        var target = hashAt === -1 ? href : href.slice(0, hashAt);
        try { target = decodeURIComponent(target); } catch (e) { /* keep it as written */ }

        var parts = target.charAt(0) === '/' ? []
                  : String(fromPath || '').split('/').slice(0, -1);
        var segs = target.split('/');
        for (var i = 0; i < segs.length; i++) {
            if (segs[i] === '' || segs[i] === '.') continue;
            if (segs[i] === '..') {
                if (!parts.length) return null;
                parts.pop();
            } else {
                parts.push(segs[i]);
            }
        }
        return parts.length ? { path: parts.join('/'), hash: hash } : null;
    }

    /* A readable reason for a failed request. The rate-limit case is the one
     * people actually hit, so it says so plainly and when it clears. */
    function describeHttpError(status, headers, nowMs) {
        var get = function (name) {
            try { return headers && headers.get ? headers.get(name) : null; }
            catch (e) { return null; }
        };

        if (status === 403 || status === 429) {
            var remaining = get('x-ratelimit-remaining');
            if (remaining === '0') {
                var limit = get('x-ratelimit-limit') || '60';
                var msg = "GitHub's API rate limit is used up (" + limit +
                          ' requests per hour for anonymous browsing).';
                var reset = parseInt(get('x-ratelimit-reset'), 10);
                if (isFinite(reset)) {
                    var secs = reset - Math.floor((nowMs || Date.now()) / 1000);
                    if (secs <= 60) {
                        msg += ' It resets in less than a minute.';
                    } else {
                        var mins = Math.round(secs / 60);
                        msg += ' It resets in ' + mins + (mins === 1 ? ' minute.' : ' minutes.');
                    }
                } else {
                    msg += ' It resets within the hour.';
                }
                return msg + ' Nothing is wrong with the repository — the file list will'
                           + ' come back on its own.';
            }
        }
        if (status === 404) return 'Not found (HTTP 404).';
        return 'HTTP ' + status + '.';
    }

    return { listDir: listDir, rawUrl: rawUrl, fromFileIndex: fromFileIndex,
             describeHttpError: describeHttpError, ancestorPaths: ancestorPaths,
             filesUnder: filesUnder, resolveLink: resolveLink };
}));
