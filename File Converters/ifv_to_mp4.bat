for %%i in (*.ivf) do ffmpeg -i "%%i" "%%~ni.mp4"
