import settings

class EmulatorExecutable(settings.UserFilePath):
    """
    Emulator executable path. Automatically starts rom upon patching completion.
    If using Flatpak, specify the path here.
    """
    is_exe = True
    description = "The path for emulator executable. If using Flatpak specify this path instead."

class EmulatorAdditionalArguments(list[str]):
    """ Additional arugments to be passed in when auto starting emulator. """
    args = []

class EmulatorSettings(settings.Group):
    path: EmulatorExecutable = EmulatorExecutable()
    additional_args: EmulatorAdditionalArguments = EmulatorAdditionalArguments([ ])
    auto_start: bool = True

class ISOFile(settings.UserFilePath):
    """ Locate your Luigi's Mansion ISO """
    description = "Luigi's Mansion (NTSC-U) ISO"
    copy_to = None
    md5s = ["6e3d9ae0ed2fbd2f77fa1ca09a60c494"]

class LuigisMansionSettings(settings.Group):
    iso_file: ISOFile = ISOFile(ISOFile.copy_to)
    dolphin_settings: EmulatorSettings = EmulatorSettings()
