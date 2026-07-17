# Codex Pets

这个仓库收集可独立安装的 Codex 自定义宠物。目前包含：

- `chouchou-codex-pet`：Chouchou，Pet v2，支持 neutral 帧和 16 个环视方向的奶油色虎斑小猫。
- `otto-codex-pet`：Otto，Pet v2，支持 neutral 帧和 16 个注视方向的戴绿色睡帽小水獭。
- `zhuchouta-codex-pet`：Zhuchouta，Pet v2，由小猪、小水獭和虎斑小猫组成，支持 neutral 帧和 16 个环视方向。

## 下载后直接使用

1. 点击 GitHub 的 `Code > Download ZIP`，然后解压。
2. 打开普通 Windows PowerShell，进入要安装的宠物目录。
3. 运行该目录内的安装脚本。

安装 Chouchou v2：

```powershell
cd .\chouchou-codex-pet
.\setup-chouchou-pet.ps1 -SpritePath .\spritesheet.webp
```

安装 Otto v2：

```powershell
cd .\otto-codex-pet
.\setup-otto-pet.ps1 -SpritePath .\spritesheet.webp
```

安装 Zhuchouta v2：

```powershell
cd .\zhuchouta-codex-pet
.\setup-zhuchouta-pet.ps1 -SpritePath .\spritesheet.webp
```

如果 PowerShell 阻止本地脚本执行，可以只对本次安装使用：

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-otto-pet.ps1 -SpritePath .\spritesheet.webp
```

安装脚本会把 `pet.json` 和 `spritesheet.webp` 一起写入 `%USERPROFILE%\.codex\pets\<pet-id>`。安装后打开 Codex，进入 `Settings > Appearance > Pets` 选择对应宠物；如果没有显示，点击 `Wake Pet`。

Python 与 Pillow 只用于安装前自动校验；没有安装时，脚本会跳过校验并继续复制已经随仓库验证通过的正式文件。

## GitHub 目录结构

每个宠物目录都保留可独立下载、校验和安装的发布文件：

```text
<pet>-codex-pet/
├── README.md
├── pet.json
├── spritesheet.webp
├── spritesheet-preview.png
├── setup-<pet>-pet.ps1
└── validate_spritesheet.py
```

部分目录还包含 `art_prompt.txt`，用于记录角色美术与图集规范，不参与安装。

## 图集版本

| 项目 | Sprite 版本 | 总尺寸 | 网格 | 单格 |
| --- | --- | --- | --- | --- |
| Chouchou | v2 | `1536 × 2288` | `8 × 11` | `192 × 208` |
| Otto | v2 | `1536 × 2288` | `8 × 11` | `192 × 208` |
| Zhuchouta | v2 | `1536 × 2288` | `8 × 11` | `192 × 208` |

所有图集均使用透明背景，未使用格必须完全透明。Pet v2 的第 0 行第 6 列是 neutral 帧，第 9–10 行依次提供 16 个方向：

- 第 9 行：`000`、`022.5`、`045`、`067.5`、`090`、`112.5`、`135`、`157.5`
- 第 10 行：`180`、`202.5`、`225`、`247.5`、`270`、`292.5`、`315`、`337.5`

其中 `000` 表示向上，`090` 表示屏幕右侧，`180` 表示向下，`270` 表示屏幕左侧。

## 手动校验

在对应宠物目录内运行：

```powershell
python .\validate_spritesheet.py .\spritesheet.webp
```

三个宠物的 v2 校验器都会检查清单版本、`8 × 11` 图集尺寸、已使用格内容、未使用格透明状态，以及完全透明像素的 RGB 残留。
