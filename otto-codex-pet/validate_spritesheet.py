import json
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

# v2 在 idle 行追加一个中性帧，并增加两行共 16 个注视方向。
USED_FRAMES = {
    0: set(range(0, 7)),  # idle 0-5 + neutral 6
    1: set(range(0, 8)),  # running-right
    2: set(range(0, 8)),  # running-left
    3: set(range(0, 4)),  # waving
    4: set(range(0, 5)),  # jumping
    5: set(range(0, 8)),  # failed
    6: set(range(0, 6)),  # waiting
    7: set(range(0, 6)),  # running / task work
    8: set(range(0, 6)),  # review
    9: set(range(0, 8)),  # look 000-157.5 degrees
    10: set(range(0, 8)),  # look 180-337.5 degrees
}


def is_fully_transparent(frame: Image.Image) -> bool:
    return frame.getchannel("A").getbbox() is None


def validate_manifest(image_path: Path) -> None:
    manifest_path = image_path.with_name("pet.json")
    if not manifest_path.exists():
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("spriteVersionNumber") != 2:
        raise ValueError("pet.json 必须包含 spriteVersionNumber: 2。")
    if manifest.get("spritesheetPath") != image_path.name:
        raise ValueError(
            "pet.json 的 spritesheetPath 与待校验图集文件名不一致。"
        )


def validate_sheet(image_path: Path) -> None:
    if not image_path.exists():
        raise FileNotFoundError(f"找不到文件：{image_path}")

    validate_manifest(image_path)

    with Image.open(image_path) as source:
        if source.size != (SHEET_WIDTH, SHEET_HEIGHT):
            raise ValueError(
                f"图集尺寸错误：当前为 {source.size[0]}×{source.size[1]}，"
                f"要求为 {SHEET_WIDTH}×{SHEET_HEIGHT}"
            )

        image = source.convert("RGBA")

        for row in range(ROWS):
            for col in range(COLS):
                left = col * FRAME_WIDTH
                top = row * FRAME_HEIGHT
                frame = image.crop(
                    (left, top, left + FRAME_WIDTH, top + FRAME_HEIGHT)
                )

                if col in USED_FRAMES[row]:
                    if is_fully_transparent(frame):
                        raise ValueError(
                            f"已使用格不能为空：第 {row} 行，第 {col} 列。"
                        )
                elif not is_fully_transparent(frame):
                    raise ValueError(
                        f"未使用格必须全透明：第 {row} 行，第 {col} 列不为空。"
                    )

        raw = image.tobytes()
        if any(
            raw[index] == 0 and raw[index - 3 : index] != b"\x00\x00\x00"
            for index in range(3, len(raw), 4)
        ):
            raise ValueError("透明像素中存在非零 RGB 残留。")

    print("Otto v2 图集校验通过。")


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
