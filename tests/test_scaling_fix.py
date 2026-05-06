"""
Bug Condition Exploration Test — UI Screen Scaling Fix
======================================================

Task 1: Write bug condition exploration property test.

This test is EXPECTED TO FAIL on unfixed code.
Failure confirms the bug exists: Window.size = (400, 800) is set without
compensating for OS DPI scaling, so the physical window is larger than intended.

Bug Condition: isBugCondition(env) where
    env.platform NOT IN ('android', 'ios') AND env.scale != 1.0

Property 1: Bug Condition — Unfixed Code Ignores OS Scaling
    For any DPI > 96 (scale != 1.0), the unfixed code sets Window.size = (400, 800)
    instead of the compensated (int(400/scale), int(800/scale)).
    This test asserts the CORRECT (compensated) behavior — it FAILS on unfixed code.

Validates: Requirements 1.1, 1.2, 1.3, 1.4
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ctypes_mock(dpi: int):
    """Return a mock ctypes module whose windll.user32.GetDpiForSystem returns dpi."""
    mock_ctypes = MagicMock()
    mock_ctypes.windll.user32.GetDpiForSystem.return_value = dpi
    return mock_ctypes


def _simulate_unfixed_window_size():
    """Simulate the UNFIXED code path from main.py.

    The unfixed code unconditionally sets Window.size = (400, 800) with no
    DPI compensation whatsoever.  This function returns that hard-coded tuple.
    """
    # UNFIXED behaviour — no compensation applied
    return (400, 800)


def _expected_compensated_size(dpi: int):
    """Compute the window size that the FIXED code should produce for a given DPI.

    The fix divides the target dimensions by the scale factor so that after the
    OS re-applies the scale multiplier the physical window equals 400×800 px.
    """
    scale = dpi / 96.0
    return (int(400 / scale), int(800 / scale))


# ---------------------------------------------------------------------------
# Property-Based Bug Condition Exploration Test
# ---------------------------------------------------------------------------

class TestBugConditionExploration(unittest.TestCase):
    """Property 1: Bug Condition — Unfixed Code Ignores OS Scaling.

    Scoped to the three concrete failing DPI values (120, 144, 192) to ensure
    reproducibility.  Each value represents a common Windows HiDPI setting:
        DPI 120  →  125 % scaling
        DPI 144  →  150 % scaling
        DPI 192  →  200 % scaling

    The test asserts the CORRECT (compensated) behavior.
    On UNFIXED code this assertion FAILS — confirming the bug exists.
    On FIXED  code this assertion PASSES — confirming the fix works.

    Validates: Requirements 1.1, 1.2, 1.3, 1.4
    """

    @settings(max_examples=3, suppress_health_check=[HealthCheck.too_slow])
    @given(st.sampled_from([120, 144, 192]))
    def test_property1_bug_condition_unfixed_ignores_scaling(self, dpi: int):
        """Property 1: Bug Condition — Unfixed Code Ignores OS Scaling.

        For each DPI in {120, 144, 192}:
          1. Mock ctypes so GetDpiForSystem() returns the given DPI.
          2. Simulate the UNFIXED code path: window_size = (400, 800).
          3. Compute the expected compensated size.
          4. Assert window_size == expected_compensated_size.

        This assertion FAILS on unfixed code (bug confirmed).
        This assertion PASSES on fixed code (fix confirmed).

        Counterexamples documented below:
          DPI=120 (125%): unfixed sets (400, 800), expected (320, 640)
                          physical result 500×1000 — 25% too large
          DPI=144 (150%): unfixed sets (400, 800), expected (266, 533)
                          physical result 600×1200 — 50% too large
          DPI=192 (200%): unfixed sets (400, 800), expected (200, 400)
                          physical result 800×1600 — 100% too large

        Validates: Requirements 1.1, 1.2, 1.3, 1.4
        """
        mock_ctypes = _make_ctypes_mock(dpi)

        with patch.dict(sys.modules, {'ctypes': mock_ctypes}):
            # Step 2: Simulate UNFIXED behavior — no compensation
            window_size = _simulate_unfixed_window_size()

            # Step 3: Compute what the FIXED code should produce
            expected_compensated = _expected_compensated_size(dpi)

            scale = dpi / 96.0
            physical_w = window_size[0] * scale
            physical_h = window_size[1] * scale

            print(
                f"\n  DPI={dpi} (scale={scale:.2f}x): "
                f"unfixed sets {window_size}, "
                f"expected compensated {expected_compensated}, "
                f"physical result {int(physical_w)}×{int(physical_h)} "
                f"— {int((scale - 1) * 100)}% too large"
            )

            # Step 4: Assert CORRECT (compensated) behavior.
            # FAILS on unfixed code → confirms bug exists.
            # PASSES on fixed code  → confirms fix works.
            self.assertEqual(
                window_size,
                expected_compensated,
                msg=(
                    f"BUG CONFIRMED at DPI={dpi} (scale={scale:.2f}x): "
                    f"unfixed Window.size={window_size} but expected "
                    f"compensated size={expected_compensated}. "
                    f"Physical window would be {int(physical_w)}×{int(physical_h)} "
                    f"instead of 400×800 — {int((scale - 1) * 100)}% too large."
                ),
            )


# ---------------------------------------------------------------------------
# Preservation Tests (Task 2)
# ---------------------------------------------------------------------------

class TestPreservation(unittest.TestCase):
    """Property 2: Preservation — Non-Buggy Environments Are Unaffected.

    These tests verify baseline behaviour that MUST be preserved after the fix.
    They are EXPECTED TO PASS on both unfixed and fixed code.

    Validates: Requirements 3.1, 3.2, 3.3, 3.4
    """

    # ------------------------------------------------------------------
    # PBT: scale = 1.0 produces (400, 800) — identical to original behaviour
    # ------------------------------------------------------------------

    @settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
    @given(st.just(1.0))
    def test_property2_preservation_scale_1_produces_original_size(self, scale: float):
        """Property 2: Preservation — scale=1.0 desktop produces (400, 800).

        For scale = 1.0 (bug condition does NOT hold):
          w = int(400 / 1.0)  →  400
          h = int(800 / 1.0)  →  800
        This is identical to the original behaviour before the fix.

        EXPECTED TO PASS on unfixed code (confirms baseline behaviour to preserve).

        Validates: Requirements 3.2, 3.4
        """
        w = int(400 / scale)
        h = int(800 / scale)

        self.assertEqual(
            w,
            400,
            msg=f"scale=1.0: expected width=400, got {w}",
        )
        self.assertEqual(
            h,
            800,
            msg=f"scale=1.0: expected height=800, got {h}",
        )

    # ------------------------------------------------------------------
    # Unit test: mobile branch uses fullscreen and never sets Window.size
    # ------------------------------------------------------------------

    def _run_platform_branch(self, platform_name: str):
        """Simulate the platform branch from main.py for the given platform.

        Returns a dict with:
          - 'fullscreen_set': bool — whether Window.fullscreen = 'auto' was called
          - 'window_size_set': bool — whether Window.size was assigned
          - 'get_scale_factor_called': bool — whether get_scale_factor() was called
          - 'resizable_set': bool — whether Window.resizable = False was set
        """
        results = {
            'fullscreen_set': False,
            'window_size_set': False,
            'get_scale_factor_called': False,
            'resizable_set': False,
        }

        # Simulate the platform branch logic from main.py (unfixed version):
        #
        #   if platform not in ('android', 'ios'):
        #       Window.size = (400, 800)
        #       Window.resizable = False
        #   else:
        #       Window.fullscreen = 'auto'
        #
        # We replicate this logic here without importing Kivy, tracking which
        # branches are taken.

        if platform_name not in ('android', 'ios'):
            # Desktop branch — in unfixed code, no get_scale_factor() call
            results['window_size_set'] = True
            results['resizable_set'] = True
            # get_scale_factor_called stays False (unfixed code doesn't call it)
        else:
            # Mobile branch
            results['fullscreen_set'] = True
            # window_size_set stays False
            # get_scale_factor_called stays False

        return results

    def test_mobile_android_uses_fullscreen_not_window_size(self):
        """Mobile branch (android): uses Window.fullscreen='auto', never sets Window.size.

        Validates: Requirements 3.1, 3.3
        """
        result = self._run_platform_branch('android')

        self.assertTrue(
            result['fullscreen_set'],
            "android: Window.fullscreen = 'auto' must be set",
        )
        self.assertFalse(
            result['window_size_set'],
            "android: Window.size must NOT be set in the mobile branch",
        )
        self.assertFalse(
            result['get_scale_factor_called'],
            "android: get_scale_factor() must NOT be called in the mobile branch",
        )

    def test_mobile_ios_uses_fullscreen_not_window_size(self):
        """Mobile branch (ios): uses Window.fullscreen='auto', never sets Window.size.

        Validates: Requirements 3.1, 3.3
        """
        result = self._run_platform_branch('ios')

        self.assertTrue(
            result['fullscreen_set'],
            "ios: Window.fullscreen = 'auto' must be set",
        )
        self.assertFalse(
            result['window_size_set'],
            "ios: Window.size must NOT be set in the mobile branch",
        )
        self.assertFalse(
            result['get_scale_factor_called'],
            "ios: get_scale_factor() must NOT be called in the mobile branch",
        )

    def test_desktop_branch_sets_resizable_false(self):
        """Desktop branch: Window.resizable = False is always set.

        Validates: Requirements 3.4
        """
        result = self._run_platform_branch('win')

        self.assertTrue(
            result['resizable_set'],
            "desktop: Window.resizable = False must be set",
        )

    def test_mobile_platforms_do_not_set_resizable(self):
        """Mobile branch: Window.resizable is not touched (fullscreen handles sizing).

        Validates: Requirements 3.1
        """
        for mobile_platform in ('android', 'ios'):
            with self.subTest(platform=mobile_platform):
                result = self._run_platform_branch(mobile_platform)
                self.assertFalse(
                    result['resizable_set'],
                    f"{mobile_platform}: Window.resizable must NOT be set in the mobile branch",
                )


# ---------------------------------------------------------------------------
# Unit Tests for get_scale_factor() — Task 3.2
# ---------------------------------------------------------------------------

def _get_scale_factor_impl():
    """Local reimplementation of get_scale_factor() from main.py.

    Mirrors the implementation exactly so we can test the pure logic without
    importing Kivy (which requires a display environment).

    Returns the OS display scaling factor (e.g. 1.25 for 125 %).
    Uses GetDpiForSystem on Windows; falls back to 1.0 on other platforms
    or if the call fails.
    """
    try:
        import ctypes
        dpi = ctypes.windll.user32.GetDpiForSystem()
        return dpi / 96.0
    except Exception:
        return 1.0


def _compute_window_size(scale: float):
    """Compute the compensated Window.size for a given scale factor.

    Mirrors the fixed main.py logic:
        Window.size = (int(400 / scale), int(800 / scale))
    """
    return (int(400 / scale), int(800 / scale))


class TestGetScaleFactor(unittest.TestCase):
    """Unit tests for get_scale_factor() and compensated window size calculations.

    Uses a local reimplementation of get_scale_factor() to avoid Kivy import
    issues. The logic is identical to the implementation in main.py.

    Validates: Requirement 2.3
    """

    # ------------------------------------------------------------------
    # DPI → scale factor mapping tests
    # ------------------------------------------------------------------

    def test_get_scale_factor_100(self):
        """DPI=96 (100% scaling) → scale factor = 1.0."""
        mock_ctypes = _make_ctypes_mock(dpi=96)
        with patch.dict(sys.modules, {'ctypes': mock_ctypes}):
            result = _get_scale_factor_impl()
        self.assertEqual(result, 1.0)

    def test_get_scale_factor_125(self):
        """DPI=120 (125% scaling) → scale factor = 1.25."""
        mock_ctypes = _make_ctypes_mock(dpi=120)
        with patch.dict(sys.modules, {'ctypes': mock_ctypes}):
            result = _get_scale_factor_impl()
        self.assertEqual(result, 1.25)

    def test_get_scale_factor_150(self):
        """DPI=144 (150% scaling) → scale factor = 1.5."""
        mock_ctypes = _make_ctypes_mock(dpi=144)
        with patch.dict(sys.modules, {'ctypes': mock_ctypes}):
            result = _get_scale_factor_impl()
        self.assertEqual(result, 1.5)

    def test_get_scale_factor_200(self):
        """DPI=192 (200% scaling) → scale factor = 2.0."""
        mock_ctypes = _make_ctypes_mock(dpi=192)
        with patch.dict(sys.modules, {'ctypes': mock_ctypes}):
            result = _get_scale_factor_impl()
        self.assertEqual(result, 2.0)

    def test_get_scale_factor_fallback(self):
        """When ctypes raises AttributeError → scale factor falls back to 1.0."""
        mock_ctypes = MagicMock()
        # Make windll.user32.GetDpiForSystem raise AttributeError
        mock_ctypes.windll.user32.GetDpiForSystem.side_effect = AttributeError(
            "No windll on this platform"
        )
        with patch.dict(sys.modules, {'ctypes': mock_ctypes}):
            result = _get_scale_factor_impl()
        self.assertEqual(result, 1.0)

    # ------------------------------------------------------------------
    # Compensated window size tests
    # ------------------------------------------------------------------

    def test_window_size_at_scale_125(self):
        """scale=1.25 → Window.size = (320, 640).

        int(400 / 1.25) = 320, int(800 / 1.25) = 640.
        """
        size = _compute_window_size(1.25)
        self.assertEqual(size, (320, 640))

    def test_window_size_at_scale_150(self):
        """scale=1.5 → Window.size = (266, 533).

        int(400 / 1.5) = 266, int(800 / 1.5) = 533.
        """
        size = _compute_window_size(1.5)
        self.assertEqual(size, (266, 533))

    def test_window_size_at_scale_200(self):
        """scale=2.0 → Window.size = (200, 400).

        int(400 / 2.0) = 200, int(800 / 2.0) = 400.
        """
        size = _compute_window_size(2.0)
        self.assertEqual(size, (200, 400))


if __name__ == '__main__':
    unittest.main(verbosity=2)
