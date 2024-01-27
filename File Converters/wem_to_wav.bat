for %%i in (*.wem) do "./vgmstream-cli.exe" -o %%~ni.wav %%i
pause