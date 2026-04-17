import tkinter as tk
from tkinter import Menu, Toplevel, Label, Scale, Button, Checkbutton
import random
import time
import os
import sys
import winsound
from PIL import Image, ImageTk
import threading

class PetApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("萌宠桌面小助手")
        
        # 配置参数
        self.pet_size = 100  # 默认大小
        self.sound_enabled = True
        self.auto_start = False
        
        # 宠物状态
        self.current_state = "idle"
        self.current_pet = "cat"
        self.current_skin = "orange"
        
        # 位置和动画参数
        self.x = 100
        self.y = 100
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # 动画帧索引
        self.frame_index = 0
        self.animation_speed = 200  # 毫秒
        
        # 随机行为参数
        self.walk_direction = 1  # 1=右，-1=左
        self.walk_distance = 0
        self.random_timer = None
        
        # 创建窗口
        self.setup_window()
        self.create_pet_images()
        self.setup_mouse_events()
        self.setup_context_menu()
        self.start_animation()
        self.start_random_behavior()
        
    def setup_window(self):
        # 窗口设置：透明、无边框、置顶
        self.root.overrideredirect(True)  # 去除边框
        self.root.attributes("-topmost", True)  # 置顶
        self.root.attributes("-transparentcolor", "white")  # 透明色
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 设置初始位置（右下角）
        self.x = screen_width - self.pet_size - 50
        self.y = screen_height - self.pet_size - 100
        
        # 初始化窗口大小和位置
        self.root.geometry(f"{self.pet_size}x{self.pet_size}+{self.x}+{self.y}")
        
    def create_pet_images(self):
        # 创建简单的宠物图案（使用文本和简单图形）
        # 由于没有实际图片文件，我们使用Canvas绘制
        self.pet_canvas = tk.Canvas(self.root, width=self.pet_size, height=self.pet_size, 
                                      bg="white", highlightthickness=0)
        self.pet_canvas.pack(fill=tk.BOTH, expand=True)
        
    def draw_pet(self):
        self.pet_canvas.delete("all")
        size = self.pet_size
        center = size // 2
        
        # 根据宠物类型选择绘制方法
        if self.current_pet == "cat":
            self.draw_cat(center)
        elif self.current_pet == "dog":
            self.draw_dog(center)
        elif self.current_pet == "rabbit":
            self.draw_rabbit(center)
    
    # ==================== 猫咪绘制方法 ====================
    def draw_cat(self, center):
        if self.current_state == "idle":
            self.draw_idle_cat(center)
        elif self.current_state == "walk":
            self.draw_walk_cat(center)
        elif self.current_state == "happy":
            self.draw_happy_cat(center)
        elif self.current_state == "sleep":
            self.draw_sleep_cat(center)
        elif self.current_state == "jump":
            self.draw_jump_cat(center)
    
    def draw_idle_cat(self, center):
        size = self.pet_size
        # 身体
        self.pet_canvas.create_oval(center-30, center-10, center+30, center+25, 
                                      fill=self.get_skin_color(), outline="black")
        # 头
        self.pet_canvas.create_oval(center-25, center-40, center+25, center-10, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（尖耳朵）
        self.pet_canvas.create_polygon(center-20, center-35, center-30, center-50, center-10, center-45, 
                                         fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_polygon(center+20, center-35, center+30, center-50, center+10, center-45, 
                                         fill=self.get_skin_color(), outline="black")
        # 眼睛（眨眼动画）
        eye_y = center-28
        if self.frame_index % 20 < 2:  # 偶尔眨眼
            self.pet_canvas.create_line(center-12, eye_y, center-8, eye_y, width=2)
            self.pet_canvas.create_line(center+8, eye_y, center+12, eye_y, width=2)
        else:
            self.pet_canvas.create_oval(center-12, eye_y-2, center-8, eye_y+2, fill="black")
            self.pet_canvas.create_oval(center+8, eye_y-2, center+12, eye_y+2, fill="black")
        # 鼻子（粉色小鼻子）
        self.pet_canvas.create_oval(center-2, center-20, center+2, center-17, fill="pink")
        # 嘴（W形嘴）
        self.pet_canvas.create_arc(center-8, center-18, center+8, center-12, 
                                     start=180, extent=180, style=tk.ARC)
        # 胡须
        self.pet_canvas.create_line(center-25, center-18, center-8, center-20, width=1)
        self.pet_canvas.create_line(center-25, center-15, center-8, center-17, width=1)
        self.pet_canvas.create_line(center+8, center-20, center+25, center-18, width=1)
        self.pet_canvas.create_line(center+8, center-17, center+25, center-15, width=1)
        # 尾巴（长尾巴摇摆）
        tail_x = center+35
        tail_y = center+10
        tail_wave = 5 if self.frame_index % 10 < 5 else -5
        self.pet_canvas.create_line(tail_x, tail_y, tail_x+15, tail_y+tail_wave, 
                                      width=4, fill=self.get_skin_color(), smooth=True)
    
    def draw_walk_cat(self, center):
        size = self.pet_size
        # 身体
        self.pet_canvas.create_oval(center-30, center-10, center+30, center+25, 
                                      fill=self.get_skin_color(), outline="black")
        # 头
        self.pet_canvas.create_oval(center-25, center-40, center+25, center-10, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵
        self.pet_canvas.create_polygon(center-20, center-35, center-30, center-50, center-10, center-45, 
                                         fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_polygon(center+20, center-35, center+30, center-50, center+10, center-45, 
                                         fill=self.get_skin_color(), outline="black")
        # 眼睛
        eye_y = center-28
        self.pet_canvas.create_oval(center-12, eye_y-2, center-8, eye_y+2, fill="black")
        self.pet_canvas.create_oval(center+8, eye_y-2, center+12, eye_y+2, fill="black")
        # 鼻子
        self.pet_canvas.create_oval(center-2, center-20, center+2, center-17, fill="pink")
        # 嘴
        self.pet_canvas.create_arc(center-8, center-18, center+8, center-12, 
                                     start=180, extent=180, style=tk.ARC)
        # 走路的腿（动画）
        leg_offset = 5 if self.frame_index % 4 < 2 else -5
        self.pet_canvas.create_line(center-15, center+25, center-15, center+35+leg_offset, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center-5, center+25, center-5, center+35-leg_offset, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+5, center+25, center+5, center+35+leg_offset, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+15, center+25, center+15, center+35-leg_offset, 
                                      width=4, fill=self.get_skin_color())
        # 尾巴摆动
        tail_x = center+35
        tail_y = center+10
        tail_wave = 8 if self.frame_index % 4 < 2 else -8
        self.pet_canvas.create_line(tail_x, tail_y, tail_x+15, tail_y+tail_wave, 
                                      width=4, fill=self.get_skin_color(), smooth=True)
    
    def draw_happy_cat(self, center):
        size = self.pet_size
        # 身体
        self.pet_canvas.create_oval(center-30, center-10, center+30, center+25, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（稍微大一点表示开心）
        self.pet_canvas.create_oval(center-28, center-42, center+28, center-8, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵
        self.pet_canvas.create_polygon(center-22, center-37, center-32, center-52, center-12, center-47, 
                                         fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_polygon(center+22, center-37, center+32, center-52, center+12, center-47, 
                                         fill=self.get_skin_color(), outline="black")
        # 开心的眼睛（弯月形）
        eye_y = center-28
        self.pet_canvas.create_arc(center-14, eye_y-4, center-6, eye_y+4, 
                                     start=180, extent=180, style=tk.ARC, width=2)
        self.pet_canvas.create_arc(center+6, eye_y-4, center+14, eye_y+4, 
                                     start=180, extent=180, style=tk.ARC, width=2)
        # 鼻子
        self.pet_canvas.create_oval(center-2, center-20, center+2, center-17, fill="pink")
        # 开心的嘴（大微笑）
        self.pet_canvas.create_arc(center-12, center-22, center+12, center-8, 
                                     start=180, extent=180, width=2)
        # 腮红
        self.pet_canvas.create_oval(center-22, center-22, center-16, center-16, fill="pink", outline="")
        self.pet_canvas.create_oval(center+16, center-22, center+22, center-16, fill="pink", outline="")
        # 开心跳动的效果
        jump_offset = -5 if self.frame_index % 4 < 2 else 0
        # 尾巴快速摇摆
        tail_x = center+35
        tail_y = center+10 + jump_offset
        tail_wave = 10 if self.frame_index % 2 == 0 else -10
        self.pet_canvas.create_line(tail_x, tail_y, tail_x+18, tail_y+tail_wave, 
                                      width=4, fill=self.get_skin_color(), smooth=True)
    
    def draw_sleep_cat(self, center):
        size = self.pet_size
        # 身体（蜷缩状）
        self.pet_canvas.create_oval(center-35, center-5, center+25, center+30, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（靠在身体上）
        self.pet_canvas.create_oval(center-30, center-25, center, center+5, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵
        self.pet_canvas.create_polygon(center-25, center-20, center-35, center-35, center-15, center-30, 
                                         fill=self.get_skin_color(), outline="black")
        # 睡眠的眼睛（闭着）
        eye_y = center-13
        self.pet_canvas.create_line(center-22, eye_y, center-15, eye_y, width=2)
        self.pet_canvas.create_line(center-8, eye_y, center-1, eye_y, width=2)
        # Zzz 睡眠符号
        z_offset = self.frame_index % 30
        if z_offset < 10:
            self.pet_canvas.create_text(center+20, center-30, text="Z", font=("Arial", 12), fill="gray")
        elif z_offset < 20:
            self.pet_canvas.create_text(center+20, center-30, text="Z", font=("Arial", 12), fill="gray")
            self.pet_canvas.create_text(center+30, center-40, text="z", font=("Arial", 10), fill="gray")
        else:
            self.pet_canvas.create_text(center+20, center-30, text="Z", font=("Arial", 12), fill="gray")
            self.pet_canvas.create_text(center+30, center-40, text="z", font=("Arial", 10), fill="gray")
            self.pet_canvas.create_text(center+40, center-50, text="z", font=("Arial", 8), fill="gray")
    
    def draw_jump_cat(self, center):
        size = self.pet_size
        # 跳跃高度
        jump_height = 20 if self.frame_index % 4 < 2 else 0
        
        # 身体
        self.pet_canvas.create_oval(center-30, center-10-jump_height, center+30, center+25-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 头
        self.pet_canvas.create_oval(center-25, center-40-jump_height, center+25, center-10-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵
        self.pet_canvas.create_polygon(center-20, center-35-jump_height, center-30, center-50-jump_height, 
                                         center-10, center-45-jump_height, 
                                         fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_polygon(center+20, center-35-jump_height, center+30, center-50-jump_height, 
                                         center+10, center-45-jump_height, 
                                         fill=self.get_skin_color(), outline="black")
        # 惊讶的眼睛
        eye_y = center-28-jump_height
        self.pet_canvas.create_oval(center-12, eye_y-3, center-8, eye_y+3, fill="black")
        self.pet_canvas.create_oval(center+8, eye_y-3, center+12, eye_y+3, fill="black")
        # 惊讶的嘴
        self.pet_canvas.create_oval(center-4, center-18-jump_height, center+4, center-12-jump_height, 
                                      fill="black")
        # 跳跃的腿（伸展）
        self.pet_canvas.create_line(center-15, center+25, center-20, center+40, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center-5, center+25, center-10, center+40, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+5, center+25, center+10, center+40, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+15, center+25, center+20, center+40, 
                                      width=4, fill=self.get_skin_color())
        # 尾巴
        tail_x = center+35
        tail_y = center+10-jump_height
        self.pet_canvas.create_line(tail_x, tail_y, tail_x+20, tail_y, 
                                      width=4, fill=self.get_skin_color(), smooth=True)
    
    # ==================== 狗狗绘制方法 ====================
    def draw_dog(self, center):
        if self.current_state == "idle":
            self.draw_idle_dog(center)
        elif self.current_state == "walk":
            self.draw_walk_dog(center)
        elif self.current_state == "happy":
            self.draw_happy_dog(center)
        elif self.current_state == "sleep":
            self.draw_sleep_dog(center)
        elif self.current_state == "jump":
            self.draw_jump_dog(center)
    
    def draw_idle_dog(self, center):
        size = self.pet_size
        # 身体（更健壮的身体）
        self.pet_canvas.create_oval(center-32, center-8, center+32, center+28, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（更圆的头）
        self.pet_canvas.create_oval(center-28, center-42, center+28, center-8, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（垂耳 - 狗狗特征）
        self.pet_canvas.create_oval(center-35, center-40, center-20, center-20, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+20, center-40, center+35, center-20, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵内部（粉色）
        self.pet_canvas.create_oval(center-33, center-38, center-22, center-22, 
                                      fill="#FFB6C1", outline="")
        self.pet_canvas.create_oval(center+22, center-38, center+33, center-22, 
                                      fill="#FFB6C1", outline="")
        # 眼睛（眨眼动画）
        eye_y = center-26
        if self.frame_index % 20 < 2:
            self.pet_canvas.create_line(center-15, eye_y, center-10, eye_y, width=2)
            self.pet_canvas.create_line(center+10, eye_y, center+15, eye_y, width=2)
        else:
            self.pet_canvas.create_oval(center-15, eye_y-3, center-10, eye_y+3, fill="black")
            self.pet_canvas.create_oval(center+10, eye_y-3, center+15, eye_y+3, fill="black")
            # 狗狗的眼睛有高光
            self.pet_canvas.create_oval(center-13, eye_y-1, center-11, eye_y+1, fill="white")
            self.pet_canvas.create_oval(center+12, eye_y-1, center+14, eye_y+1, fill="white")
        # 鼻子（黑色椭圆鼻子 - 狗狗特征）
        self.pet_canvas.create_oval(center-6, center-18, center+6, center-12, fill="black")
        # 鼻子高光
        self.pet_canvas.create_oval(center-4, center-16, center-2, center-14, fill="gray")
        # 嘴（狗狗的嘴 - 有舌头）
        self.pet_canvas.create_line(center, center-12, center, center-8, width=2)
        # 舌头（偶尔伸出）
        if self.frame_index % 10 < 5:
            self.pet_canvas.create_oval(center-3, center-6, center+3, center+2, fill="pink", outline="")
        # 眉毛（狗狗特征）
        self.pet_canvas.create_arc(center-18, center-32, center-10, center-28, 
                                     start=0, extent=180, style=tk.ARC, width=2)
        self.pet_canvas.create_arc(center+10, center-32, center+18, center-28, 
                                     start=0, extent=180, style=tk.ARC, width=2)
        # 尾巴（短而卷曲的尾巴 - 狗狗特征）
        tail_x = center+35
        tail_y = center+5
        tail_wave = 8 if self.frame_index % 6 < 3 else -8
        # 卷曲的尾巴
        self.pet_canvas.create_arc(tail_x-5, tail_y-10, tail_x+20, tail_y+10, 
                                     start=270, extent=180+tail_wave, style=tk.ARC, 
                                     width=4, outline=self.get_skin_color())
    
    def draw_walk_dog(self, center):
        size = self.pet_size
        # 身体
        self.pet_canvas.create_oval(center-32, center-8, center+32, center+28, 
                                      fill=self.get_skin_color(), outline="black")
        # 头
        self.pet_canvas.create_oval(center-28, center-42, center+28, center-8, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（垂耳）
        self.pet_canvas.create_oval(center-35, center-40, center-20, center-20, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+20, center-40, center+35, center-20, 
                                      fill=self.get_skin_color(), outline="black")
        # 眼睛
        eye_y = center-26
        self.pet_canvas.create_oval(center-15, eye_y-3, center-10, eye_y+3, fill="black")
        self.pet_canvas.create_oval(center+10, eye_y-3, center+15, eye_y+3, fill="black")
        # 鼻子
        self.pet_canvas.create_oval(center-6, center-18, center+6, center-12, fill="black")
        # 嘴和舌头
        self.pet_canvas.create_line(center, center-12, center, center-8, width=2)
        self.pet_canvas.create_oval(center-3, center-6, center+3, center+2, fill="pink", outline="")
        # 走路的腿
        leg_offset = 6 if self.frame_index % 4 < 2 else -6
        self.pet_canvas.create_line(center-18, center+28, center-18, center+40+leg_offset, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center-8, center+28, center-8, center+40-leg_offset, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+8, center+28, center+8, center+40+leg_offset, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+18, center+28, center+18, center+40-leg_offset, 
                                      width=5, fill=self.get_skin_color())
        # 爪子
        paw_color = "#8B4513" if self.current_skin != "black" else "#555555"
        self.pet_canvas.create_oval(center-22, center+38+leg_offset, center-14, center+43+leg_offset, 
                                      fill=paw_color, outline="black")
        self.pet_canvas.create_oval(center-12, center+38-leg_offset, center-4, center+43-leg_offset, 
                                      fill=paw_color, outline="black")
        self.pet_canvas.create_oval(center+4, center+38+leg_offset, center+12, center+43+leg_offset, 
                                      fill=paw_color, outline="black")
        self.pet_canvas.create_oval(center+14, center+38-leg_offset, center+22, center+43-leg_offset, 
                                      fill=paw_color, outline="black")
        # 尾巴摇摆
        tail_x = center+35
        tail_y = center+5
        tail_wave = 15 if self.frame_index % 4 < 2 else -15
        self.pet_canvas.create_arc(tail_x-5, tail_y-12, tail_x+22, tail_y+8, 
                                     start=270, extent=160+tail_wave, style=tk.ARC, 
                                     width=4, outline=self.get_skin_color())
    
    def draw_happy_dog(self, center):
        size = self.pet_size
        # 身体
        self.pet_canvas.create_oval(center-32, center-8, center+32, center+28, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（开心时头稍微抬起）
        head_offset = -3 if self.frame_index % 4 < 2 else 0
        self.pet_canvas.create_oval(center-28, center-45+head_offset, center+28, center-11+head_offset, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（垂耳，开心时稍微竖起）
        ear_offset = -5 if self.frame_index % 4 < 2 else 0
        self.pet_canvas.create_oval(center-35, center-43+ear_offset, center-20, center-23+ear_offset, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+20, center-43+ear_offset, center+35, center-23+ear_offset, 
                                      fill=self.get_skin_color(), outline="black")
        # 开心的眼睛（弯月形，狗狗的眼睛更大）
        eye_y = center-29
        self.pet_canvas.create_arc(center-17, eye_y-5, center-8, eye_y+5, 
                                     start=180, extent=180, style=tk.ARC, width=2)
        self.pet_canvas.create_arc(center+8, eye_y-5, center+17, eye_y+5, 
                                     start=180, extent=180, style=tk.ARC, width=2)
        # 鼻子
        self.pet_canvas.create_oval(center-6, center-20, center+6, center-14, fill="black")
        # 开心的嘴（大微笑，舌头伸出）
        self.pet_canvas.create_arc(center-15, center-18, center+15, center-2, 
                                     start=180, extent=180, width=2, fill="", outline="black")
        # 大舌头
        self.pet_canvas.create_oval(center-5, center-4, center+5, center+8, fill="pink", outline="")
        # 腮红
        self.pet_canvas.create_oval(center-25, center-24, center-18, center-18, fill="pink", outline="")
        self.pet_canvas.create_oval(center+18, center-24, center+25, center-18, fill="pink", outline="")
        # 开心跳动的效果
        jump_offset = -8 if self.frame_index % 4 < 2 else 0
        # 尾巴快速摇摆（非常开心）
        tail_x = center+35
        tail_y = center+5 + jump_offset
        tail_wave = 25 if self.frame_index % 2 == 0 else -25
        self.pet_canvas.create_arc(tail_x-5, tail_y-15, tail_x+25, tail_y+5, 
                                     start=270, extent=140+tail_wave, style=tk.ARC, 
                                     width=4, outline=self.get_skin_color())
    
    def draw_sleep_dog(self, center):
        size = self.pet_size
        # 身体（趴着睡）
        self.pet_canvas.create_oval(center-35, center, center+35, center+35, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（趴在身体上，侧向一边）
        self.pet_canvas.create_oval(center-30, center-15, center-5, center+15, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（一只垂着）
        self.pet_canvas.create_oval(center-35, center-20, center-25, center-5, 
                                      fill=self.get_skin_color(), outline="black")
        # 睡眠的眼睛（闭着，狗狗的眼睛位置不同）
        eye_y = center-2
        self.pet_canvas.create_line(center-25, eye_y, center-18, eye_y, width=2)
        self.pet_canvas.create_line(center-12, eye_y+2, center-5, eye_y+2, width=2)
        # 鼻子
        self.pet_canvas.create_oval(center-8, center+5, center-2, center+10, fill="black")
        # 呼吸动画（身体起伏）
        breath_offset = 2 if self.frame_index % 10 < 5 else 0
        # Zzz 睡眠符号
        z_offset = self.frame_index % 30
        if z_offset < 10:
            self.pet_canvas.create_text(center+15, center-20, text="Z", font=("Arial", 12), fill="gray")
        elif z_offset < 20:
            self.pet_canvas.create_text(center+15, center-20, text="Z", font=("Arial", 12), fill="gray")
            self.pet_canvas.create_text(center+25, center-30, text="z", font=("Arial", 10), fill="gray")
        else:
            self.pet_canvas.create_text(center+15, center-20, text="Z", font=("Arial", 12), fill="gray")
            self.pet_canvas.create_text(center+25, center-30, text="z", font=("Arial", 10), fill="gray")
            self.pet_canvas.create_text(center+35, center-40, text="z", font=("Arial", 8), fill="gray")
    
    def draw_jump_dog(self, center):
        size = self.pet_size
        # 跳跃高度
        jump_height = 25 if self.frame_index % 4 < 2 else 0
        
        # 身体
        self.pet_canvas.create_oval(center-32, center-8-jump_height, center+32, center+28-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 头
        self.pet_canvas.create_oval(center-28, center-42-jump_height, center+28, center-8-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（跳跃时耳朵向后）
        self.pet_canvas.create_oval(center-38, center-38-jump_height, center-23, center-18-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+23, center-38-jump_height, center+38, center-18-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 惊讶的眼睛（狗狗的眼睛更大）
        eye_y = center-26-jump_height
        self.pet_canvas.create_oval(center-16, eye_y-4, center-9, eye_y+4, fill="black")
        self.pet_canvas.create_oval(center+9, eye_y-4, center+16, eye_y+4, fill="black")
        self.pet_canvas.create_oval(center-14, eye_y-2, center-12, eye_y+2, fill="white")
        self.pet_canvas.create_oval(center+12, eye_y-2, center+14, eye_y+2, fill="white")
        # 惊讶的嘴（O形）
        self.pet_canvas.create_oval(center-5, center-15-jump_height, center+5, center-5-jump_height, 
                                      fill="black")
        # 跳跃的腿（伸展）
        self.pet_canvas.create_line(center-18, center+28, center-25, center+45, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center-8, center+28, center-5, center+45, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+8, center+28, center+5, center+45, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+18, center+28, center+25, center+45, 
                                      width=5, fill=self.get_skin_color())
        # 尾巴（竖起）
        tail_x = center+35
        tail_y = center+5-jump_height
        self.pet_canvas.create_arc(tail_x-5, tail_y-18, tail_x+20, tail_y-2, 
                                     start=270, extent=120, style=tk.ARC, 
                                     width=4, outline=self.get_skin_color())
    
    # ==================== 兔子绘制方法 ====================
    def draw_rabbit(self, center):
        if self.current_state == "idle":
            self.draw_idle_rabbit(center)
        elif self.current_state == "walk":
            self.draw_walk_rabbit(center)
        elif self.current_state == "happy":
            self.draw_happy_rabbit(center)
        elif self.current_state == "sleep":
            self.draw_sleep_rabbit(center)
        elif self.current_state == "jump":
            self.draw_jump_rabbit(center)
    
    def draw_idle_rabbit(self, center):
        size = self.pet_size
        # 身体（圆润的身体）
        self.pet_canvas.create_oval(center-25, center-5, center+25, center+30, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（更小更圆的头）
        self.pet_canvas.create_oval(center-20, center-35, center+20, center-5, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（长而直立的耳朵 - 兔子特征）
        ear_left_wave = 3 if self.frame_index % 15 < 7 else -3
        ear_right_wave = -3 if self.frame_index % 15 < 7 else 3
        # 左耳
        self.pet_canvas.create_oval(center-18+ear_left_wave, center-65, center-8+ear_left_wave, center-35, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center-16+ear_left_wave, center-63, center-10+ear_left_wave, center-37, 
                                      fill="#FFB6C1", outline="")
        # 右耳
        self.pet_canvas.create_oval(center+8+ear_right_wave, center-65, center+18+ear_right_wave, center-35, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+10+ear_right_wave, center-63, center+16+ear_right_wave, center-37, 
                                      fill="#FFB6C1", outline="")
        # 眼睛（兔子的眼睛在两侧）
        eye_y = center-20
        if self.frame_index % 20 < 2:
            self.pet_canvas.create_line(center-12, eye_y, center-6, eye_y, width=2)
            self.pet_canvas.create_line(center+6, eye_y, center+12, eye_y, width=2)
        else:
            self.pet_canvas.create_oval(center-12, eye_y-3, center-6, eye_y+3, fill="black")
            self.pet_canvas.create_oval(center+6, eye_y-3, center+12, eye_y+3, fill="black")
            # 兔子的眼睛有高光
            self.pet_canvas.create_oval(center-10, eye_y-1, center-8, eye_y+1, fill="white")
            self.pet_canvas.create_oval(center+8, eye_y-1, center+10, eye_y+1, fill="white")
        # 鼻子（三瓣嘴 - 兔子特征）
        self.pet_canvas.create_polygon(center-3, center-12, center, center-10, center+3, center-12, 
                                         fill="pink", outline="black")
        # 三瓣嘴
        self.pet_canvas.create_line(center, center-10, center, center-4, width=2)
        self.pet_canvas.create_arc(center-8, center-8, center-2, center-2, 
                                     start=180, extent=180, style=tk.ARC)
        self.pet_canvas.create_arc(center+2, center-8, center+8, center-2, 
                                     start=180, extent=180, style=tk.ARC)
        # 胡须
        self.pet_canvas.create_line(center-20, center-8, center-6, center-10, width=1)
        self.pet_canvas.create_line(center-20, center-5, center-6, center-7, width=1)
        self.pet_canvas.create_line(center+6, center-10, center+20, center-8, width=1)
        self.pet_canvas.create_line(center+6, center-7, center+20, center-5, width=1)
        # 尾巴（非常短的尾巴 - 兔子特征，几乎看不见）
        tail_x = center+28
        tail_y = center+20
        self.pet_canvas.create_oval(tail_x, tail_y, tail_x+5, tail_y+5, 
                                      fill="white", outline="black")
    
    def draw_walk_rabbit(self, center):
        size = self.pet_size
        # 身体
        self.pet_canvas.create_oval(center-25, center-5, center+25, center+30, 
                                      fill=self.get_skin_color(), outline="black")
        # 头
        self.pet_canvas.create_oval(center-20, center-35, center+20, center-5, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（行走时耳朵稍微摆动）
        ear_wave = 5 if self.frame_index % 4 < 2 else -5
        self.pet_canvas.create_oval(center-18+ear_wave, center-65, center-8+ear_wave, center-35, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center-16+ear_wave, center-63, center-10+ear_wave, center-37, 
                                      fill="#FFB6C1", outline="")
        self.pet_canvas.create_oval(center+8-ear_wave, center-65, center+18-ear_wave, center-35, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+10-ear_wave, center-63, center+16-ear_wave, center-37, 
                                      fill="#FFB6C1", outline="")
        # 眼睛
        eye_y = center-20
        self.pet_canvas.create_oval(center-12, eye_y-3, center-6, eye_y+3, fill="black")
        self.pet_canvas.create_oval(center+6, eye_y-3, center+12, eye_y+3, fill="black")
        # 鼻子和三瓣嘴
        self.pet_canvas.create_polygon(center-3, center-12, center, center-10, center+3, center-12, 
                                         fill="pink", outline="black")
        self.pet_canvas.create_line(center, center-10, center, center-4, width=2)
        self.pet_canvas.create_arc(center-8, center-8, center-2, center-2, 
                                     start=180, extent=180, style=tk.ARC)
        self.pet_canvas.create_arc(center+2, center-8, center+8, center-2, 
                                     start=180, extent=180, style=tk.ARC)
        # 走路的腿（兔子的后腿更长）
        leg_offset = 7 if self.frame_index % 4 < 2 else -7
        # 前腿
        self.pet_canvas.create_line(center-12, center+30, center-12, center+42+leg_offset, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+5, center+30, center+5, center+42-leg_offset, 
                                      width=4, fill=self.get_skin_color())
        # 后腿（更长）
        self.pet_canvas.create_line(center-5, center+30, center-8, center+45-leg_offset, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+12, center+30, center+15, center+45+leg_offset, 
                                      width=5, fill=self.get_skin_color())
        # 尾巴
        tail_x = center+28
        tail_y = center+20
        self.pet_canvas.create_oval(tail_x, tail_y, tail_x+5, tail_y+5, 
                                      fill="white", outline="black")
    
    def draw_happy_rabbit(self, center):
        size = self.pet_size
        # 身体
        self.pet_canvas.create_oval(center-25, center-5, center+25, center+30, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（开心时头稍微抬起）
        head_offset = -5 if self.frame_index % 4 < 2 else 0
        self.pet_canvas.create_oval(center-20, center-38+head_offset, center+20, center-8+head_offset, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（开心时耳朵竖起并摆动）
        ear_joy = 8 if self.frame_index % 2 == 0 else -8
        self.pet_canvas.create_oval(center-18+ear_joy, center-68+head_offset, center-8+ear_joy, center-38+head_offset, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center-16+ear_joy, center-66+head_offset, center-10+ear_joy, center-40+head_offset, 
                                      fill="#FFB6C1", outline="")
        self.pet_canvas.create_oval(center+8-ear_joy, center-68+head_offset, center+18-ear_joy, center-38+head_offset, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+10-ear_joy, center-66+head_offset, center+16-ear_joy, center-40+head_offset, 
                                      fill="#FFB6C1", outline="")
        # 开心的眼睛（弯月形）
        eye_y = center-23+head_offset
        self.pet_canvas.create_arc(center-14, eye_y-4, center-4, eye_y+4, 
                                     start=180, extent=180, style=tk.ARC, width=2)
        self.pet_canvas.create_arc(center+4, eye_y-4, center+14, eye_y+4, 
                                     start=180, extent=180, style=tk.ARC, width=2)
        # 鼻子
        self.pet_canvas.create_polygon(center-3, center-15+head_offset, center, center-13+head_offset, center+3, center-15+head_offset, 
                                         fill="pink", outline="black")
        # 开心的三瓣嘴（微笑）
        self.pet_canvas.create_arc(center-10, center-15+head_offset, center+10, center-5+head_offset, 
                                     start=180, extent=180, width=2)
        # 腮红
        self.pet_canvas.create_oval(center-18, center-18+head_offset, center-12, center-12+head_offset, fill="pink", outline="")
        self.pet_canvas.create_oval(center+12, center-18+head_offset, center+18, center-12+head_offset, fill="pink", outline="")
        # 开心跳动的效果
        jump_offset = -10 if self.frame_index % 4 < 2 else 0
        # 尾巴（开心时尾巴稍微动一下）
        tail_x = center+28
        tail_y = center+20 + jump_offset
        tail_wave = 3 if self.frame_index % 2 == 0 else 0
        self.pet_canvas.create_oval(tail_x+tail_wave, tail_y, tail_x+5+tail_wave, tail_y+5, 
                                      fill="white", outline="black")
    
    def draw_sleep_rabbit(self, center):
        size = self.pet_size
        # 身体（蜷缩成一团睡）
        self.pet_canvas.create_oval(center-30, center-5, center+30, center+35, 
                                      fill=self.get_skin_color(), outline="black")
        # 头（藏在身体里）
        self.pet_canvas.create_oval(center-20, center-10, center+10, center+15, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（耷拉下来）
        self.pet_canvas.create_oval(center-20, center-25, center-10, center-5, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+5, center-25, center+15, center-5, 
                                      fill=self.get_skin_color(), outline="black")
        # 睡眠的眼睛（闭着）
        eye_y = center
        self.pet_canvas.create_line(center-15, eye_y, center-10, eye_y, width=2)
        self.pet_canvas.create_line(center+3, eye_y, center+8, eye_y, width=2)
        # 呼吸动画
        breath_offset = 3 if self.frame_index % 10 < 5 else 0
        # Zzz 睡眠符号（兔子的睡眠符号从耳朵旁边冒出来）
        z_offset = self.frame_index % 30
        if z_offset < 10:
            self.pet_canvas.create_text(center+20, center-15, text="Z", font=("Arial", 10), fill="gray")
        elif z_offset < 20:
            self.pet_canvas.create_text(center+20, center-15, text="Z", font=("Arial", 10), fill="gray")
            self.pet_canvas.create_text(center+30, center-25, text="z", font=("Arial", 8), fill="gray")
        else:
            self.pet_canvas.create_text(center+20, center-15, text="Z", font=("Arial", 10), fill="gray")
            self.pet_canvas.create_text(center+30, center-25, text="z", font=("Arial", 8), fill="gray")
            self.pet_canvas.create_text(center+40, center-35, text="z", font=("Arial", 6), fill="gray")
    
    def draw_jump_rabbit(self, center):
        size = self.pet_size
        # 跳跃高度（兔子跳得更高）
        jump_height = 35 if self.frame_index % 4 < 2 else 0
        
        # 身体
        self.pet_canvas.create_oval(center-25, center-5-jump_height, center+25, center+30-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 头
        self.pet_canvas.create_oval(center-20, center-35-jump_height, center+20, center-5-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 耳朵（跳跃时耳朵向后）
        self.pet_canvas.create_oval(center-22, center-60-jump_height, center-12, center-30-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        self.pet_canvas.create_oval(center+12, center-60-jump_height, center+22, center-30-jump_height, 
                                      fill=self.get_skin_color(), outline="black")
        # 惊讶的眼睛
        eye_y = center-20-jump_height
        self.pet_canvas.create_oval(center-12, eye_y-4, center-6, eye_y+4, fill="black")
        self.pet_canvas.create_oval(center+6, eye_y-4, center+12, eye_y+4, fill="black")
        # 惊讶的三瓣嘴（O形）
        self.pet_canvas.create_oval(center-4, center-12-jump_height, center+4, center-4-jump_height, 
                                      fill="black")
        # 跳跃的腿（兔子的后腿完全伸展）
        self.pet_canvas.create_line(center-12, center+30, center-15, center+50, 
                                      width=4, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+5, center+30, center+8, center+50, 
                                      width=4, fill=self.get_skin_color())
        # 后腿（完全伸展）
        self.pet_canvas.create_line(center-5, center+30, center-10, center+55, 
                                      width=5, fill=self.get_skin_color())
        self.pet_canvas.create_line(center+12, center+30, center+17, center+55, 
                                      width=5, fill=self.get_skin_color())
        # 尾巴
        tail_x = center+28
        tail_y = center+20-jump_height
        self.pet_canvas.create_oval(tail_x, tail_y, tail_x+5, tail_y+5, 
                                      fill="white", outline="black")
    
    # ==================== 通用方法 ====================
    def get_skin_color(self):
        colors = {
            "orange": "#FFA500",
            "white": "#F5F5F5",
            "black": "#333333",
            "gray": "#808080",
            "brown": "#8B4513"
        }
        return colors.get(self.current_skin, "#FFA500")
    
    def setup_mouse_events(self):
        self.pet_canvas.bind("<Button-1>", self.on_click)
        self.pet_canvas.bind("<Button-3>", self.on_right_click)
        self.pet_canvas.bind("<B1-Motion>", self.on_drag)
        self.pet_canvas.bind("<ButtonRelease-1>", self.on_release)
    
    def on_click(self, event):
        # 点击时互动：跳一下或开心
        self.stop_random_behavior()
        self.current_state = "happy"
        if self.sound_enabled:
            self.play_click_sound()
        
        # 2秒后恢复idle
        self.root.after(2000, self.restore_idle)
    
    def play_click_sound(self):
        try:
            winsound.Beep(1000, 100)
        except:
            pass
    
    def on_right_click(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def on_drag(self, event):
        if not self.dragging:
            self.dragging = True
            self.drag_offset_x = event.x
            self.drag_offset_y = event.y
        
        # 计算新位置
        self.x = self.root.winfo_pointerx() - self.drag_offset_x
        self.y = self.root.winfo_pointery() - self.drag_offset_y
        
        # 更新窗口位置
        self.root.geometry(f"{self.pet_size}x{self.pet_size}+{self.x}+{self.y}")
        
        # 拖动时停止随机行为
        self.stop_random_behavior()
    
    def on_release(self, event):
        self.dragging = False
        # 松开后恢复随机行为
        self.root.after(1000, self.start_random_behavior)
    
    def setup_context_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)
        
        # 切换宠物
        pet_menu = Menu(self.context_menu, tearoff=0)
        pet_menu.add_command(label="猫咪", command=lambda: self.change_pet("cat"))
        pet_menu.add_command(label="狗狗", command=lambda: self.change_pet("dog"))
        pet_menu.add_command(label="兔子", command=lambda: self.change_pet("rabbit"))
        self.context_menu.add_cascade(label="切换宠物", menu=pet_menu)
        
        # 更换皮肤
        skin_menu = Menu(self.context_menu, tearoff=0)
        skin_menu.add_command(label="橘色", command=lambda: self.change_skin("orange"))
        skin_menu.add_command(label="白色", command=lambda: self.change_skin("white"))
        skin_menu.add_command(label="黑色", command=lambda: self.change_skin("black"))
        skin_menu.add_command(label="灰色", command=lambda: self.change_skin("gray"))
        skin_menu.add_command(label="棕色", command=lambda: self.change_skin("brown"))
        self.context_menu.add_cascade(label="更换皮肤", menu=skin_menu)
        
        # 设置
        self.context_menu.add_command(label="设置", command=self.show_settings)
        
        # 分隔线
        self.context_menu.add_separator()
        
        # 退出
        self.context_menu.add_command(label="退出", command=self.root.quit)
    
    def change_pet(self, pet_type):
        self.current_pet = pet_type
        self.draw_pet()
    
    def change_skin(self, skin_color):
        self.current_skin = skin_color
        self.draw_pet()
    
    def show_settings(self):
        # 创建设置窗口
        settings_window = Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("300x250")
        settings_window.resizable(False, False)
        
        # 大小调整
        Label(settings_window, text="宠物大小:").pack(pady=10)
        size_scale = Scale(settings_window, from_=50, to=200, orient=tk.HORIZONTAL, 
                           command=self.update_size)
        size_scale.set(self.pet_size)
        size_scale.pack(pady=5)
        
        # 音效开关
        sound_var = tk.BooleanVar(value=self.sound_enabled)
        sound_check = Checkbutton(settings_window, text="开启音效", variable=sound_var,
                                   command=lambda: self.toggle_sound(sound_var.get()))
        sound_check.pack(pady=10)
        
        # 开机自启
        autostart_var = tk.BooleanVar(value=self.auto_start)
        autostart_check = Checkbutton(settings_window, text="开机自启", variable=autostart_var,
                                       command=lambda: self.toggle_autostart(autostart_var.get()))
        autostart_check.pack(pady=10)
        
        # 关闭按钮
        Button(settings_window, text="关闭", command=settings_window.destroy).pack(pady=20)
    
    def update_size(self, value):
        self.pet_size = int(value)
        self.root.geometry(f"{self.pet_size}x{self.pet_size}+{self.x}+{self.y}")
        self.pet_canvas.config(width=self.pet_size, height=self.pet_size)
        self.draw_pet()
    
    def toggle_sound(self, enabled):
        self.sound_enabled = enabled
    
    def toggle_autostart(self, enabled):
        self.auto_start = enabled
        # 实际的开机自启实现需要操作注册表，这里简化处理
    
    def start_animation(self):
        self.frame_index += 1
        self.draw_pet()
        self.root.after(self.animation_speed, self.start_animation)
    
    def start_random_behavior(self):
        # 随机行为：闲逛、打瞌睡
        if self.random_timer:
            self.root.after_cancel(self.random_timer)
        
        # 随机选择行为
        behavior = random.choice(["idle", "walk", "sleep", "happy"])
        duration = random.randint(3000, 10000)  # 3-10秒
        
        if behavior == "walk":
            self.current_state = "walk"
            self.walk_distance = random.randint(50, 200)
            self.walk_direction = random.choice([1, -1])
        elif behavior == "sleep":
            self.current_state = "sleep"
        elif behavior == "happy":
            self.current_state = "happy"
        else:
            self.current_state = "idle"
        
        # 设置下一个行为
        self.random_timer = self.root.after(duration, self.start_random_behavior)
    
    def stop_random_behavior(self):
        if self.random_timer:
            self.root.after_cancel(self.random_timer)
            self.random_timer = None
    
    def restore_idle(self):
        if not self.dragging:
            self.current_state = "idle"
            self.start_random_behavior()
    
    def update_walk(self):
        if self.current_state == "walk" and self.walk_distance > 0:
            # 移动宠物
            step = 2
            self.x += self.walk_direction * step
            self.walk_distance -= step
            
            # 边界检查
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            if self.x < 0:
                self.x = 0
                self.walk_direction = 1
            elif self.x > screen_width - self.pet_size:
                self.x = screen_width - self.pet_size
                self.walk_direction = -1
            
            # 更新位置
            self.root.geometry(f"{self.pet_size}x{self.pet_size}+{self.x}+{self.y}")
        
        # 继续更新
        self.root.after(50, self.update_walk)
    
    def run(self):
        # 启动行走更新
        self.update_walk()
        self.root.mainloop()

if __name__ == "__main__":
    app = PetApp()
    app.run()
