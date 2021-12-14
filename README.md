# bilibili__download

# How to use
need python3 and psql

```shell
git clone https://github.com/PatchyVideo/bilibili__download
cd bilibili__download
pip install -r requirements.txt
```
create datebase and table by using database.sql

Auto download:

```shell
nohup python get_video.py &
```

Get storaged video info:

```shell
nohup python video_storage.py &
```
