import tkinter as tk
import json
import os
from typing import Optional, Callable, Dict, Any
from core.config import (
    NurtureConfig,
    PetState
)


class NurtureAttributes:
    def __init__(self):
        self._mood: int = NurtureConfig.DEFAULT_MOOD
        self._hunger: int = NurtureConfig.DEFAULT_HUNGER
        self._energy: int = NurtureConfig.DEFAULT_ENERGY
        self._affection: int = NurtureConfig.DEFAULT_AFFECTION
        self._level: int = NurtureConfig.DEFAULT_LEVEL
        self._experience: int = NurtureConfig.DEFAULT_EXPERIENCE
    
    @property
    def mood(self) -> int:
        return self._mood
    
    @mood.setter
    def mood(self, value: int):
        self._mood = max(0, min(NurtureConfig.MAX_MOOD, value))
    
    @property
    def hunger(self) -> int:
        return self._hunger
    
    @hunger.setter
    def hunger(self, value: int):
        self._hunger = max(0, min(NurtureConfig.MAX_HUNGER, value))
    
    @property
    def energy(self) -> int:
        return self._energy
    
    @energy.setter
    def energy(self, value: int):
        self._energy = max(0, min(NurtureConfig.MAX_ENERGY, value))
    
    @property
    def affection(self) -> int:
        return self._affection
    
    @affection.setter
    def affection(self, value: int):
        self._affection = max(0, min(NurtureConfig.MAX_AFFECTION, value))
    
    @property
    def level(self) -> int:
        return self._level
    
    @level.setter
    def level(self, value: int):
        self._level = max(1, min(NurtureConfig.MAX_LEVEL, value))
    
    @property
    def experience(self) -> int:
        return self._experience
    
    @experience.setter
    def experience(self, value: int):
        self._experience = max(0, value)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "mood": self._mood,
            "hunger": self._hunger,
            "energy": self._energy,
            "affection": self._affection,
            "level": self._level,
            "experience": self._experience
        }
    
    def from_dict(self, data: Dict[str, Any]):
        if "mood" in data:
            self._mood = data["mood"]
        if "hunger" in data:
            self._hunger = data["hunger"]
        if "energy" in data:
            self._energy = data["energy"]
        if "affection" in data:
            self._affection = data["affection"]
        if "level" in data:
            self._level = data["level"]
        if "experience" in data:
            self._experience = data["experience"]


