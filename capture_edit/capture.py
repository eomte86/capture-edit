"""웹 페이지 / 요소 스크린샷 캡처 (Playwright 기반).

전체 페이지 인쇄(PDF) 방식과 달리 요소 단위로 직접 찍기 때문에
사이드바 때문에 오른쪽이 잘리는 문제를 원천적으로 피할 수 있다.
"""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright


def capture(
    url: str,
    out_path: str | Path,
    selector: str | None = None,
    viewport: tuple[int, int] = (1280, 900),
    wait_ms: int = 1000,
    full_page: bool = False,
) -> Path:
    """URL을 열어 스크린샷을 저장한다.

    selector가 주어지면 해당 요소만 찍고, 없으면 페이지 전체(또는
    full_page=True일 때 전체 높이)를 찍는다. 저장된 파일 경로를 반환한다.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(
                viewport={"width": viewport[0], "height": viewport[1]}
            )
            page.goto(url, wait_until="networkidle")
            if wait_ms:
                page.wait_for_timeout(wait_ms)
            if selector:
                # locator.screenshot()은 요소가 나타날 때까지 자동 대기한다.
                page.locator(selector).first.screenshot(path=str(out_path))
            else:
                page.screenshot(path=str(out_path), full_page=full_page)
        finally:
            browser.close()
    return out_path
