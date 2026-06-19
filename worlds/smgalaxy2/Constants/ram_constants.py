# The base address of all the pointers
GAMESYSTEM = 0x806A1228

# Gets the current Game status, as if you are in-game, in the menu, viewing the logo, etc.
# GameSystem -> GameSystemSceneController -> SceneControlInfo
CURRENT_SCENE_POINTER_LIST: list[int] = [0x24, 0x0] # 32 chars

# Gets the current galaxy that you are in. This address also says "File-Select" if you have not chosen a file yet.
# GameSystem -> GameSystemSceneController -> SceneControlInfo
CURRENT_GALAXY_POINTER_LIST: list[int] = [0x24, 0x20] # 32 chars

# RAM Address offset to the start of all Galaxy struct address pointers
# GameSystem -> GameSequenceDirector -> SaveDataHandleSequence -> UserFile -> GameDataHolder -> GameDataAllGalaxyStorage
GALAXY_DATA_POINTER_LIST: list[int] = [0xC, 0x8, 0xC, 0x0, 0xC, 0x8]
STAR_BIT_FLAG_OFFSET: int = 0x8

# RAM Address for handling 1-ups
# GameSystem -> GameSequenceDirector -> SaveDataHandleSequence -> UserFile -> GameDataHolder -> GameDataPlayerStatus
ONEUP_POINTER_LIST: list[int] = [0xC, 0x8, 0xC, 0x0, 0x8, 0x4]
