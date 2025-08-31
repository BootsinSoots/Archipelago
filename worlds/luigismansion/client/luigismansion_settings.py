import settings

class DolphinExecutable(settings.UserFilePath):
    """
    Dolphin emulator executable path.
    Automatically starts rom upon patching completion.
    """
    is_exe = True
    description = "The path for dolphin emulator executable."

class ISOFile(settings.UserFilePath):
    """
    Locate your Luigi's Mansion ISO
    """
    description = "Luigi's Mansion (NTSC-U) ISO"
    copy_to = "Luigi's Mansion (NTSC-U).iso"
    md5s = ["6e3d9ae0ed2fbd2f77fa1ca09a60c494"]

class LuigisMansionSettings(settings.Group):
    iso_file: ISOFile = ISOFile(ISOFile.copy_to)
    dolphin_path: DolphinExecutable = DolphinExecutable()
    auto_start_dolphin: bool = True
