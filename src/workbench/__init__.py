"""Workbench infrastructure for the Prompt Builder CLI.

This module contains the core infrastructure for feature discovery,
registration, and CLI integration. Feature developers should not
modify this module - instead, create features in src/contrib/.
"""

from src.workbench.contrib import (
    FeatureCategory,
    FeatureManifest,
    FeatureContext,
    FeatureResult,
    FeatureRunner,
)

__all__ = [
    "FeatureCategory",
    "FeatureManifest",
    "FeatureContext",
    "FeatureResult",
    "FeatureRunner",
]
