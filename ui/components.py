import tkinter as tk
from tkinter import Menu, Toplevel, Label, Scale, Button, Checkbutton
from typing import Optional, Callable, Any
from core.config import (
    PetType,
    SkinColor,
    UIConfig,
    PetDisplayNames
)
from pets.factory import PetFactory, SkinManager


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