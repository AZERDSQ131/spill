from AppKit import (
    NSApplication,
    NSApplicationActivationPolicyAccessory,
    NSBackingStoreBuffered,
    NSBorderlessWindowMask,
    NSColor,
    NSFont,
    NSTextField,
    NSWindow,
    NSView,
    NSVisualEffectView,
    NSVisualEffectMaterialHUDWindow,
    NSVisualEffectStateActive,
)
from Quartz.CoreGraphics import CGDisplayBounds, CGMainDisplayID


class OverlayWindow(NSWindow):
    def canBecomeKeyWindow(self):
        return False

    def canBecomeMainWindow(self):
        return False


def _make_window(rect, corner_radius=12):
    win = OverlayWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        rect, NSBorderlessWindowMask, NSBackingStoreBuffered, False
    )
    win.setOpaque_(False)
    win.setAlphaValue_(0.0)
    win.setLevel_(2000)
    win.ignoresMouseEvents = True

    blur = NSVisualEffectView.alloc().initWithFrame_(win.contentView().bounds())
    blur.setMaterial_(NSVisualEffectMaterialHUDWindow)
    blur.setState_(NSVisualEffectStateActive)
    blur.setWantsLayer_(True)
    blur.layer().setCornerRadius_(corner_radius)
    blur.layer().setMasksToBounds_(True)
    win.contentView().addSubview_(blur)
    return win, blur


def _make_label(parent, frame, font_size=20, weight=0.6):
    label = NSTextField.alloc().initWithFrame_(frame)
    label.setStringValue_("")
    label.setFont_(NSFont.systemFontOfSize_weight_(font_size, weight))
    label.setTextColor_(NSColor.whiteColor())
    label.setBackgroundColor_(NSColor.clearColor())
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setEditable_(False)
    label.setSelectable_(False)
    label.setAlignment_(1)
    parent.addSubview_(label)
    return label


class Overlay:
    def __init__(self):
        self.app = NSApplication.sharedApplication()
        # Accessory : pas d'icône Dock, pas de menu, fenêtres toujours visibles
        self.app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        screen = CGDisplayBounds(CGMainDisplayID())
        sw, sh = screen.size.width, screen.size.height

        # Fen\u00eatre HUD principale (centre de l'\u00e9cran)
        win_w, win_h = 340, 64
        x = (sw - win_w) / 2
        y = sh / 2.5
        self.window, blur = _make_window(((x, y), (win_w, win_h)))
        self.label = _make_label(blur, ((0, 12), (win_w, 40)))

        # Indicateur idle : petit pill en bas \u00e0 droite
        idle_w, idle_h = 52, 52
        idle_x = sw - idle_w - 20
        idle_y = 20
        self.idle_window, idle_blur = _make_window(
            ((idle_x, idle_y), (idle_w, idle_h)), corner_radius=26
        )
        self.idle_label = _make_label(
            idle_blur, ((0, 8), (idle_w, idle_h - 8)), font_size=28, weight=0.0
        )
        self.idle_label.setStringValue_("\U0001f3a4")

        self.window.orderOut_(None)
        self.idle_window.orderOut_(None)

    def show_idle(self):
        self.window.setAlphaValue_(0.0)
        self.window.orderOut_(None)
        self.idle_window.orderFrontRegardless()
        self.idle_window.setAlphaValue_(0.82)

    def show_recording(self):
        self.idle_window.setAlphaValue_(0.0)
        self.idle_window.orderOut_(None)
        self.label.setStringValue_("\U0001f3a4  Enregistrement\u2026")
        self.window.orderFrontRegardless()
        self.window.setAlphaValue_(0.92)

    def show_processing(self):
        self.label.setStringValue_("\u26a1  Transcription\u2026")
        self.window.setAlphaValue_(0.92)
        self.window.orderFrontRegardless()

    def show_error(self, message):
        self.label.setStringValue_(f"\u26a0  {message}")
        self.window.setAlphaValue_(0.92)
        self.window.orderFrontRegardless()

    def hide(self):
        self.window.setAlphaValue_(0.0)
        self.window.orderOut_(None)
        self.show_idle()

    def update(self):
        self.app.updateWindows()

    def close(self):
        self.window.close()
        self.idle_window.close()
