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


class RabbitPet(PetBase):
    PET_TYPE = PetType.RABBIT
    DISPLAY_NAME = PetDisplayNames.PET_NAMES[PetType.RABBIT]
    
    def _draw_idle(self, center: int):
        self._draw_rabbit_body(center)
        self._draw_rabbit_head(center)
        self._draw_rabbit_ears_idle(center)
        self._draw_rabbit_eyes_idle(center)
        self._draw_rabbit_nose_mouth(center)
        self._draw_rabbit_whiskers(center)
        self._draw_rabbit_tail(center)
    
    def _draw_walk(self, center: int):
        self._draw_rabbit_body(center)
        self._draw_rabbit_head(center)
        self._draw_rabbit_ears_walk(center)
        self._draw_rabbit_eyes_open(center)
        self._draw_rabbit_nose_mouth(center)
        self._draw_rabbit_legs_walk(center)
        self._draw_rabbit_tail(center)
    
    def _draw_happy(self, center: int):
        jump_offset = self._get_happy_jump_offset()
        head_offset = -5 if self._frame_index % 4 < 2 else 0
        
        self._draw_rabbit_body(center, jump_offset)
        self._draw_rabbit_head_happy(center, head_offset, jump_offset)
        self._draw_rabbit_ears_happy(center, head_offset, jump_offset)
        self._draw_rabbit_eyes_happy(center, head_offset, jump_offset)
        self._draw_rabbit_nose_mouth_happy(center, head_offset, jump_offset)
        self._draw_rabbit_blush(center, head_offset, jump_offset)
        self._draw_rabbit_tail_happy(center, jump_offset)
    
    def _draw_sleep(self, center: int):
        breath_offset = self._get_breath_offset()
        
        self._draw_rabbit_body_sleep(center, breath_offset)
        self._draw_rabbit_head_sleep(center)
        self._draw_rabbit_ears_sleep(center)
        self._draw_rabbit_eyes_sleep(center)
        self._draw_rabbit_zzz(center)
    
    def _draw_jump(self, center: int):
        jump_height = 35 if self._frame_index % 4 < 2 else 0
        
        self._draw_rabbit_body(center, -jump_height)
        self._draw_rabbit_head(center, -jump_height)
        self._draw_rabbit_ears_jump(center, -jump_height)
        self._draw_rabbit_eyes_surprised(center, -jump_height)
        self._draw_rabbit_mouth_surprised(center, -jump_height)
        self._draw_rabbit_legs_jump(center)
        self._draw_rabbit_tail(center, -jump_height)
    
    def _draw_rabbit_body(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 25, center - 5 + y_offset,
            center + 25, center + 30 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_rabbit_head(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 20, center - 35 + y_offset,
            center + 20, center - 5 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_rabbit_head_happy(self, center: int, head_offset: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 20, center - 38 + head_offset + y_offset,
            center + 20, center - 8 + head_offset + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_rabbit_ears_idle(self, center: int):
        ear_left_wave = 3 if self._frame_index % 15 < 7 else -3
        ear_right_wave = -3 if self._frame_index % 15 < 7 else 3
        
        self._renderer.draw_oval(
            center - 18 + ear_left_wave, center - 65,
            center - 8 + ear_left_wave, center - 35,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center - 16 + ear_left_wave, center - 63,
            center - 10 + ear_left_wave, center - 37,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
        
        self._renderer.draw_oval(
            center + 8 + ear_right_wave, center - 65,
            center + 18 + ear_right_wave, center - 35,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 10 + ear_right_wave, center - 63,
            center + 16 + ear_right_wave, center - 37,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
    
    def _draw_rabbit_ears_walk(self, center: int):
        ear_wave = 5 if self._frame_index % 4 < 2 else -5
        
        self._renderer.draw_oval(
            center - 18 + ear_wave, center - 65,
            center - 8 + ear_wave, center - 35,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center - 16 + ear_wave, center - 63,
            center - 10 + ear_wave, center - 37,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
        
        self._renderer.draw_oval(
            center + 8 - ear_wave, center - 65,
            center + 18 - ear_wave, center - 35,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 10 - ear_wave, center - 63,
            center + 16 - ear_wave, center - 37,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
    
    def _draw_rabbit_ears_happy(self, center: int, head_offset: int, y_offset: int = 0):
        ear_joy = 8 if self._frame_index % 2 == 0 else -8
        
        self._renderer.draw_oval(
            center - 18 + ear_joy, center - 68 + head_offset + y_offset,
            center - 8 + ear_joy, center - 38 + head_offset + y_offset,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center - 16 + ear_joy, center - 66 + head_offset + y_offset,
            center - 10 + ear_joy, center - 40 + head_offset + y_offset,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
        
        self._renderer.draw_oval(
            center + 8 - ear_joy, center - 68 + head_offset + y_offset,
            center + 18 - ear_joy, center - 38 + head_offset + y_offset,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 10 - ear_joy, center - 66 + head_offset + y_offset,
            center + 16 - ear_joy, center - 40 + head_offset + y_offset,
            fill=ColorPalette.INNER_EAR_COLOR, outline=""
        )
    
    def _draw_rabbit_ears_sleep(self, center: int):
        self._renderer.draw_oval(
            center - 20, center - 25,
            center - 10, center - 5,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 5, center - 25,
            center + 15, center - 5,
            fill=self.skin_hex
        )
    
    def _draw_rabbit_ears_jump(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 22, center - 60 + y_offset,
            center - 12, center - 30 + y_offset,
            fill=self.skin_hex
        )
        self._renderer.draw_oval(
            center + 12, center - 60 + y_offset,
            center + 22, center - 30 + y_offset,
            fill=self.skin_hex
        )
    
    def _draw_rabbit_eyes_idle(self, center: int):
        eye_y = center - 20
        if self._should_blink():
            self._renderer.draw_closed_eye(center - 12, eye_y, center - 6, eye_y, width=2)
            self._renderer.draw_closed_eye(center + 6, eye_y, center + 12, eye_y, width=2)
        else:
            self._renderer.draw_open_eye(center - 12, eye_y - 3, center - 6, eye_y + 3, highlight=True)
            self._renderer.draw_open_eye(center + 6, eye_y - 3, center + 12, eye_y + 3, highlight=True)
    
    def _draw_rabbit_eyes_open(self, center: int):
        eye_y = center - 20
        self._renderer.draw_open_eye(center - 12, eye_y - 3, center - 6, eye_y + 3, highlight=True)
        self._renderer.draw_open_eye(center + 6, eye_y - 3, center + 12, eye_y + 3, highlight=True)
    
    def _draw_rabbit_eyes_happy(self, center: int, head_offset: int, y_offset: int = 0):
        eye_y = center - 23 + head_offset + y_offset
        self._renderer.draw_happy_eye(center - 14, eye_y - 4, center - 4, eye_y + 4, width=2)
        self._renderer.draw_happy_eye(center + 4, eye_y - 4, center + 14, eye_y + 4, width=2)
    
    def _draw_rabbit_eyes_sleep(self, center: int):
        eye_y = center
        self._renderer.draw_closed_eye(center - 15, eye_y, center - 10, eye_y, width=2)
        self._renderer.draw_closed_eye(center + 3, eye_y, center + 8, eye_y, width=2)
    
    def _draw_rabbit_eyes_surprised(self, center: int, y_offset: int = 0):
        eye_y = center - 20 + y_offset
        self._renderer.draw_open_eye(center - 12, eye_y - 4, center - 6, eye_y + 4, highlight=True)
        self._renderer.draw_open_eye(center + 6, eye_y - 4, center + 12, eye_y + 4, highlight=True)
    
    def _draw_rabbit_nose_mouth(self, center: int, y_offset: int = 0):
        self._renderer.draw_three_lobed_nose(
            center - 3, center - 12 + y_offset,
            center + 3, center - 10 + y_offset
        )
        self._renderer.draw_line(center, center - 10 + y_offset, center, center - 4 + y_offset, width=2)
        self._renderer.draw_smile_arc(
            center - 8, center - 8 + y_offset,
            center - 2, center - 2 + y_offset
        )
        self._renderer.draw_smile_arc(
            center + 2, center - 8 + y_offset,
            center + 8, center - 2 + y_offset
        )
    
    def _draw_rabbit_nose_mouth_happy(self, center: int, head_offset: int, y_offset: int = 0):
        self._renderer.draw_three_lobed_nose(
            center - 3, center - 15 + head_offset + y_offset,
            center + 3, center - 13 + head_offset + y_offset
        )
        self._renderer.draw_smile_arc(
            center - 10, center - 15 + head_offset + y_offset,
            center + 10, center - 5 + head_offset + y_offset,
            width=2
        )
    
    def _draw_rabbit_mouth_surprised(self, center: int, y_offset: int = 0):
        self._renderer.draw_oval(
            center - 4, center - 12 + y_offset,
            center + 4, center - 4 + y_offset,
            fill=ColorPalette.BLACK
        )
    
    def _draw_rabbit_whiskers(self, center: int, y_offset: int = 0):
        self._renderer.draw_line(center - 20, center - 8 + y_offset, center - 6, center - 10 + y_offset, width=1)
        self._renderer.draw_line(center - 20, center - 5 + y_offset, center - 6, center - 7 + y_offset, width=1)
        self._renderer.draw_line(center + 6, center - 10 + y_offset, center + 20, center - 8 + y_offset, width=1)
        self._renderer.draw_line(center + 6, center - 7 + y_offset, center + 20, center - 5 + y_offset, width=1)
    
    def _draw_rabbit_blush(self, center: int, head_offset: int, y_offset: int = 0):
        self._renderer.draw_blush(
            center - 18, center - 18 + head_offset + y_offset,
            center - 12, center - 12 + head_offset + y_offset
        )
        self._renderer.draw_blush(
            center + 12, center - 18 + head_offset + y_offset,
            center + 18, center - 12 + head_offset + y_offset
        )
    
    def _draw_rabbit_tail(self, center: int, y_offset: int = 0):
        tail_x = center + 28
        tail_y = center + 20 + y_offset
        self._renderer.draw_oval(tail_x, tail_y, tail_x + 5, tail_y + 5, 
                                   fill=ColorPalette.WHITE, outline=ColorPalette.BLACK)
    
    def _draw_rabbit_tail_happy(self, center: int, y_offset: int = 0):
        tail_x = center + 28
        tail_y = center + 20 + y_offset
        tail_wave = 3 if self._frame_index % 2 == 0 else 0
        self._renderer.draw_oval(tail_x + tail_wave, tail_y, tail_x + 5 + tail_wave, tail_y + 5, 
                                   fill=ColorPalette.WHITE, outline=ColorPalette.BLACK)
    
    def _draw_rabbit_legs_walk(self, center: int):
        leg_offset = 7 if self._frame_index % 4 < 2 else -7
        
        self._renderer.draw_line(center - 12, center + 30, center - 12, center + 42 + leg_offset, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center + 5, center + 30, center + 5, center + 42 - leg_offset, 
                                   width=4, fill=self.skin_hex)
        
        self._renderer.draw_line(center - 5, center + 30, center - 8, center + 45 - leg_offset, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center + 12, center + 30, center + 15, center + 45 + leg_offset, 
                                   width=5, fill=self.skin_hex)
    
    def _draw_rabbit_legs_jump(self, center: int):
        self._renderer.draw_line(center - 12, center + 30, center - 15, center + 50, 
                                   width=4, fill=self.skin_hex)
        self._renderer.draw_line(center + 5, center + 30, center + 8, center + 50, 
                                   width=4, fill=self.skin_hex)
        
        self._renderer.draw_line(center - 5, center + 30, center - 10, center + 55, 
                                   width=5, fill=self.skin_hex)
        self._renderer.draw_line(center + 12, center + 30, center + 17, center + 55, 
                                   width=5, fill=self.skin_hex)
    
    def _draw_rabbit_body_sleep(self, center: int, breath_offset: int = 0):
        self._renderer.draw_oval(center - 30, center - 5, center + 30, center + 35, 
                                   fill=self.skin_hex)
    
    def _draw_rabbit_head_sleep(self, center: int):
        self._renderer.draw_oval(center - 20, center - 10, center + 10, center + 15, 
                                   fill=self.skin_hex)
    
    def _draw_rabbit_zzz(self, center: int):
        z_level = self._get_z_level()
        self._renderer.draw_zzz_rabbit(center, center, z_level)