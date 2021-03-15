# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401


mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"                             # My terminal of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm+" -e fish"),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("rofi -show drun -config ~/.config/rofi/themes/dk-dmenu.rasi -display-drun \"Run: \" -drun-display-format \"{name}\""),
             desc='Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key(["control", "shift"], "e",
             lazy.spawn("emacsclient -c -a emacs"),
             desc='Doom Emacs'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         Key([mod], "r",
             lazy.to_screen(2),
             desc='Keyboard focus to monitor 3'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Window controls
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod, "shift"], "m",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### My applications launched with SUPER + ALT + KEY
         Key([mod, "mod1"], "b",
             lazy.spawn("firefox"),
             desc='firefox browser'
             ),
         Key([mod, "mod1"], "f",
             lazy.spawn("pcmanfm"),
             desc='file browser'
             ),
         Key([mod, "mod1"], "e",
             lazy.spawn("code"),
             desc='code editor'
             ),
         ### Hardware Configs
         # Volume
         Key([], "XF86AudioRaiseVolume", 
             lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
             desc='volume up'
             ),
         Key([], "XF86AudioLowerVolume", 
             lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
             desc='volume down'
             ),
         Key([], "XF86AudioMute",
             lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
             desc='volume on/off'
             ),
         # Brightness
         Key([], "XF86MonBrightnessUp",
             lazy.spawn("brightnessctl set +10%"),
             desc='brightness up'
             ),
         Key([], "XF86MonBrightnessDown",
             lazy.spawn("brightnessctl set 10%-"),
             desc='brightness down'
             ),
         # Lock
         Key([mod, "control"], "l",
             lazy.spawn("slock"),
             desc='lock screen'
             ),    
]

group_names = [("WWW", {'layout': 'monadtall'}),
               ("DEV", {'layout': 'monadtall'}),
               ("DOC", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("VID", {'layout': 'monadtall'}),
               ("GFX", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "bd93f9",
                "border_normal": "282a36"
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.RatioTile(**layout_theme),
    #layout.Floating(**layout_theme),
    #layout.Max(**layout_theme),
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.TreeTab(
    #     font = "Ubuntu",
    #     fontsize = 10,
    #     sections = ["FIRST", "SECOND"],
    #     section_fontsize = 11,
    #     bg_color = "141414",
    #     active_bg = "90C435",
    #     active_fg = "000000",
    #     inactive_bg = "384323",
    #     inactive_fg = "a0a0a0",
    #     padding_y = 5,
    #     section_top = 10,
    #     panel_width = 320
    #     ),
    ]

colors = [["#282a36", "#282a36"], # background  0
          ["#44475a", "#44475a"], # selection   1
          ["#6272a4", "#6272a4"], # comment     2
          ["#f8f8f2", "#f8f8f2"], # foreground  3
          ["#8be9fd", "#8be9fd"], # cyan        4
          ["#50fa7b", "#50fa7b"], # green       5
          ["#ffb86c", "#ffb86c"], # orange      6
          ["#ff79c6", "#ff79c6"], # pink        7
          ["#bd93f9", "#bd93f9"], # purple      8
          ["#ff5555", "#ff5555"], # red         9
          ["#f1fa8c", "#f1fa8c"]] # yellow      10
          

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize = 12,
    padding = 3,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[3],
                       padding = 10,
                       fontsize = 20
                       ),                   
              widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),                   
              widget.GroupBox(
                       font = "FiraCode Bold",
                       fontsize = 10,
                       active = colors[7],
                       inactive = colors[1],
                       block_highlight_text_color = colors[8],
                       highlight_color = colors[8],
                       highlight_method = "border",
                       this_current_screen_border = colors[8],
                       this_screen_border = colors [8],
                       other_current_screen_border = colors[0],
                       other_screen_border = colors[0],
                       urgent_border = colors[9],
                       disable_drag = True
                       ),
              widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),         
              widget.CurrentLayout(
                       foreground = colors[7],
                       background = colors[0],
                       padding = 5
                       ),
              widget.WindowCount(
                       show_zero = True,
                       background = colors[0],
                       foreground = colors[7],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),                  
              widget.WindowName(
                       font = "FiraCode Bold",
                       fontsize = 10,
                       foreground = colors[3],
                       background = colors[0],
                       ),
               widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),
              widget.TextBox(
                       text = " ",
                       padding = 2,
                       foreground = colors[9],
                       background = colors[0],
                       fontsize = 15
                       ),          
              widget.CheckUpdates(
                       distro = "Arch_yay",
                       display_format = "{updates} Updates",
                       foreground = colors[9],
                       background = colors[0],
                       update_interval = 1800,
                       padding = 5
                       ),                  
              widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),
              widget.TextBox(
                       text = "直",
                       foreground = colors[6],
                       background = colors[0],
                       fontsize = 15
                       ),          
              widget.Net(
                       format = '{down} ↓ ↑ {up}',
                       foreground = colors[6],
                       background = colors[0],
                       padding = 5
                       ),
               widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),         
               widget.TextBox(
                       text = "﬙",
                       padding = 2,
                       foreground = colors[10],
                       background = colors[0],
                       fontsize = 15
                       ),               
               widget.CPU(
                       format = '{freq_current}GHz {load_percent}%',
                       foreground = colors[10],
                       background = colors[0],
                       padding = 5
                       ),         
              widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),         
              widget.TextBox(
                       text = "",
                       padding = 2,
                       foreground = colors[5],
                       background = colors[0],
                       fontsize = 15
                       ),
              widget.ThermalSensor(
                       foreground = colors[5],
                       background = colors[0],
                       threshold = 90,
                       padding = 5
                       ),
               widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),         
              widget.TextBox(
                       text = "",
                       foreground = colors[4],
                       background = colors[0],
                       fontsize = 15
                       ),
              widget.Memory(
                       foreground = colors[4],
                       background = colors[0],
                       padding = 5
                       ),         
              widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),
              widget.TextBox(
                       text = " ",
                       padding = 2,
                       foreground = colors[8],
                       background = colors[0],
                       fontsize = 15
                       ),                  
              widget.Clock(
                       foreground = colors[8],
                       background = colors[0],
                       padding = 5,
                       format = "%A, %B %d - %H:%M %P"
                       ),
              widget.TextBox(
                       text = '|',
                       background = colors[0],
                       foreground = colors[3],
                       fontsize = 10
                       ),         
              widget.Systray(
                       icon_size = 20,
                       foreground = colors[3],
                       background = colors[0],
                       padding = 10
                       ),        
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=25)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=25)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=25))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),  # tastyworks exit box
    Match(title='Qalculate!'),  # qalculate-gtk
    Match(wm_class='kdenlive'),  # kdenlive
    Match(wm_class='pinentry-gtk-2'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
