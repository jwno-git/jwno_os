from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.backend.wayland import InputConfig
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import base
from widgets.cpu_temp import CPUTempWidget
import subprocess
import os

@hook.subscribe.startup_once
def autostart():
    # Start display manager first
    subprocess.Popen(["kanshi"])
    # Autostart systray applications
    subprocess.Popen(["nm-applet", "--indicator"])
    # Autostart services
    subprocess.Popen(["dunst"])
    subprocess.Popen(["wl-paste", "--watch", "cliphist", "store"])
    # Set cursor theme environment variables for the Wayland session
    os.environ["XCURSOR_THEME"] = "BreezeX-RosePine-Linux"
    os.environ["XCURSOR_SIZE"] = "24"

mod = "mod4"
terminal = "foot"

# Keybinds
keys = [
    Key([mod], "a", lazy.spawn("sh -c 'tofi-run | sh'")),
    # Key([mod], "b",),
    Key([mod], "c", lazy.spawn("sh -c 'cliphist list | cut -f2- | tofi --config ~/.config/tofi/clipboard | cliphist store'")),
    Key([mod, "shift"], "c", lazy.spawn("cliphist wipe")),
    # Key([mod], "d",),
    # Key([mod], "e",),
    Key([mod], "f", lazy.spawn("foot")),
    # Key([mod], "g",),
    # Key([mod], "h",),
    # Key([mod], "i",),
    # Key([mod], "j",),
    # Key([mod], "k",),
    # Key([mod], "l",),
    Key([mod], "m", lazy.spawn("wlr-randr --output eDP-1 --pos 0,1080 --output HDMI-A-1 --pos 480,0")),
    # Key([mod], "n",),
    # Key([mod], "o",),
    # Key([mod], "p", lazy.spawn("colourpicker")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    # Key([mod], "r",),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod], "s", lazy.spawn("sh -c 'wf-recorder -r 30 -g 1280x720 -f ~/Videos/recording_$(date +%Y%m%d_%H%M%S).mp4'")),
    Key([mod, "shift"], "s", lazy.spawn("pkill -INT wf-recorder")),
    Key(["control", "mod1"], "s", lazy.spawn("sh -c 'grim -g \"$(slurp)\" - | swappy -f - -o ~/Pictures/Screenshots/screenshot-$(date +%Y%m%d-%H%M%S).png'")),
    # Key([mod], "t",),
    # Key([mod], "u",),
    Key([mod], "v", lazy.spawn("foot -e zsh -l -c 'vim'")),
    Key([mod], "w", lazy.spawn("firefox")),
    Key([mod, "shift"], "w", lazy.spawn("chromium-browser")),
    # Key([mod], "x",),
    # Key([mod], "y",),
    # Key([mod], "z",),
    Key([mod], "return", lazy.next_layout()),
    Key([mod], "space", lazy.group['scratchpad'].dropdown_toggle('terminal')),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod], "Right", lazy.screen.next_group()),
    Key([mod], "Left", lazy.screen.prev_group()),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 25%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 25%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [
    Group("1", screen_affinity=0),  # External monitor when connected
    Group("2", screen_affinity=1),  # Always laptop screen
    Group("3", screen_affinity=1),  # Always laptop screen
]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            Key([mod, "control"], i.name, lazy.window.togroup(i.name, switch_group=False))
            # Or, use below if you prefer not to switch to that group.
            # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            # desc="move focused window to group {}".format(i.name)),
        ]
    )

# Add scratchpad group AFTER regular groups are processed
groups.append(ScratchPad("scratchpad", [
    DropDown("terminal", terminal,
             width=1.00, height=1.00, x=0, y=0,
             opacity=0.90,
             on_focus_lost_hide=False),
]))

layouts = [
    layout.Max(),
    layout.MonadWide(
    ratio=0.65,
    border_focus='#00FFFF',
	border_normal='#290F34',
	border_width=1,
	margin=6,
	),
]

