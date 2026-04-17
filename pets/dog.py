from typing import Optional
from pets.base import PetBase
from core.config import (
    PetState,
    SkinColor,
    ColorPalette,
    PetType,
    PetDisplayNames,
    AnimationFrames
)


class DogPet(PetBase):
    PET_TYPE = PetType.DOG
    DISPLAY_NAME = PetDisplayNames.PET_NAMES[PetType.DOG]
    
    def _draw_idle(self, center: int):
        self._draw_dog_body(center)
        self._draw_dog_head(center)
        self._draw_dog_ears(center)
        self._draw_dog_ears_inner(center)
        self._draw_dog_eyebrows(center)
        self._draw_dog_eyes_idle(center)
        self._draw_dog_nose(center)
        self._draw_dog_mouth(center)
        self._draw_dog_tail_idle(center)
    
    def _draw_walk(self, center: int):
        self._draw_dog_body(center)
        self._draw_dog_head(center)
        self._draw_dog_ears(center)
        self._draw_dog_ears_inner(center)
        self._draw_dog_eyes_open(center)
        self._draw_dog_nose(center)
        self._draw_dog_mouth_with_tongue(center)
        self._draw_dog_legs_walk(center)
        self._draw_dog_paws(center)
        self._draw_dog_tail_walk(center)
    
    def _draw_happy(self, center: int):
        jump_offset = self._get_happy_jump_offset()
        head_offset = -3 if self._frame_index % 4 < 2 else 0
        
        self._draw_dog_body(center, jump_offset)
        self._draw_dog_head_happy(center, head_offset, jump_offset)
        self._draw_dog_ears_happy(center, head_offset, jump_offset)
        self._draw_dog_eyes_happy(center, head_offset, jump_offset)
        self._draw_dog_nose_happy(center, head_offset, jump_offset)
        self._draw_dog_mouth_happy(center, head_offset, jump_offset)
        self._draw_dog_blush(center, head_offset, jump_offset)
        self._draw_dog_tail_happy(center, jump_offset)
    
    def _draw_sleep(self, center: int):
        breath_offset = self._get_breath_offset()
        
        self._draw_dog_body_sleep(center, breath_offset)
        self._draw_dog_head_sleep(center)
        self._draw_dog_ear_sleep(center)
        self._draw_dog_eyes_sleep(center)
        self._draw_dog_nose_sleep(center)
        self._draw_dog_zzz(center)
    
    def _draw_jump(self, center: int):
        jump_height = 25 if self._frame_index % 4 < 2 else 0
        
        self._draw_dog_body(center, -jump_height)
        self._draw_dog_head(center, -jump_height)
        self._draw_dog_ears_jump(center, -jump_height)
        self._draw_dog_eyes_surprised(center, -jump_height)
        self._draw_dog_mouth_surprised(center, -jump_height)
        self._draw_dog_legs_jump(center)
        self._draw_dog_tail_jump(center, -jump_height)
    
    def _draw_dog_body(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 32, center - 8 + y_offset,
            center + 32, center + 28 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_dog_head(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 28, center - 42 + y_offset,
            center + 28, center - 8 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_dog_head_happy(self, center: int, head_offset: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 28, center - 45 + head_offset + y_offset,
            center + 28, center - 11 + head_offset + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_dog_ears(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 35, center - 40 + y_offset,
            center - 20, center - 20 + y_offset,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 20, center - 40 + y_offset,
            center + 35, center - 20 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_dog_ears_inner(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 33, center - 38 + y_offset,
            center - 22, center - 22 + y_offset,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
        self._renderer.draw_oval(
            center + 22, center - 38 + y_offset,
            center + 33, center - 22 + y_offset,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
    
    def _draw_dog_ears_happy(self, center: int, head_offset: int, y_offset: int = 0):
        ear_offset = -5 if self._frame_index % 4 < 2 else 0
        self._renderer.draw_oval(
            center - 35, center - 43 + ear_offset + head_offset + y_offset,
            center - 20, center - 23 + ear_offset + head_offset + y_offset,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 20, center - 43 + ear_offset + head_offset + y_offset,
            center + 35, center - 23 + ear_offset + head_offset + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_dog_ears_jump(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 38, center - 38 + y_offset,
            center - 23, center - 18 + y_offset,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 23, center - 38 + y_offset,
            center + 38, center - 18 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_dog_eyebrows(self, center: int, y_offset: int = 0):
        self._renderer.draw_arc(
            center - 18, center - 32 + y_offset,
            center - 10, center - 28 + y_offset,
            start=0, extent=180, style="arc", width=2
        )
        self._renderer.draw_arc(
            center + 10, center - 32 + y_offset,
            center + 18, center - 28 + y_offset,
            start=0, extent=180, style="arc", width=2
        )
    
    def _draw_dog_eyes_idle(self, center: int):
        eye_y = center - 26
        if self._should_blink():
            self._renderer.draw_closed_eye(center - 15, eye_y, center - 10, eye_y, width=2)
            self._renderer.draw_closed_eye(center + 10, eye_y, center + 15, eye_y, width=2)
        else:
            self._renderer.draw_open_eye(center - 15, eye_y - 3, center - 10, eye_y + 3, highlight=True)
            self._renderer.draw_open_eye(center + 10, eye_y - 3, center + 15, eye_y + 3, highlight=True)
    
    def _draw_dog_eyes_open(self, center: int):
        eye_y = center - 26
        self._renderer.draw_open_eye(center - 15, eye_y - 3, center - 10, eye_y + 3, highlight=True)
        self._renderer.draw_open_eye(center + 10, eye_y - 3, center + 15, eye_y + 3, highlight=True)
    
    def _draw_dog_eyes_happy(self, center: int, head_offset: int, y_offset: int = 0):
        eye_y = center - 29 + head_offset + y_offset
        self._renderer.draw_happy_eye(center - 17, eye_y - 5, center - 8, eye_y + 5, width=2)
        self._renderer.draw_happy_eye(center + 8, eye_y - 5, center + 17, eye_y + 5, width=2)
    
    def _draw_dog_eyes_sleep(self, center: int):
        eye_y = center - 2
        self._renderer.draw_closed_eye(center - 25, eye_y, center - 18, eye_y, width=2)
        self._renderer.draw_closed_eye(center - 12, eye_y + 2, center - 5, eye_y + 2, width=2)
    
    def _draw_dog_eyes_surprised(self, center: int, y_offset: int = 0):
        eye_y = center - 26 + y_offset
        self._renderer.draw_open_eye(center - 16, eye_y - 4, center - 9, eye_y + 4, highlight=True)
        self._renderer.draw_open_eye(center + 9, eye_y - 4, center + 16, eye_y + 4, highlight=True)
    
    def _draw_dog_nose(self, center: int, y_offset: int = 0):
        self._renderer.draw_black_nose(center - 6, center - 18 + y_offset, center + 6, center - 12 + y_offset)
    
    def _draw_dog_nose_happy(self, center: int, head_offset: int, y_offset: int = 0):
        self._renderer.draw_black_nose(
            center - 6, center - 20 + head_offset + y_offset, 
            center + 6, center - 14 + head_offset + y_offset
        )
    
    def _draw_dog_nose_sleep(self, center: int):
        self._renderer.draw_black_nose(center - 8, center + 5, center - 2, center + 10)
    
    def _draw_dog_mouth(self, center: int, y_offset: int = 0):
        self._renderer.draw_line(center, center - 12 + y_offset, center, center - 8 + y_offset, width=2)
        if self._is_tongue_out():
            self._renderer.draw_tongue(center - 3, center - 6 + y_offset, center + 3, center + 2 + y_offset)
    
    def _draw_dog_mouth_with_tongue(self, center: int):
        self._renderer.draw_line(center, center - 12, center, center - 8, width=2)
        self._renderer.draw_tongue(center - 3, center - 6, center + 3, center + 2)
    
    def _draw_dog_mouth_happy(self, center: int, head_offset: int, y_offset: int = 0):
        self._renderer.draw_smile_arc(
            center - 15, center - 18 + head_offset + y_offset, 
            center + 15, center - 2 + head_offset + y_offset, 
            width=2
        )
        self._renderer.draw_tongue(
            center - 5, center - 4 + head_offset + y_offset, 
            center + 5, center + 8 + head_offset + y_offset
        )
    
    def _draw_dog_mouth_surprised(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 5, center - 15 + y_offset, 
            center + 5, center - 5 + y_offset, 
            fill=ColorPalette.BLACK
        )
    
    def _draw_dog_blush(self, center: int, head_offset: int, y_offset: int = 0):
        self._renderer.draw_blush(
            center - 25, center - 24 + head_offset + y_offset, 
            center - 18, center - 18 + head_offset + y_offset
        )
        self._renderer.draw_blush(
            center + 18, center - 24 + head_offset + y_offset, 
            center + 25, center - 18 + head_offset + y_offset
        )
    
    def _draw_dog_tail_idle(self, center: int):
        tail_x = center + 35
        tail_y = center + 5
        tail_wave = 8 if self._frame_index % 6 < 3 else -8
        self._renderer.draw_arc(
            tail_x - 5, tail_y - 10, tail_x + 20, tail_y + 10,
            start=270, extent=180 + tail_wave, style="arc",
            width=4, outline=self.skin_hex
        )
    
    def _draw_dog_tail_walk(self, center: int):
        tail_x = center + 35
        tail_y = center + 5
        tail_wave = 15 if self._frame_index % 4 < 2 else -15
        self._renderer.draw_arc(
            tail_x - 5, tail_y - 12, tail_x + 22, tail_y + 8,
            start=270, extent=160 + tail_wave, style="arc",
            width=4, outline=self.skin_hex
        )
    
    def _draw_dog_tail_happy(self, center: int, y_offset: int = 0):
        tail_x = center + 35
        tail_y = center + 5 + y_offset
        tail_wave = 25 if self._frame_index % 2 == 0 else -25
        self._renderer.draw_arc(
            tail_x - 5, tail_y - 15, tail_x + 25, tail_y + 5,
            start=270, extent=140 + tail_wave, style="arc",
            width=4, outline=self.skin_hex
        )
    
    def _draw_dog_tail_jump(self, center: int, y_offset: int = 0):
        tail_x = center + 35
        tail_y = center + 5 + y_offset
        self._renderer.draw_arc(
            tail_x - 5, tail_y - 18, tail_x + 20, tail_y - 2,
            start=270, extent=120, style="arc",
            width=4, outline=self.skin_hex
        )
    
    def _draw_dog_legs_walk(self, center: int):
        leg_offset = 6 if self._frame_index % 4 < 2 else -6
        self._renderer.draw_line(center - 18, center + 28, center - 18, center + 40 + leg_offset, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center - 8, center + 28, center - 8, center + 40 - leg_offset, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center + 8, center + 28, center + 8, center + 40 + leg_offset, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center + 18, center + 28, center + 18, center + 40 - leg_offset, 
                                   width=5, fill=self.skin_hex)
    
    def _draw_dog_paws(self, center: int):
        leg_offset = 6 if self._frame_index % 4 < 2 else -6
        paw_color = ColorPalette.BROWN_DARK if self._skin_color != SkinColor.BLACK else ColorPalette.WHITE_LIGHT
        
        self._renderer.draw_oval(center - 22, center + 38 + leg_offset, center - 14, center + 43 + leg_offset, 
                                   fill=paw_color)
        self._renderer.draw_oval(center - 12, center + 38 - leg_offset, center - 4, center + 43 - leg_offset, 
                                   fill=paw_color)
        self._renderer.draw_oval(center + 4, center + 38 + leg_offset, center + 12, center + 43 + leg_offset, 
                                   fill=paw_color)
        self._renderer.draw_oval(center + 14, center + 38 - leg_offset, center + 22, center + 43 - leg_offset, 
                                   fill=paw_color)
    
    def _draw_dog_legs_jump(self, center: int):
        self._renderer.draw_line(center - 18, center + 28, center - 25, center + 45, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center - 8, center + 28, center - 5, center + 45, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center + 8, center + 28, center + 5, center + 45, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center + 18, center + 28, center + 25, center + 45, 
                                   width=5, fill=self.skin_hex)
    
    def _draw_dog_body_sleep(self, center: int, breath_offset: int = 0):
        self._renderer.draw_oval(center - 35, center, center + 35, center + 35, fill=self.skin_hex)
    
    def _draw_dog_head_sleep(self, center: int):
        self._renderer.draw_oval(center - 30, center - 15, center - 5, center + 15, fill=self.skin_hex)
    
    def _draw_dog_ear_sleep(self, center: int):
        self._renderer.draw_oval(center - 35, center - 20, center - 25, center - 5, fill=self.skin_hex)
    
    def _draw_dog_zzz(self, center: int):
        z_level = self._get_z_level()
        self._renderer.draw_zzz(center - 5, center, z_level)