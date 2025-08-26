

import os
import subprocess

# 源目录
SOURCE_DIR = "./output"
# 目标目录
TARGET_DIR = "./to_mp3"

os.makedirs(TARGET_DIR, exist_ok=True)

def convert_to_mp3(input_path, output_path):
    """调用 ffmpeg 把 m4s 转成 mp3"""
    try:
        print(f"🎵 开始转换: {input_path} -> {output_path}")
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-vn", "-acodec", "libmp3lame", output_path],
            capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
        if result.returncode == 0:
            print(f"✅ 转换成功: {output_path}")
        else:
            print(f"❌ ffmpeg 错误: {result.stderr}")
    except Exception as e:
        print(f"❌ 转换失败 {input_path}: {e}")

def main():
    print(f"🚀 扫描目录: {SOURCE_DIR}")
    files = os.listdir(SOURCE_DIR)
    m4s_files = [f for f in files if f.lower().endswith(".m4s")]

    if not m4s_files:
        print("⚠️ 没有找到任何 .m4s 文件，请检查 SOURCE_DIR 是否正确。")
        return

    for filename in m4s_files:
        input_path = os.path.join(SOURCE_DIR, filename)
        output_name = os.path.splitext(filename)[0] + ".mp3"
        output_path = os.path.join(TARGET_DIR, output_name)
        convert_to_mp3(input_path, output_path)

if __name__ == "__main__":
    main()
