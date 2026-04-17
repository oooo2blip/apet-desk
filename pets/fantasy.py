from typing import Optional, List
from pets.base import PetBase
from core.config import (
    PetState,
    SkinColor,
    ColorPalette,
    PetType,
    PetDisplayNames,
    AnimationFrames,
    PastelTheme
)


class FantasyPet(PetBase):
    PET_TYPE = PetType.FANTASY
    DISPLAY_NAME = PetDisplayNames.PET_NAMES[PetType.FANTASY]
    
    PASTEL_SKIN_MAP = {
        SkinColor.PASTEL_LAVENDER: PastelTheme.SOFT_LAVENDER,
        SkinColor.PASTEL_PINK: PastelTheme.SOFT_PINK,
        SkinColor.PASTEL_MINT: PastelTheme.SOFT_MINT
    }
    
    def _get_pastel_skin(self) -> str:
        if self._skin_color in self.PASTEL_SKIN_MAP:
            return self.PASTEL_SKIN_MAP[self._skin_color]
        return PastelTheme.SOFT_LAVENDER
    
    def _get_gradient_colors(self) -> tuple:
        skin = self._get_pastel_skin()
        if skin == PastelTheme.SOFT_LAVENDER:
            return PastelTheme.GRADIENT_BLUE_PURPLE
        elif skin == PastelTheme.SOFT_PINK:
            return PastelTheme.GRADIENT_PINK_ORANGE
        elif skin == PastelTheme.SOFT_MINT:
            return PastelTheme.GRADIENT_MINT
        return PastelTheme.GRADIENT_BLUE_PURPLE
    
    def _get_glow_color(self) -> str:
        skin = self._get_pastel_skin()
        if skin == PastelTheme.SOFT_LAVENDER:
            return PastelTheme.GLOW_LAVENDER
        elif skin == PastelTheme.SOFT_PINK:
            return PastelTheme.GLOW_PINK
        elif skin == PastelTheme.SOFT_MINT:
            return PastelTheme.GLOW_MINT
        return PastelTheme.GLOW_LAVENDER
    
    def _get_eye_colors(self) -> tuple:
        skin = self._get_pastel_skin()
        if skin == PastelTheme.SOFT_LAVENDER:
            return PastelTheme.EYE_GRADIENT_DARK
        elif skin == PastelTheme.SOFT_PINK:
            return (PastelTheme.GLOW_PINK, PastelTheme.SOFT_CORAL)
        elif skin == PastelTheme.SOFT_MINT:
            return (PastelTheme.GLOW_MINT, PastelTheme.SOFT_TEAL)
        return PastelTheme.EYE_GRADIENT_DARK
    
    def _draw_idle(self, center: int):
        breath_offset = self._get_breath_offset()
        self._draw_fantasy_body(center, breath_offset)
        self._draw_fantasy_head(center, breath_offset)
        self._draw_fantasy_ears(center, breath_offset)
        self._draw_fantasy_eyes_idle(center, breath_offset)
        self._draw_fantasy_mouth_idle(center, breath_offset)
        self._draw_fantasy_blush(center, breath_offset)
        self._draw_fantasy_tail_idle(center)
        self._draw_soft_glow(center, breath_offset)
    
    def _draw_walk(self, center: int):
        breath_offset = self._get_breath_offset()
        self._draw_fantasy_body(center, breath_offset)
        self._draw_fantasy_head(center, breath_offset)
        self._draw_fantasy_ears(center, breath_offset)
        self._draw_fantasy_eyes_open(center, breath_offset)
        self._draw_fantasy_mouth_smile(center, breath_offset)
        self._draw_fantasy_blush(center, breath_offset)
        self._draw_fantasy_legs_walk(center)
        self._draw_fantasy_tail_walk(center)
        self._draw_soft_glow(center, breath_offset)
    
    def _draw_happy(self, center: int):
        jump_offset = self._get_happy_jump_offset()
        head_bounce = -2 if self._frame_index % 4 < 2 else 0
        
        self._draw_fantasy_body(center, jump_offset)
        self._draw_fantasy_head(center, jump_offset + head_bounce)
        self._draw_fantasy_ears_happy(center, jump_offset + head_bounce)
        self._draw_fantasy_eyes_happy(center, jump_offset + head_bounce)
        self._draw_fantasy_mouth_happy(center, jump_offset + head_bounce)
        self._draw_fantasy_blush_intense(center, jump_offset + head_bounce)
        self._draw_fantasy_tail_happy(center, jump_offset)
        self._draw_soft_glow(center, jump_offset)
    
    def _draw_sleep(self, center: int):
        breath_offset = self._get_breath_offset()
        
        self._draw_fantasy_body_sleep(center, breath_offset)
        self._draw_fantasy_head_sleep(center)
        self._draw_fantasy_ears_sleep(center)
        self._draw_fantasy_eyes_sleep(center)
        self._draw_fantasy_zzz(center)
        self._draw_sleep_glow(center, breath_offset)
    
    def _draw_jump(self, center: int):
        jump_height = 25 if self._frame_index % 4 < 2 else 0
        
        self._draw_fantasy_body(center, -jump_height)
        self._draw_fantasy_head(center, -jump_height)
        self._draw_fantasy_ears_surprised(center, -jump_height)
        self._draw_fantasy_eyes_surprised(center, -jump_height)
        self._draw_fantasy_mouth_surprised(center, -jump_height)
        self._draw_fantasy_legs_jump(center)
        self._draw_fantasy_tail_jump(center, -jump_height)
        self._draw_soft_glow(center, -jump_height)
    
    def _draw_soft_glow(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        glow_color = self._get_glow_color()
        head_x1 = center - 35
        head_y1 = center - 55 + y_offset
        head_x2 = center + 35
        head_y2 = center - 10 + y_offset
        
        self._renderer.draw_soft_glow_outline(
            head_x1, head_y1, head_x2, head_y2,
            glow_color, layers=2
        )
    
    def _draw_sleep_glow(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        glow_color = PastelTheme.SOFT_MINT
        body_x1 = center - 30
        body_y1 = center - 5 + y_offset
        body_x2 = center + 30
        body_y2 = center + 30 + y_offset
        
        self._renderer.draw_soft_glow_outline(
            body_x1, body_y1, body_x2, body_y2,
            glow_color, layers=1
        )
    
    def _draw_fantasy_body(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        colors = self._get_gradient_colors()
        glow_color = self._get_glow_color()
        
        self._renderer.draw_gradient_oval(
            center - 28, center - 8 + y_offset,
            center + 28, center + 28 + y_offset,
            colors=colors,
            glow_color=glow_color
        )
    
    def _draw_fantasy_head(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        colors = self._get_gradient_colors()
        glow_color = self._get_glow_color()
        
        self._renderer.draw_jelly_oval(
            center - 35, center - 55 + y_offset,
            center + 35, center - 10 + y_offset,
            base_color=colors[1],
            highlight_color=PastelTheme.EYE_HIGHLIGHT,
            glow_color=glow_color
        )
    
    def _draw_fantasy_ears(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        glow_color = self._get_glow_color()
        
        ear_wave = 2 if self._frame_index % 15 < 7 else -2
        
        self._renderer.draw_round_ear(
            center - 25, center - 50 + y_offset + ear_wave,
            radius=12,
            base_color=skin_color,
            inner_color=PastelTheme.INNER_EAR_COLOR,
            glow_color=glow_color
        )
        
        self._renderer.draw_round_ear(
            center + 25, center - 50 + y_offset - ear_wave,
            radius=12,
            base_color=skin_color,
            inner_color=PastelTheme.INNER_EAR_COLOR,
            glow_color=glow_color
        )
    
    def _draw_fantasy_ears_happy(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        glow_color = self._get_glow_color()
        
        ear_bounce = -5 if self._frame_index % 2 == 0 else 0
        
        self._renderer.draw_round_ear(
            center - 25, center - 52 + y_offset + ear_bounce,
            radius=13,
            base_color=skin_color,
            inner_color=PastelTheme.INNER_EAR_COLOR,
            glow_color=glow_color
        )
        
        self._renderer.draw_round_ear(
            center + 25, center - 52 + y_offset + ear_bounce,
            radius=13,
            base_color=skin_color,
            inner_color=PastelTheme.INNER_EAR_COLOR,
            glow_color=glow_color
        )
    
    def _draw_fantasy_ears_surprised(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        glow_color = self._get_glow_color()
        
        self._renderer.draw_round_ear(
            center - 25, center - 55 + y_offset - 3,
            radius=14,
            base_color=skin_color,
            inner_color=PastelTheme.INNER_EAR_COLOR,
            glow_color=glow_color
        )
        
        self._renderer.draw_round_ear(
            center + 25, center - 55 + y_offset - 3,
            radius=14,
            base_color=skin_color,
            inner_color=PastelTheme.INNER_EAR_COLOR,
            glow_color=glow_color
        )
    
    def _draw_fantasy_ears_sleep(self, center: int):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        
        self._renderer.draw_round_ear(
            center - 20, center - 18,
            radius=10,
            base_color=skin_color,
            inner_color=PastelTheme.INNER_EAR_COLOR
        )
    
    def _draw_fantasy_eyes_idle(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        eye_y = center - 35 + y_offset
        eye_colors = self._get_eye_colors()
        
        if self._should_blink():
            self._renderer.draw_happy_closed_eye(
                center - 18, eye_y - 4, center - 8, eye_y + 4,
                width=2
            )
            self._renderer.draw_happy_closed_eye(
                center + 8, eye_y - 4, center + 18, eye_y + 4,
                width=2
            )
        else:
            self._renderer.draw_gradient_eye(
                center - 13, eye_y, radius=8,
                eye_colors=eye_colors
            )
            self._renderer.draw_gradient_eye(
                center + 13, eye_y, radius=8,
                eye_colors=eye_colors
            )
    
    def _draw_fantasy_eyes_open(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        eye_y = center - 35 + y_offset
        eye_colors = self._get_eye_colors()
        
        self._renderer.draw_gradient_eye(
            center - 13, eye_y, radius=8,
            eye_colors=eye_colors
        )
        self._renderer.draw_gradient_eye(
            center + 13, eye_y, radius=8,
            eye_colors=eye_colors
        )
    
    def _draw_fantasy_eyes_happy(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        eye_y = center - 35 + y_offset
        
        self._renderer.draw_happy_closed_eye(
            center - 20, eye_y - 5, center - 6, eye_y + 5,
            width=2
        )
        self._renderer.draw_happy_closed_eye(
            center + 6, eye_y - 5, center + 20, eye_y + 5,
            width=2
        )
    
    def _draw_fantasy_eyes_sleep(self, center: int):
        if self._renderer is None:
            return
        
        eye_y = center - 8
        
        self._renderer.draw_closed_eye(
            center - 18, eye_y, center - 10, eye_y, width=2
        )
        self._renderer.draw_closed_eye(
            center + 10, eye_y, center + 18, eye_y, width=2
        )
    
    def _draw_fantasy_eyes_surprised(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        eye_y = center - 35 + y_offset
        eye_colors = self._get_eye_colors()
        
        self._renderer.draw_gradient_eye(
            center - 14, eye_y, radius=10,
            eye_colors=eye_colors
        )
        self._renderer.draw_gradient_eye(
            center + 14, eye_y, radius=10,
            eye_colors=eye_colors
        )
    
    def _draw_fantasy_mouth_idle(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        mouth_y = center - 22 + y_offset
        
        self._renderer.draw_smile_arc(
            center - 6, mouth_y, center + 6, mouth_y + 8,
            width=2
        )
    
    def _draw_fantasy_mouth_smile(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        mouth_y = center - 22 + y_offset
        
        self._renderer.draw_smile_arc(
            center - 8, mouth_y - 2, center + 8, mouth_y + 10,
            width=2
        )
    
    def _draw_fantasy_mouth_happy(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        mouth_y = center - 20 + y_offset
        
        self._renderer.draw_smile_arc(
            center - 12, mouth_y - 5, center + 12, mouth_y + 12,
            width=2
        )
        
        self._renderer.draw_tongue(
            center - 5, mouth_y + 3, center + 5, mouth_y + 12
        )
    
    def _draw_fantasy_mouth_surprised(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        mouth_y = center - 20 + y_offset
        
        self._renderer.draw_oval(
            center - 6, mouth_y, center + 6, mouth_y + 10,
            fill=ColorPalette.BLACK
        )
    
    def _draw_fantasy_blush(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        self._renderer.draw_soft_blush(
            center - 28, center - 25 + y_offset,
            center - 20, center - 17 + y_offset
        )
        self._renderer.draw_soft_blush(
            center + 20, center - 25 + y_offset,
            center + 28, center - 17 + y_offset
        )
    
    def _draw_fantasy_blush_intense(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        self._renderer.draw_soft_blush(
            center - 30, center - 28 + y_offset,
            center - 18, center - 16 + y_offset
        )
        self._renderer.draw_soft_blush(
            center + 18, center - 28 + y_offset,
            center + 30, center - 16 + y_offset
        )
    
    def _draw_fantasy_tail_idle(self, center: int):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        tail_x = center + 30
        tail_y = center + 8
        tail_wave = 6 if self._frame_index % 10 < 5 else -6
        
        self._renderer.draw_line(
            tail_x, tail_y, tail_x + 18, tail_y + tail_wave,
            width=6, fill=skin_color, smooth=True
        )
        
        self._renderer.draw_oval(
            tail_x + 16, tail_y + tail_wave - 3,
            tail_x + 24, tail_y + tail_wave + 3,
            fill=skin_color, outline=""
        )
    
    def _draw_fantasy_tail_walk(self, center: int):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        tail_x = center + 30
        tail_y = center + 8
        tail_wave = 10 if self._frame_index % 4 < 2 else -10
        
        self._renderer.draw_line(
            tail_x, tail_y, tail_x + 20, tail_y + tail_wave,
            width=6, fill=skin_color, smooth=True
        )
        
        self._renderer.draw_oval(
            tail_x + 18, tail_y + tail_wave - 4,
            tail_x + 26, tail_y + tail_wave + 4,
            fill=skin_color, outline=""
        )
    
    def _draw_fantasy_tail_happy(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        tail_x = center + 30
        tail_y = center + 8 + y_offset
        tail_wave = 15 if self._frame_index % 2 == 0 else -15
        
        self._renderer.draw_line(
            tail_x, tail_y, tail_x + 22, tail_y + tail_wave,
            width=6, fill=skin_color, smooth=True
        )
        
        self._renderer.draw_oval(
            tail_x + 20, tail_y + tail_wave - 5,
            tail_x + 28, tail_y + tail_wave + 5,
            fill=skin_color, outline=""
        )
    
    def _draw_fantasy_tail_jump(self, center: int, y_offset: int = 0):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        tail_x = center + 30
        tail_y = center + 8 + y_offset
        
        self._renderer.draw_line(
            tail_x, tail_y, tail_x + 25, tail_y - 10,
            width=6, fill=skin_color, smooth=True
        )
        
        self._renderer.draw_oval(
            tail_x + 23, tail_y - 15,
            tail_x + 31, tail_y - 7,
            fill=skin_color, outline=""
        )
    
    def _draw_fantasy_legs_walk(self, center: int):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        leg_offset = 5 if self._frame_index % 4 < 2 else -5
        
        self._renderer.draw_oval(
            center - 18, center + 25,
            center - 12, center + 38 + leg_offset,
            fill=skin_color, outline=""
        )
        self._renderer.draw_oval(
            center - 8, center + 25,
            center - 2, center + 38 - leg_offset,
            fill=skin_color, outline=""
        )
        self._renderer.draw_oval(
            center + 2, center + 25,
            center + 8, center + 38 + leg_offset,
            fill=skin_color, outline=""
        )
        self._renderer.draw_oval(
            center + 12, center + 25,
            center + 18, center + 38 - leg_offset,
            fill=skin_color, outline=""
        )
    
    def _draw_fantasy_legs_jump(self, center: int):
        if self._renderer is None:
            return
        
        skin_color = self._get_pastel_skin()
        
        self._renderer.draw_oval(
            center - 20, center + 28,
            center - 14, center + 45,
            fill=skin_color, outline=""
        )
        self._renderer.draw_oval(
            center - 10, center + 28,
            center - 4, center + 45,
            fill=skin_color, outline=""
        )
        self._renderer.draw_oval(
            center + 4, center + 28,
            center + 10, center + 45,
            fill=skin_color, outline=""
        )
        self._renderer.draw_oval(
            center + 14, center + 28,
            center + 20, center + 45,
            fill=skin_color, outline=""
        )
    
    def _draw_fantasy_body_sleep(self, center: int, breath_offset: int = 0):
        if self._renderer is None:
            return
        
        colors = self._get_gradient_colors()
        
        self._renderer.draw_gradient_oval(
            center - 32, center + breath_offset,
            center + 28, center + 35 + breath_offset,
            colors=colors
        )
    
    def _draw_fantasy_head_sleep(self, center: int):
        if self._renderer is None:
            return
        
        colors = self._get_gradient_colors()
        
        self._renderer.draw_jelly_oval(
            center - 28, center - 20,
            center - 2, center + 15,
            base_color=colors[1],
            highlight_color=PastelTheme.EYE_HIGHLIGHT
        )
    
    def _draw_fantasy_zzz(self, center: int):
        if self._renderer is None:
            return
        
        z_level = self._get_z_level()
        self._renderer.draw_zzz(center - 15, center, z_level)
