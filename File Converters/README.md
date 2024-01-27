# File Converters

## What is this?
A collection of file conversion tools for:
- wav to wem 
- wem to wav 
- ivf to mp4 
- mp4 to ivf 
- mp3 to wav

## Requirements
- Wwise (version 2019.2.15.7667)
- [FFMPEG](https://ffmpeg.org/)
- [vgmstream](https://github.com/vgmstream/vgmstream)

## ivf to mp4, mp4 to ivf, mp3 to wav (FFMPEG)
- Place the bat file in \installation_location\ffmpeg\bin
- Place the files to convert in \installation_location\ffmpeg\bin
- Run the bat file.

## wem to wav (vgmstream)
- Place the bat file in installation_location\vgmstream
- Place the files to convert in installation_location\vgmstream
- Run the bat file.

## wav to wem
- Put your wav files in wav_to_wem\convert\input. 
- Run convert.bat
- Get your wem files from wav_to_wem\convert\output.
- If it still doesn't work for you, in convert.txt change "C:\Program Files (x86)\Audiokinetic\Wwise 2019.2.15.7667\Authoring\x64\Release\bin\WwiseCLI.exe" to whatever the location is of WwiseCLI.exe on your computer then resave it as  convert.bat. Oh and make sure Wwise (version 2019.2.15.7667) is installed.