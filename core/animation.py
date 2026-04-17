import tkinter as tk
from typing import Optional, Callable, Any
from core.config import (
    AnimationConfig,
    PetState,
    Direction
)


class AnimationEngine:
    def __init__(self, root: tk.Tk, on_frame_update: Callable[[], None]):
        self._root = root
        self._on_frame_update = on_frame_update
        self._animation_speed: int = AnimationConfig.DEFAULT_ANIMATION_SPEED
        self._frame_index: int = 0
        self._animation_timer: Optional[str] = None
        self._is_running: bool = False
    
    @property
    def frame_index(self) -> int:
        return self._frame_index
    
    @property
    def animation_speed(self) -> int:
        return self._animation_speed
    
    @animation_speed.setter
    def animation_speed(self, value: int):
        self._animation_speed = max(50, value)
    
    def start(self):
        if self._is_running:
            return
        self._is_running = True
        self._schedule_next_frame()
    
    def stop(self):
        if self._animation_timer is not None:
            self._root.after_cancel(self._animation_timer)
            self._animation_timer = None
        self._is_running = False
    
    def _schedule_next_frame(self):
        if not self._is_running:
            return
        self._animation_timer = self._root.after(
            self._animation_speed,
            self._update_frame
        )
    
    def _update_frame(self):
        self._frame_index += 1
        self._on_frame_update()
        self._schedule_next_frame()
    
    def reset(self):
        self._frame_index = 0


class WalkController:
    def __init__(
        self,
        root: tk.Tk,
        on_position_update: Callable[[int, int], None],
        get_screen_size: Callable[[], tuple[int, int]],
        get_pet_size: Callable[[], int]
    ):
        self._root = root
        self._on_position_update = on_position_update
        self._get_screen_size = get_screen_size
        self._get_pet_size = get_pet_size
        
        self._x: int = 0
        self._y: int = 0
        self._direction: Direction = Direction.RIGHT
        self._walk_distance: int = 0
        self._walk_timer: Optional[str] = None
        self._is_walking: bool = False
        self._is_running: bool = False
    
    @property
    def is_walking(self) -> bool:
        return self._is_walking
    
    @property
    def direction(self) -> Direction:
        return self._direction
    
    def set_position(self, x: int, y: int):
        self._x = x
        self._y = y
    
    def start_walk(self, distance: int, direction: Direction):
        self._walk_distance = distance
        self._direction = direction
        self._is_walking = True
        
        if not self._is_running:
            self._is_running = True
            self._schedule_next_step()
    
    def stop_walk(self):
        self._is_walking = False
        self._walk_distance = 0
    
    def stop(self):
        self._is_walking = False
        self._is_running = False
        if self._walk_timer is not None:
            self._root.after_cancel(self._walk_timer)
            self._walk_timer = None
    
    def _schedule_next_step(self):
        if not self._is_running:
            return
        self._walk_timer = self._root.after(
            AnimationConfig.WALK_UPDATE_INTERVAL,
            self._update_walk
        )
    
    def _update_walk(self):
        if self._is_walking and self._walk_distance > 0:
            step = AnimationConfig.WALK_STEP
            self._x += self._direction.value * step
            self._walk_distance -= step
            
            screen_width, screen_height = self._get_screen_size()
            pet_size = self._get_pet_size()
            
            if self._x < 0:
                self._x = 0
                self._direction = Direction.RIGHT
            elif self._x > screen_width - pet_size:
                self._x = screen_width - pet_size
                self._direction = Direction.LEFT
            
            self._on_position_update(self._x, self._y)
        
        self._schedule_next_step()