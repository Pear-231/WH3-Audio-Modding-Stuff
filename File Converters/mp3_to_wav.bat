for %%i in (*.mp3) do ffmpeg -i "%%i" "%%~ni.wav"