class NurtureManager:
    def __init__(
        self,
        root: tk.Tk,
        on_attribute_change: Optional[Callable[[str, int, int], None]] = None,
        on_state_suggestion: Optional[Callable[[PetState], None]] = None,
        on_level_up: Optional[Callable[[int], None]] = None
    ):
        self._root = root
        self._attributes = NurtureAttributes()
        self._on_attribute_change = on_attribute_change
        self._on_state_suggestion = on_state_suggestion
        self._on_level_up = on_level_up
        
        self._hunger_timer: Optional[str] = None
        self._energy_timer: Optional[str] = None
        self._mood_timer: Optional[str] = None
        self._interaction_cooldown: bool = False
        self._is_running: bool = False
    
    @property
    def attributes(self) -> NurtureAttributes:
        return self._attributes
    
    @property
    def mood(self) -> int:
        return self._attributes.mood
    
    @property
    def hunger(self) -> int:
        return self._attributes.hunger
    
    @property
    def energy(self) -> int:
        return self._attributes.energy
    
    @property
    def affection(self) -> int:
        return self._attributes.affection
    
    @property
    def level(self) -> int:
        return self._attributes.level
    
    @property
    def experience(self) -> int:
        return self._attributes.experience
    
    def start(self):
        if self._is_running:
            return
        self._is_running = True
        self._start_decay_timers()
    
    def stop(self):
        self._is_running = False
        self._stop_decay_timers()
    
    def _start_decay_timers(self):
        self._hunger_timer = self._root.after(
            NurtureConfig.HUNGER_DECAY_INTERVAL,
            self._decay_hunger
        )
        self._energy_timer = self._root.after(
            NurtureConfig.ENERGY_DECAY_INTERVAL,
            self._decay_energy
        )
        self._mood_timer = self._root.after(
            NurtureConfig.MOOD_DECAY_INTERVAL,
            self._decay_mood
        )
    
    def _stop_decay_timers(self):
        if self._hunger_timer is not None:
            self._root.after_cancel(self._hunger_timer)
            self._hunger_timer = None
        if self._energy_timer is not None:
            self._root.after_cancel(self._energy_timer)
            self._energy_timer = None
        if self._mood_timer is not None:
            self._root.after_cancel(self._mood_timer)
            self._mood_timer = None
    
    def _decay_hunger(self):
        if not self._is_running:
            return
        
        old_value = self._attributes.hunger
        self._attributes.hunger -= NurtureConfig.HUNGER_DECAY_RATE
        new_value = self._attributes.hunger
        
        if old_value != new_value:
            self._notify_attribute_change("hunger", old_value, new_value)
            self._check_critical_state()
        
        self._hunger_timer = self._root.after(
            NurtureConfig.HUNGER_DECAY_INTERVAL,
            self._decay_hunger
        )
    
    def _decay_energy(self):
        if not self._is_running:
            return
        
        old_value = self._attributes.energy
        self._attributes.energy -= NurtureConfig.ENERGY_DECAY_RATE
        new_value = self._attributes.energy
        
        if old_value != new_value:
            self._notify_attribute_change("energy", old_value, new_value)
            self._check_critical_state()
        
        self._energy_timer = self._root.after(
            NurtureConfig.ENERGY_DECAY_INTERVAL,
            self._decay_energy
        )
    
    def _decay_mood(self):
        if not self._is_running:
            return
        
        old_value = self._attributes.mood
        self._attributes.mood -= NurtureConfig.MOOD_DECAY_RATE
        new_value = self._attributes.mood
        
        if old_value != new_value:
            self._notify_attribute_change("mood", old_value, new_value)
            self._check_critical_state()
        
        self._mood_timer = self._root.after(
            NurtureConfig.MOOD_DECAY_INTERVAL,
            self._decay_mood
        )
    
    def _notify_attribute_change(self, attr_name: str, old_value: int, new_value: int):
        if self._on_attribute_change is not None:
            self._on_attribute_change(attr_name, old_value, new_value)
    
    def _check_critical_state(self):
        if self._on_state_suggestion is None:
            return
        
        if self._attributes.hunger <= NurtureConfig.CRITICAL_HUNGER_THRESHOLD:
            self._on_state_suggestion(PetState.SLEEP)
        elif self._attributes.energy <= NurtureConfig.CRITICAL_ENERGY_THRESHOLD:
            self._on_state_suggestion(PetState.SLEEP)
        elif self._attributes.mood <= NurtureConfig.LOW_MOOD_THRESHOLD:
            self._on_state_suggestion(PetState.IDLE)
    
    def _add_experience(self, amount: int):
        old_exp = self._attributes.experience
        old_level = self._attributes.level
        
        self._attributes.experience += amount
        
        while (self._attributes.experience >= NurtureConfig.EXPERIENCE_PER_LEVEL and 
               self._attributes.level < NurtureConfig.MAX_LEVEL):
            self._attributes.experience -= NurtureConfig.EXPERIENCE_PER_LEVEL
            self._attributes.level += 1
            
            if self._on_level_up is not None:
                self._on_level_up(self._attributes.level)
        
        if old_exp != self._attributes.experience:
            self._notify_attribute_change("experience", old_exp, self._attributes.experience)
        if old_level != self._attributes.level:
            self._notify_attribute_change("level", old_level, self._attributes.level)
    
    def _set_cooldown(self):
        self._interaction_cooldown = True
        self._root.after(NurtureConfig.INTERACTION_COOLDOWN, self._reset_cooldown)
    
    def _reset_cooldown(self):
        self._interaction_cooldown = False
    
    def pet(self) -> bool:
        if self._interaction_cooldown:
            return False
        
        old_mood = self._attributes.mood
        old_affection = self._attributes.affection
        
        self._attributes.mood += NurtureConfig.PET_MOOD_BOOST
        self._attributes.affection += NurtureConfig.PET_AFFECTION_BOOST
        
        if old_mood != self._attributes.mood:
            self._notify_attribute_change("mood", old_mood, self._attributes.mood)
        if old_affection != self._attributes.affection:
            self._notify_attribute_change("affection", old_affection, self._attributes.affection)
        
        self._add_experience(NurtureConfig.PET_EXPERIENCE_BOOST)
        self._set_cooldown()
        
        return True
    
    def feed(self) -> bool:
        if self._interaction_cooldown:
            return False
        
        old_hunger = self._attributes.hunger
        old_mood = self._attributes.mood
        
        self._attributes.hunger += NurtureConfig.FEED_HUNGER_BOOST
        self._attributes.mood += NurtureConfig.FEED_MOOD_BOOST
        
        if old_hunger != self._attributes.hunger:
            self._notify_attribute_change("hunger", old_hunger, self._attributes.hunger)
        if old_mood != self._attributes.mood:
            self._notify_attribute_change("mood", old_mood, self._attributes.mood)
        
        self._add_experience(NurtureConfig.FEED_EXPERIENCE_BOOST)
        self._set_cooldown()
        
        return True
    
    def rest(self) -> bool:
        if self._interaction_cooldown:
            return False
        
        old_energy = self._attributes.energy
        old_mood = self._attributes.mood
        
        self._attributes.energy += NurtureConfig.REST_ENERGY_BOOST
        self._attributes.mood += NurtureConfig.REST_MOOD_BOOST
        
        if old_energy != self._attributes.energy:
            self._notify_attribute_change("energy", old_energy, self._attributes.energy)
        if old_mood != self._attributes.mood:
            self._notify_attribute_change("mood", old_mood, self._attributes.mood)
        
        self._add_experience(NurtureConfig.REST_EXPERIENCE_BOOST)
        self._set_cooldown()
        
        return True
    
    def get_recommended_state(self) -> PetState:
        if (self._attributes.hunger <= NurtureConfig.CRITICAL_HUNGER_THRESHOLD or
            self._attributes.energy <= NurtureConfig.CRITICAL_ENERGY_THRESHOLD):
            return PetState.SLEEP
        elif self._attributes.mood <= NurtureConfig.LOW_MOOD_THRESHOLD:
            return PetState.IDLE
        elif self._attributes.mood >= 80:
            return PetState.HAPPY
        else:
            return PetState.IDLE
    
    def can_do_intimate_action(self) -> bool:
        required_affection = NurtureConfig.AFFECTION_UNLOCK_LEVELS.get(self._attributes.level, 0)
        return self._attributes.affection >= required_affection
    
    def save(self, directory: str = "") -> bool:
        try:
            if not directory:
                directory = os.getcwd()
            
            file_path = os.path.join(directory, NurtureConfig.SAVE_FILE_NAME)
            data = self._attributes.to_dict()
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def load(self, directory: str = "") -> bool:
        try:
            if not directory:
                directory = os.getcwd()
            
            file_path = os.path.join(directory, NurtureConfig.SAVE_FILE_NAME)
            
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            old_data = self._attributes.to_dict()
            self._attributes.from_dict(data)
            
            if self._on_attribute_change is not None:
                new_data = self._attributes.to_dict()
                for key in old_data:
                    if old_data[key] != new_data[key]:
                        self._notify_attribute_change(key, old_data[key], new_data[key])
            
            return True
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        return self._attributes.to_dict()
    
    def from_dict(self, data: Dict[str, Any]):
        old_data = self._attributes.to_dict()
        self._attributes.from_dict(data)
        
        if self._on_attribute_change is not None:
            new_data = self._attributes.to_dict()
            for key in old_data:
                if old_data[key] != new_data[key]:
                    self._notify_attribute_change(key, old_data[key], new_data[key])