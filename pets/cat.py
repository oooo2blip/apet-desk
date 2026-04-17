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


class CatPet(PetBase):
    PET_TYPE = PetType.CAT
    DISPLAY_NAME = PetDisplayNames.PET_NAMES[PetType.CAT]
    
    def _draw_idle(self, center: int):
        self._draw_cat_body(center)
        self._draw_cat_head(center)
        self._draw_cat_ears(center)
        self._draw_cat_eyes_idle(center)
        self._draw_cat_nose_mouth(center)
        self._draw_cat_whiskers(center)
        self._draw_cat_tail_idle(center)
    
    def _draw_walk(self, center: int):
        self._draw_cat_body(center)
        self._draw_cat_head(center)
        self._draw_cat_ears(center)
        self._draw_cat_eyes_open(center)
        self._draw_cat_nose_mouth(center)
        self._draw_cat_legs_walk(center)
        self._draw_cat_tail_walk(center)
    
    def _draw_happy(self, center: int):
        jump_offset = self._get_happy_jump_offset()
        
        self._draw_cat_body(center, jump_offset)
        self._draw_cat_head_happy(center, jump_offset)
        self._draw_cat_ears_happy(center, jump_offset)
        self._draw_cat_eyes_happy(center, jump_offset)
        self._draw_cat_nose_mouth_happy(center, jump_offset)
        self._draw_cat_blush(center, jump_offset)
        self._draw_cat_tail_happy(center, jump_offset)
    
    def _draw_sleep(self, center: int):
        self._draw_cat_body_sleep(center)
        self._draw_cat_head_sleep(center)
        self._draw_cat_ear_sleep(center)
        self._draw_cat_eyes_sleep(center)
        self._draw_cat_zzz(center)
    
    def _draw_jump(self, center: int):
        jump_height = 20 if self._frame_index % 4 < 2 else 0
        
        self._draw_cat_body(center, -jump_height)
        self._draw_cat_head(center, -jump_height)
        self._draw_cat_ears(center, -jump_height)
        self._draw_cat_eyes_surprised(center, -jump_height)
        self._draw_cat_mouth_surprised(center, -jump_height)
        self._draw_cat_legs_jump(center)
        self._draw_cat_tail_jump(center, -jump_height)
    
    def _draw_cat_body(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 30, center - 10 + y_offset,
            center + 30, center + 25 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_cat_head(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 25, center - 40 + y_offset,
            center + 25, center - 10 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_cat_head_happy(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 28, center - 42 + y_offset,
            center + 28, center - 8 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_cat_ears(self, center: int, y_offset: int = 0):
        self._renderer.draw_polygon(
            [center - 20, center - 35 + y_offset,
             center - 30, center - 50 + y_offset,
             center - 10, center - 45 + y_offset],
            fill=self.skin_hex
        )
        self._renderer.draw_polygon(
            [center + 20, center - 35 + y_offset,
             center + 30, center - 50 + y_offset,
             center + 10, center - 45 + y_offset],
            fill=self.skin_hex
        )
    
    def _draw_cat_ears_happy(self, center: int, y_offset: int = 0):
        self._renderer.draw_polygon(
            [center - 22, center - 37 + y_offset,
             center - 32, center - 52 + y_offset,
             center - 12, center - 47 + y_offset],
            fill=self.skin_hex
        )
        self._renderer.draw_polygon(
            [center + 22, center - 37 + y_offset,
             center + 32, center - 52 + y_offset,
             center + 12, center - 47 + y_offset],
            fill=self.skin_hex
        )
    
    def _draw_cat_eyes_idle(self, center: int):
        eye_y = center - 28
        if self._should_blink():
            self._renderer.draw_closed_eye(center - 12, eye_y, center - 8, eye_y, width=2)
            self._renderer.draw_closed_eye(center + 8, eye_y, center + 12, eye_y, width=2)
        else:
            self._renderer.draw_open_eye(center - 12, eye_y - 2, center - 8, eye_y + 2)
            self._renderer.draw_open_eye(center + 8, eye_y - 2, center + 12, eye_y + 2)
    
    def _draw_cat_eyes_open(self, center: int):
        eye_y = center - 28
        self._renderer.draw_open_eye(center - 12, eye_y - 2, center - 8, eye_y + 2)
        self._renderer.draw_open_eye(center + 8, eye_y - 2, center + 12, eye_y + 2)
    
    def _draw_cat_eyes_happy(self, center: int, y_offset: int = 0):
        eye_y = center - 28 + y_offset
        self._renderer.draw_happy_eye(center - 14, eye_y - 4, center - 6, eye_y + 4, width=2)
        self._renderer.draw_happy_eye(center + 6, eye_y - 4, center + 14, eye_y + 4, width=2)
    
    def _draw_cat_eyes_sleep(self, center: int):
        eye_y = center - 13
        self._renderer.draw_closed_eye(center - 22, eye_y, center - 15, eye_y, width=2)
        self._renderer.draw_closed_eye(center - 8, eye_y, center - 1, eye_y, width=2)
    
    def _draw_cat_eyes_surprised(self, center: int, y_offset: int = 0):
        eye_y = center - 28 + y_offset
        self._renderer.draw_open_eye(center - 12, eye_y - 3, center - 8, eye_y + 3)
        self._renderer.draw_open_eye(center + 8, eye_y - 3, center + 12, eye_y + 3)
    
    def _draw_cat_nose_mouth(self, center: int):
        self._renderer.draw_pink_nose(center - 2, center - 20, center + 2, center - 17)
        self._renderer.draw_smile_arc(center - 8, center - 18, center + 8, center - 12)
    
    def _draw_cat_nose_mouth_happy(self, center: int, y_offset: int = 0):
        self._renderer.draw_pink_nose(center - 2, center - 20 + y_offset, center + 2, center - 17 + y_offset)
        self._renderer.draw_smile_arc(center - 12, center - 22 + y_offset, center + 12, center - 8 + y_offset, width=2)
    
    def _draw_cat_mouth_surprised(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(center - 4, center - 18 + y_offset, center + 4, center - 12 + y_offset, 
                                   fill=ColorPalette.BLACK)
    
    def _draw_cat_whiskers(self, center: int):
        self._renderer.draw_line(center - 25, center - 18, center - 8, center - 20, width=1)
        self._renderer.draw_line(center - 25, center - 15, center - 8, center - 17, width=1)
        self._renderer.draw_line(center + 8, center - 20, center + 25, center - 18, width=1)
        self._renderer.draw_line(center + 8, center - 17, center + 25, center - 15, width=1)
    
    def _draw_cat_blush(self, center: int, y_offset: int = 0):
        self._renderer.draw_blush(center - 22, center - 22 + y_offset, center - 16, center - 16 + y_offset)
        self._renderer.draw_blush(center + 16, center - 22 + y_offset, center + 22, center - 16 + y_offset)
    
    def _draw_cat_tail_idle(self, center: int):
        tail_x = center + 35
        tail_y = center + 10
        tail_wave = 5 if self._frame_index % 10 < 5 else -5
        self._renderer.draw_line(tail_x, tail_y, tail_x + 15, tail_y + tail_wave, 
                                   width=4, fill=self.skin_hex, smooth=True)
    
    def _draw_cat_tail_walk(self, center: int):
        tail_x = center + 35
        tail_y = center + 10
        tail_wave = 8 if self._frame_index % 4 < 2 else -8
        self._renderer.draw_line(tail_x, tail_y, tail_x + 15, tail_y + tail_wave, 
                                   width=4, fill=self.skin_hex, smooth=True)
    
    def _draw_cat_tail_happy(self, center: int, y_offset: int = 0):
        tail_x = center + 35
        tail_y = center + 10 + y_offset
        tail_wave = 10 if self._frame_index % 2 == 0 else -10
        self._renderer.draw_line(tail_x, tail_y, tail_x + 18, tail_y + tail_wave, 
                                   width=4, fill=self.skin_hex, smooth=True)
    
    def _draw_cat_tail_jump(self, center: int, y_offset: int = 0):
        tail_x = center + 35
        tail_y = center + 10 + y_offset
        self._renderer.draw_line(tail_x, tail_y, tail_x + 20, tail_y, 
                                   width=4, fill=self.skin_hex, smooth=True)
    
    def _draw_cat_legs_walk(self, center: int):
        leg_offset = 5 if self._frame_index % 4 < 2 else -5
        self._renderer.draw_line(center - 15, center + 25, center - 15, center + 35 + leg_offset, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center - 5, center + 25, center - 5, center + 35 - leg_offset, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center + 5, center + 25, center + 5, center + 35 + leg_offset, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center + 15, center + 25, center + 15, center + 35 - leg_offset, 
                                   width=4, fill=self.skin_hex)
    
    def _draw_cat_legs_jump(self, center: int):
        self._renderer.draw_line(center - 15, center + 25, center - 20, center + 40, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center - 5, center + 25, center - 10, center + 40, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center + 5, center + 25, center + 10, center + 40, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center + 15, center + 25, center + 20, center + 40, 
                                   width=4, fill=self.skin_hex)
    
    def _draw_cat_body_sleep(self, center: int):
        self._renderer.draw_oval(center - 35, center - 5, center + 25, center + 30, 
                                   fill=self.skin_hex)
    
    def _draw_cat_head_sleep(self, center: int):
        self._renderer.draw_oval(center - 30, center - 25, center, center + 5, 
                                   fill=self.skin_hex)
    
    def _draw_cat_ear_sleep(self, center: int):
        self._renderer.draw_polygon(
            [center - 25, center - 20, center - 35, center - 35, center - 15, center - 30],
            fill=self.skin_hex
        )
    
    def _draw_cat_zzz(self, center: int):
        z_level = self._get_z_level()
        self._renderer.draw_zzz(center, center, z_level)