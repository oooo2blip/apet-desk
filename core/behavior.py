import tkinter as tk
import random
from typing import Optional, Callable, List
from core.config import (
    PetState,
    AnimationConfig,
    Direction
)


class BehaviorEngine:
    def __init__(
        self,
        root: tk.Tk,
        on_state_change: Callable[[PetState], None],
        on_start_walk: Callable[[int, Direction], None]
    ):
        self._root = root
        self._on_state_change = on_state_change
        self._on_start_walk = on_start_walk
        
        self._behavior_timer: Optional[str] = None
        self._is_running: bool = False
        self._current_state: PetState = PetState.IDLE
        self._available_behaviors: List[PetState] = [
            PetState.IDLE,
            PetState.WALK,
            PetState.SLEEP,
            PetState.HAPPY,
            PetState.JUMP
        ]
    
    @property
    def current_state(self) -> PetState:
        return self._current_state
    
    def start(self):
        if self._is_running:
            return
        self._is_running = True
        self._schedule_next_behavior()
    
    def stop(self):
        self._is_running = False
        if self._behavior_timer is not None:
            self._root.after_cancel(self._behavior_timer)
            self._behavior_timer = None
    
    def trigger_interaction(self, interaction_state: PetState = PetState.HAPPY, duration: int = AnimationConfig.INTERACTION_DURATION):
        self.stop()
        self._current_state = interaction_state
        self._on_state_change(interaction_state)
        
        self._root.after(duration, self._restore_idle)
    
    def _restore_idle(self):
        if not self._is_running:
            self._current_state = PetState.IDLE
            self._on_state_change(PetState.IDLE)
            self.start()
    
    def _get_state_duration(self, state: PetState) -> int:
        if state == PetState.JUMP:
            return random.randint(
                AnimationConfig.JUMP_DURATION_MIN,
                AnimationConfig.JUMP_DURATION_MAX
            )
        elif state == PetState.HAPPY:
            return random.randint(
                AnimationConfig.HAPPY_DURATION_MIN,
                AnimationConfig.HAPPY_DURATION_MAX
            )
        elif state == PetState.SLEEP:
            return random.randint(
                AnimationConfig.SLEEP_DURATION_MIN,
                AnimationConfig.SLEEP_DURATION_MAX
            )
        else:
            return random.randint(
                AnimationConfig.IDLE_STATE_DURATION_MIN,
                AnimationConfig.IDLE_STATE_DURATION_MAX
            )
    
    def _schedule_next_behavior(self):
        if not self._is_running:
            return
        
        duration = self._get_state_duration(self._current_state)
        self._behavior_timer = self._root.after(duration, self._select_next_behavior)
    
    def _select_next_behavior(self):
        if not self._is_running:
            return
        
        behavior = random.choice(self._available_behaviors)
        
        if behavior == PetState.WALK:
            self._current_state = PetState.WALK
            self._on_state_change(PetState.WALK)
            
            distance = random.randint(
                AnimationConfig.WALK_DISTANCE_MIN,
                AnimationConfig.WALK_DISTANCE_MAX
            )
            direction = random.choice([Direction.RIGHT, Direction.LEFT])
            self._on_start_walk(distance, direction)
        
        elif behavior == PetState.SLEEP:
            self._current_state = PetState.SLEEP
            self._on_state_change(PetState.SLEEP)
        
        elif behavior == PetState.HAPPY:
            self._current_state = PetState.HAPPY
            self._on_state_change(PetState.HAPPY)
        
        elif behavior == PetState.JUMP:
            self._current_state = PetState.JUMP
            self._on_state_change(PetState.JUMP)
        
        else:
            self._current_state = PetState.IDLE
            self._on_state_change(PetState.IDLE)
        
        self._schedule_next_behavior()
    
    def add_behavior(self, state: PetState):
        if state not in self._available_behaviors:
            self._available_behaviors.append(state)
    
    def remove_behavior(self, state: PetState):
        if state in self._available_behaviors:
            self._available_behaviors.remove(state)