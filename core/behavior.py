import tkinter as tk
import random
from typing import Optional, Callable, List, Any
from core.config import (
    PetState,
    AnimationConfig,
    Direction,
    NurtureConfig
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
        
        self._nurture_manager: Optional[Any] = None
    
    def set_nurture_manager(self, nurture_manager: Any):
        self._nurture_manager = nurture_manager
    
    def _get_nurture_recommended_state(self) -> Optional[PetState]:
        if self._nurture_manager is None:
            return None
        
        return self._nurture_manager.get_recommended_state()
    
    def _should_override_behavior(self, recommended_state: PetState) -> bool:
        if recommended_state == PetState.SLEEP:
            return True
        return False
    
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
        
        recommended_state = self._get_nurture_recommended_state()
        
        if recommended_state is not None and self._should_override_behavior(recommended_state):
            self._apply_behavior(recommended_state)
            self._schedule_next_behavior()
            return
        
        behavior = self._select_weighted_behavior()
        self._apply_behavior(behavior)
        self._schedule_next_behavior()
    
    def _select_weighted_behavior(self) -> PetState:
        if self._nurture_manager is None:
            return random.choice(self._available_behaviors)
        
        attrs = self._nurture_manager.attributes
        weights = {}
        
        for behavior in self._available_behaviors:
            weights[behavior] = 1.0
        
        if attrs.mood >= 80:
            weights[PetState.HAPPY] = 3.0
            weights[PetState.JUMP] = 2.0
        
        if attrs.mood < 30:
            weights[PetState.HAPPY] = 0.2
            weights[PetState.JUMP] = 0.3
            weights[PetState.IDLE] = 2.0
        
        if attrs.energy < 40:
            weights[PetState.WALK] = 0.3
            weights[PetState.JUMP] = 0.2
            weights[PetState.SLEEP] = 2.0
        
        if attrs.hunger < 40:
            weights[PetState.WALK] = 0.4
            weights[PetState.JUMP] = 0.4
            weights[PetState.IDLE] = 1.5
        
        behaviors = list(weights.keys())
        total_weight = sum(weights.values())
        r = random.uniform(0, total_weight)
        
        cumulative = 0.0
        for behavior in behaviors:
            cumulative += weights[behavior]
            if r <= cumulative:
                return behavior
        
        return random.choice(self._available_behaviors)
    
    def _apply_behavior(self, behavior: PetState):
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
    
    def add_behavior(self, state: PetState):
        if state not in self._available_behaviors:
            self._available_behaviors.append(state)
    
    def remove_behavior(self, state: PetState):
        if state in self._available_behaviors:
            self._available_behaviors.remove(state)