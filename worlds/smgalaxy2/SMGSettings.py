import settings

class EmulatorExecutable(settings.UserFilePath):
    """
    Emulator executable path. Automatically starts rom upon patching completion.
    If using Flatpak, specify the path here.
    """
    is_exe = True
    description = "The path for emulator executable. If using Flatpak, specify this path instead."

class EmulatorAdditionalArguments(list):
    """ Additional arugments to be passed in when auto starting emulator."""
    pass

class EmulatorSettings(settings.Group):
    """Various Emulator specific settings (such as Dolphin)"""
    path: EmulatorExecutable = EmulatorExecutable()
    additional_args: EmulatorAdditionalArguments = EmulatorAdditionalArguments()
    auto_start: bool = True

class ISOFile(settings.UserFilePath):
    """Locate your Super Mario Galaxy ISO"""
    description = "Super Mario Galaxy (USA) ISO"
    copy_to = None

class DolphinProcessName(str):
    """The name of the Dolphin process to connect to. Leave blank for system default."""
    pass

class SuperMarioGalaxy(settings.Group):
    """Various Super Mario Galaxy Settings"""
    iso_file: ISOFile = ISOFile(ISOFile.copy_to)
    dolphin_settings: EmulatorSettings = EmulatorSettings()
    dolphin_process_name: DolphinProcessName = DolphinProcessName("")
