import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pynst

class TestCacheMatcher(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="pynst_match_test_")
        self.cache_repo = os.path.join(self.test_dir, "cache_repo")
        self.collect_dir = os.path.join(self.test_dir, "collect_dir")
        os.makedirs(self.cache_repo, exist_ok=True)
        os.makedirs(self.collect_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_unoriginal_filename_detection(self):
        """Verify is_unoriginal_filename accurately distinguishes generic from unique names."""
        generic_names = [
            "model.safetensors",
            "MODEL.SAFETENSORS",
            "diffusion_pytorch_model.safetensors",
            "pytorch_model.bin",
            "pytorch_model.safetensors",
            "model.bin",
            "model.pt",
            "model.pth",
            "weights.safetensors",
            "adapter_model.safetensors",
            "config.json",
            "tokenizer.json",
            "special_tokens_map.json",
            "model-00001-of-00003.safetensors",
            "pytorch_model-00002-of-00004.bin",
            "diffusion_pytorch_model-00001-of-00002.safetensors",
            "consolidated.00.pth",
        ]
        for name in generic_names:
            self.assertTrue(
                pynst.is_unoriginal_filename(name),
                f"Expected '{name}' to be classified as unoriginal/generic"
            )

        unique_names = [
            "flux1-dev.safetensors",
            "wan2.2-i2v-rapid-aio-example.json",
            "sd_xl_base_1.0.safetensors",
            "clip_g.safetensors",
            "t5xxl_fp8_e4m3fn.safetensors",
            "my_finetune_weights_v2.safetensors",
        ]
        for name in unique_names:
            self.assertFalse(
                pynst.is_unoriginal_filename(name),
                f"Expected '{name}' to be classified as unique"
            )

    def test_extract_url_cache_identity(self):
        """Verify URL components (domain, account, repo, main_dir_name) are correctly parsed."""
        hf_url = "https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/model.safetensors"
        domain, account, repo_name, subdirs, main_dir, sub_dir = pynst.extract_url_cache_identity(hf_url, "model.safetensors")
        self.assertEqual(domain, "huggingface")
        self.assertEqual(account, "phr00t")
        self.assertEqual(repo_name, "wan2.2-14b-rapid-allinone")
        self.assertIn("phr00t", main_dir)
        self.assertIn("wan2.2-14b-rapid-allinone", main_dir)
        self.assertEqual(sub_dir, "default")

        # Subdirectory URL
        sub_url = "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/unet/diffusion_pytorch_model.safetensors"
        d, a, r, subs, m_dir, s_dir = pynst.extract_url_cache_identity(sub_url, "diffusion_pytorch_model.safetensors")
        self.assertEqual(a, "stabilityai")
        self.assertEqual(r, "stable-diffusion-xl-base-1.0")
        self.assertEqual(subs, ["unet"])
        self.assertEqual(s_dir, "unet")

    def test_model_safetensors_disables_pure_filename_match_when_webfile_down(self):
        """When webfile is unreachable (expected_size == -1), pure filename match is disabled for model.safetensors."""
        # Setup an unrelated checkpoints/model.safetensors
        unrelated_dir = os.path.join(self.cache_repo, "checkpoints")
        os.makedirs(unrelated_dir, exist_ok=True)
        unrelated_file = os.path.join(unrelated_dir, "model.safetensors")
        with open(unrelated_file, "wb") as f:
            f.write(b"unrelated_model_data_12345")

        url = "https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/model.safetensors"
        # Remote size unknown (-1)
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=-1,
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNone(matched, "Should NOT match pure filename for model.safetensors when webfile is down")

    def test_model_safetensors_matches_account_repo_folder_when_webfile_down(self):
        """When webfile is unreachable (expected_size == -1), file in matching account/repo folder IS used."""
        matching_dir = os.path.join(self.collect_dir, "huggingface_Phr00t_WAN2.2-14B-Rapid-AllInOne", "default")
        os.makedirs(matching_dir, exist_ok=True)
        target_file = os.path.join(matching_dir, "model.safetensors")
        with open(target_file, "wb") as f:
            f.write(b"cached_wan_model_content")

        url = "https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/model.safetensors"
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=-1,
            repos=[self.collect_dir],
            url=url
        )
        self.assertEqual(os.path.abspath(matched), os.path.abspath(target_file))

    def test_model_safetensors_rejects_conflicting_huggingface_account(self):
        """Files located in a different huggingface account's folder are rejected even if size matches."""
        # Folder for other author
        other_dir = os.path.join(self.cache_repo, "huggingface_otherauthor_othermodel", "default")
        os.makedirs(other_dir, exist_ok=True)
        other_file = os.path.join(other_dir, "model.safetensors")
        file_bytes = b"dummy_model_bytes_4000"
        with open(other_file, "wb") as f:
            f.write(file_bytes)

        url = "https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/model.safetensors"
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=len(file_bytes),
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNone(matched, "Conflicting account folder must NOT match model.safetensors")

    def test_same_author_different_repo_rejected_for_generic_filename(self):
        """The same author with a different model repo folder must not match generic model.safetensors."""
        other_repo_dir = os.path.join(self.cache_repo, "Phr00t", "othermodel")
        os.makedirs(other_repo_dir, exist_ok=True)
        other_file = os.path.join(other_repo_dir, "model.safetensors")
        with open(other_file, "wb") as f:
            f.write(b"data_other_model")

        url = "https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/model.safetensors"
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=-1,
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNone(matched, "Same author but different repo folder must not match generic filename")

    def test_unique_filename_fallback_when_webfile_down(self):
        """Unique filenames can fall back to pure filename match when webfile is down as last resort."""
        generic_dir = os.path.join(self.cache_repo, "some_unrelated_folder")
        os.makedirs(generic_dir, exist_ok=True)
        unique_file = os.path.join(generic_dir, "flux1-dev-fp8-custom-v1.safetensors")
        with open(unique_file, "wb") as f:
            f.write(b"flux1_custom_data")

        url = "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev-fp8-custom-v1.safetensors"
        matched = pynst.find_file_in_repos(
            filename="flux1-dev-fp8-custom-v1.safetensors",
            expected_size=-1,
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNotNone(matched)
        self.assertEqual(os.path.abspath(matched), os.path.abspath(unique_file))

    def test_exact_account_repo_prioritized_over_generic_folder(self):
        """Exact account/repo folder match is prioritized over generic folder even if sizes are identical."""
        content = b"identical_size_model_weights_12345"

        # Candidate 1: Generic checkpoints folder
        gen_dir = os.path.join(self.cache_repo, "models", "checkpoints")
        os.makedirs(gen_dir, exist_ok=True)
        gen_file = os.path.join(gen_dir, "unique_flux.safetensors")
        with open(gen_file, "wb") as f:
            f.write(content)

        # Candidate 2: Exact account & repo folder
        acc_dir = os.path.join(self.cache_repo, "huggingface_black-forest-labs_flux.1-dev", "default")
        os.makedirs(acc_dir, exist_ok=True)
        acc_file = os.path.join(acc_dir, "unique_flux.safetensors")
        with open(acc_file, "wb") as f:
            f.write(content)

        url = "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/unique_flux.safetensors"
        matched = pynst.find_file_in_repos(
            filename="unique_flux.safetensors",
            expected_size=len(content),
            repos=[self.cache_repo],
            url=url
        )
        self.assertEqual(os.path.abspath(matched), os.path.abspath(acc_file))

    def test_size_mismatch_disqualified_in_default_mode(self):
        """When expected_size is known and local size differs, candidate is disqualified in filelistandsize mode."""
        acc_dir = os.path.join(self.cache_repo, "huggingface_author_repo", "default")
        os.makedirs(acc_dir, exist_ok=True)
        local_file = os.path.join(acc_dir, "model.safetensors")
        with open(local_file, "wb") as f:
            f.write(b"short")

        url = "https://huggingface.co/author/repo/resolve/main/model.safetensors"
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=100000,
            repos=[self.cache_repo],
            matchmode="filelistandsize",
            url=url
        )
        self.assertIsNone(matched)

    def test_mirror_same_repo_diff_author_matches_when_filesize_matches(self):
        """A mirror with different author but same repo space, subpath, and file size is accepted."""
        content = b"vexo_weights_content_555"
        mirror_dir = os.path.join(self.cache_repo, "huggingface_humanb_vexo", "tensors")
        os.makedirs(mirror_dir, exist_ok=True)
        mirror_file = os.path.join(mirror_dir, "vexo3b.safetensors")
        with open(mirror_file, "wb") as f:
            f.write(content)

        url = "https://huggingface.co/persona/vexo/resolve/main/tensors/vexo3b.safetensors"
        matched = pynst.find_file_in_repos(
            filename="vexo3b.safetensors",
            expected_size=len(content),
            repos=[self.cache_repo],
            url=url
        )
        self.assertEqual(os.path.abspath(matched), os.path.abspath(mirror_file))

    def test_mirror_same_repo_diff_author_matches_when_offline_if_no_original(self):
        """When original is offline (-1) and no same-author match exists, mirror with same repo space and subpath matches."""
        content = b"vexo_weights_content_offline"
        mirror_dir = os.path.join(self.collect_dir, "huggingface_humanb_vexo", "tensors")
        os.makedirs(mirror_dir, exist_ok=True)
        mirror_file = os.path.join(mirror_dir, "vexo3b.safetensors")
        with open(mirror_file, "wb") as f:
            f.write(content)

        url = "https://huggingface.co/persona/vexo/resolve/main/tensors/vexo3b.safetensors"
        matched = pynst.find_file_in_repos(
            filename="vexo3b.safetensors",
            expected_size=-1,
            repos=[self.collect_dir],
            url=url
        )
        self.assertEqual(os.path.abspath(matched), os.path.abspath(mirror_file))

    def test_original_author_prioritized_over_mirror_different_author(self):
        """When both original author and mirror exist, original author is prioritized."""
        orig_content = b"original_content_data"
        mirror_content = b"original_content_data"

        # Mirror file
        mirror_dir = os.path.join(self.cache_repo, "huggingface_humanb_vexo", "tensors")
        os.makedirs(mirror_dir, exist_ok=True)
        mirror_file = os.path.join(mirror_dir, "vexo3b.safetensors")
        with open(mirror_file, "wb") as f:
            f.write(mirror_content)

        # Original file
        orig_dir = os.path.join(self.cache_repo, "huggingface_persona_vexo", "tensors")
        os.makedirs(orig_dir, exist_ok=True)
        orig_file = os.path.join(orig_dir, "vexo3b.safetensors")
        with open(orig_file, "wb") as f:
            f.write(orig_content)

        url = "https://huggingface.co/persona/vexo/resolve/main/tensors/vexo3b.safetensors"
        # Test both when size is known and when offline
        matched_online = pynst.find_file_in_repos(
            filename="vexo3b.safetensors",
            expected_size=len(orig_content),
            repos=[self.cache_repo],
            url=url
        )
        self.assertEqual(os.path.abspath(matched_online), os.path.abspath(orig_file))

        matched_offline = pynst.find_file_in_repos(
            filename="vexo3b.safetensors",
            expected_size=-1,
            repos=[self.cache_repo],
            url=url
        )
        self.assertEqual(os.path.abspath(matched_offline), os.path.abspath(orig_file))

    def test_different_author_different_repo_still_rejected(self):
        """Different author with different repo space is NOT a mirror and is rejected."""
        content = b"unrelated_othermodel_data"
        other_dir = os.path.join(self.cache_repo, "huggingface_humanb_othermodel", "tensors")
        os.makedirs(other_dir, exist_ok=True)
        other_file = os.path.join(other_dir, "vexo3b.safetensors")
        with open(other_file, "wb") as f:
            f.write(content)

        url = "https://huggingface.co/persona/vexo/resolve/main/tensors/vexo3b.safetensors"
        matched = pynst.find_file_in_repos(
            filename="vexo3b.safetensors",
            expected_size=len(content),
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNone(matched, "Different repo space from different author must NOT match")

    def test_unrelated_model_safetensors_not_considered_and_no_mismatch_logged(self):
        """Unrelated model.safetensors in folders like Ace-Step or HunyuanVideo must not match or be logged."""
        # Create unrelated model folder with a model.safetensors of different size
        ace_dir = os.path.join(self.cache_repo, "Ace-Step1.5", "acestep-5Hz-lm-1.7B")
        os.makedirs(ace_dir, exist_ok=True)
        with open(os.path.join(ace_dir, "model.safetensors"), "wb") as f:
            f.write(b"ace_step_bytes_different_size")

        hunyuan_dir = os.path.join(self.cache_repo, "HunyuanVideo", "text_encoder_2")
        os.makedirs(hunyuan_dir, exist_ok=True)
        with open(os.path.join(hunyuan_dir, "model.safetensors"), "wb") as f:
            f.write(b"hunyuan_bytes_different_size")

        url = "https://huggingface.co/openbmb/VoxCPM2/resolve/main/model.safetensors"
        # Remote size is known and large
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=4580080592,
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNone(matched, "Unrelated model.safetensors must never match generic unoriginal name")

    def test_subpath_mismatch_disqualifies_generic_model_safetensors(self):
        """When downloading speech_tokenizer/model.safetensors, default/model.safetensors must NOT match or be logged."""
        # Create default/model.safetensors in the same repository
        base_dir = os.path.join(self.cache_repo, "huggingface_Qwen_Qwen3-TTS-12Hz-1.7B-Base", "default")
        os.makedirs(base_dir, exist_ok=True)
        with open(os.path.join(base_dir, "model.safetensors"), "wb") as f:
            f.write(b"base_model_content_3857413744")

        # URL asks for speech_tokenizer/model.safetensors
        url = "https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base/resolve/main/speech_tokenizer/model.safetensors"
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=682293092,
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNone(matched, "default/model.safetensors must NOT match speech_tokenizer/model.safetensors")

        # Also test offline mode (expected_size == -1): it must NEVER substitute default for speech_tokenizer
        matched_offline = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=-1,
            repos=[self.cache_repo],
            url=url
        )
        self.assertIsNone(matched_offline, "Offline mode must NOT substitute default/model.safetensors for speech_tokenizer")

    def test_subpath_match_correctly_matches_when_present(self):
        """When downloading speech_tokenizer/model.safetensors, speech_tokenizer/model.safetensors DOES match."""
        st_dir = os.path.join(self.cache_repo, "huggingface_Qwen_Qwen3-TTS-12Hz-1.7B-Base", "speech_tokenizer")
        os.makedirs(st_dir, exist_ok=True)
        target_path = os.path.join(st_dir, "model.safetensors")
        with open(target_path, "wb") as f:
            f.write(b"speech_tokenizer_content_682293092")

        url = "https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base/resolve/main/speech_tokenizer/model.safetensors"
        matched = pynst.find_file_in_repos(
            filename="model.safetensors",
            expected_size=len(b"speech_tokenizer_content_682293092"),
            repos=[self.cache_repo],
            url=url
        )
        self.assertEqual(os.path.abspath(matched), os.path.abspath(target_path))

if __name__ == "__main__":
    unittest.main()
