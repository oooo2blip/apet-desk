from enum import Enum


class CyberpunkTheme:
    ELECTRIC_BLUE = "#00D4FF"
    NEON_PINK = "#FF00FF"
    GLITCH_PURPLE = "#9D00FF"
    TECH_BLACK = "#0A0A0A"
    CYBER_GREEN = "#39FF14"
    NEON_ORANGE = "#FF5E00"
    NEON_YELLOW = "#FFFF00"
    
    NEON_GLOW_COLORS = [
        ELECTRIC_BLUE,
        NEON_PINK,
        GLITCH_PURPLE,
        CYBER_GREEN,
        NEON_ORANGE
    ]
    
    GLOW_ALPHA_LAYERS = [
        {"color": ELECTRIC_BLUE, "offset": 2, "width": 3},
        {"color": NEON_PINK, "offset": 1, "width": 2},
        {"color": GLITCH_PURPLE, "offset": 0, "width": 1},
    ]


class PetState(Enum):
    IDLE = "idle"
    WALK = "walk"
    HAPPY = "happy"
    SLEEP = "sleep"
    JUMP = "jump"


class PetType(Enum):
    CAT = "cat"
    DOG = "dog"
    RABBIT = "rabbit"


class SkinColor(Enum):
    ORANGE = "orange"
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    BROWN = "brown"


class Direction(Enum):
    RIGHT = 1
    LEFT = -1


class AnimationConfig:
    DEFAULT_ANIMATION_SPEED = 200
    WALK_UPDATE_INTERVAL = 50
    IDLE_STATE_DURATION_MIN = 3000
    IDLE_STATE_DURATION_MAX = 10000
    INTERACTION_DURATION = 2000
    POST_DRAG_DELAY = 1000
    WALK_DISTANCE_MIN = 50
    WALK_DISTANCE_MAX = 200
    WALK_STEP = 2
    JUMP_DURATION_MIN = 1000
    JUMP_DURATION_MAX = 3000
    HAPPY_DURATION_MIN = 2000
    HAPPY_DURATION_MAX = 5000
    SLEEP_DURATION_MIN = 5000
    SLEEP_DURATION_MAX = 15000


class UIConfig:
    DEFAULT_PET_SIZE = 100
    MIN_PET_SIZE = 50
    MAX_PET_SIZE = 200
    DEFAULT_POSITION_OFFSET_X = 50
    DEFAULT_POSITION_OFFSET_Y = 100
    SETTINGS_WINDOW_WIDTH = 300
    SETTINGS_WINDOW_HEIGHT = 250
    TRANSPARENT_COLOR = "white"


class SoundConfig:
    CLICK_FREQUENCY = 1000
    CLICK_DURATION = 100


class ColorPalette:
    SKIN_COLORS = {
        SkinColor.ORANGE: "#FFA500",
        SkinColor.WHITE: "#F5F5F5",
        SkinColor.BLACK: "#333333",
        SkinColor.GRAY: "#808080",
        SkinColor.BROWN: "#8B4513"
    }
    INNER_EAR_COLOR = "#FFB6C1"
    NOSE_COLOR = "pink"
    BLACK = "black"
    WHITE = "white"
    GRAY = "gray"
    BROWN_DARK = "#8B4513"
    WHITE_LIGHT = "#555555"
    PINK = "pink"


class PetDisplayNames:
    PET_NAMES = {
        PetType.CAT: "猫咪",
        PetType.DOG: "狗狗",
        PetType.RABBIT: "兔子"
    }
    SKIN_NAMES = {
        SkinColor.ORANGE: "橘色",
        SkinColor.WHITE: "白色",
        SkinColor.BLACK: "黑色",
        SkinColor.GRAY: "灰色",
        SkinColor.BROWN: "棕色"
    }


class AnimationFrames:
    BLINK_FRAME_INTERVAL = 20
    BLINK_FRAME_DURATION = 2
    TAIL_WAVE_INTERVAL = 10
    WALK_LEG_INTERVAL = 4
    HAPPY_JUMP_INTERVAL = 4
    SLEEP_Z_INTERVAL = 30
    EAR_WAVE_INTERVAL = 15
    TONGUE_INTERVAL = 10
    BREATH_INTERVAL = 10