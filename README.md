# Codex Pets

这个仓库收集可独立安装的 Codex 自定义宠物。目前包含：

- `otto-codex-pet`：Otto，V1，戴绿色睡帽的小水獭。
- `chouchou-codex-pet`：Chouchou，V2，支持 16 个环视方向的奶油色虎斑小猫。
- `zhuchouta-codex-pet`：Zhuchouta，V2，由小猪、小水獭和虎斑小猫组成，支持 16 个环视方向。

每个宠物目录采用相同的 GitHub 发布结构：

```text
<pet>-codex-pet/
├── README.md
├── pet.json
├── spritesheet.webp
├── spritesheet-preview.png
├── setup-<pet>-pet.ps1
└── validate_spritesheet.py
```

- `pet.json`：Codex 自定义宠物清单。
- `spritesheet.webp`：正式透明背景图集。
- `spritesheet-preview.png`：GitHub 预览图，不参与安装。
- `setup-*-pet.ps1`：Windows 安装脚本。
- `validate_spritesheet.py`：对应版本的图集规格校验脚本。

## 安装

进入对应宠物目录后运行安装脚本。

Otto V1：

```powershell
cd .\otto-codex-pet
.\setup-otto-pet.ps1 -SpritePath .\spritesheet.webp
```

Chouchou V2：

```powershell
cd .\chouchou-codex-pet
.\setup-chouchou-pet.ps1 -SpritePath .\spritesheet.webp
```

Zhuchouta V2：

```powershell
cd .\zhuchouta-codex-pet
.\setup-zhuchouta-pet.ps1 -SpritePath .\spritesheet.webp
```

安装完成后，在 Codex 中进入 `Settings > Appearance > Pets`，选择对应宠物；如果没有显示，点击 `Wake Pet`。

## 图集规格

所有版本均使用 `192 × 208` 单格和透明背景。

| 版本 | 图集尺寸 | 网格 | 内容 |
| --- | --- | --- | --- |
| V1 | `1536 × 1872` | `8 × 9` | 9 行标准动画 |
| V2 | `1536 × 2288` | `8 × 11` | 9 行标准动画、1 个 neutral 帧、16 个环视方向 |

Chouchou 与 Zhuchouta V2 的方向行按顺时针排列：

- 第 9 行：`000`、`022.5`、`045`、`067.5`、`090`、`112.5`、`135`、`157.5`
- 第 10 行：`180`、`202.5`、`225`、`247.5`、`270`、`292.5`、`315`、`337.5`

其中 `000` 表示向上，`090` 表示屏幕右侧，`180` 表示向下，`270` 表示屏幕左侧。

## 校验

每个宠物目录都带有与其版本匹配的校验脚本：

```powershell
python .\validate_spritesheet.py .\spritesheet.webp
```

校验会检查图集尺寸、网格、使用格内容和未使用格透明状态；V2 宠物还会检查完全透明像素的 RGB 残留。
