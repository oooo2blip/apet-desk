import tkinter as tk
from tkinter import Menu, Toplevel, Label, Scale, Button, Checkbutton
from typing import Optional, Callable, Any, List
from core.config import (
    PetType,
    SkinColor,
    UIConfig,
    PetDisplayNames,
    ColorPalette
)
from pets.factory import PetFactory, SkinManager
import random


class DragHandler:
    def __init__(
        self,
        root: tk.Tk,
        canvas: tk.Canvas,
        on_drag_start: Callable[[], None],
        on_drag_end: Callable[[], None],
        on_position_update: Callable[[int, int], None]
    ):
        self._root = root
        self._canvas = canvas
        self._on_drag_start = on_drag_start
        self._on_drag_end = on_drag_end
        self._on_position_update = on_position_update
        
        self._is_dragging: bool = False
        self._drag_offset_x: int = 0
        self._drag_offset_y: int = 0
        self._current_x: int = 0
        self._current_y: int = 0
        
        self._bind_events()
    
    @property
    def is_dragging(self) -> bool:
        return self._is_dragging
    
    def set_position(self, x: int, y: int):
        self._current_x = x
        self._current_y = y
    
    def _bind_events(self):
        self._canvas.bind("<Button-1>", self._on_click)
        self._canvas.bind("<B1-Motion>", self._on_drag)
        self._canvas.bind("<ButtonRelease-1>", self._on_release)
    
    def _on_click(self, event: tk.Event):
        pass
    
    def _on_drag(self, event: tk.Event):
        if not self._is_dragging:
            self._is_dragging = True
            self._drag_offset_x = event.x
            self._drag_offset_y = event.y
            self._on_drag_start()
        
        self._current_x = self._root.winfo_pointerx() - self._drag_offset_x
        self._current_y = self._root.winfo_pointery() - self._drag_offset_y
        
        self._on_position_update(self._current_x, self._current_y)
    
    def _on_release(self, event: tk.Event):
        self._is_dragging = False
        self._on_drag_end()


class ContextMenu:
    def __init__(
        self,
        root: tk.Tk,
        canvas: tk.Canvas,
        on_pet_change: Callable[[PetType], None],
        on_skin_change: Callable[[SkinColor], None],
        on_settings_open: Callable[[], None],
        on_quit: Callable[[], None]
    ):
        self._root = root
        self._canvas = canvas
        self._on_pet_change = on_pet_change
        self._on_skin_change = on_skin_change
        self._on_settings_open = on_settings_open
        self._on_quit = on_quit
        
        self._context_menu = self._create_context_menu()
        self._bind_events()
    
    def _create_context_menu(self) -> Menu:
        context_menu = Menu(self._root, tearoff=0)
        
        pet_menu = Menu(context_menu, tearoff=0)
        for pet_type in PetFactory.get_available_pet_types():
            display_name = PetFactory.get_pet_display_name(pet_type)
            pet_menu.add_command(
                label=display_name,
                command=lambda pt=pet_type: self._on_pet_change(pt)
            )
        context_menu.add_cascade(label="切换宠物", menu=pet_menu)
        
        skin_menu = Menu(context_menu, tearoff=0)
        for skin_color in SkinManager.get_available_skins():
            display_name = PetFactory.get_skin_display_name(skin_color)
            skin_menu.add_command(
                label=display_name,
                command=lambda sc=skin_color: self._on_skin_change(sc)
            )
        context_menu.add_cascade(label="更换皮肤", menu=skin_menu)
        
        context_menu.add_command(label="设置", command=self._on_settings_open)
        context_menu.add_separator()
        context_menu.add_command(label="退出", command=self._on_quit)
        
        return context_menu
    
    def _bind_events(self):
        self._canvas.bind("<Button-3>", self._show_menu)
    
    def _show_menu(self, event: tk.Event):
        self._context_menu.tk_popup(event.x_root, event.y_root)


