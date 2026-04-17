import tkinter as tk
from tkinter import Menu, Toplevel, Label, Scale, Button, Checkbutton
from typing import Optional, Callable, Any, List, Tuple
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
    
    TRANSPARENT_COLOR = "#00FF00"
    
    def __init__(
        self, 
        root: tk.Tk, 
        pet_size: int = 100,
        get_pet_position: Optional[Callable[[], Tuple[int, int]]] = None
    ):
        self._root = root
        self._pet_size = pet_size
        self._get_pet_position = get_pet_position
        self._bubble_window: Optional[tk.Toplevel] = None
        self._canvas: Optional[tk.Canvas] = None
        self._hide_timer: Optional[str] = None
        self._is_visible: bool = False
        self._current_text: str = ""
        self._current_emotion: str = "happy"
    
    def _create_bubble_window(self):
        if self._bubble_window is not None:
            return
        
        self._bubble_window = tk.Toplevel(self._root)
        self._bubble_window.overrideredirect(True)
        self._bubble_window.attributes("-topmost", True)
        self._bubble_window.attributes("-transparentcolor", self.TRANSPARENT_COLOR)
        self._bubble_window.withdraw()
        
        self._canvas = tk.Canvas(
            self._bubble_window,
            width=300,
            height=150,
            bg=self.TRANSPARENT_COLOR,
            highlightthickness=0
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)
    
    def _calculate_bubble_size(self, text: str) -> Tuple[int, int]:
        padding_x = 20
        padding_y = 15
        min_width = 100
        min_height = 50
        
        text_width = len(text) * 12 + padding_x * 2
        text_height = 40 + padding_y
        
        bubble_width = max(min_width, text_width)
        bubble_height = max(min_height, text_height)
        
        return bubble_width, bubble_height
    
    def _calculate_position(self, bubble_width: int, bubble_height: int) -> Tuple[int, int]:
        if self._get_pet_position is not None:
            pet_x, pet_y = self._get_pet_position()
        else:
            pet_x = self._root.winfo_x()
            pet_y = self._root.winfo_y()
        
        bubble_x = pet_x + (self._pet_size - bubble_width) // 2
        bubble_y = pet_y - bubble_height - 10
        
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        
        if bubble_x < 10:
            bubble_x = 10
        elif bubble_x + bubble_width > screen_width - 10:
            bubble_x = screen_width - bubble_width - 10
        
        if bubble_y < 10:
            bubble_y = pet_y + self._pet_size + 10
        
        return bubble_x, bubble_y
    
    def _draw_bubble(self, text: str, emotion: str):
        if self._canvas is None:
            return
        
        self._canvas.delete("all")
        
        bubble_width, bubble_height = self._calculate_bubble_size(text)
        center_x = 150
        center_y = 60
        
        bubble_x1 = center_x - bubble_width // 2
        bubble_y1 = center_y - bubble_height // 2
        bubble_x2 = center_x + bubble_width // 2
        bubble_y2 = center_y + bubble_height // 2
        
        bg_color = ColorPalette.WHITE
        if emotion == "happy":
            bg_color = "#FFF9E6"
        elif emotion == "surprised":
            bg_color = "#E6F7FF"
        elif emotion == "tired":
            bg_color = "#F0F0F0"
        elif emotion == "curious":
            bg_color = "#E8F5E9"
        elif emotion == "playful":
            bg_color = "#FCE4EC"
        
        self._canvas.create_oval(
            bubble_x1, bubble_y1, bubble_x2, bubble_y2,
            fill=bg_color, outline=ColorPalette.BLACK, width=2
        )
        
        self._canvas.create_oval(
            bubble_x1 + 3, bubble_y1 + 3, bubble_x2 - 3, bubble_y2 - 3,
            fill=bg_color, outline=""
        )
        
        tail_x = center_x
        tail_y1 = bubble_y2
        tail_y2 = bubble_y2 + 20
        tail_offset = 12
        
        self._canvas.create_polygon(
            tail_x - tail_offset, tail_y1,
            tail_x + tail_offset, tail_y1,
            tail_x, tail_y2,
            fill=bg_color, outline=ColorPalette.BLACK
        )
        
        self._canvas.create_text(
            center_x, center_y, text=text,
            font=("Microsoft YaHei", 11), fill=ColorPalette.BLACK
        )
    
    def show(self, text: str, duration: int = 3000, emotion: str = "happy"):
        self.hide()
        
        self._create_bubble_window()
        
        if self._bubble_window is None or self._canvas is None:
            return
        
        self._current_text = text
        self._current_emotion = emotion
        
        self._draw_bubble(text, emotion)
        
        bubble_width, bubble_height = self._calculate_bubble_size(text)
        window_width = 300
        window_height = 150
        
        self._bubble_window.geometry(f"{window_width}x{window_height}")
        
        bubble_x, bubble_y = self._calculate_position(window_width, window_height)
        self._bubble_window.geometry(f"+{bubble_x}+{bubble_y}")
        
        self._bubble_window.deiconify()
        self._bubble_window.lift()
        self._root.lift()
        
        self._is_visible = True
        
        if self._hide_timer is not None:
            self._root.after_cancel(self._hide_timer)
        
        self._hide_timer = self._root.after(duration, self.hide)
    
    def show_random(self, emotion: str = "happy", duration: int = 3000):
        phrases = self.DEFAULT_PHRASES.get(emotion, self.DEFAULT_PHRASES["happy"])
        text = random.choice(phrases)
        self.show(text, duration, emotion)
    
    def update_position(self):
        if not self._is_visible or self._bubble_window is None:
            return
        
        window_width = 300
        window_height = 150
        
        bubble_x, bubble_y = self._calculate_position(window_width, window_height)
        self._bubble_window.geometry(f"+{bubble_x}+{bubble_y}")
    
    def hide(self):
        if self._hide_timer is not None:
            try:
                self._root.after_cancel(self._hide_timer)
            except Exception:
                pass
            self._hide_timer = None
        
        if self._bubble_window is not None:
            try:
                self._bubble_window.withdraw()
            except Exception:
                pass
        
        self._is_visible = False
    
    @property
    def is_visible(self) -> bool:
        return self._is_visible
    
    @property
    def current_text(self) -> str:
        return self._current_text
    
    @property
    def current_emotion(self) -> str:
        return self._current_emotion


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
    
    TRANSPARENT_COLOR = "#00FF00"
    
    def __init__(
        self, 
        root: tk.Tk, 
        pet_size: int = 100,
        get_pet_position: Optional[Callable[[], Tuple[int, int]]] = None
    ):
        self._root = root
        self._pet_size = pet_size
        self._get_pet_position = get_pet_position
        self._emotion_window: Optional[tk.Toplevel] = None
        self._canvas: Optional[tk.Canvas] = None
        self._emotion_items: List[int] = []
        self._hide_timer: Optional[str] = None
        self._animation_timer: Optional[str] = None
        self._is_visible: bool = False
        self._current_emotion: Optional[str] = None
        self._animation_frame: int = 0
    
    def _create_emotion_window(self):
        if self._emotion_window is not None:
            return
        
        self._emotion_window = tk.Toplevel(self._root)
        self._emotion_window.overrideredirect(True)
        self._emotion_window.attributes("-topmost", True)
        self._emotion_window.attributes("-transparentcolor", self.TRANSPARENT_COLOR)
        self._emotion_window.withdraw()
        
        self._canvas = tk.Canvas(
            self._emotion_window,
            width=200,
            height=200,
            bg=self.TRANSPARENT_COLOR,
            highlightthickness=0
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)
    
    def _calculate_position(self) -> Tuple[int, int]:
        if self._get_pet_position is not None:
            pet_x, pet_y = self._get_pet_position()
        else:
            pet_x = self._root.winfo_x()
            pet_y = self._root.winfo_y()
        
        emotion_x = pet_x + (self._pet_size - 200) // 2
        emotion_y = pet_y - 80
        
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        
        if emotion_x < 10:
            emotion_x = 10
        elif emotion_x + 200 > screen_width - 10:
            emotion_x = screen_width - 210
        
        if emotion_y < 10:
            emotion_y = pet_y + self._pet_size + 10
        
        return emotion_x, emotion_y
    
    def show(self, emotion: str = "heart", duration: int = 2000, count: int = 3):
        self.hide()
        
        self._create_emotion_window()
        
        if self._emotion_window is None or self._canvas is None:
            return
        
        if emotion not in self.EMOTION_SYMBOLS:
            emotion = "heart"
        
        self._current_emotion = emotion
        self._animation_frame = 0
        
        emotion_data = self.EMOTION_SYMBOLS[emotion]
        symbols = emotion_data["symbols"]
        color = emotion_data["color"]
        
        center_x = 100
        center_y = 100
        positions = [
            (center_x - 50, center_y - 40),
            (center_x + 50, center_y - 35),
            (center_x, center_y - 50),
            (center_x - 35, center_y - 60),
            (center_x + 35, center_y - 55)
        ]
        
        self._emotion_items = []
        for i in range(min(count, len(positions))):
            symbol = random.choice(symbols)
            x, y = positions[i]
            offset_x = random.randint(-15, 15)
            offset_y = random.randint(-15, 15)
            
            self._emotion_items.append(self._canvas.create_text(
                x + offset_x, y + offset_y,
                text=symbol,
                font=("Segoe UI Emoji", 18),
                fill=color
            ))
        
        emotion_x, emotion_y = self._calculate_position()
        self._emotion_window.geometry(f"200x200+{emotion_x}+{emotion_y}")
        
        self._emotion_window.deiconify()
        self._emotion_window.lift()
        self._root.lift()
        
        self._is_visible = True
        self._start_animation()
        
        if self._hide_timer is not None:
            self._root.after_cancel(self._hide_timer)
        
        self._hide_timer = self._root.after(duration, self.hide)
    
    def _start_animation(self):
        if self._animation_timer is not None:
            self._root.after_cancel(self._animation_timer)
        
        self._animate_emotion()
    
    def _animate_emotion(self):
        if not self._is_visible or self._canvas is None:
            return
        
        self._animation_frame += 1
        float_offset = self._animation_frame % 4
        
        for i, item in enumerate(self._emotion_items):
            try:
                y_offset = -float_offset if i % 2 == 0 else float_offset
                self._canvas.move(item, 0, y_offset * 0.8)
            except Exception:
                pass
        
        self._animation_timer = self._root.after(150, self._animate_emotion)
    
    def show_random(self, duration: int = 2000):
        emotions = list(self.EMOTION_SYMBOLS.keys())
        emotion = random.choice(emotions)
        self.show(emotion, duration)
    
    def update_position(self):
        if not self._is_visible or self._emotion_window is None:
            return
        
        emotion_x, emotion_y = self._calculate_position()
        self._emotion_window.geometry(f"+{emotion_x}+{emotion_y}")
    
    def hide(self):
        if self._hide_timer is not None:
            try:
                self._root.after_cancel(self._hide_timer)
            except Exception:
                pass
            self._hide_timer = None
        
        if self._animation_timer is not None:
            try:
                self._root.after_cancel(self._animation_timer)
            except Exception:
                pass
            self._animation_timer = None
        
        if self._emotion_window is not None:
            try:
                self._emotion_window.withdraw()
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