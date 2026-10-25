"""capture-edit: 웹 요소 캡처 + 이미지 편집을 한 번에."""

from .capture import capture
from .edit import edit_image

__version__ = "0.1.0"
__all__ = ["capture", "edit_image"]
