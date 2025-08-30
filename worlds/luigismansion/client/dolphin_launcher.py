""" Module for launching dolphin emulator """
import logging
import subprocess
import psutil
import settings
import Utils

logger = logging.getLogger("Client")

class DolphinLauncher():
    """
    Manages interactions between the LMClient and the dolphin emulator.
    """
    launch_path: str = settings.get_settings().luigismansion_options.dolphin_path
    auto_start: bool = settings.get_settings().luigismansion_options.auto_start_dolphin
    dolphin_process_name = "dolphin"

    def __init__(self, launch_path: str = None, auto_start: bool = None):
        """
        :param launch_path: The path to the dolphin executable.
            Handled by the ArchipelagoLauncher in the host.yaml file.
        :param auto_start: Determines if the the consumer should launch dolphin.
            Handled by the ArchipelagoLauncher in the host.yaml file.
        """
        if launch_path:
            self.launch_path = launch_path
        if auto_start:
            self.auto_start = auto_start

    async def launch_dolphin_async(self, rom: str = None):
        """
        Launches the dolphin process if not already running.

        :param rom: The rom to load into dolphin emulator when starting the process,
            if 'None' the process won't load any rom.
        """
        if _check_dolphin_process_open(self):
            logger.info("Dolphin process is already open, skipping.")
            return

        if not self.auto_start:
            logger.info("Host.yaml settings defined 'auto_start_dolphin' to false, skipping.")
            return

        args = [ self.launch_path ]
        logger.info("Attempting to open dolphin emulator at: %s", self.launch_path)
        if rom is not None:
            logger.info("Attempting to open dolphin emulator with rom path:%s", rom)
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
        if ctx.dolphin_process_name in proc.name():
            logger.info("Located existing dolphin process: %s, not opening another.", proc.name())
            return True
    logger.info("No existing dolphin processes.")
    return False
