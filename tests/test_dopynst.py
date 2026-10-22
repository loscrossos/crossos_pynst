import unittest
import os
import sys
import tempfile
import shutil
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pynst

class TestDoPynst(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="pynst_test_")
        self.target_dir = os.path.join(self.test_dir, "target")
        os.makedirs(self.target_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_dopynst_in_allowed_keys(self):
        """Verify CMD_DOPYNST is defined and can pass validation."""
        self.assertEqual(pynst.CMD_DOPYNST, "DOPYNST")
        
        test_script = os.path.join(self.test_dir, "test.pynst.txt")
        with open(test_script, "w", encoding="utf-8") as f:
            f.write("DOPYNST other.pynst.txt ./target\n")
            
        allowed = {pynst.CMD_DOPYNST}
        # validate_file should not exit with error
        pynst.validate_file(test_script, allowed_keywords=allowed, limited_keywords={})

    def test_parse_inputfile_with_dopynst(self):
        """Verify parse_inputfile parses DOPYNST with options and quoted arguments."""
        test_script = os.path.join(self.test_dir, "test.pynst.txt")
        with open(test_script, "w", encoding="utf-8") as f:
            f.write('DOPYNST --embedded --noblob "path with spaces/installer.pynst.txt" "./target dir"\n')
            
        commands = pynst.parse_inputfile(Path(test_script))
        self.assertEqual(len(commands), 1)
        cmd, params = commands[0]
        self.assertEqual(cmd, "DOPYNST")
        self.assertEqual(params, ["--embedded", "--noblob", "path with spaces/installer.pynst.txt", "./target dir"])

    def test_dopynst_execution_dryrun(self):
        """Verify executing DOPYNST in dryrun mode logs the command without failing."""
        sub_installer = os.path.join(self.test_dir, "sub.pynst.txt")
        with open(sub_installer, "w", encoding="utf-8") as f:
            f.write("PRINTIT Sub-installer running\n")

        main_installer = os.path.join(self.test_dir, "main.pynst.txt")
        with open(main_installer, "w", encoding="utf-8") as f:
            f.write(f"DOPYNST --dryrun \"{sub_installer}\" \"{self.target_dir}\"\n")

        cmd = [sys.executable, str(PROJECT_ROOT / "pynst.py"), "--dryrun", main_installer, self.target_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        self.assertIn("DOPYNST", result.stdout)

    def test_dopynst_execution_live(self):
        """Verify executing DOPYNST actually runs the sub-installer process."""
        sub_target = os.path.join(self.test_dir, "sub_target")
        os.makedirs(sub_target, exist_ok=True)
        
        sub_installer = os.path.join(self.test_dir, "sub.pynst.txt")
        with open(sub_installer, "w", encoding="utf-8") as f:
            f.write("PRINTIT Hello from sub installer!\n")

        main_installer = os.path.join(self.test_dir, "main.pynst.txt")
        with open(main_installer, "w", encoding="utf-8") as f:
            f.write(f"DOPYNST \"{sub_installer}\" \"{sub_target}\"\n")

        cmd = [sys.executable, str(PROJECT_ROOT / "pynst.py"), main_installer, self.target_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        self.assertIn("Hello from sub installer!", result.stdout)

    def test_dopynst_failure_propagates(self):
        """Verify that a failure in the child installer causes the parent DOPYNST to abort."""
        sub_target = os.path.join(self.test_dir, "sub_target")
        os.makedirs(sub_target, exist_ok=True)

        sub_installer = os.path.join(self.test_dir, "sub_fail.pynst.txt")
        with open(sub_installer, "w", encoding="utf-8") as f:
            # HASFILE on a non-existent file will abort the child run
            f.write("HASFILE nonexistent_file_xyz_123.txt\n")

        main_installer = os.path.join(self.test_dir, "main.pynst.txt")
        with open(main_installer, "w", encoding="utf-8") as f:
            f.write(f"DOPYNST \"{sub_installer}\" \"{sub_target}\"\n")

        cmd = [sys.executable, str(PROJECT_ROOT / "pynst.py"), main_installer, self.target_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue("failed with exit code" in result.stdout or "failed with exit code" in result.stderr)

    def test_remote_url_installer(self):
        """Verify that input files can be fetched via HTTP/HTTPS URL and executed."""
        # Serve a dummy pynst file via local HTTP server
        server_dir = os.path.join(self.test_dir, "http_server")
        os.makedirs(server_dir, exist_ok=True)
        remote_script_path = os.path.join(server_dir, "remote.pynst.txt")
        with open(remote_script_path, "w", encoding="utf-8") as f:
            f.write("PRINTIT Remote script executed successfully!\n")

        class CustomHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=server_dir, **kwargs)
            def log_message(self, format, *args):
                pass  # suppress server log output

        httpd = HTTPServer(("127.0.0.1", 0), CustomHandler)
        port = httpd.server_address[1]
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()

        try:
            url = f"http://127.0.0.1:{port}/remote.pynst.txt"

            # 1. Test direct invocation via CLI
            direct_target = os.path.join(self.test_dir, "direct_target")
            os.makedirs(direct_target, exist_ok=True)
            cmd = [sys.executable, str(PROJECT_ROOT / "pynst.py"), url, direct_target]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            self.assertIn("Remote script executed successfully!", result.stdout)

            # 2. Test invocation via DOPYNST
            dopynst_target = os.path.join(self.test_dir, "dopynst_target")
            os.makedirs(dopynst_target, exist_ok=True)
            main_installer = os.path.join(self.test_dir, "main_url.pynst.txt")
            with open(main_installer, "w", encoding="utf-8") as f:
                f.write(f"DOPYNST \"{url}\" \"{dopynst_target}\"\n")

            cmd = [sys.executable, str(PROJECT_ROOT / "pynst.py"), main_installer, self.target_dir]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            self.assertIn("Remote script executed successfully!", result.stdout)
        finally:
            httpd.shutdown()
            httpd.server_close()

if __name__ == "__main__":
    unittest.main()
