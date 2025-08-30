# 小破站歌单转存
> 使用插件ffmpeg  
> 为了避免溯源,真实的数据已被删除


## 缓存文件格式分析
```bash
文件夹结构:
|- fold0
|- - fold1
|- - - fold3
|- - - - 80
|- - - - - audio.m4s
|- - - - - video.m4s
|- - - - entry.json
|- - - - danmaku.xml
|- - - fold4
|- - - - 80
|- - - - - audio.m4s
|- - - - - video.m4s
|- - - - entry.json
|- - - - danmaku.xml
|- - - fold5
|- - - - 80
|- - - - - audio.m4s
|- - - - - video.m4s
|- - - - entry.json
|- - - - danmaku.xml
```
在这个文件夹中,需要用的就是audio.m4s文件与entry.json

## 使用说明
 ```bash
   pip install -r requirements.txt
   ```
修改`main.py`中文件夹信息,然后运行脚本

## 0.2版本更新
[版本大更新]综合成为一个处理文件,添加音乐的exif信息

## 0.1版本
### 脚本原理
1. 获取缓存中分离出来的音频文件
2. 将m4s文件转为mp3格式
3. `main.py`负责把m4s文件按照指定名称复制出来
4. `change_format.py`负责转换格式
