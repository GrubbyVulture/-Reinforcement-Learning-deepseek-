#!/usr/bin/env python
import os
import sys
from pathlib import Path
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

# 1. 输出目录
OUTPUT_DIR = Path("my_saved_plots_v1_origin")
OUTPUT_DIR.mkdir(exist_ok=True)

# 2. 自动发现 runs 目录（当前工作目录下的 runs）
RUNS_DIR = Path("output_origin/runs")
if not RUNS_DIR.is_dir():
    sys.exit("未找到 runs 目录，请确认脚本在工作目录下运行！")

# 3. 遍历所有子目录（每个子目录是一个 run）
for run_dir in RUNS_DIR.iterdir():
    if not run_dir.is_dir():
        continue

    print(f"🔍 处理 run: {run_dir.name}")
    event_files = list(run_dir.glob("events.out.tfevents.*"))
    if not event_files:
        print("  └─ 未找到事件文件，跳过")
        continue

    # 4. 加载事件
    ea = EventAccumulator(str(run_dir))
    ea.Reload()

    # 5. 提取所有图像标签
    img_tags = ea.Tags().get("images", [])
    if not img_tags:
        print("  └─ 无图像，跳过")
        continue

    for tag in img_tags:
        images = ea.Images(tag)          # List[ImageEvent]
        for img in images:
            # 构造文件名：run名_标签_stepxxx.png
            fname = f"{run_dir.name}_{tag.replace('/', '_')}_step{img.step}.png"
            save_path = OUTPUT_DIR / fname
            with open(save_path, "wb") as f:
                f.write(img.encoded_image_string)
            print(f"  └─ 已保存 {save_path}")

print("✅ 全部提取完成！")