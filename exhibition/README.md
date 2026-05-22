# Exhibition Package

2026 電機系專題展覽的整合套件。

## 結構

```
exhibition/
├── README.md              # 你在這裡
├── api.py                 # FastAPI 後端 (TODO, 廖振廷負責)
├── frontend/              # 前端 SPA (組員負責)
│   ├── README.md
│   └── ...                # 組員自選框架
└── static/                # 靜態素材，FastAPI 掛載到 /static/*
    ├── data/
    │   ├── gallery.json   # mock，正式版由 scripts/build_gallery_data.py 產生
    │   └── stats.json
    └── videos/
        ├── opus_only/     # 10 部 Opus baseline 影片 (TODO)
        └── full_system/   # 10 部本系統影片 (TODO)
```

## 文件

- **規格主文件**: [`docs/exhibition_interface.md`](../docs/exhibition_interface.md)
- **完整計畫**: 廖振廷的 plan file `~/.claude/plans/ancient-hugging-petal.md`

## Deadline

**2026-05-26 (二) 晚上**
