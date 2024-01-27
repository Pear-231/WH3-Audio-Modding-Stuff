# Bnk Patcher

## What is this?
This is a tool to patch bnks for **non-VO audio** and **music** made with Wwise. It works by patching the header and some music objects to the v136 format of WH3 banks. It also scrambles all non-mixer IDs including wem files and renames wems to match this and changes specific IDs for objects such as mixers or audio busses to what you set them to. This script reuses and modifies some parts of ChaosRobie's excellent dialogue event merger script.

## Requirements
- Python 3.6+
- Visual Studio Code
- [wwiser](https://github.com/bnnm/wwiser)

## Use
- Download the script and open it in a code editor e.g. Visual Studio Code.
- Add your input and output paths for your banks to `bnk_paths`.
- Add the path of your wems to `wems_path`.
- Specify whether you want to scramble the wems as well by changing `scramble_wems` to True of False.
- Add any IDs that need replacing to `ids_to_replace`.
- Run the script with Python.
