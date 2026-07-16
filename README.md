# Codex Pets

这个仓库收集 Codex 自定义宠物图集。目前包含三只宠物：

- `otto-codex-pet`：戴绿色睡帽的小水獭 Otto，已升级到 Pet v2，支持 16 个注视方向。
- `chouchou-codex-pet`：奶油色虎斑小猫 Chouchou。
- `zhuchouta-codex-pet`：小猪、小水獭和虎斑小猫组成的组合宠物 Zhuchouta。

每个宠物项目都可以独立安装。项目内包含：

- `pet.json`：Codex 自定义宠物清单。
- `spritesheet.webp`：透明背景宠物图集。
- `spritesheet-preview.png`：带棋盘格和网格线的预览图，不参与安装。
- `setup-*-pet.ps1`：Windows 安装脚本。
- `validate_spritesheet.py`：与该宠物版本匹配的图集校验脚本。

## 安装

进入对应宠物目录后运行安装脚本。

Otto：

```powershell
cd .\otto-codex-pet
.\setup-otto-pet.ps1 -SpritePath .\spritesheet.webp
```

Chouchou：

```powershell
cd .\chouchou-codex-pet
.\setup-chouchou-pet.ps1 -SpritePath .\spritesheet.webp
```

Zhuchouta：

```powershell
cd .\zhuchouta-codex-pet
.\setup-zhuchouta-pet.ps1 -SpritePath .\spritesheet.webp
```

安装完成后，打开 Codex：

1. 进入 `Settings > Appearance > Pets`
2. 选择对应宠物
3. 如果宠物没有显示，点击 `Wake Pet`

## 图集版本

| 项目 | Sprite 版本 | 总尺寸 | 网格 | 单格 |
| --- | --- | --- | --- | --- |
| Otto | v2 | `1536 × 2288` | `8 × 11` | `192 × 208` |
| Chouchou | v1 | `1536 × 1872` | `8 × 9` | `192 × 208` |
| Zhuchouta | v1 | `1536 × 1872` | `8 × 9` | `192 × 208` |

所有图集均使用透明背景，未使用格必须完全透明。Otto v2 在第 0 行第 6 列增加 neutral 中性帧，并在第 9–10 行提供 16 个注视方向。每个子目录的 README 和校验脚本是对应宠物的完整规格来源。

## 校验

在对应宠物目录内运行：

```powershell
python .\validate_spritesheet.py .\spritesheet.webp
```

校验会检查尺寸、网格、已使用格和未使用格的透明状态；Otto v2 还会检查清单版本与透明像素 RGB 残留。
