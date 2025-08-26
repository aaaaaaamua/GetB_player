import os
import json
import shutil

# 源目录（改成你的实际路径）
SOURCE_DIR = "source_folder"
# 目标目录（改成你要保存的路径）
TARGET_DIR = "./output"

# 确保目标目录存在
os.makedirs(TARGET_DIR, exist_ok=True)

def process_entry(entry_path):
    """处理一个 entry.json 文件"""
    try:
        with open(entry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 获取音乐名称
        filename = data["page_data"]["part"].strip()

        # 找到 audio.m4s 路径
        audio_path = os.path.join(os.path.dirname(entry_path), "80", "audio.m4s")
        if not os.path.exists(audio_path):
            print(f"⚠️ 未找到 audio.m4s: {audio_path}")
            return

        # 新文件路径（加上 .m4s 后缀）
        safe_name = "".join(c for c in filename if c not in r'\/:*?"<>|')  # 过滤非法文件名字符
        target_path = os.path.join(TARGET_DIR, safe_name + ".m4s")

        # 复制文件
        shutil.copy2(audio_path, target_path)
        print(f"✅ 已复制: {target_path}")

    except Exception as e:
        print(f"❌ 处理失败 {entry_path}: {e}")

def main():
    # 遍历文件夹
    for root, dirs, files in os.walk(SOURCE_DIR):
        if "entry.json" in files:
            entry_path = os.path.join(root, "entry.json")
            process_entry(entry_path)

if __name__ == "__main__":
    main()


