# Codex Pets

这个仓库收集 Codex 自定义宠物图集。目前包含三只宠物：

- `otto-codex-pet`：戴绿色睡帽的小水獭 Otto。
- `chouchou-codex-pet`：奶油色虎斑小猫 Chouchou。
- `zhuchouta-codex-pet`：小猪、小水獭和虎斑小猫组成的组合宠物 Zhuchouta。

每个宠物项目都可以独立安装。项目内包含：

- `pet.json`：Codex 自定义宠物清单。
- `spritesheet.webp`：透明背景宠物图集。
- `spritesheet-preview.png`：带棋盘格和网格线的预览图，不参与安装。
- `setup-*-pet.ps1`：Windows 安装脚本。
- `validate_spritesheet.py`：图集规格校验脚本。

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

## 图集规格

Codex 自定义宠物图集使用固定规格：

- 文件尺寸：`1536 × 1872`
- 网格：`8 × 9`
- 单格尺寸：`192 × 208`
- 背景：透明
- 未使用格：完全透明

行定义：

| 行 | 动画 | 使用列 |
| --- | --- | --- |
| 0 | idle | 0-5 |
| 1 | running-right | 0-7 |
| 2 | running-left | 0-7 |
| 3 | waving | 0-3 |
| 4 | jumping | 0-4 |
| 5 | failed | 0-7 |
| 6 | waiting | 0-5 |
| 7 | running | 0-5 |
| 8 | review | 0-5 |

## 校验

每个项目都带有校验脚本：

```powershell
python .\validate_spritesheet.py .\spritesheet.webp
```

校验会检查尺寸、网格和未使用格透明状态。
