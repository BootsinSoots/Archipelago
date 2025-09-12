""" Module for launching dolphin emulator """
import logging
import subprocess
import psutil
import settings
import Utils

from .luigismansion_settings import LuigisMansionSettings
from .constants import AP_LOGGER_NAME

logger = logging.getLogger(AP_LOGGER_NAME)

class DolphinLauncher:
    """
    Manages interactions between the LMClient and the dolphin emulator.
    """
    luigismansion_settings: LuigisMansionSettings
    dolphin_process_name = "dolphin"

    def __init__(self, luigismansion_settings: LuigisMansionSettings = None):
        """
        :param launch_path: The path to the dolphin executable.
            Handled by the ArchipelagoLauncher in the host.yaml file.
        :param auto_start: Determines if the the consumer should launch dolphin.
            Handled by the ArchipelagoLauncher in the host.yaml file.
        """
        if luigismansion_settings is None:
            self.luigismansion_settings = settings.get_settings().luigismansion_options
        else:
            self.luigismansion_settings = luigismansion_settings

    async def launch_dolphin_async(self, rom: str):
        """
        Launches the dolphin process if not already running.

        :param rom: The rom to load into dolphin emulator when starting the process,
            if 'None' the process won't load any rom.
        """
        if not self.luigismansion_settings.auto_start_dolphin:
            logger.info("Host.yaml settings 'auto_start_dolphin' is 'false', skipping.")
            return

        if _check_dolphin_process_open(self):
            return

        args = [ self.luigismansion_settings.dolphin_path ]
        logger.info("Attempting to open Dolphin emulator at: %s", self.luigismansion_settings.dolphin_path)
        if not rom:
            logger.info("Attempting to open Dolphin emulator with rom path:%s", rom)
            args.append(f"--exec={rom}")

        subprocess.Popen(
            args,
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def _check_dolphin_process_open(ctx: DolphinLauncher) -> bool:
    for proc in psutil.process_iter():
        if ctx.dolphin_process_name in proc.name().lower():
            logger.info("Located existing Dolphin process: %s, skipping.", proc.name())
            return True
    logger.info("No existing Dolphin processes, continuing.")
    return False
