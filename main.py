import os
import json
import subprocess
import requests
from mutagen.easyid3 import EasyID3

# 源目录（改成你的实际路径）
SOURCE_DIR = "source_folder"
# 转换后的 mp3 保存目录
MP3_DIR = "./to_mp3"

os.makedirs(MP3_DIR, exist_ok=True)


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


def process_entry(entry_path):
    """处理一个 entry.json 文件：先转成 mp3，再重命名移动"""
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

        # 临时输出文件（先转，后改名）
        temp_output = os.path.join(MP3_DIR, "temp_output.mp3")

        # 转换成 mp3
        convert_to_mp3(audio_path, temp_output)

        # 最终文件名（过滤非法字符）
        safe_name = "".join(c for c in filename if c not in r'\/:*?"<>|')
        final_output = os.path.join(MP3_DIR, safe_name + ".mp3")

        # 如果重名就加序号
        base, ext = os.path.splitext(final_output)
        counter = 1
        while os.path.exists(final_output):
            final_output = f"{base}_{counter}{ext}"
            counter += 1

        # 重命名
        os.rename(temp_output, final_output)
        print(f"✅ 已保存并重命名: {final_output}")

        # 添加标签
        add_music_info(filename, final_output)

    except Exception as e:
        print(f"❌ 处理失败 {entry_path}: {e}")


def add_music_info(music_name,music_path):
    try:
        musicInfo = requests.get(
            f"http://search.kuwo.cn/r.s?all={music_name}&ft=music& itemset=web_2013&client=kt&pn=0&rn=5&rformat=json&encoding=utf8").text.replace(
            "\'", "\"")
        musicInfo = json.loads(musicInfo)
        music_name = musicInfo["abslist"][0]["NAME"]
        musci_artist = musicInfo["abslist"][0]["ARTIST"]

        # 加载MP3文件
        audio = EasyID3(music_path)
        # 修改元数据信息
        audio['title'] = music_name
        audio['artist'] = musci_artist
        # 保存修改
        audio.save()
        print(f"✅ 成功添加音乐标签: {music_name}")
    except Exception as e:
        print(f"❌ 获取音乐信息失败 {music_name}: {e}")


def main():
    print(f"🚀 扫描目录: {SOURCE_DIR}")
    for root, dirs, files in os.walk(SOURCE_DIR):
        if "entry.json" in files:
            entry_path = os.path.join(root, "entry.json")
            process_entry(entry_path)


if __name__ == "__main__":
    main()
