"""캡처한 이미지 후처리: 자르기, 제목 스트립, 출처 캡션, 리사이즈.

차트 안의 수치나 그래프 자체는 건드리지 않는다. 자르는 건 바깥 여백만,
제목과 출처는 이미지 위아래 여백에 붙인다.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# 한글 렌더링용 폰트 후보 (앞에서부터 존재하는 것을 사용).
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/malgun.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _load_font(size: int, font_path: str | None = None):
    paths = ([font_path] if font_path else []) + FONT_CANDIDATES
    for path in paths:
        if not path:
            continue
        try:
            # TTC(컬렉션)는 face index가 필요하고, TTF는 불필요하다.
            return ImageFont.truetype(path, size, index=0)
        except Exception:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def edit_image(
    src_path: str | Path,
    out_path: str | Path,
    title: str | None = None,
    source: str | None = None,
    crop: tuple[int, int, int, int] | None = None,
    width: int | None = None,
    title_size: int = 44,
    source_size: int = 26,
    title_height: int = 105,
    source_height: int = 62,
    font_path: str | None = None,
) -> Path:
    """캡처본을 편집해 저장하고 경로를 반환한다."""
    img = Image.open(src_path).convert("RGB")
    if crop:
        img = img.crop(crop)

    top_h = title_height if title else 0
    bottom_h = source_height if source else 0
    out = Image.new("RGB", (img.width, top_h + img.height + bottom_h), "white")
    draw = ImageDraw.Draw(out)
    if title:
        draw.text(
            (24, 26), title, fill="black",
            font=_load_font(title_size, font_path),
        )
    out.paste(img, (0, top_h))
    if source:
        draw.text(
            (24, top_h + img.height + 14),
            source,
            fill="#666666",
            font=_load_font(source_size, font_path),
        )
    if width and width != out.width:
        ratio = width / out.width
        out = out.resize((width, round(out.height * ratio)), Image.LANCZOS)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path)
    return out_path