widget_defaults = dict(
    font="sans",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
    wallpaper='~/Pictures/Wallpapers/wallpaper-qtile.png',
	wallpaper_mode='fill',
        top=bar.Bar(
            [
        widget.Spacer(
			background="#00000000",
			length=5,
		),
        widget.Memory(
            format='  {MemPercent:.1f}%',
            measure_mem='G',
            update_interval=2,
            foreground='B0E0E6',
        ),
        widget.Spacer(
			background="#00000000",
			length=5,
		),
        widget.Memory(
            format='  {SwapPercent:.1f}%',
            measure_swap='G',
            update_interval=2,
            foreground='B0E0E6',
        ),
        widget.Spacer(
			background="#00000000",
			length=5,
		),
        widget.DF(
            partition='/boot/efi',
            format='  {r:.0f}%',
            measure='M',  # Using MB since EFI partitions are typically small
            warn_space=50,  # Warning when less than 50MB free
            visible_on_warn=False,  # Always show, not just on warning
            update_interval=60,
            foreground='B0E0E6',
            warn_color='ff6600',  # Orange warning color
        ),
        widget.Spacer(
			background="#00000000",
			length=5,
		),
        widget.DF(
            partition='/',
            format='  {r:.0f}%',
            measure='G',  # Using GB for root partition
            warn_space=5,  # Warning when less than 5GB free
            visible_on_warn=False,  # Always show, not just on warning
            update_interval=60,
            foreground='B0E0E6',
            warn_color='ff0000',  # Red warning color
        ),
        widget.Spacer(),
        widget.StatusNotifier(),
        widget.Spacer(length=10), 
        widget.Backlight(
            foreground='#B0E0E6',
            background='#00000000',
            backlight_name='amdgpu_bl1',
            format='💡 {percent:2.0%}',
            step=5,
		),
		widget.Spacer(length=10),
		widget.PulseVolume(
            foreground='#B0E0E6',
            background='#00000000',
            fmt='🔊 {}',
		),
        widget.Spacer(
			background="#00000000",
			length=10,
		),
        CPUTempWidget(
            foreground='#B0E0E6',
            background='#00000000',
            update_interval=2,
            fmt='🌡 {}',
            fnormat='<span color=#666666">🔋  </span>{percent:2.0%}',
            ),
        widget.Spacer(length=10),
        widget.Battery(
            foreground='#B0E0E6',
            background='#00000000',
            format='🔋 {percent:2.0%}',
            low_percentage=0.15,
            low_foreground='#FF6B6B',
        ),
       widget.Spacer(length=5),
            ],
            24,
            background='#00000000',
        ),
    ),
    Screen(  # External monitor (HDMI-A-1) - no bar
        wallpaper='~/Pictures/Wallpapers/wallpaper.png',
        wallpaper_mode='fill',
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus='#8A7BAD',
    border_normal='#8A7BAD',
    border_width=1,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry

        # GIMP floating rules
        Match(wm_class="gimp"),  # All GIMP windows
        Match(wm_class="Gimp"),  # Alternative capitalization
        Match(wm_class="gimp-2.10"),  # Version-specific
        Match(title="GIMP Startup"),  # Startup splash
        Match(title="Change Foreground Color"),  # Color picker dialog
        Match(title="Change Background Color"),  # Background color dialog
        Match(title="Colors"),  # Color dialogs
        Match(title="Tool Options"),  # Tool options dialog
        Match(title="Layers"),  # Layers dialog
        Match(title="Channels"),  # Channels dialog
        Match(title="Paths"),  # Paths dialog
        Match(title="Undo History"),  # Undo history dialog
        Match(title="Navigation"),  # Navigation dialog
        Match(role="gimp-toolbox"),  # GIMP toolbox
        Match(role="gimp-dock"),  # GIMP docks
        Match(role="gimp-image-window"),  # GIMP image windows
        Match(wm_type="dialog"),  # Generic dialog windows
        Match(wm_type="utility"),  # Utility windows
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "1267:12729:ASUE140D:00 04F3:31B9 Touchpad": InputConfig(
        tap=True,
        natural_scroll=True,
        dwt=True
    ),
}

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = "BreezeX-RosePine-Linux"
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
