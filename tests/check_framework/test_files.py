from pathlib import Path

from django.conf import global_settings
from django.core.checks import Error
from django.core.checks.files import (
    check_setting_file_upload_temp_dir,
    check_setting_upload_limits,
)
from django.test import SimpleTestCase


class FilesCheckTests(SimpleTestCase):
    def test_file_upload_temp_dir(self):
        tests = [
            None,
            "",
            Path.cwd(),
            str(Path.cwd()),
        ]
        for setting in tests:
            with self.subTest(setting), self.settings(FILE_UPLOAD_TEMP_DIR=setting):
                self.assertEqual(check_setting_file_upload_temp_dir(None), [])

    def test_file_upload_temp_dir_nonexistent(self):
        for setting in ["nonexistent", Path("nonexistent")]:
            with self.subTest(setting), self.settings(FILE_UPLOAD_TEMP_DIR=setting):
                self.assertEqual(
                    check_setting_file_upload_temp_dir(None),
                    [
                        Error(
                            "The FILE_UPLOAD_TEMP_DIR setting refers to the "
                            "nonexistent directory 'nonexistent'.",
                            id="files.E001",
                        ),
                    ],
                )


class UploadLimitsCheckTests(SimpleTestCase):
    upload_settings = (
        "DATA_UPLOAD_MAX_MEMORY_SIZE",
        "DATA_UPLOAD_MAX_NUMBER_FIELDS",
        "DATA_UPLOAD_MAX_NUMBER_FILES",
        "FILE_UPLOAD_MAX_MEMORY_SIZE",
    )

    def setUp(self):
        self.enterContext(
            self.settings(
                **{
                    setting_name: getattr(global_settings, setting_name)
                    for setting_name in self.upload_settings
                }
            )
        )

    def test_defaults(self):
        self.assertEqual(check_setting_upload_limits(None), [])

    def test_invalid_values(self):
        for setting_name in self.upload_settings:
            for value in (-1, "2621440", True, False):
                with self.subTest(setting=setting_name, value=value):
                    with self.settings(**{setting_name: value}):
                        errors = check_setting_upload_limits(None)
                    self.assertEqual(len(errors), 1)
                    self.assertEqual(errors[0].id, "files.E002")
                    self.assertIn(setting_name, errors[0].msg)

    def test_zero(self):
        for setting_name in self.upload_settings:
            with self.subTest(setting=setting_name, value=0):
                with self.settings(**{setting_name: 0}):
                    self.assertEqual(check_setting_upload_limits(None), [])

    def test_data_upload_limits_allow_none(self):
        for setting_name in self.upload_settings[:3]:
            with self.subTest(setting=setting_name, value=None):
                with self.settings(**{setting_name: None}):
                    self.assertEqual(check_setting_upload_limits(None), [])

    def test_file_upload_memory_limit_disallows_none(self):
        with self.settings(FILE_UPLOAD_MAX_MEMORY_SIZE=None):
            errors = check_setting_upload_limits(None)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].id, "files.E002")
        self.assertIn("FILE_UPLOAD_MAX_MEMORY_SIZE", errors[0].msg)
