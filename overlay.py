from AppKit import (
    NSApplication,
    NSApplicationActivationPolicyAccessory,
    NSBackingStoreBuffered,
    NSBorderlessWindowMask,
    NSColor,
    NSFont,
    NSTextField,
    NSWindow,
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
        self.app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        screen = CGDisplayBounds(CGMainDisplayID())
        sw, sh = screen.size.width, screen.size.height

        win_w, win_h = 340, 64
        x = (sw - win_w) / 2
        y = sh / 2.5
        self.window, blur = _make_window(((x, y), (win_w, win_h)))
        self.label = _make_label(blur, ((0, 12), (win_w, 40)))
        self.window.orderOut_(None)

    def show_idle(self):
        self.window.setAlphaValue_(0.0)
        self.window.orderOut_(None)

    def show_recording(self):
        self.label.setStringValue_("\U0001f3a4  Enregistrement…")
        self.window.orderFrontRegardless()
        self.window.setAlphaValue_(0.92)

    def show_processing(self):
        self.label.setStringValue_("⚡  Transcription…")
        self.window.setAlphaValue_(0.92)
        self.window.orderFrontRegardless()

    def show_error(self, message):
        self.label.setStringValue_(f"⚠  {message}")
        self.window.setAlphaValue_(0.92)
        self.window.orderFrontRegardless()

    def hide(self):
        self.window.setAlphaValue_(0.0)
        self.window.orderOut_(None)

    def update(self):
        self.app.updateWindows()

    def close(self):
        self.window.close()
