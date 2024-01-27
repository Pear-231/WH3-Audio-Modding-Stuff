.\WsourcesMaker.exe input
for %%s in (..\*.wproj) do "C:\Program Files (x86)\Audiokinetic\Wwise 2019.2.15.7667\Authoring\x64\Release\bin\WwiseCLI.exe" "%%s" -ConvertExternalSources convert\list.wsources -ExternalSourcesOutput convert\output
pause