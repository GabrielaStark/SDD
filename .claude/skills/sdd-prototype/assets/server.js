'use strict';

// Optional preview server. Set credentials through the environment; use TLS remotely.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const user = process.env.AUTH_USER;
const password = process.env.AUTH_PASS;
if (!user || !password || /[:\r\n]/.test(user) || /[\r\n]/.test(password)) {
  console.error('Set valid AUTH_USER and AUTH_PASS; no default credentials are provided.');
  process.exit(1);
}
let publicRoot;
try {
  publicRoot = fs.realpathSync(path.join(__dirname, 'public'));
  if (!fs.statSync(publicRoot).isDirectory()) throw new Error('Not a directory');
} catch {
  console.error('Create public/ beside server.js before starting the preview.');
  process.exit(1);
}
const expected = crypto.createHash('sha256').update(`${user}:${password}`).digest();
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.gif': 'image/gif', '.ico': 'image/x-icon',
  '.woff': 'font/woff', '.woff2': 'font/woff2',
};

const server = http.createServer((req, res) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Cache-Control', 'no-store');
  const auth = /^Basic ([A-Za-z0-9+/]+={0,2})$/i.exec(req.headers.authorization || '');
  const actual = auth && crypto.createHash('sha256')
    .update(Buffer.from(auth[1], 'base64')).digest();
  if (!actual || !crypto.timingSafeEqual(actual, expected)) {
    res.writeHead(401, { 'WWW-Authenticate': 'Basic realm="Prototype", charset="UTF-8"' });
    return res.end('Authentication required');
  }
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.writeHead(405, { Allow: 'GET, HEAD' });
    return res.end('Method not allowed');
  }
  let pathname;
  try {
    pathname = decodeURIComponent(req.url.split('?')[0]);
    if (!pathname.startsWith('/') || pathname.includes('\0') || pathname.includes('\\') ||
        pathname.split('/').some(segment => segment.startsWith('.'))) throw new Error('Invalid path');
  } catch {
    res.writeHead(400);
    return res.end('Invalid path');
  }
  if (pathname.endsWith('/')) pathname += 'index.html';
  try {
    const file = fs.realpathSync(path.resolve(publicRoot, '.' + pathname));
    const relative = path.relative(publicRoot, file);
    if (relative.startsWith('..' + path.sep) || relative === '..' || path.isAbsolute(relative)) {
      throw new Error('Outside public root');
    }
    if (relative.split(path.sep).some(segment => segment.startsWith('.'))) throw new Error('Hidden file');
    const contentType = types[path.extname(file).toLowerCase()];
    const stat = fs.statSync(file);
    if (!stat.isFile() || !contentType) throw new Error('Not public content');
    res.writeHead(200, { 'Content-Type': contentType, 'Content-Length': stat.size });
    if (req.method === 'HEAD') return res.end();
    fs.createReadStream(file).on('error', () => res.destroy()).pipe(res);
  } catch {
    res.writeHead(404);
    res.end('Not found');
  }
});
server.on('error', error => {
  console.error(`Preview server failed: ${error.code || 'UNKNOWN'}`);
  process.exitCode = 1;
});
server.listen(Number(process.env.PORT || 3000), process.env.HOST || '127.0.0.1', () => {
  console.log(`Prototype preview listening on port ${server.address().port}`);
});
