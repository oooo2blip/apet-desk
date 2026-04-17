import tkinter as tk
import math
from typing import Optional, Tuple, List
from core.config import ColorPalette, CyberpunkTheme


class Renderer:
    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._drawn_items: List[int] = []
        self._glow_phase: float = 0.0
        self._glitch_phase: float = 0.0
    
    def clear(self):
        for item in self._drawn_items:
            self._canvas.delete(item)
        self._drawn_items.clear()
    
    def draw_oval(self, x1: int, y1: int, x2: int, y2: int, 
                   fill: str = "", outline: str = ColorPalette.BLACK, 
                   width: int = 1) -> int:
        item = self._canvas.create_oval(x1, y1, x2, y2, fill=fill, outline=outline, width=width)
        self._drawn_items.append(item)
        return item
    
    def draw_polygon(self, points: List[int], 
                      fill: str = "", outline: str = ColorPalette.BLACK, 
                      width: int = 1) -> int:
        item = self._canvas.create_polygon(*points, fill=fill, outline=outline, width=width)
        self._drawn_items.append(item)
        return item
    
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, 
                  fill: str = ColorPalette.BLACK, width: int = 1, 
                  smooth: bool = False) -> int:
        item = self._canvas.create_line(x1, y1, x2, y2, fill=fill, width=width, smooth=smooth)
        self._drawn_items.append(item)
        return item
    
    def draw_arc(self, x1: int, y1: int, x2: int, y2: int, 
                  start: int = 0, extent: int = 90, style: str = tk.ARC,
                  fill: str = "", outline: str = ColorPalette.BLACK, 
                  width: int = 1) -> int:
        item = self._canvas.create_arc(x1, y1, x2, y2, start=start, extent=extent, 
                                        style=style, fill=fill, outline=outline, width=width)
        self._drawn_items.append(item)
        return item
    
    def draw_text(self, x: int, y: int, text: str, 
                  font: Tuple[str, int] = ("Arial", 12), 
                  fill: str = ColorPalette.BLACK) -> int:
        item = self._canvas.create_text(x, y, text=text, font=font, fill=fill)
        self._drawn_items.append(item)
        return item
    
    def draw_smile_arc(self, x1: int, y1: int, x2: int, y2: int, width: int = 1) -> int:
        return self.draw_arc(x1, y1, x2, y2, start=180, extent=180, width=width)
    
    def draw_closed_eye(self, x1: int, y1: int, x2: int, y2: int, width: int = 2) -> int:
        return self.draw_line(x1, y1, x2, y2, width=width)
    
    def draw_open_eye(self, x1: int, y1: int, x2: int, y2: int, 
                       fill: str = ColorPalette.BLACK, 
                       highlight: bool = False) -> List[int]:
        items = []
        items.append(self.draw_oval(x1, y1, x2, y2, fill=fill))
        if highlight:
            highlight_x1 = x1 + (x2 - x1) * 0.4
            highlight_y1 = y1 + (y2 - y1) * 0.3
            highlight_x2 = x1 + (x2 - x1) * 0.6
            highlight_y2 = y1 + (y2 - y1) * 0.5
            items.append(self.draw_oval(highlight_x1, highlight_y1, highlight_x2, highlight_y2, 
                                         fill=ColorPalette.WHITE, outline=""))
        return items
    
    def draw_happy_eye(self, x1: int, y1: int, x2: int, y2: int, width: int = 2) -> int:
        return self.draw_arc(x1, y1, x2, y2, start=180, extent=180, style=tk.ARC, width=width)
    
    def draw_pink_nose(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return self.draw_oval(x1, y1, x2, y2, fill=ColorPalette.PINK, outline=ColorPalette.BLACK)
    
    def draw_black_nose(self, x1: int, y1: int, x2: int, y2: int, 
                         highlight: bool = True) -> List[int]:
        items = []
        items.append(self.draw_oval(x1, y1, x2, y2, fill=ColorPalette.BLACK))
        if highlight:
            highlight_x1 = x1 + (x2 - x1) * 0.2
            highlight_y1 = y1 + (y2 - y1) * 0.2
            highlight_x2 = x1 + (x2 - x1) * 0.4
            highlight_y2 = y1 + (y2 - y1) * 0.4
            items.append(self.draw_oval(highlight_x1, highlight_y1, highlight_x2, highlight_y2, 
                                         fill=ColorPalette.GRAY, outline=""))
        return items
    
    def draw_three_lobed_nose(self, x1: int, y1: int, x2: int, y2: int) -> int:
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [x1, cy, cx, y1, x2, cy]
        return self.draw_polygon(points, fill=ColorPalette.PINK, outline=ColorPalette.BLACK)
    
    def draw_blush(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return self.draw_oval(x1, y1, x2, y2, fill=ColorPalette.PINK, outline="")
    
    def draw_tongue(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return self.draw_oval(x1, y1, x2, y2, fill=ColorPalette.PINK, outline="")
    
    def draw_zzz(self, base_x: int, base_y: int, z_level: int):
        if z_level < 10:
            self.draw_text(base_x + 20, base_y - 30, "Z", ("Arial", 12), ColorPalette.GRAY)
        elif z_level < 20:
            self.draw_text(base_x + 20, base_y - 30, "Z", ("Arial", 12), ColorPalette.GRAY)
            self.draw_text(base_x + 30, base_y - 40, "z", ("Arial", 10), ColorPalette.GRAY)
        else:
            self.draw_text(base_x + 20, base_y - 30, "Z", ("Arial", 12), ColorPalette.GRAY)
            self.draw_text(base_x + 30, base_y - 40, "z", ("Arial", 10), ColorPalette.GRAY)
            self.draw_text(base_x + 40, base_y - 50, "z", ("Arial", 8), ColorPalette.GRAY)
    
    def draw_zzz_rabbit(self, base_x: int, base_y: int, z_level: int):
        if z_level < 10:
            self.draw_text(base_x + 20, base_y - 15, "Z", ("Arial", 10), ColorPalette.GRAY)
        elif z_level < 20:
            self.draw_text(base_x + 20, base_y - 15, "Z", ("Arial", 10), ColorPalette.GRAY)
            self.draw_text(base_x + 30, base_y - 25, "z", ("Arial", 8), ColorPalette.GRAY)
        else:
            self.draw_text(base_x + 20, base_y - 15, "Z", ("Arial", 10), ColorPalette.GRAY)
            self.draw_text(base_x + 30, base_y - 25, "z", ("Arial", 8), ColorPalette.GRAY)
            self.draw_text(base_x + 40, base_y - 35, "z", ("Arial", 6), ColorPalette.GRAY)
    
    def update_glow_phase(self, delta: float = 0.1):
        self._glow_phase += delta
        if self._glow_phase > 2 * math.pi:
            self._glow_phase -= 2 * math.pi
    
    def update_glitch_phase(self, delta: float = 0.2):
        self._glitch_phase += delta
        if self._glitch_phase > 1.0:
            self._glitch_phase = 0.0
    
    def get_breath_intensity(self) -> float:
        return 0.5 + 0.5 * math.sin(self._glow_phase)
    
    def draw_neon_glow_oval(self, x1: int, y1: int, x2: int, y2: int,
                             primary_color: str = CyberpunkTheme.PRIMARY_GLOW,
                             secondary_color: str = CyberpunkTheme.SECONDARY_GLOW,
                             glow_layers: int = 2,
                             base_width: int = 1) -> List[int]:
        items = []
        breath_intensity = self.get_breath_intensity()
        
        for i in range(glow_layers):
            offset = (glow_layers - i) * 2
            width = base_width + i
            opacity_factor = 1.0 - (i / glow_layers) * 0.5
            
            glow_x1 = x1 - offset
            glow_y1 = y1 - offset
            glow_x2 = x2 + offset
            glow_y2 = y2 + offset
            
            if i % 2 == 0:
                color = primary_color
            else:
                color = secondary_color
            
            items.append(self._canvas.create_oval(
                glow_x1, glow_y1, glow_x2, glow_y2,
                outline=color,
                width=width
            ))
        
        self._drawn_items.extend(items)
        return items
    
    def draw_neon_glow_polygon(self, points: List[int],
                                primary_color: str = CyberpunkTheme.PRIMARY_GLOW,
                                secondary_color: str = CyberpunkTheme.SECONDARY_GLOW,
                                glow_layers: int = 2) -> List[int]:
        items = []
        
        for i in range(glow_layers):
            offset = (glow_layers - i) * 2
            width = 1 + i
            
            scaled_points = []
            center_x = sum(points[::2]) / (len(points) // 2)
            center_y = sum(points[1::2]) / (len(points) // 2)
            
            for j in range(0, len(points), 2):
                px = points[j]
                py = points[j + 1]
                dx = px - center_x
                dy = py - center_y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 0:
                    scale = (dist + offset) / dist
                else:
                    scale = 1.0
                scaled_points.append(center_x + dx * scale)
                scaled_points.append(center_y + dy * scale)
            
            if i % 2 == 0:
                color = primary_color
            else:
                color = secondary_color
            
            items.append(self._canvas.create_polygon(
                *scaled_points,
                outline=color,
                width=width,
                fill=""
            ))
        
        self._drawn_items.extend(items)
        return items
    
    def draw_neon_glow_line(self, x1: int, y1: int, x2: int, y2: int,
                             primary_color: str = CyberpunkTheme.PRIMARY_GLOW,
                             secondary_color: str = CyberpunkTheme.SECONDARY_GLOW,
                             glow_layers: int = 2,
                             base_width: int = 2) -> List[int]:
        items = []
        
        for i in range(glow_layers):
            offset = (glow_layers - i) * 2
            width = base_width + i
            
            if i % 2 == 0:
                color = primary_color
            else:
                color = secondary_color
            
            items.append(self._canvas.create_line(
                x1, y1 - offset, x2, y2 - offset,
                fill=color,
                width=width,
                smooth=True
            ))
            items.append(self._canvas.create_line(
                x1, y1 + offset, x2, y2 + offset,
                fill=color,
                width=width,
                smooth=True
            ))
        
        items.append(self._canvas.create_line(
            x1, y1, x2, y2,
            fill=CyberpunkTheme.SOFT_AMBER,
            width=base_width // 2,
            smooth=True
        ))
        
        self._drawn_items.extend(items)
        return items
    
    def draw_glitch_effect(self, x1: int, y1: int, x2: int, y2: int,
                            intensity: float = 0.3) -> List[int]:
        items = []
        
        if self._glitch_phase > 0.95:
            glitch_offset = 1
            segment_height = (y2 - y1) // 6
            
            for i in range(2):
                seg_y1 = y1 + (i + 2) * segment_height
                seg_y2 = seg_y1 + segment_height
                
                if i % 2 == 0:
                    offset_x = glitch_offset
                else:
                    offset_x = -glitch_offset
                
                color = CyberpunkTheme.SOFT_CYAN
                
                items.append(self._canvas.create_line(
                    x1 + offset_x, seg_y1,
                    x2 + offset_x, seg_y1,
                    fill=color,
                    width=1
                ))
        
        self._drawn_items.extend(items)
        return items
    
    def draw_pulse_flash(self, center_x: int, center_y: int,
                         radius: int, intensity: float) -> List[int]:
        items = []
        
        if intensity <= 0:
            return items
        
        colors = [
            CyberpunkTheme.SOFT_MAUVE,
            CyberpunkTheme.SOFT_CYAN,
            CyberpunkTheme.SOFT_AMBER
        ]
        
        for i, color in enumerate(colors):
            r = int(radius * 0.6 * (1 + i * 0.15) * intensity)
            alpha_width = 1
            
            items.append(self._canvas.create_oval(
                center_x - r, center_y - r,
                center_x + r, center_y + r,
                outline=color,
                width=alpha_width
            ))
        
        self._drawn_items.extend(items)
        return items
    
    def draw_neon_text(self, x: int, y: int, text: str,
                       font: Tuple[str, int] = ("Arial", 12),
                       glow_color: str = CyberpunkTheme.PRIMARY_GLOW,
                       text_color: str = CyberpunkTheme.SOFT_AMBER) -> List[int]:
        items = []
        
        for offset in [(-1, -1), (1, -1), (-1, 1), (1, 1),
                       (-2, 0), (2, 0), (0, -2), (0, 2)]:
            items.append(self._canvas.create_text(
                x + offset[0], y + offset[1],
                text=text,
                font=font,
                fill=glow_color
            ))
        
        items.append(self._canvas.create_text(
            x, y,
            text=text,
            font=font,
            fill=text_color
        ))
        
        self._drawn_items.extend(items)
        return items