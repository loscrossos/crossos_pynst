import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import urllib.error

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pynst

class TestGitFallback(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="pynst_git_fb_test_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_parse_git_file_url(self):
        """Test URL parsing for various GitHub, GitLab, and Bitbucket URLs."""
        # 1. GitHub raw with refs/heads
        url1 = "https://github.com/loscrossos/videoscript/raw/refs/heads/main/videoscript.pynst.txt"
        info1 = pynst.parse_git_file_url(url1)
        self.assertIsNotNone(info1)
        self.assertEqual(info1["host"], "github.com")
        self.assertEqual(info1["owner"], "loscrossos")
        self.assertEqual(info1["repo"], "videoscript")
        self.assertEqual(info1["ref"], "main")
        self.assertEqual(info1["path"], "videoscript.pynst.txt")

        # 2. GitHub raw standard
        url2 = "https://github.com/owner/myrepo/raw/dev/src/pkg/module.py"
        info2 = pynst.parse_git_file_url(url2)
        self.assertIsNotNone(info2)
        self.assertEqual(info2["owner"], "owner")
        self.assertEqual(info2["repo"], "myrepo")
        self.assertEqual(info2["ref"], "dev")
        self.assertEqual(info2["path"], "src/pkg/module.py")

        # 3. raw.githubusercontent.com
        url3 = "https://raw.githubusercontent.com/owner/myrepo/v1.0.0/config.json"
        info3 = pynst.parse_git_file_url(url3)
        self.assertIsNotNone(info3)
        self.assertEqual(info3["host"], "github.com")
        self.assertEqual(info3["ref"], "v1.0.0")
        self.assertEqual(info3["path"], "config.json")

        # 4. GitHub blob link
        url4 = "https://github.com/owner/myrepo/blob/main/docs/README.md"
        info4 = pynst.parse_git_file_url(url4)
        self.assertIsNotNone(info4)
        self.assertEqual(info4["path"], "docs/README.md")

        # 5. GitLab raw
        url5 = "https://gitlab.com/gl_owner/gl_repo/-/raw/main/setup.py"
        info5 = pynst.parse_git_file_url(url5)
        self.assertIsNotNone(info5)
        self.assertEqual(info5["owner"], "gl_owner")
        self.assertEqual(info5["repo"], "gl_repo")
        self.assertEqual(info5["path"], "setup.py")

        # 6. Non-git URL (should return None)
        url6 = "https://huggingface.co/owner/repo/resolve/main/model.safetensors"
        self.assertIsNone(pynst.parse_git_file_url(url6))

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_fetch_file_via_gh_cli(self, mock_subprocess_run, mock_which):
        """Verify fallback uses gh api if available."""
        mock_which.side_effect = lambda cmd: "/usr/bin/gh" if cmd == "gh" else None
        mock_res = MagicMock()
        mock_res.returncode = 0
        mock_res.stdout = b"PRINTIT Downloaded via GH CLI\n"
        mock_subprocess_run.return_value = mock_res

        dest = os.path.join(self.test_dir, "out.txt")
        url = "https://github.com/loscrossos/videoscript/raw/refs/heads/main/videoscript.pynst.txt"
        success = pynst.fetch_file_via_git_or_gh(url, dest)
        self.assertTrue(success)
        self.assertTrue(os.path.isfile(dest))
        with open(dest, "rb") as f:
            self.assertEqual(f.read(), b"PRINTIT Downloaded via GH CLI\n")

        # Verify gh api command arguments
        mock_subprocess_run.assert_called_once()
        cmd_args = mock_subprocess_run.call_args[0][0]
        self.assertEqual(cmd_args[0], "gh")
        self.assertEqual(cmd_args[1], "api")
        self.assertIn("repos/loscrossos/videoscript/contents/videoscript.pynst.txt?ref=main", cmd_args[2])

    @patch("urllib.request.urlretrieve")
    @patch("pynst.fetch_file_via_git_or_gh")
    def test_download_to_temp_triggers_fallback_on_404(self, mock_fallback, mock_urlretrieve):
        """Verify download_to_temp falls back to git/gh when HTTP request raises 404 HTTPError."""
        # Simulate HTTP 404
        mock_urlretrieve.side_effect = urllib.error.HTTPError(
            url="https://github.com/loscrossos/videoscript/raw/main/file.txt",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None
        )

        def write_fake_file(url, dest):
            Path(dest).write_text("FALLBACK CONTENT", encoding="utf-8")
            return True

        mock_fallback.side_effect = write_fake_file

        url = "https://github.com/loscrossos/videoscript/raw/main/file.txt"
        temp_path = pynst.download_to_temp(url, force_download=True)
        try:
            self.assertTrue(temp_path.is_file())
            self.assertEqual(temp_path.read_text(encoding="utf-8"), "FALLBACK CONTENT")
            mock_fallback.assert_called_once()
        finally:
            if temp_path.exists():
                temp_path.unlink()

if __name__ == "__main__":
    unittest.main()
