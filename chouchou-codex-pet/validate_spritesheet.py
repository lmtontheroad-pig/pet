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
ROWS = 11
SHEET_WIDTH = FRAME_WIDTH * COLS
SHEET_HEIGHT = FRAME_HEIGHT * ROWS

# V2 在 idle 行第 6 列额外保存 neutral 帧；第 9、10 行保存 16 个方向。
USED_FRAMES = {
    0: set(range(0, 7)),  # idle 0-5 + neutral 6
    1: set(range(0, 8)),  # running-right
    2: set(range(0, 8)),  # running-left
    3: set(range(0, 4)),  # waving
    4: set(range(0, 5)),  # jumping
    5: set(range(0, 8)),  # failed
    6: set(range(0, 6)),  # waiting
    7: set(range(0, 6)),  # running
    8: set(range(0, 6)),  # review
    9: set(range(0, 8)),  # look 000-157.5
    10: set(range(0, 8)),  # look 180-337.5
}


def is_fully_transparent(frame: Image.Image) -> bool:
    return frame.getchannel("A").getbbox() is None


def count_transparent_rgb_residue(image: Image.Image) -> int:
    rgba_bytes = image.tobytes()
    return sum(
        1
        for index in range(0, len(rgba_bytes), 4)
        if rgba_bytes[index + 3] == 0
        and (
            rgba_bytes[index] != 0
            or rgba_bytes[index + 1] != 0
            or rgba_bytes[index + 2] != 0
        )
    )


def validate_sheet(image_path: Path) -> None:
    if not image_path.exists():
        raise FileNotFoundError(f"找不到文件：{image_path}")

    with Image.open(image_path) as opened:
        if opened.size != (SHEET_WIDTH, SHEET_HEIGHT):
            raise ValueError(
                f"V2 图集尺寸错误：当前为 {opened.size[0]}×{opened.size[1]}，"
                f"要求为 {SHEET_WIDTH}×{SHEET_HEIGHT}"
            )

        image = opened.convert("RGBA")

        for row in range(ROWS):
            for col in range(COLS):
                left = col * FRAME_WIDTH
                top = row * FRAME_HEIGHT
                frame = image.crop(
                    (left, top, left + FRAME_WIDTH, top + FRAME_HEIGHT)
                )
                used = col in USED_FRAMES[row]
                empty = is_fully_transparent(frame)

                if used and empty:
                    raise ValueError(
                        f"V2 使用格不能为空：第 {row} 行，第 {col} 列为空。"
                    )
                if not used and not empty:
                    raise ValueError(
                        f"V2 未使用格必须全透明：第 {row} 行，第 {col} 列不为空。"
                    )

        residue = count_transparent_rgb_residue(image)
        if residue:
            raise ValueError(
                f"完全透明像素仍有 RGB 残留：共 {residue} 个像素。"
            )

    print("Chouchou V2 图集校验通过。")
    print(f"尺寸：{SHEET_WIDTH}×{SHEET_HEIGHT}；网格：{COLS}×{ROWS}。")


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "用法：python validate_spritesheet.py spritesheet.webp",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        validate_sheet(Path(sys.argv[1]))
    except Exception as exc:
        print(f"校验失败：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
