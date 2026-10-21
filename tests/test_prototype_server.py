import base64
import http.client
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / '.claude/skills/sdd-prototype/assets/server.js'


@unittest.skipUnless(shutil.which('node'), 'Node.js required for preview-server smoke checks')
class PrototypeServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        shutil.copy(SERVER, self.directory / 'server.js')
        (self.directory / 'public').mkdir()
        (self.directory / 'public/index.html').write_text('<h1>MOCKUP NO FUNCIONAL</h1>')
        (self.directory / 'public/.hidden.html').write_text('hidden')
        (self.directory / 'private.html').write_text('private context')
        (self.directory / 'public/escape.html').symlink_to(self.directory / 'private.html')
        self.env = {**os.environ, 'AUTH_USER': 'preview-user', 'AUTH_PASS': 'test-only-password', 'PORT': '0', 'HOST': '127.0.0.1'}

    def start(self):
        self.proc = subprocess.Popen(['node', str(self.directory / 'server.js')], env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(self.stop)
        # The readiness line is emitted only after binding; no fixed sleep required.
        import selectors
        with selectors.DefaultSelector() as selector:
            selector.register(self.proc.stdout, selectors.EVENT_READ)
            self.assertTrue(selector.select(5), 'Server did not start within five seconds')
        line = self.proc.stdout.readline()
        self.assertIn('listening on port', line)
        self.port = int(line.split()[-1])

    def stop(self):
        self.proc.terminate()
        try:
            self.proc.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.communicate()

    def request(self, path='/', credentials='preview-user:test-only-password', method='GET'):
        connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=3)
        headers = {} if credentials is None else {'Authorization': 'Basic ' + base64.b64encode(credentials.encode()).decode()}
        connection.request(method, path, headers=headers)
        response = connection.getresponse()
        status, body = response.status, response.read()
        connection.close()
        return status, body

    def test_credentials_required_at_start(self):
        self.env.pop('AUTH_PASS')
        result = subprocess.run(['node', str(self.directory / 'server.js')], env=self.env, capture_output=True, text=True, timeout=5)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('no default credentials', result.stderr)

    def test_auth_public_files_and_private_boundaries(self):
        self.start()
        self.assertEqual(401, self.request(credentials=None)[0])
        self.assertEqual(401, self.request(credentials='wrong:password')[0])
        self.assertEqual(200, self.request()[0])
        self.assertEqual((200, b''), self.request(method='HEAD'))
        self.assertEqual(405, self.request(method='POST')[0])
        for path in ('/private.html', '/server.js', '/validation-log-v1.md', '/escape.html', '/.hidden.html', '/../private.html', '/%2e%2e/private.html', '/%ZZ', '/%00'):
            with self.subTest(path=path):
                status, body = self.request(path)
                self.assertIn(status, (400, 404))
                self.assertNotIn(b'private context', body)


if __name__ == '__main__':
    unittest.main()