class SettingsWindow:
    def __init__(
        self,
        root: tk.Tk,
        initial_size: int,
        sound_enabled: bool,
        auto_start: bool,
        on_size_change: Callable[[int], None],
        on_sound_toggle: Callable[[bool], None],
        on_autostart_toggle: Callable[[bool], None]
    ):
        self._root = root
        self._initial_size = initial_size
        self._sound_enabled = sound_enabled
        self._auto_start = auto_start
        self._on_size_change = on_size_change
        self._on_sound_toggle = on_sound_toggle
        self._on_autostart_toggle = on_autostart_toggle
        
        self._window: Optional[Toplevel] = None
    
    def show(self):
        if self._window is not None:
            self._window.lift()
            return
        
        self._window = Toplevel(self._root)
        self._window.title("设置")
        self._window.geometry(
            f"{UIConfig.SETTINGS_WINDOW_WIDTH}x{UIConfig.SETTINGS_WINDOW_HEIGHT}"
        )
        self._window.resizable(False, False)
        self._window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._create_widgets()
    
    def _create_widgets(self):
        Label(self._window, text="宠物大小:").pack(pady=10)
        
        size_scale = Scale(
            self._window,
            from_=UIConfig.MIN_PET_SIZE,
            to=UIConfig.MAX_PET_SIZE,
            orient=tk.HORIZONTAL,
            command=self._on_size_update
        )
        size_scale.set(self._initial_size)
        size_scale.pack(pady=5)
        
        self._sound_var = tk.BooleanVar(value=self._sound_enabled)
        sound_check = Checkbutton(
            self._window,
            text="开启音效",
            variable=self._sound_var,
            command=self._on_sound_update
        )
        sound_check.pack(pady=10)
        
        self._autostart_var = tk.BooleanVar(value=self._auto_start)
        autostart_check = Checkbutton(
            self._window,
            text="开机自启",
            variable=self._autostart_var,
            command=self._on_autostart_update
        )
        autostart_check.pack(pady=10)
        
        Button(self._window, text="关闭", command=self._on_close).pack(pady=20)
    
    def _on_size_update(self, value: str):
        size = int(value)
        self._on_size_change(size)
    
    def _on_sound_update(self):
        self._on_sound_toggle(self._sound_var.get())
    
    def _on_autostart_update(self):
        self._on_autostart_toggle(self._autostart_var.get())
    
    def _on_close(self):
        if self._window is not None:
            self._window.destroy()
            self._window = None


class SpeechBubble:
    DEFAULT_PHRASES = {
        "happy": [
            "主人好！",
            "今天天气真不错！",
            "看到你真开心！",
            "嘿嘿，我好喜欢这里！",
            "主人，陪我玩吧！"
        ],
        "curious": [
            "这是什么呀？",
            "让我看看~",
            "嗯？有新东西吗？",
            "主人在看什么呢？"
        ],
        "surprised": [
            "哇！吓我一跳！",
            "哦天啊！",
            "这是怎么回事？",
            "哇塞！"
        ],
        "tired": [
            "我有点困了...",
            "让我休息一会儿吧",
            "zzz...",
            "好累啊，想睡觉"
        ],
        "playful": [
            "来追我呀！",
            "我跳！",
            "主人，和我玩游戏吧！",
            "看我表演！"
        ]
    }
    
    def __init__(self, canvas: tk.Canvas, pet_size: int = 100):
        self._canvas = canvas
        self._pet_size = pet_size
        self._bubble_items: List[int] = []
        self._hide_timer: Optional[str] = None
        self._is_visible: bool = False
    
    def show(self, text: str, duration: int = 3000, emotion: str = "happy"):
        self.hide()
        
        center = self._pet_size // 2
        bubble_x = center
        bubble_y = center - 60
        
        padding_x = 15
        padding_y = 10
        min_width = 80
        min_height = 30
        
        text_width = len(text) * 12 + padding_x * 2
        text_height = 20 + padding_y * 2
        
        bubble_width = max(min_width, text_width)
        bubble_height = max(min_height, text_height)
        
        bubble_x1 = bubble_x - bubble_width // 2
        bubble_y1 = bubble_y - bubble_height // 2
        bubble_x2 = bubble_x + bubble_width // 2
        bubble_y2 = bubble_y + bubble_height // 2
        
        bg_color = ColorPalette.WHITE
        if emotion == "happy":
            bg_color = "#FFF9E6"
        elif emotion == "surprised":
            bg_color = "#E6F7FF"
        elif emotion == "tired":
            bg_color = "#F0F0F0"
        
        self._bubble_items.append(self._canvas.create_oval(
            bubble_x1, bubble_y1, bubble_x2, bubble_y2,
            fill=bg_color, outline=ColorPalette.BLACK, width=1
        ))
        
        self._bubble_items.append(self._canvas.create_oval(
            bubble_x1 + 2, bubble_y1 + 2, bubble_x2 - 2, bubble_y2 - 2,
            fill=bg_color, outline=""
        ))
        
        tail_x = center
        tail_y1 = bubble_y2
        tail_y2 = bubble_y2 + 10
        self._bubble_items.append(self._canvas.create_polygon(
            tail_x - 6, tail_y1,
            tail_x + 6, tail_y1,
            tail_x, tail_y2,
            fill=bg_color, outline=ColorPalette.BLACK
        ))
        
        self._bubble_items.append(self._canvas.create_text(
            bubble_x, bubble_y, text=text,
            font=("Arial", 10), fill=ColorPalette.BLACK
        ))
        
        self._is_visible = True
        
        if self._hide_timer is not None:
            self._canvas.after_cancel(self._hide_timer)
        
        self._hide_timer = self._canvas.after(duration, self.hide)
    
    def show_random(self, emotion: str = "happy", duration: int = 3000):
        phrases = self.DEFAULT_PHRASES.get(emotion, self.DEFAULT_PHRASES["happy"])
        text = random.choice(phrases)
        self.show(text, duration, emotion)
    
    def hide(self):
        if self._hide_timer is not None:
            try:
                self._canvas.after_cancel(self._hide_timer)
            except Exception:
                pass
            self._hide_timer = None
        
        for item in self._bubble_items:
            try:
                self._canvas.delete(item)
            except Exception:
                pass
        self._bubble_items.clear()
        self._is_visible = False
    
    @property
    def is_visible(self) -> bool:
        return self._is_visible


