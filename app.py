import tkinter as tk
import winsound
import os
from typing import Optional, Tuple, Dict, Any
from core.config import (
    PetState,
    PetType,
    SkinColor,
    Direction,
    UIConfig,
    SoundConfig,
    AnimationConfig
)
from core.animation import AnimationEngine, WalkController
from core.behavior import BehaviorEngine
from core.nurture import NurtureManager
from pets.base import PetBase
from pets.factory import PetFactory, SkinManager
from ui.renderer import Renderer
from ui.components import DragHandler, ContextMenu, SettingsWindow, SpeechBubble, EmotionDisplay


class PetApplication:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("萌宠桌面小助手")
        
        self._pet_size: int = UIConfig.DEFAULT_PET_SIZE
        self._sound_enabled: bool = True
        self._auto_start: bool = False
        
        self._x: int = 0
        self._y: int = 0
        
        self._canvas: Optional[tk.Canvas] = None
        self._renderer: Optional[Renderer] = None
        self._current_pet: Optional[PetBase] = None
        self._current_pet_type: PetType = PetType.FANTASY
        self._current_skin: SkinColor = SkinColor.PASTEL_LAVENDER
        
        self._animation_engine: Optional[AnimationEngine] = None
        self._walk_controller: Optional[WalkController] = None
        self._behavior_engine: Optional[BehaviorEngine] = None
        
        self._drag_handler: Optional[DragHandler] = None
        self._context_menu: Optional[ContextMenu] = None
        self._settings_window: Optional[SettingsWindow] = None
        
        self._speech_bubble: Optional[SpeechBubble] = None
        self._emotion_display: Optional[EmotionDisplay] = None
        
        self._nurture_manager: Optional[NurtureManager] = None
        
        self._initialize()
    
    def _initialize(self):
        self._setup_window()
        self._create_canvas()
        self._create_pet()
        self._setup_engines()
        self._setup_nurture_system()
        self._setup_ui_components()
        self._bind_click_event()
        self._start_engines()
    
    def _setup_window(self):
        self._root.overrideredirect(True)
        self._root.attributes("-topmost", True)
        self._root.attributes("-transparentcolor", UIConfig.TRANSPARENT_COLOR)
        
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        
        self._x = screen_width - self._pet_size - UIConfig.DEFAULT_POSITION_OFFSET_X
        self._y = screen_height - self._pet_size - UIConfig.DEFAULT_POSITION_OFFSET_Y
        
        self._update_window_geometry()
    
    def _create_canvas(self):
        self._canvas = tk.Canvas(
            self._root,
            width=self._pet_size,
            height=self._pet_size,
            bg=UIConfig.TRANSPARENT_COLOR,
            highlightthickness=0
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._renderer = Renderer(self._canvas)
    
    def _create_pet(self):
        self._current_pet = PetFactory.create_pet(
            self._current_pet_type,
            self._current_skin
        )
        self._current_pet.size = self._pet_size
        self._current_pet.set_renderer(self._renderer)
        
        if self._nurture_manager is not None:
            self._current_pet.set_nurture_manager(self._nurture_manager)
    
    def _setup_engines(self):
        self._animation_engine = AnimationEngine(
            self._root,
            self._on_frame_update
        )
        
        self._walk_controller = WalkController(
            self._root,
            self._on_position_update,
            self._get_screen_size,
            self._get_pet_size
        )
        self._walk_controller.set_position(self._x, self._y)
        
        self._behavior_engine = BehaviorEngine(
            self._root,
            self._on_state_change,
            self._on_start_walk
        )
    
    def _setup_nurture_system(self):
        self._nurture_manager = NurtureManager(
            self._root,
            on_attribute_change=self._on_nurture_attribute_change,
            on_state_suggestion=self._on_nurture_state_suggestion,
            on_level_up=self._on_nurture_level_up
        )
        
        save_dir = self._get_save_directory()
        self._nurture_manager.load(save_dir)
        
        if self._behavior_engine is not None:
            self._behavior_engine.set_nurture_manager(self._nurture_manager)
        
        if self._current_pet is not None:
            self._current_pet.set_nurture_manager(self._nurture_manager)
    
    def _get_save_directory(self) -> str:
        return os.path.dirname(os.path.abspath(__file__))
    
    def _on_nurture_attribute_change(self, attr_name: str, old_value: int, new_value: int):
        pass
    
    def _on_nurture_state_suggestion(self, state: PetState):
        pass
    
    def _on_nurture_level_up(self, level: int):
        if self._speech_bubble is not None:
            self._speech_bubble.show(f"升级啦！现在是 {level} 级！", 5000, "happy")
        
        if self._emotion_display is not None:
            self._emotion_display.show("star", 3000, 5)
    
    def _setup_ui_components(self):
        self._drag_handler = DragHandler(
            self._root,
            self._canvas,
            self._on_drag_start,
            self._on_drag_end,
            self._on_position_update
        )
        self._drag_handler.set_position(self._x, self._y)
        
        self._context_menu = ContextMenu(
            self._root,
            self._canvas,
            self._on_pet_change,
            self._on_skin_change,
            self._show_settings,
            self._quit
        )
        
        self._settings_window = SettingsWindow(
            self._root,
            self._pet_size,
            self._sound_enabled,
            self._auto_start,
            self._on_size_change,
            self._on_sound_toggle,
            self._on_autostart_toggle
        )
        
        self._speech_bubble = SpeechBubble(
            self._root,
            self._pet_size,
            self._get_pet_position
        )
        self._emotion_display = EmotionDisplay(
            self._root,
            self._pet_size,
            self._get_pet_position
        )
    
    def _bind_click_event(self):
        self._canvas.bind("<Button-1>", self._on_click, add="+")
        self._canvas.bind("<Double-Button-1>", self._on_double_click, add="+")
        self._canvas.bind("<Button-2>", self._on_middle_click, add="+")
    
    def _start_engines(self):
        self._animation_engine.start()
        self._behavior_engine.start()
        if self._nurture_manager is not None:
            self._nurture_manager.start()
    
    def _on_frame_update(self):
        if self._current_pet is None:
            return
        
        self._current_pet.frame_index = self._animation_engine.frame_index
        self._current_pet.draw()
    
    def _on_position_update(self, x: int, y: int):
        self._x = x
        self._y = y
        self._update_window_geometry()
        
        if self._speech_bubble is not None and self._speech_bubble.is_visible:
            self._speech_bubble.update_position()
        
        if self._emotion_display is not None and self._emotion_display.is_visible:
            self._emotion_display.update_position()
    
    def _on_state_change(self, state: PetState):
        if self._current_pet is not None:
            self._current_pet.state = state
    
    def _on_start_walk(self, distance: int, direction: Direction):
        self._walk_controller.start_walk(distance, direction)
    
    def _on_click(self, event: tk.Event):
        if self._drag_handler.is_dragging:
            return
        
        self._behavior_engine.trigger_interaction(PetState.HAPPY)
        
        if self._nurture_manager is not None:
            self._nurture_manager.pet()
        
        if self._current_pet is not None and hasattr(self._current_pet, 'trigger_pulse'):
            self._current_pet.trigger_pulse()
        
        if self._speech_bubble is not None:
            self._speech_bubble.show_random("happy", 3000)
        
        if self._emotion_display is not None:
            self._emotion_display.show("heart", 2000, 3)
        
        if self._sound_enabled:
            self._play_click_sound()
    
    def _on_double_click(self, event: tk.Event):
        if self._drag_handler.is_dragging:
            return
        
        if self._nurture_manager is not None:
            success = self._nurture_manager.feed()
            if success:
                self._behavior_engine.trigger_interaction(PetState.HAPPY)
                
                if self._current_pet is not None and hasattr(self._current_pet, 'trigger_pulse'):
                    self._current_pet.trigger_pulse()
                
                if self._speech_bubble is not None:
                    self._speech_bubble.show("好吃！谢谢主人~", 3000, "happy")
                
                if self._emotion_display is not None:
                    self._emotion_display.show("star", 2000, 3)
                
                if self._sound_enabled:
                    self._play_click_sound()
    
    def _on_middle_click(self, event: tk.Event):
        if self._drag_handler.is_dragging:
            return
        
        if self._nurture_manager is not None:
            success = self._nurture_manager.rest()
            if success:
                self._behavior_engine.trigger_interaction(PetState.SLEEP, duration=3000)
                
                if self._speech_bubble is not None:
                    self._speech_bubble.show("休息一下~ zzz", 3000, "tired")
                
                if self._emotion_display is not None:
                    self._emotion_display.show("sleep", 2000, 2)
    
    def _play_click_sound(self):
        try:
            winsound.Beep(SoundConfig.CLICK_FREQUENCY, SoundConfig.CLICK_DURATION)
        except Exception:
            pass
    
    def _on_drag_start(self):
        self._behavior_engine.stop()
        self._walk_controller.stop_walk()
    
    def _on_drag_end(self):
        self._root.after(
            AnimationConfig.POST_DRAG_DELAY,
            self._behavior_engine.start
        )
    
    def _on_pet_change(self, pet_type: PetType):
        self._current_pet_type = pet_type
        self._create_pet()
        if self._current_pet is not None:
            self._current_pet.state = self._behavior_engine.current_state
            self._current_pet.draw()
    
    def _on_skin_change(self, skin_color: SkinColor):
        self._current_skin = skin_color
        if self._current_pet is not None:
            self._current_pet.skin_color = skin_color
            self._current_pet.draw()
    
    def _on_size_change(self, size: int):
        self._pet_size = size
        self._update_window_geometry()
        self._canvas.config(width=self._pet_size, height=self._pet_size)
        
        if self._current_pet is not None:
            self._current_pet.size = self._pet_size
            self._current_pet.draw()
        
        if self._speech_bubble is not None:
            self._speech_bubble.hide()
        
        if self._emotion_display is not None:
            self._emotion_display.hide()
    
    def _on_sound_toggle(self, enabled: bool):
        self._sound_enabled = enabled
    
    def _on_autostart_toggle(self, enabled: bool):
        self._auto_start = enabled
    
    def _show_settings(self):
        self._settings_window.show()
    
    def _quit(self):
        if self._nurture_manager is not None:
            self._nurture_manager.stop()
            save_dir = self._get_save_directory()
            self._nurture_manager.save(save_dir)
        
        self._animation_engine.stop()
        self._walk_controller.stop()
        self._behavior_engine.stop()
        self._root.quit()
    
    def _update_window_geometry(self):
        self._root.geometry(
            f"{self._pet_size}x{self._pet_size}+{self._x}+{self._y}"
        )
    
    def _get_screen_size(self) -> Tuple[int, int]:
        return (
            self._root.winfo_screenwidth(),
            self._root.winfo_screenheight()
        )
    
    def _get_pet_size(self) -> int:
        return self._pet_size
    
    def _get_pet_position(self) -> Tuple[int, int]:
        return (self._x, self._y)
    
    def run(self):
        self._root.mainloop()