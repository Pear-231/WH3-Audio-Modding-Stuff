# Wwise WAAPI Tools
Here are a collection of tools that interact with Wwise's 'WAAPI' API.

## Requirements
- Python 3.6+
- Wwise and the Wwise SDK Package installed, and the Wwise Authoring API enabled (Project > User Preferences... > Enable Wwise Authoring API)
- waapi-client python project installed (Paste the following in cmd: `py -3 -m pip install waapi-client scipy`)

## rename_random_container_to_path
This renames all selected random containers to the combined path of all decendent objects. This is useful when pathing dialogue event states to see what the container is referring to.
### Instructions
- Download this repository.
- Go to `%APPDATA%\Audiokinetic\Wwise\Add-ons` (create the Add-ons folder if not there).
- Copy the `Commands` and `rename_random_container_to_path` folders from the repository and paste them into the `Add-ons` folder.
The folder structure should look like this:
```
--> Add-ons:
  --> Commands
  --> rename_random_container_to_path
  --> etc..
```
- To use it in Wwise right click on the selected random containers, click Audio Mixer Tools, then click Rename Random Container To Path. Alternatively press the shortcut Ctrl + Shift + R.

## dialogue_events_generator
This generates all the dialogue evetns extracted from the WH3 core dat file.

## mixer_generator
This generates mixers based with the names of all the dialogue events extracted from the WH3 core dat file.

## states_generator
This generates all the state groups and states extracted from the WH3 core dat file. 

## mixer_hierarchy_builder
This generates mixers, random containers, and imports sounds from an input of following a specific folder strucutre.
### Instructions
- Replace the path with the folder you want to import.