class EmotionDisplay:
    EMOTION_SYMBOLS = {
        "heart": {
            "symbols": ["❤️", "💕", "💖"],
            "color": "#FF6B6B",
            "description": "开心、喜欢"
        },
        "star": {
            "symbols": ["⭐", "✨", "🌟"],
            "color": "#FFD700",
            "description": "惊讶、兴奋"
        },
        "music": {
            "symbols": ["🎵", "🎶", "♪"],
            "color": "#9B59B6",
            "description": "唱歌、愉快"
        },
        "question": {
            "symbols": ["❓", "🤔", "?"],
            "color": "#3498DB",
            "description": "困惑、好奇"
        },
        "exclamation": {
            "symbols": ["❗", "❕", "!"],
            "color": "#E74C3C",
            "description": "惊讶、激动"
        },
        "sweat": {
            "symbols": ["💧", "😅", "💦"],
            "color": "#3498DB",
            "description": "尴尬、紧张"
        },
        "angry": {
            "symbols": ["💢", "😠", "👊"],
            "color": "#E74C3C",
            "description": "生气、愤怒"
        },
        "sleep": {
            "symbols": ["💤", "😴", "zzz"],
            "color": "#95A5A6",
            "description": "困倦、睡觉"
        }
    }
    
    def __init__(self, canvas: tk.Canvas, pet_size: int = 100):
        self._canvas = canvas
        self._pet_size = pet_size
        self._emotion_items: List[int] = []
        self._hide_timer: Optional[str] = None
        self._animation_timer: Optional[str] = None
        self._is_visible: bool = False
        self._current_emotion: Optional[str] = None
        self._animation_frame: int = 0
    
    def show(self, emotion: str = "heart", duration: int = 2000, count: int = 3):
        self.hide()
        
        if emotion not in self.EMOTION_SYMBOLS:
            emotion = "heart"
        
        self._current_emotion = emotion
        self._animation_frame = 0
        
        emotion_data = self.EMOTION_SYMBOLS[emotion]
        symbols = emotion_data["symbols"]
        color = emotion_data["color"]
        
        center = self._pet_size // 2
        positions = [
            (center - 40, center - 50),
            (center + 40, center - 45),
            (center, center - 60),
            (center - 25, center - 70),
            (center + 25, center - 65)
        ]
        
        for i in range(min(count, len(positions))):
            symbol = random.choice(symbols)
            x, y = positions[i]
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            
            self._emotion_items.append(self._canvas.create_text(
                x + offset_x, y + offset_y,
                text=symbol,
                font=("Arial", 14, "bold"),
                fill=color
            ))
        
        self._is_visible = True
        self._start_animation()
        
        if self._hide_timer is not None:
            self._canvas.after_cancel(self._hide_timer)
        
        self._hide_timer = self._canvas.after(duration, self.hide)
    
    def _start_animation(self):
        if self._animation_timer is not None:
            self._canvas.after_cancel(self._animation_timer)
        
        self._animate_emotion()
    
    def _animate_emotion(self):
        if not self._is_visible:
            return
        
        self._animation_frame += 1
        float_offset = self._animation_frame % 4
        
        for i, item in enumerate(self._emotion_items):
            try:
                y_offset = -float_offset if i % 2 == 0 else float_offset
                self._canvas.move(item, 0, y_offset * 0.5)
            except Exception:
                pass
        
        self._animation_timer = self._canvas.after(150, self._animate_emotion)
    
    def show_random(self, duration: int = 2000):
        emotions = list(self.EMOTION_SYMBOLS.keys())
        emotion = random.choice(emotions)
        self.show(emotion, duration)
    
    def hide(self):
        if self._hide_timer is not None:
            try:
                self._canvas.after_cancel(self._hide_timer)
            except Exception:
                pass
            self._hide_timer = None
        
        if self._animation_timer is not None:
            try:
                self._canvas.after_cancel(self._animation_timer)
            except Exception:
                pass
            self._animation_timer = None
        
        for item in self._emotion_items:
            try:
                self._canvas.delete(item)
            except Exception:
                pass
        self._emotion_items.clear()
        self._is_visible = False
        self._current_emotion = None
    
    @property
    def is_visible(self) -> bool:
        return self._is_visible
    
    @property
    def current_emotion(self) -> Optional[str]:
        return self._current_emotion