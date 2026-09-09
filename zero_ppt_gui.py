import sys
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango

class ZeroPPT(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero PPT - Ultimate Studio")
        self.set_default_size(1300, 800)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= LEFT PANEL (Thumbnails) =================
        self.panel_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.panel_left.set_size_request(220, -1)
        self.panel_left.get_style_context().add_class("panel-side")
        main_box.pack_start(self.panel_left, False, False, 0)
        
        logo = Gtk.Label(label="Z E R O P P T")
        logo.get_style_context().add_class("logo")
        logo.set_margin_top(20)
        logo.set_margin_bottom(20)
        self.panel_left.pack_start(logo, False, False, 0)
        
        btn_new_slide = Gtk.Button(label="➕ Add Slide")
        btn_new_slide.get_style_context().add_class("action-btn")
        self.panel_left.pack_start(btn_new_slide, False, False, 10)
        
        for i in range(1, 4):
            thumb = Gtk.Box()
            thumb.set_size_request(180, 100)
            thumb.get_style_context().add_class("thumbnail")
            if i == 1:
                thumb.get_style_context().add_class("thumb-selected")
            lbl = Gtk.Label(label=f"Slide {i}")
            lbl.set_margin_start(10)
            lbl.set_margin_top(10)
            lbl.set_halign(Gtk.Align.START)
            lbl.set_valign(Gtk.Align.START)
            thumb.add(lbl)
            
            align = Gtk.Alignment.new(0.5, 0, 0, 0)
            align.set_padding(10, 10, 0, 0)
            align.add(thumb)
            self.panel_left.pack_start(align, False, False, 0)
            
        # ================= WORKSPACE (Slide Canvas) =================
        self.workspace = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.workspace.get_style_context().add_class("workspace")
        main_box.pack_start(self.workspace, True, True, 0)
        
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        top_bar.get_style_context().add_class("top-bar")
        self.workspace.pack_start(top_bar, False, False, 0)
        
        btn_play = Gtk.Button(label="▶️ Present")
        btn_play.get_style_context().add_class("play-btn")
        top_bar.pack_end(btn_play, False, False, 10)
        
        align_slide = Gtk.Alignment.new(0.5, 0.5, 0, 0)
        self.slide = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.slide.set_size_request(800, 450)
        self.slide.get_style_context().add_class("main-slide")
        
        s_title = Gtk.Label(label="Ultimate Studio Vision")
        s_title.get_style_context().add_class("slide-title")
        s_title.set_halign(Gtk.Align.CENTER)
        s_title.set_margin_top(150)
        
        s_sub = Gtk.Label(label="Reinventing the way we present.")
        s_sub.get_style_context().add_class("slide-sub")
        s_sub.set_halign(Gtk.Align.CENTER)
        s_sub.set_margin_top(20)
        
        self.slide.pack_start(s_title, False, False, 0)
        self.slide.pack_start(s_sub, False, False, 0)
        align_slide.add(self.slide)
        self.workspace.pack_start(align_slide, True, True, 0)
        
        # ================= RIGHT PANEL (Properties) =================
        self.panel_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.panel_right.set_size_request(260, -1)
        self.panel_right.get_style_context().add_class("panel-side")
        main_box.pack_start(self.panel_right, False, False, 0)
        
        l_props = Gtk.Label(label="ANIMATION")
        l_props.get_style_context().add_class("section-label")
        l_props.set_halign(Gtk.Align.START)
        l_props.set_margin_start(20)
        l_props.set_margin_top(20)
        self.panel_right.pack_start(l_props, False, False, 10)
        
        props = [
            ("Transition", "Magic Move"),
            ("Duration", "1.5s"),
            ("Easing", "Ease In/Out")
        ]
        
        for name, val in props:
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            vbox.set_margin_start(20)
            vbox.set_margin_end(20)
            vbox.set_margin_bottom(15)
            
            ln = Gtk.Label(label=name)
            ln.get_style_context().add_class("prop-lbl")
            ln.set_halign(Gtk.Align.START)
            
            entry = Gtk.Entry()
            entry.set_text(val)
            entry.get_style_context().add_class("prop-entry")
            
            vbox.pack_start(ln, False, False, 5)
            vbox.pack_start(entry, False, False, 0)
            self.panel_right.pack_start(vbox, False, False, 0)
            
    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .panel-side { background-color: rgba(10, 12, 18, 0.98); border-right: 1px solid rgba(255, 255, 255, 0.05); border-left: 1px solid rgba(255, 255, 255, 0.05); }
            .logo { color: #FFFFFF; font-size: 18px; font-weight: 900; letter-spacing: 3px; text-shadow: 0 0 15px rgba(255, 102, 0, 0.6); }
            .action-btn { background: rgba(255,255,255,0.05); color: #FFFFFF; border-radius: 8px; border: none; padding: 10px; margin: 0 20px; transition: all 0.2s; font-weight: bold; }
            .action-btn:hover { background: rgba(255,255,255,0.1); }
            .thumbnail { background-color: #111111; border: 2px solid transparent; border-radius: 8px; color: #888888; }
            .thumb-selected { border: 2px solid #FF6600; color: #FFFFFF; }
            .workspace { background: #1C1C1E; }
            .top-bar { background: transparent; padding: 15px; }
            .play-btn { background: linear-gradient(45deg, #FF6600, #FF3300); color: #FFFFFF; font-weight: bold; border: none; border-radius: 8px; padding: 8px 15px; box-shadow: 0 5px 15px rgba(255, 102, 0, 0.3); }
            .main-slide { background: radial-gradient(circle at center, #2A2A2D, #1C1C1E); border-radius: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1); }
            .slide-title { color: #FFFFFF; font-size: 48px; font-weight: bold; text-shadow: 0 5px 15px rgba(0,0,0,0.5); }
            .slide-sub { color: #FF6600; font-size: 24px; }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .prop-lbl { color: #8B94A5; font-size: 13px; font-weight: bold; }
            .prop-entry { background: #0A0D14; color: #FFFFFF; border: 1px solid #1C2333; border-radius: 8px; padding: 8px; }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroPPT()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
