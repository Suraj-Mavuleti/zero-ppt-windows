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
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero PPT - Presentation Editor")
        self.geometry("800x600")
        self.configure(fg_color="#1a1a24")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Zero PPT - Presentation Editor", font=("Helvetica", 24, "bold"), text_color="#00C7FF")
        self.header.pack(pady=20)
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)
        
        self.setup_ui()
        
    
    def setup_ui(self):
        self.slides = [{"title": "Slide 1", "content": "Welcome to Zero PPT!"}]
        self.current_idx = 0
        
        self.title_var = ctk.StringVar(value=self.slides[0]["title"])
        self.title_entry = ctk.CTkEntry(self.main_frame, textvariable=self.title_var, font=("Arial", 28, "bold"))
        self.title_entry.pack(fill=ctk.X, pady=10)
        
        self.content_box = ctk.CTkTextbox(self.main_frame, font=("Arial", 18))
        self.content_box.pack(fill=ctk.BOTH, expand=True, pady=10)
        self.content_box.insert("0.0", self.slides[0]["content"])
        
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill=ctk.X, pady=10)
        
        ctk.CTkButton(btn_frame, text="< Prev", command=self.prev).pack(side=ctk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Next >", command=self.next).pack(side=ctk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="+ New Slide", command=self.new_slide).pack(side=ctk.RIGHT, padx=10)
        ctk.CTkButton(btn_frame, text="Save Slide", command=self.save_slide).pack(side=ctk.RIGHT, padx=10)
        
        self.status = ctk.CTkLabel(self.main_frame, text="Slide 1 of 1")
        self.status.pack(pady=5)
        
    def save_slide(self):
        self.slides[self.current_idx]["title"] = self.title_var.get()
        self.slides[self.current_idx]["content"] = self.content_box.get("0.0", "end")
        
    def load_slide(self):
        self.title_var.set(self.slides[self.current_idx]["title"])
        self.content_box.delete("0.0", "end")
        self.content_box.insert("0.0", self.slides[self.current_idx]["content"])
        self.status.configure(text=f"Slide {self.current_idx + 1} of {len(self.slides)}")
        
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
        self.slides.append({"title": "New Slide", "content": "- Point 1"})
        self.current_idx = len(self.slides) - 1
        self.load_slide()


if __name__ == "__main__":
    app = App()
    app.mainloop()
