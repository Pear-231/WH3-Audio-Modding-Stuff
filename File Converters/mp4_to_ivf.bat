for %%i in (*.mp4) do ffmpeg -i "%%i" -c:v libvpx -crf 4 -b:v 10M -r 30 "%%~ni.ivf"
