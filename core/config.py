from enum import Enum
from typing import Tuple


class PastelTheme:
    SOFT_LAVENDER = "#E6E0F8"
    SOFT_PERIWINKLE = "#D4C4FB"
    SOFT_MAUVE = "#F8E0FB"
    SOFT_PINK = "#FADADD"
    SOFT_PEACH = "#FFE5D9"
    SOFT_CORAL = "#FFD6E0"
    SOFT_MINT = "#E8FFF5"
    SOFT_SAGE = "#D1FAE5"
    SOFT_TEAL = "#CCFBF1"
    
    GRADIENT_BLUE_PURPLE = ("#D4C4FB", "#E6E0F8", "#F3E8FF")
    GRADIENT_PINK_ORANGE = ("#FFD6E0", "#FADADD", "#FFE5D9")
    GRADIENT_MINT = ("#D1FAE5", "#E8FFF5", "#CCFBF1")
    
    GLOW_LAVENDER = "#C4B5FD"
    GLOW_PINK = "#F9A8D4"
    GLOW_MINT = "#6EE7B7"
    
    EYE_GRADIENT_DARK = ("#A78BFA", "#8B5CF6")
    EYE_GRADIENT_LIGHT = ("#C4B5FD", "#DDD6FE")
    EYE_HIGHLIGHT = "#FFFFFF"
    
    BLUSH_COLOR = "#FECDD3"
    INNER_EAR_COLOR = "#FBCFE8"


class CyberpunkTheme:
    SOFT_CYAN = "#7EC8E3"
    SOFT_LAVENDER = "#D8BFD8"
    SOFT_MAUVE = "#E6B0AA"
    SOFT_PEACH = "#FADBD8"
    SOFT_SAGE = "#A9DFBF"
    SOFT_AMBER = "#F9E79F"
    SOFT_MINT = "#A3E4D7"
    
    PRIMARY_GLOW = "#7EC8E3"
    SECONDARY_GLOW = "#D8BFD8"
    ACCENT_GLOW = "#E6B0AA"
    
    BUBBLE_BG = "#2C3E50"
    BUBBLE_BORDER = "#7EC8E3"
    BUBBLE_TEXT = "#F8F9F9"
    
    NEON_GLOW_COLORS = [
        PRIMARY_GLOW,
        SECONDARY_GLOW,
        ACCENT_GLOW
    ]


class MinimalTheme:
    BG_LIGHT = "#FAFAFA"
    BG_MEDIUM = "#F0F0F0"
    BG_DARK = "#E0E0E0"
    
    TEXT_PRIMARY = "#333333"
    TEXT_SECONDARY = "#666666"
    TEXT_DISABLED = "#999999"
    
    BORDER_LIGHT = "#E8E8E8"
    BORDER_MEDIUM = "#D0D0D0"
    
    ACCENT_PRIMARY = "#4A90D9"
    ACCENT_HOVER = "#357ABD"
    ACCENT_LIGHT = "#E8F4FD"
    
    SUCCESS = "#5DB075"
    WARNING = "#F5A623"
    ERROR = "#E74C3C"
    
    TRANSPARENT_MASK = "#FFFFFF"


class PetState(Enum):
    IDLE = "idle"
    WALK = "walk"
    HAPPY = "happy"
    SLEEP = "sleep"
    JUMP = "jump"
    SAD = "sad"
    EAT = "eat"


class PetType(Enum):
    CAT = "cat"


class SkinColor(Enum):
    ORANGE = "orange"
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    BROWN = "brown"
    PASTEL_LAVENDER = "pastel_lavender"
    PASTEL_PINK = "pastel_pink"
    PASTEL_MINT = "pastel_mint"


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
    SETTINGS_WINDOW_HEIGHT = 400
    TRANSPARENT_COLOR = "white"
    
    DEFAULT_ALPHA = 1.0
    MIN_ALPHA = 0.1
    MAX_ALPHA = 1.0
    DEFAULT_TOPMOST = True
    DEFAULT_SAVE_CONFIG = True
    CONFIG_FILE_NAME = "pet_config.json"


class SoundConfig:
    CLICK_FREQUENCY = 1000
    CLICK_DURATION = 100


class ColorPalette:
    SKIN_COLORS = {
        SkinColor.ORANGE: "#FFA500",
        SkinColor.WHITE: "#F5F5F5",
        SkinColor.BLACK: "#333333",
        SkinColor.GRAY: "#808080",
        SkinColor.BROWN: "#8B4513",
        SkinColor.PASTEL_LAVENDER: PastelTheme.SOFT_LAVENDER,
        SkinColor.PASTEL_PINK: PastelTheme.SOFT_PINK,
        SkinColor.PASTEL_MINT: PastelTheme.SOFT_MINT
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
        PetType.CAT: "猫咪"
    }
    SKIN_NAMES = {
        SkinColor.ORANGE: "橘色",
        SkinColor.WHITE: "白色",
        SkinColor.BLACK: "黑色",
        SkinColor.GRAY: "灰色",
        SkinColor.BROWN: "棕色",
        SkinColor.PASTEL_LAVENDER: "薰衣草紫",
        SkinColor.PASTEL_PINK: "樱花粉",
        SkinColor.PASTEL_MINT: "薄荷绿"
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


class NurtureConfig:
    MAX_MOOD = 100
    MAX_HUNGER = 100
    MAX_ENERGY = 100
    MAX_AFFECTION = 1000
    MAX_LEVEL = 10
    
    DEFAULT_MOOD = 80
    DEFAULT_HUNGER = 80
    DEFAULT_ENERGY = 80
    DEFAULT_AFFECTION = 0
    DEFAULT_LEVEL = 1
    DEFAULT_EXPERIENCE = 0
    
    HUNGER_DECAY_RATE = 1
    HUNGER_DECAY_INTERVAL = 60000
    
    ENERGY_DECAY_RATE = 1
    ENERGY_DECAY_INTERVAL = 60000
    
    MOOD_DECAY_RATE = 1
    MOOD_DECAY_INTERVAL = 120000
    
    PET_MOOD_BOOST = 15
    PET_AFFECTION_BOOST = 10
    PET_EXPERIENCE_BOOST = 5
    
    FEED_HUNGER_BOOST = 30
    FEED_MOOD_BOOST = 5
    FEED_EXPERIENCE_BOOST = 3
    
    REST_ENERGY_BOOST = 30
    REST_MOOD_BOOST = 5
    REST_EXPERIENCE_BOOST = 2
    
    EXPERIENCE_PER_LEVEL = 100
    
    AFFECTION_UNLOCK_LEVELS = {
        1: 0,
        2: 50,
        3: 150,
        4: 300,
        5: 500,
        6: 650,
        7: 750,
        8: 850,
        9: 925,
        10: 1000
    }
    
    CRITICAL_HUNGER_THRESHOLD = 20
    CRITICAL_ENERGY_THRESHOLD = 20
    LOW_MOOD_THRESHOLD = 30
    
    SAVE_FILE_NAME = "pet_save.json"
    
    INTERACTION_COOLDOWN = 1000