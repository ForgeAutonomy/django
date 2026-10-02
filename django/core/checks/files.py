from pathlib import Path

from django.conf import settings

from . import Error, Tags, register


@register(Tags.files)
def check_setting_file_upload_temp_dir(app_configs, **kwargs):
    setting = getattr(settings, "FILE_UPLOAD_TEMP_DIR", None)
    if setting and not Path(setting).is_dir():
        return [
            Error(
                f"The FILE_UPLOAD_TEMP_DIR setting refers to the nonexistent "
                f"directory '{setting}'.",
                id="files.E001",
            ),
        ]
    return []


@register(Tags.files)
def check_setting_upload_limits(app_configs, **kwargs):
    setting_allows_none = {
        "DATA_UPLOAD_MAX_MEMORY_SIZE": True,
        "DATA_UPLOAD_MAX_NUMBER_FIELDS": True,
        "DATA_UPLOAD_MAX_NUMBER_FILES": True,
        "FILE_UPLOAD_MAX_MEMORY_SIZE": False,
    }
    errors = []
    for setting_name, allows_none in setting_allows_none.items():
        value = getattr(settings, setting_name)
        if (type(value) is int and value >= 0) or (value is None and allows_none):
            continue
        allowed_values = "a non-negative integer"
        if allows_none:
            allowed_values += " or None"
        errors.append(
            Error(
                f"The {setting_name} setting must be {allowed_values}.",
                id="files.E002",
            )
        )
    return errors
