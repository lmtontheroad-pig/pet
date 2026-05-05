import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("缺少 Pillow。请先安装：pip install pillow", file=sys.stderr)
    sys.exit(1)

FRAME_WIDTH = 192
FRAME_HEIGHT = 208
COLS = 8
ROWS = 9
SHEET_WIDTH = FRAME_WIDTH * COLS
SHEET_HEIGHT = FRAME_HEIGHT * ROWS

USED_FRAMES = {
    0: set(range(0, 6)),  # idle
    1: set(range(0, 8)),  # running-right
    2: set(range(0, 8)),  # running-left
    3: set(range(0, 4)),  # waving
    4: set(range(0, 5)),  # jumping
    5: set(range(0, 8)),  # failed
    6: set(range(0, 6)),  # waiting
    7: set(range(0, 6)),  # running
    8: set(range(0, 6)),  # review
}


def is_fully_transparent(frame: Image.Image) -> bool:
    rgba = frame.convert("RGBA")
    alpha = rgba.getchannel("A")
    return alpha.getbbox() is None


def validate_sheet(image_path: Path) -> None:
    if not image_path.exists():
        raise FileNotFoundError(f"找不到文件：{image_path}")

    with Image.open(image_path) as image:
        if image.size != (SHEET_WIDTH, SHEET_HEIGHT):
            raise ValueError(
                f"图集尺寸错误：当前为 {image.size[0]}×{image.size[1]}，"
                f"要求为 {SHEET_WIDTH}×{SHEET_HEIGHT}"
            )

        for row in range(ROWS):
            for col in range(COLS):
                left = col * FRAME_WIDTH
                top = row * FRAME_HEIGHT
                right = left + FRAME_WIDTH
                bottom = top + FRAME_HEIGHT

                frame = image.crop((left, top, right, bottom))

                if col not in USED_FRAMES[row]:
                    if not is_fully_transparent(frame):
                        raise ValueError(
                            f"未使用格必须全透明：第 {row} 行，第 {col} 列 不为空。"
                        )

    print("图集校验通过。")


def main():
    if len(sys.argv) != 2:
        print("用法：python validate_spritesheet.py spritesheet.webp", file=sys.stderr)
        sys.exit(1)

    image_path = Path(sys.argv[1])

    try:
        validate_sheet(image_path)
    except Exception as exc:
        print(f"校验失败：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
