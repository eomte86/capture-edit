"""capture-edit CLI: 캡처부터 편집까지 한 명령으로.

사용법 예시:
    capture-edit --url https://example.com/chart --selector ".chart-card" \\
        --title "나스닥 종합지수 일봉 (1개월)" \\
        --source "출처: Npay 증권 (2026-10-23 기준)" \\
        --out nasdaq.png

    capture-edit --url https://example.com --preset npay-chart --out out.png
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from .capture import capture
from .edit import edit_image

# 프리셋으로 채울 수 있는 옵션 (명령줄 옵션이 우선한다).
PRESET_KEYS = ("selector", "title", "source", "crop", "width")


def _parse_crop(value: str) -> tuple[int, int, int, int]:
    parts = [int(p.strip()) for p in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "--crop 형식은 'left,top,right,bottom'이다 (예: 55,80,1225,1060)"
        )
    return (parts[0], parts[1], parts[2], parts[3])


def _parse_viewport(value: str) -> tuple[int, int]:
    try:
        w, h = value.lower().split("x")
        return (int(w), int(h))
    except ValueError:
        raise argparse.ArgumentTypeError(
            "--viewport 형식은 'WIDTHxHEIGHT'이다 (예: 1280x900)"
        )


def _load_preset(name: str, presets_file: str) -> dict:
    path = Path(presets_file)
    if not path.exists():
        raise SystemExit(f"프리셋 파일을 찾을 수 없다: {presets_file}")
    presets = json.loads(path.read_text(encoding="utf-8"))
    if name not in presets:
        raise SystemExit(
            f"프리셋 '{name}'이(가) 없다. 사용 가능: {', '.join(presets)}"
        )
    return presets[name]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="capture-edit",
        description="웹 요소를 캡처하고 제목/출처 스트립을 붙여 저장한다.",
    )
    parser.add_argument("--url", required=True, help="캡처할 페이지 URL")
    parser.add_argument("--selector", help="요소만 찍을 CSS 선택자 (없으면 페이지 전체)")
    parser.add_argument("--out", required=True, help="최종 이미지 저장 경로")
    parser.add_argument("--title", help="이미지 위에 붙일 제목")
    parser.add_argument("--source", help="이미지 아래에 붙일 출처 캡션")
    parser.add_argument("--crop", type=_parse_crop, help="'left,top,right,bottom'")
    parser.add_argument("--width", type=int, help="최종 이미지 너비로 리사이즈")
    parser.add_argument("--viewport", type=_parse_viewport, default=(1280, 900))
    parser.add_argument("--wait-ms", type=int, default=1000,
                        help="페이지 로드 후 대기 시간(ms)")
    parser.add_argument("--full-page", action="store_true",
                        help="selector가 없을 때 전체 높이를 찍는다")
    parser.add_argument("--keep-raw", help="편집 전 원본 캡처 저장 경로")
    parser.add_argument("--preset", help="presets.json에 정의된 프리셋 이름")
    parser.add_argument("--presets-file", default="presets.json")
    parser.add_argument("--font", help="제목/출처용 폰트 파일 경로")
    args = parser.parse_args(argv)

    # 프리셋: 명령줄에 없는 옵션만 채운다.
    if args.preset:
        preset = _load_preset(args.preset, args.presets_file)
        supplied = {a.split("=")[0] for a in sys.argv[1:] if a.startswith("--")}
        for key in PRESET_KEYS:
            flag = f"--{key}"
            if flag not in supplied and key in preset:
                setattr(args, key, preset[key])

    raw_path = Path(args.keep_raw) if args.keep_raw else None
    tmp_dir = None
    if raw_path is None:
        tmp_dir = tempfile.TemporaryDirectory()
        raw_path = Path(tmp_dir.name) / "raw.png"

    capture(
        args.url,
        raw_path,
        selector=args.selector,
        viewport=args.viewport,
        wait_ms=args.wait_ms,
        full_page=args.full_page,
    )
    final_path = edit_image(
        raw_path,
        args.out,
        title=args.title,
        source=args.source,
        crop=args.crop,
        width=args.width,
        font_path=args.font,
    )
    print(f"saved: {final_path}")
    if tmp_dir is not None:
        tmp_dir.cleanup()


if __name__ == "__main__":
    main()
