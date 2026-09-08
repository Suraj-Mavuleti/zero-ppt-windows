import customtkinter as ctk
import threading
import time
import math
import socket
import urllib.request
import json
import sqlite3
import random

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Presentation Studio")
        self.geometry("1100x750")
        
        # Premium Enterprise Color Palette
        self.bg_color = "#0B0C10"          # Deep rich black/gray
        self.sidebar_color = "#1F2833"     # Slate gray sidebar
        self.accent_color = "#66FCF1"      # Neon cyan accent
        self.text_primary = "#FFFFFF"      # Crisp white
        self.text_secondary = "#C5C6C7"    # Soft gray text
        self.panel_bg = "#161920"          # Slightly raised panel
        
        self.configure(fg_color=self.bg_color)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)
        
        # Branding
        self.logo_label = ctk.CTkLabel(self.sidebar, text="PPT", font=ctk.CTkFont("Segoe UI", size=26, weight="bold"), text_color=self.accent_color)
        self.logo_label.grid(row=0, column=0, padx=25, pady=(35, 5), sticky="w")
        
        self.version_label = ctk.CTkLabel(self.sidebar, text="Enterprise Edition v8.5", font=ctk.CTkFont("Segoe UI", size=12), text_color=self.text_secondary)
        self.version_label.grid(row=1, column=0, padx=25, pady=(0, 35), sticky="w")
        
        # Nav Buttons
        self.btn_dash = ctk.CTkButton(self.sidebar, text="  Overview", font=ctk.CTkFont("Segoe UI", size=14, weight="bold"), fg_color=self.panel_bg, text_color=self.text_primary, anchor="w", hover_color=self.accent_color)
        self.btn_dash.grid(row=2, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_set = ctk.CTkButton(self.sidebar, text="  Configuration", font=ctk.CTkFont("Segoe UI", size=14), fg_color="transparent", text_color=self.text_secondary, anchor="w", hover_color=self.panel_bg)
        self.btn_set.grid(row=3, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_logs = ctk.CTkButton(self.sidebar, text="  Diagnostics", font=ctk.CTkFont("Segoe UI", size=14), fg_color="transparent", text_color=self.text_secondary, anchor="w", hover_color=self.panel_bg)
        self.btn_logs.grid(row=4, column=0, padx=15, pady=8, sticky="ew")
        
        # Main Work Area
        self.main_view = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.header = ctk.CTkLabel(self.main_view, text="Presentation Studio", font=ctk.CTkFont("Segoe UI", size=32, weight="bold"), text_color=self.text_primary)
        self.header.pack(anchor="w", pady=(0, 20))
        
        # Premium Content Glass Panel
        self.main_frame = ctk.CTkFrame(self.main_view, fg_color=self.panel_bg, corner_radius=15, border_width=1, border_color="#2A2F3A")
        self.main_frame.pack(fill=ctk.BOTH, expand=True)
        
        self.setup_ui()
        
    
    def setup_ui(self):
        self.slides = [{"title": "Executive Summary", "content": "- Q4 Revenue Growth\n- Market Expansion\n- Risk Analysis"}]
        self.current_idx = 0
        
        top_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_bar.pack(fill=ctk.X, padx=25, pady=25)
        
        self.title_var = ctk.StringVar(value=self.slides[0]["title"])
        self.title_entry = ctk.CTkEntry(top_bar, textvariable=self.title_var, font=ctk.CTkFont("Segoe UI", 28, "bold"), fg_color="transparent", border_width=0, text_color=self.text_primary)
        self.title_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        self.status = ctk.CTkLabel(top_bar, text="Slide 1 of 1", font=ctk.CTkFont(size=14), text_color=self.text_secondary)
        self.status.pack(side=ctk.RIGHT)
        
        # Content Editor
        self.content_box = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont("Segoe UI", 18), fg_color="#101217", text_color=self.text_secondary, corner_radius=10, border_width=1, border_color="#2A2F3A")
        self.content_box.pack(fill=ctk.BOTH, expand=True, padx=25, pady=(0, 25))
        self.content_box.insert("0.0", self.slides[0]["content"])
        
        # Toolbar Bottom
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill=ctk.X, padx=25, pady=(0, 25))
        
        btn_kwargs = {"font": ctk.CTkFont(weight="bold"), "corner_radius": 8, "height": 36}
        
        ctk.CTkButton(btn_frame, text="◀ Previous", fg_color=self.sidebar_color, hover_color=self.panel_bg, command=self.prev, **btn_kwargs).pack(side=ctk.LEFT, padx=(0, 10))
        ctk.CTkButton(btn_frame, text="Next ▶", fg_color=self.sidebar_color, hover_color=self.panel_bg, command=self.next, **btn_kwargs).pack(side=ctk.LEFT)
        
        ctk.CTkButton(btn_frame, text="💾 Save Changes", fg_color=self.accent_color, text_color="#000000", hover_color="#45A29E", command=self.save_slide, **btn_kwargs).pack(side=ctk.RIGHT)
        ctk.CTkButton(btn_frame, text="✚ New Slide", fg_color="transparent", border_width=1, border_color=self.accent_color, text_color=self.accent_color, hover_color=self.sidebar_color, command=self.new_slide, **btn_kwargs).pack(side=ctk.RIGHT, padx=10)
        
    def save_slide(self):
        self.slides[self.current_idx]["title"] = self.title_var.get()
        self.slides[self.current_idx]["content"] = self.content_box.get("0.0", "end")
        self.header.configure(text="Presentation Studio - (Saved)")
        
    def load_slide(self):
        self.title_var.set(self.slides[self.current_idx]["title"])
        self.content_box.delete("0.0", "end")
        self.content_box.insert("0.0", self.slides[self.current_idx]["content"])
        self.status.configure(text=f"Slide {self.current_idx + 1} of {len(self.slides)}")
        self.header.configure(text="Presentation Studio")
        
    def prev(self):
        self.save_slide()
        if self.current_idx > 0:
            self.current_idx -= 1
            self.load_slide()
            
    def next(self):
        self.save_slide()
        if self.current_idx < len(self.slides) - 1:
            self.current_idx += 1
            self.load_slide()
            
    def new_slide(self):
        self.save_slide()
        self.slides.append({"title": "Untitled Slide", "content": "• New point..."})
        self.current_idx = len(self.slides) - 1
        self.load_slide()


if __name__ == "__main__":
    app = App()
    app.mainloop()
