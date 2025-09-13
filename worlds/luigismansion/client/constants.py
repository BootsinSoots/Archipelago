""" Collection of commonly used constants for Luigi's Mansion. """

CLIENT_VERSION = "V0.5.5"
CLIENT_NAME = "Luigi's Mansion Client"
AP_LOGGER_NAME = "Client"

# All the dolphin connection messages used in the client
CONNECTION_REFUSED_STATUS = "Detected a non-randomized ROM for LM. Please close and load a different one. Retrying in 5 seconds..."
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure LM is running."
NO_SLOT_NAME_STATUS = "No slot name was detected. Ensure a randomized ROM is loaded. Retrying in 5 seconds..."
CONNECTION_VERIFY_SERVER = "Dolphin was confirmed to be opened and ready, Connect to the server when ready..."
CONNECTION_INITIAL_STATUS = "Dolphin emulator was not detected to be running. Retrying in 5 seconds..."
CONNECTION_CONNECTED_STATUS = "Dolphin is connected, AP is connected, Ready to play LM!"

# Static time to wait for health and death checks
CHECKS_WAIT = 3
LONGER_MODIFIER = 2

# This address is used to track which room Luigi is in within the main mansion map (Map2)
ROOM_ID_ADDR = 0x803D8B7C
ROOM_ID_OFFSET = 0x35C

# Wait timer constants for between loops
WAIT_TIMER_SHORT_TIMEOUT: float = 0.125
WAIT_TIMER_LONG_TIMEOUT: float = 5
