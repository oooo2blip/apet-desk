from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable
from core.config import (
    PetState,
    SkinColor,
    ColorPalette,
    AnimationFrames
)


class PetBase(ABC):
    PET_TYPE = None
    DISPLAY_NAME = None
    
    def __init__(self, skin_color: SkinColor = SkinColor.ORANGE):
        self._state: PetState = PetState.IDLE
        self._skin_color: SkinColor = skin_color
        self._frame_index: int = 0
        self._size: int = 100
        self._renderer: Optional[Any] = None
        self._state_handlers: Dict[PetState, Callable[[int], None]] = {
            PetState.IDLE: self._draw_idle,
            PetState.WALK: self._draw_walk,
            PetState.HAPPY: self._draw_happy,
            PetState.SLEEP: self._draw_sleep,
            PetState.JUMP: self._draw_jump
        }
    
    @property
    def state(self) -> PetState:
        return self._state
    
    @state.setter
    def state(self, value: PetState):
        self._state = value
    
    @property
    def skin_color(self) -> SkinColor:
        return self._skin_color
    
    @skin_color.setter
    def skin_color(self, value: SkinColor):
        self._skin_color = value
    
    @property
    def skin_hex(self) -> str:
        return ColorPalette.SKIN_COLORS.get(self._skin_color, "#FFA500")
    
    @property
    def frame_index(self) -> int:
        return self._frame_index
    
    @frame_index.setter
    def frame_index(self, value: int):
        self._frame_index = value
    
    @property
    def size(self) -> int:
        return self._size
    
    @size.setter
    def size(self, value: int):
        self._size = value
    
    def set_renderer(self, renderer: Any):
        self._renderer = renderer
    
    def _get_center(self) -> int:
        return self._size // 2
    
    def _should_blink(self) -> bool:
        return self._frame_index % AnimationFrames.BLINK_FRAME_INTERVAL < AnimationFrames.BLINK_FRAME_DURATION
    
    def _get_tail_wave(self, interval: int = 10) -> int:
        return 5 if self._frame_index % interval < interval // 2 else -5
    
    def _get_leg_offset(self, interval: int = 4) -> int:
        return 5 if self._frame_index % interval < interval // 2 else -5
    
    def _get_jump_offset(self, interval: int = 4) -> int:
        return -5 if self._frame_index % interval < interval // 2 else 0
    
    def _get_happy_jump_offset(self, interval: int = 4) -> int:
        return -10 if self._frame_index % interval < interval // 2 else 0
    
    def _get_breath_offset(self, interval: int = 10) -> int:
        return 2 if self._frame_index % interval < interval // 2 else 0
    
    def _is_tongue_out(self) -> bool:
        return self._frame_index % AnimationFrames.TONGUE_INTERVAL < AnimationFrames.TONGUE_INTERVAL // 2
    
    def _get_z_level(self) -> int:
        return self._frame_index % AnimationFrames.SLEEP_Z_INTERVAL
    
    def draw(self):
        if self._renderer is None:
            return
        
        self._renderer.clear()
        handler = self._state_handlers.get(self._state, self._draw_idle)
        handler(self._get_center())
    
    @abstractmethod
    def _draw_idle(self, center: int):
        pass
    
    @abstractmethod
    def _draw_walk(self, center: int):
        pass
    
    @abstractmethod
    def _draw_happy(self, center: int):
        pass
    
    @abstractmethod
    def _draw_sleep(self, center: int):
        pass
    
    @abstractmethod
    def _draw_jump(self, center: int):
        pass