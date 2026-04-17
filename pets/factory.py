from typing import Dict, Type, List, Optional
from pets.base import PetBase
from pets.cat import CatPet
from pets.dog import DogPet
from pets.rabbit import RabbitPet
from pets.fantasy import FantasyPet
from core.config import (
    PetType,
    SkinColor,
    ColorPalette,
    PetDisplayNames
)


class PetFactory:
    _registry: Dict[PetType, Type[PetBase]] = {
        PetType.CAT: CatPet,
        PetType.DOG: DogPet,
        PetType.RABBIT: RabbitPet,
        PetType.FANTASY: FantasyPet
    }
    
    @classmethod
    def register_pet(cls, pet_type: PetType, pet_class: Type[PetBase]):
        cls._registry[pet_type] = pet_class
    
    @classmethod
    def create_pet(cls, pet_type: PetType, skin_color: SkinColor = SkinColor.ORANGE) -> PetBase:
        pet_class = cls._registry.get(pet_type)
        if pet_class is None:
            raise ValueError(f"Unknown pet type: {pet_type}")
        return pet_class(skin_color)
    
    @classmethod
    def get_available_pet_types(cls) -> List[PetType]:
        return list(cls._registry.keys())
    
    @classmethod
    def get_pet_display_name(cls, pet_type: PetType) -> str:
        return PetDisplayNames.PET_NAMES.get(pet_type, str(pet_type.value))
    
    @classmethod
    def get_skin_display_name(cls, skin_color: SkinColor) -> str:
        return PetDisplayNames.SKIN_NAMES.get(skin_color, str(skin_color.value))


class SkinManager:
    _default_skin: SkinColor = SkinColor.ORANGE
    
    @classmethod
    def get_available_skins(cls) -> List[SkinColor]:
        return list(ColorPalette.SKIN_COLORS.keys())
    
    @classmethod
    def get_skin_hex(cls, skin_color: SkinColor) -> str:
        return ColorPalette.SKIN_COLORS.get(skin_color, ColorPalette.SKIN_COLORS[cls._default_skin])
    
    @classmethod
    def get_default_skin(cls) -> SkinColor:
        return cls._default_skin
    
    @classmethod
    def register_skin(cls, skin_color: SkinColor, hex_color: str, display_name: str):
        ColorPalette.SKIN_COLORS[skin_color] = hex_color
        PetDisplayNames.SKIN_NAMES[skin_color] = display_name