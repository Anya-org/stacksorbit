from conxius_orbit_gui import ConxiusOrbitGUI


def test_watch_theme_name_is_mount_safe_before_mount():
    """Theme watcher should no-op safely before the app mounts a screen."""
    app = ConxiusOrbitGUI()
    app.watch_theme_name("standard", "sovereign")

    # The class is applied from on_mount once the screen stack exists.
    assert "sovereign-theme" not in app.classes
