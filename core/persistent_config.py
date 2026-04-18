import json
import os
from typing import Dict, Any, Optional
from core.config import (
    UIConfig,
    PetType,
    SkinColor
)


class PersistentConfig:
    def __init__(self):
        self._pet_size: int = UIConfig.DEFAULT_PET_SIZE
        self._alpha: float = UIConfig.DEFAULT_ALPHA
        self._topmost: bool = UIConfig.DEFAULT_TOPMOST
        self._sound_enabled: bool = True
        self._auto_start: bool = False
        self._x: Optional[int] = None
        self._y: Optional[int] = None
        self._pet_type: PetType = PetType.CAT
        self._skin_color: SkinColor = SkinColor.ORANGE
        self._save_config: bool = UIConfig.DEFAULT_SAVE_CONFIG
    
    @property
    def pet_size(self) -> int:
        return self._pet_size
    
    @pet_size.setter
    def pet_size(self, value: int):
        self._pet_size = max(UIConfig.MIN_PET_SIZE, min(UIConfig.MAX_PET_SIZE, value))
    
    @property
    def alpha(self) -> float:
        return self._alpha
    
    @alpha.setter
    def alpha(self, value: float):
        self._alpha = max(UIConfig.MIN_ALPHA, min(UIConfig.MAX_ALPHA, value))
    
    @property
    def topmost(self) -> bool:
        return self._topmost
    
    @topmost.setter
    def topmost(self, value: bool):
        self._topmost = value
    
    @property
    def sound_enabled(self) -> bool:
        return self._sound_enabled
    
    @sound_enabled.setter
    def sound_enabled(self, value: bool):
        self._sound_enabled = value
    
    @property
    def auto_start(self) -> bool:
        return self._auto_start
    
    @auto_start.setter
    def auto_start(self, value: bool):
        self._auto_start = value
    
    @property
    def x(self) -> Optional[int]:
        return self._x
    
    @x.setter
    def x(self, value: Optional[int]):
        self._x = value
    
    @property
    def y(self) -> Optional[int]:
        return self._y
    
    @y.setter
    def y(self, value: Optional[int]):
        self._y = value
    
    @property
    def pet_type(self) -> PetType:
        return self._pet_type
    
    @pet_type.setter
    def pet_type(self, value: PetType):
        self._pet_type = value
    
    @property
    def skin_color(self) -> SkinColor:
        return self._skin_color
    
    @skin_color.setter
    def skin_color(self, value: SkinColor):
        self._skin_color = value
    
    @property
    def save_config(self) -> bool:
        return self._save_config
    
    @save_config.setter
    def save_config(self, value: bool):
        self._save_config = value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pet_size": self._pet_size,
            "alpha": self._alpha,
            "topmost": self._topmost,
            "sound_enabled": self._sound_enabled,
            "auto_start": self._auto_start,
            "x": self._x,
            "y": self._y,
            "pet_type": self._pet_type.value,
            "skin_color": self._skin_color.value,
            "save_config": self._save_config
        }
    
    def from_dict(self, data: Dict[str, Any]):
        if "pet_size" in data:
            self._pet_size = max(UIConfig.MIN_PET_SIZE, min(UIConfig.MAX_PET_SIZE, data["pet_size"]))
        if "alpha" in data:
            self._alpha = max(UIConfig.MIN_ALPHA, min(UIConfig.MAX_ALPHA, data["alpha"]))
        if "topmost" in data:
            self._topmost = data["topmost"]
        if "sound_enabled" in data:
            self._sound_enabled = data["sound_enabled"]
        if "auto_start" in data:
            self._auto_start = data["auto_start"]
        if "x" in data:
            self._x = data["x"]
        if "y" in data:
            self._y = data["y"]
        if "pet_type" in data:
            try:
                self._pet_type = PetType(data["pet_type"])
            except ValueError:
                self._pet_type = PetType.CAT
        if "skin_color" in data:
            try:
                self._skin_color = SkinColor(data["skin_color"])
            except ValueError:
                self._skin_color = SkinColor.ORANGE
        if "save_config" in data:
            self._save_config = data["save_config"]
    
    def save(self, directory: str = "") -> bool:
        if not self._save_config:
            return True
        
        try:
            if not directory:
                directory = os.getcwd()
            
            file_path = os.path.join(directory, UIConfig.CONFIG_FILE_NAME)
            data = self.to_dict()
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def load(self, directory: str = "") -> bool:
        try:
            if not directory:
                directory = os.getcwd()
            
            file_path = os.path.join(directory, UIConfig.CONFIG_FILE_NAME)
            
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.from_dict(data)
            return True
        except Exception:
            return False