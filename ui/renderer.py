import tkinter as tk
from typing import Optional, Tuple, List
from core.config import ColorPalette


class Renderer:
    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
        self._drawn_items: List[int] = []
    
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