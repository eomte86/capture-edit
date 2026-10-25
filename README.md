# capture-edit

웹 페이지의 **요소 캡처**부터 **이미지 편집**(자르기, 제목, 출처 캡션)까지
한 명령으로 처리하는 작은 도구.

## 왜 만들었나

블로그용 차트·표 이미지를 만들 때 흔히 겪는 문제:

- 페이지 전체를 인쇄하면 사이드바 때문에 차트 오른쪽이 잘린다.
- 캡처 따로, 편집 따로 하면 손이 많이 가고 매번 크기가 들쭉날쭉해진다.

이 도구는 요소 단위로 직접 찍고(잘림 없음), 제목·출처 스트립을 붙여
바로 발행 가능한 이미지로 만든다. 차트 안의 수치나 그래프 자체는 건드리지
않고, 자르는 건 바깥 여백만, 제목·출처는 이미지 위아래 여백에 붙인다.

## 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

또는 패키지로 설치:

```bash
pip install .
```

## 사용법

```bash
# 요소 하나만 찍어서 제목 + 출처 붙이기
capture-edit --url "https://stock.naver.com/worldstock/index/.IXIC/price" \
  --selector ".chart-card" \
  --title "나스닥 종합지수 일봉 (1개월)" \
  --source "출처: Npay 증권 (2026-10-23 기준)" \
  --out nasdaq.png

# 자르기 + 너비 맞추기까지 한 번에
capture-edit --url "https://example.com/page" \
  --selector "#chart" \
  --crop 55,80,1225,1060 \
  --width 1080 \
  --title "제목" --source "출처: ..." \
  --out out.png

# 원본 캡처도 따로 남기기
capture-edit --url "https://example.com" --out out.png --keep-raw raw.png
```

## 프리셋

자주 쓰는 캡처 설정을 `presets.json`에 저장해두고 이름으로 불러온다.
명령줄 옵션이 프리셋보다 우선한다.

```json
{
  "npay-nasdaq": {
    "selector": ".chart-card",
    "title": "나스닥 종합지수 일봉 (1개월)",
    "source": "출처: Npay 증권"
  }
}
```

```bash
capture-edit --url "https://stock.naver.com/worldstock/index/.IXIC/price" \
  --preset npay-nasdaq --out nasdaq.png
```

## 옵션

| 옵션 | 설명 |
| --- | --- |
| `--url` (필수) | 캡처할 페이지 URL |
| `--selector` | 요소만 찍을 CSS 선택자 (없으면 페이지 전체) |
| `--out` (필수) | 최종 이미지 저장 경로 |
| `--title` | 이미지 위에 붙일 제목 |
| `--source` | 이미지 아래에 붙일 출처 캡션 |
| `--crop` | `left,top,right,bottom` 으로 자르기 |
| `--width` | 최종 이미지 너비로 리사이즈 |
| `--viewport` | 브라우저 뷰포트, 기본 `1280x900` |
| `--wait-ms` | 로드 후 대기 시간(ms), 기본 `1000` |
| `--full-page` | selector가 없을 때 전체 높이를 찍는다 |
| `--keep-raw` | 편집 전 원본 캡처 저장 경로 |
| `--preset` / `--presets-file` | 프리셋 이름 / 프리셋 파일 (기본 `presets.json`) |
| `--font` | 제목/출처용 폰트 파일 경로 (기본: Noto Sans CJK 자동 탐색) |

## 로컬 테스트

```bash
python -m capture_edit --url "file://$(pwd)/examples/test-page.html" \
  --selector ".card" \
  --title "테스트 카드" --source "출처: 테스트" \
  --out output/test.png
```

## 라이선스

MIT. `LICENSE` 파일의 저작권자 이름을 본인 이름으로 바꿔서 사용하세요.
