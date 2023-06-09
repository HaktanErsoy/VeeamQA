import unittest
import sync
import os
import shutil


class TestSync(unittest.TestCase):
    def setUp(self):
        self.source_folder = "./tests/source_test"
        self.copy_folder = "./tests/copy_test"
        self.log_file = "./tests/log_test.txt"
        shutil.rmtree(self.copy_folder)
        shutil.rmtree(self.source_folder)
        os.remove(self.log_file)
        os.makedirs(self.source_folder, exist_ok=True)
        os.makedirs(self.copy_folder, exist_ok=True)
        f = open(self.log_file, "w+")
        f.close()

    def test_create_file(self):
        create_txt = "create_test.txt"
        f = open(f"{self.source_folder}/{create_txt}", "w+")
        f.close()
        sync.do_sync_once(self.source_folder, self.copy_folder, 3, self.log_file)

        self.assertEqual(
            set(os.listdir(self.source_folder)), set(os.listdir(self.copy_folder))
        )
        with open(self.log_file) as file:
            self.assertEqual(
                f"Created: {self.source_folder}/{create_txt} -> {self.copy_folder}/{create_txt}\n",
                file.read(),
            )

    def test_update_file(self):
        create_txt = "create_test.txt"
        update_txt = "update_test.txt"
        f = open(f"{self.source_folder}/{create_txt}", "w+")
        f.close()

        sync.do_sync_once(self.source_folder, self.copy_folder, 3, self.log_file)
        os.rename(
            f"./{self.source_folder}/{create_txt}",
            f"./{self.source_folder}/{update_txt}",
        )
        sync.do_sync_once(self.source_folder, self.copy_folder, 3, self.log_file)

        self.assertEqual(
            set(os.listdir(self.source_folder)), set(os.listdir(self.copy_folder))
        )

        with open(self.log_file) as file:
            self.assertEqual(
                f"Created: {self.source_folder}/{create_txt} -> {self.copy_folder}/{create_txt}\nCopied: {self.source_folder}/{update_txt} -> {self.copy_folder}/{update_txt}\nRemoved: {self.copy_folder}/{create_txt}\n",
                file.read(),
            )

    def test_remove_file(self):
        create_txt = "create_test.txt"
        f = open(f"{self.source_folder}/{create_txt}", "w+")
        f.close()
        sync.do_sync_once(self.source_folder, self.copy_folder, 3, self.log_file)
        os.remove(f"{self.source_folder}/{create_txt}")
        sync.do_sync_once(self.source_folder, self.copy_folder, 3, self.log_file)
        with open(self.log_file) as file:
            self.assertEqual(
                f"Created: {self.source_folder}/{create_txt} -> {self.copy_folder}/{create_txt}\nRemoved: {self.copy_folder}/{create_txt}\n",
                file.read(),
            )
