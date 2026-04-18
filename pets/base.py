from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, Tuple
import math
import os
from PIL import Image as PILImage, ImageTk
from core.config import (
    PetState,
    SkinColor,
    ColorPalette,
    AnimationFrames,
    CyberpunkTheme,
    NurtureConfig
)


class PetBase(ABC):
    PET_TYPE = None
    DISPLAY_NAME = None
    
    NEON_PRIMARY_COLOR = CyberpunkTheme.PRIMARY_GLOW
    NEON_SECONDARY_COLOR = CyberpunkTheme.SECONDARY_GLOW
    
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
        
        self._neon_phase: float = 0.0
        self._glitch_phase: float = 0.0
        self._pulse_intensity: float = 0.0
        
        self._nurture_manager: Optional[Any] = None
    
    def set_nurture_manager(self, nurture_manager: Any):
        self._nurture_manager = nurture_manager
    
    def get_nurture_attributes(self) -> Dict[str, int]:
        if self._nurture_manager is None:
            return {
                "mood": NurtureConfig.DEFAULT_MOOD,
                "hunger": NurtureConfig.DEFAULT_HUNGER,
                "energy": NurtureConfig.DEFAULT_ENERGY,
                "affection": NurtureConfig.DEFAULT_AFFECTION,
                "level": NurtureConfig.DEFAULT_LEVEL,
                "experience": NurtureConfig.DEFAULT_EXPERIENCE
            }
        
        return {
            "mood": self._nurture_manager.mood,
            "hunger": self._nurture_manager.hunger,
            "energy": self._nurture_manager.energy,
            "affection": self._nurture_manager.affection,
            "level": self._nurture_manager.level,
            "experience": self._nurture_manager.experience
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
    
    def _update_neon_phase(self):
        self._neon_phase += 0.05
        if self._neon_phase > 2 * math.pi:
            self._neon_phase -= 2 * math.pi
        
        self._glitch_phase += 0.02
        if self._glitch_phase > 1.0:
            self._glitch_phase = 0.0
        
        if self._pulse_intensity > 0:
            self._pulse_intensity -= 0.03
            if self._pulse_intensity < 0:
                self._pulse_intensity = 0
    
    def _get_breath_intensity(self) -> float:
        return 0.5 + 0.5 * math.sin(self._neon_phase)
    
    def _get_pet_bounds(self, center: int) -> Tuple[int, int, int, int]:
        padding = 5
        return (
            padding,
            padding,
            self._size - padding,
            self._size - padding
        )
    
    def _draw_neon_outline(self, center: int):
        if self._renderer is None:
            return
        
        bounds = self._get_pet_bounds(center)
        x1, y1, x2, y2 = bounds
        
        breath_intensity = self._get_breath_intensity()
        glow_layers = 2
        
        for i in range(glow_layers):
            offset = int((glow_layers - i) * 2 * breath_intensity)
            width = 1
            
            if i % 2 == 0:
                color = self.NEON_PRIMARY_COLOR
            else:
                color = self.NEON_SECONDARY_COLOR
            
            if self._state == PetState.HAPPY:
                color = CyberpunkTheme.SOFT_AMBER if i % 2 == 0 else CyberpunkTheme.SOFT_MAUVE
            elif self._state == PetState.SLEEP:
                color = CyberpunkTheme.SOFT_LAVENDER if i % 2 == 0 else CyberpunkTheme.SOFT_MINT
            elif self._state == PetState.WALK:
                color = CyberpunkTheme.SOFT_SAGE if i % 2 == 0 else CyberpunkTheme.SOFT_CYAN
            elif self._state == PetState.JUMP:
                color = CyberpunkTheme.SOFT_PEACH if i % 2 == 0 else CyberpunkTheme.SOFT_MAUVE
            
            gx1 = x1 - offset
            gy1 = y1 - offset
            gx2 = x2 + offset
            gy2 = y2 + offset
            
            self._renderer.draw_oval(gx1, gy1, gx2, gy2, fill="", outline=color, width=width)
        
        self._renderer.draw_oval(x1, y1, x2, y2, fill="", outline=CyberpunkTheme.PRIMARY_GLOW, width=1)
    
    def _draw_glitch_effect(self, center: int):
        if self._renderer is None:
            return
        
        if self._glitch_phase > 0.95:
            bounds = self._get_pet_bounds(center)
            x1, y1, x2, y2 = bounds
            
            glitch_offset = 1
            segment_height = (y2 - y1) // 6
            
            for i in range(2):
                seg_y1 = y1 + (i + 2) * segment_height
                seg_y2 = seg_y1 + segment_height
                
                if i % 2 == 0:
                    offset_x = glitch_offset
                else:
                    offset_x = -glitch_offset
                
                color = CyberpunkTheme.SOFT_CYAN
                
                self._renderer.draw_line(
                    x1 + offset_x, seg_y1,
                    x2 + offset_x, seg_y1,
                    fill=color, width=1
                )
    
    def _draw_pulse_effect(self, center: int):
        if self._renderer is None or self._pulse_intensity <= 0:
            return
        
        colors = [
            CyberpunkTheme.SOFT_MAUVE,
            CyberpunkTheme.SOFT_CYAN,
            CyberpunkTheme.SOFT_AMBER
        ]
        
        for i, color in enumerate(colors):
            r = int(self._size * 0.4 * (1 + i * 0.15) * self._pulse_intensity)
            width = 1
            
            self._renderer.draw_oval(
                center - r, center - r,
                center + r, center + r,
                fill="", outline=color, width=width
            )
    
    def trigger_pulse(self):
        self._pulse_intensity = 1.0
    
    def draw(self):
        if self._renderer is None:
            return
        
        self._renderer.clear()
        self._update_neon_phase()
        
        center = self._get_center()
        
        self._draw_pulse_effect(center)
        
        handler = self._state_handlers.get(self._state, self._draw_idle)
        handler(center)
        
        self._draw_neon_outline(center)
        self._draw_glitch_effect(center)
    
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


class ImagePetBase(PetBase):
    IMAGE_STATES = {
        PetState.IDLE: "idle",
        PetState.HAPPY: "happy",
        PetState.SLEEP: "sleep",
        PetState.SAD: "sad",
        PetState.EAT: "eat",
        PetState.WALK: "idle",
        PetState.JUMP: "happy"
    }
    
    def __init__(self, images_dir: str = None):
        super().__init__(SkinColor.ORANGE)
        
        if images_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            images_dir = os.path.join(base_dir, "images")
        
        self._images_dir = images_dir
        self._pil_images: Dict[str, PILImage.Image] = {}
        self._tk_images: Dict[str, ImageTk.PhotoImage] = {}
        self._current_image_ref: Optional[ImageTk.PhotoImage] = None
        self._canvas_image_id: Optional[int] = None
        self._images_loaded: bool = False
        self._eat_timer: Optional[Any] = None
        self._is_eating: bool = False
        self._last_known_size: int = 0
        
        self._load_pil_images()
    
    def _load_pil_images(self):
        required_states = ["idle", "happy", "sad", "sleep", "eat"]
        
        for state in required_states:
            image_path = os.path.join(self._images_dir, f"{state}.png")
            if os.path.exists(image_path):
                try:
                    pil_image = PILImage.open(image_path).convert("RGBA")
                    self._pil_images[state] = pil_image
                except Exception as e:
                    print(f"Warning: Failed to load image {image_path}: {e}")
            else:
                print(f"Warning: Image not found: {image_path}")
    
    def _convert_to_tk_images(self):
        if self._images_loaded and self._last_known_size == self._size:
            return
        
        self._tk_images.clear()
        
        for state, pil_image in self._pil_images.items():
            try:
                if self._size <= 0:
                    target_size = 100
                else:
                    target_size = self._size
                
                resized_image = pil_image.resize(
                    (target_size, target_size),
                    PILImage.Resampling.LANCZOS
                )
                
                self._tk_images[state] = ImageTk.PhotoImage(resized_image)
            except Exception as e:
                print(f"Warning: Failed to convert image {state}: {e}")
        
        self._images_loaded = True
        self._last_known_size = self._size
    
    def _get_state_from_attributes(self) -> PetState:
        attrs = self.get_nurture_attributes()
        mood = attrs.get("mood", NurtureConfig.DEFAULT_MOOD)
        hunger = attrs.get("hunger", NurtureConfig.DEFAULT_HUNGER)
        energy = attrs.get("energy", NurtureConfig.DEFAULT_ENERGY)
        
        if energy <= NurtureConfig.CRITICAL_ENERGY_THRESHOLD:
            return PetState.SLEEP
        
        if hunger <= NurtureConfig.CRITICAL_HUNGER_THRESHOLD:
            return PetState.SAD
        
        if mood <= NurtureConfig.LOW_MOOD_THRESHOLD:
            return PetState.SAD
        
        if mood >= 80:
            return PetState.HAPPY
        
        return PetState.IDLE
    
    def _get_image_key_for_state(self, state: PetState) -> str:
        return self.IMAGE_STATES.get(state, "idle")
    
    def draw(self):
        if self._renderer is None:
            return
        
        self._renderer.clear()
        self._convert_to_tk_images()
        
        if self._nurture_manager is not None:
            recommended_state = self._get_state_from_attributes()
            if self._state not in [PetState.WALK, PetState.JUMP]:
                self._state = recommended_state
        
        image_key = self._get_image_key_for_state(self._state)
        image = self._tk_images.get(image_key)
        
        if image is None:
            image = self._tk_images.get("idle")
        
        if image is not None and hasattr(self._renderer, '_canvas'):
            canvas = self._renderer._canvas
            center = self._size // 2
            
            if self._canvas_image_id is not None:
                try:
                    canvas.delete(self._canvas_image_id)
                except Exception:
                    pass
            
            self._current_image_ref = image
            self._canvas_image_id = canvas.create_image(
                center, center,
                image=image
            )
    
    def _draw_idle(self, center: int):
        pass
    
    def _draw_walk(self, center: int):
        pass
    
    def _draw_happy(self, center: int):
        pass
    
    def _draw_sleep(self, center: int):
        pass
    
    def _draw_jump(self, center: int):
        pass