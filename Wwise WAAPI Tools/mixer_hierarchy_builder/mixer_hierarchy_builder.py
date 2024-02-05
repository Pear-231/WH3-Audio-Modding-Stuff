# Add the path to the folder for your vo actor.
data_path = "C:/path/to/hierarchy/folder"

# Example folder tructure:
#{   'ovn_vo_actor_dural_durak': {   'Albion': {   'OvN': {   'Dural_Durak': {   'battle_vo_conversation_clash': {   'sounds': [   'battle_vo_conversation_clash_1.wav',
#                                                                                                                                 'battle_vo_conversation_clash_2.wav']},
#                                                                                'battle_vo_conversation_dissapointment': {   'melee': {   'sounds': [   'battle_vo_conversation_dissapointment_1.wav',
#                                                                                                                                                       'battle_vo_conversation_dissapointment_2.wav']}},
#                                                                                'battle_vo_conversation_encouragement': {   'sounds': [   'battle_vo_conversation_encouragement_1.wav',
#                                                                                                                                         'battle_vo_conversation_encouragement_2.wav']
#                                                                                                                                        }
#                                                                            }
#                                                            }
#                                                }
#                                    }
#   }

import os
import pprint
from waapi import WaapiClient, CannotConnectToWaapiException

# Builds a nested dictionary structure representing the directory and file structure starting from data_path.
def build_directory_structure(data_path):
    root_dir_name = os.path.basename(data_path)
    import_data = {root_dir_name: {}}

    def walk_directory(current_path, current_dict):
        try:
            for entry in os.listdir(current_path):
                entry_path = os.path.join(current_path, entry)
                if os.path.isdir(entry_path):
                    current_dict[entry] = {}
                    walk_directory(entry_path, current_dict[entry])
                else:
                    if 'sounds' not in current_dict:
                        current_dict['sounds'] = []
                    current_dict['sounds'].append(entry)
        except Exception as e:
            print(f"Error accessing {current_path}: {e}")

    walk_directory(data_path, import_data[root_dir_name])
    return import_data

# Retrieves all keys at a specified depth in a nested dictionary.
def get_keys_at_depth(d, target_depth, current_depth=0, collected_keys=None):
    if collected_keys is None:
        collected_keys = []

    if current_depth == target_depth:
        if isinstance(d, dict):
            collected_keys.extend(d.keys())
        return collected_keys
    elif isinstance(d, dict):
        for value in d.values():
            get_keys_at_depth(value, target_depth, current_depth + 1, collected_keys)
    elif isinstance(d, list):
        for item in d:
            get_keys_at_depth(item, target_depth, current_depth, collected_keys)
    
    return collected_keys

def find_key_at_relative_depth(data, target_key, relative_depth):
    # Store the path to the target key
    path_to_target = []

    # Flag to stop the search once the target is found
    stop_search = [False]

    # Recursive search to find and store the path to the target key.
    def find_path(data, key, path=[]):
        if stop_search[0]:
            return True  # Stop search if target is found
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    path_to_target.extend(path + [k])
                    stop_search[0] = True
                    return True
                if find_path(v, key, path + [k]):
                    return True
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if find_path(item, key, path + [(None, i)]):  # Use None as a placeholder for list items
                    return True
        return False

    # Execute the search to find the path
    find_path(data, target_key)

    # Navigate to the desired depth relative to the target key
    def get_key_at_relative_depth(path, depth):
        if depth >= 0:
            # Navigate downwards in the path
            target_depth_path = path[:len(path) - 1 + depth] if depth > 0 else path
        else:
            # Navigate upwards in the path
            target_depth_path = path[:depth] if len(path) + depth > 0 else []

        # Extract the value at the target depth
        current_data = data
        for p in target_depth_path:
            if isinstance(p, tuple):
                current_data = current_data[p[0]][p[1]]  # Handle list indices
            else:
                current_data = current_data[p]

        if isinstance(current_data, dict):
            keys = list(current_data.keys())
            # Adjusted to return a single key as a string if there's only one
            return keys[0] if len(keys) == 1 else keys
        elif isinstance(current_data, list):
            return "List"
        else:
            return current_data  # Directly return the value if it's neither a dict nor a list

    # Return the keys or values at the relative depth
    return get_key_at_relative_depth(path_to_target, relative_depth)

# Retrieves all values associated with a specific key in a nested dictionary.
def get_values_by_key(d, target_key, collected_values=None):
    if collected_values is None:
        collected_values = []
        
    if isinstance(d, dict):
        for key, value in d.items():
            if key == target_key:
                if isinstance(value, list):
                    collected_values.extend(value)
                elif isinstance(value, dict):
                    collected_values.append(value)
                else:
                    collected_values.append(value)
                return collected_values
            else:
                get_values_by_key(value, target_key, collected_values)
    elif isinstance(d, list):
        for item in d:
            get_values_by_key(item, target_key, collected_values)
    
    return collected_values

def get_wav_file_paths(data, data_path, target_key):
    paths = []  # List to store the full paths of the .wav files
    base_dir_name = os.path.basename(data_path)  # Extract the last part of the data_path

    def search(data, current_path, skip_root=True):
        """
        Recursively searches through the nested dictionary and constructs the full paths for the .wav files.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                # Skip the root directory name in data_structure if it matches the last part of data_path
                if skip_root and key == base_dir_name:
                    search(value, current_path, skip_root=False)  # Continue without adding to current_path
                    continue
                
                if key == target_key and 'sounds' in value:  # Target key with files found
                    for file in value['sounds']:
                        # Construct path ensuring double backslashes as separators
                        full_path_components = [data_path] + current_path + [key, file]
                        formatted_path = '\\'.join(full_path_components).replace('/', '\\')
                        paths.append(formatted_path)
                else:
                    # Recurse deeper into the structure
                    search(value, current_path + [key], skip_root=False)

    # Start recursive search from the root of the data_structure, skipping the root name if necessary
    search(data, [])

    return paths

def get_object_id_by_path(object_path):
    return  {
        "from": {"path": [object_path]},
        "options": {"return": ["id"]}
    }

def create_mixer(dialogue_event_mixer_path, dialogue_event_mixer):
    # Function to prepare the creation command
    return {
        "parent": dialogue_event_mixer_path,
        "type": "ActorMixer",
        "name": dialogue_event_mixer,
    }

def create_random_container(name, path):
        return  {
            "parent": path,
            "type": "RandomSequenceContainer",
            "name": name,
            "@RandomOrSequence": 1
        }

def create_sound(sound_path, wav_path):
    return  {
        "importOperation": "useExisting",
        "default": {
            "importLanguage": "English(UK)",
            "@IsStreamingEnabled": "true"
        },
        "imports": [
            {
                "objectPath": sound_path,
                "audioFile": wav_path
            }
        ]
    }

def find_mixer(dialogue_event_mixer_path):
    return  {
        "from": {"path": [dialogue_event_mixer_path]},
        "options": {"return": ["id", "name"]}
    }

def create_state(state_group_id, state_name):
    return  {
        "parent": state_group_id,
        "type": "State",
        "name": state_name
    }

# Build directory structure from a specified path
import_data = build_directory_structure(data_path)

# Pretty print the resulting directory structure
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(import_data)

# Get values by key
target_key = 'battle_vo_conversation_clash'

# Connect to Waapi and perform operations
try:
    with WaapiClient() as client:

        dialogue_event_folder_depth = 4
        culture_folder_relative_depth = -4
        author_folder_relative_depth = -3
        unit_folder_relative_depth = -2
        unit_subfolder_relative_depth = 1

        dialogue_event_folders = get_keys_at_depth(import_data, dialogue_event_folder_depth)
        for dialogue_event_mixer in dialogue_event_folders:
            
            if "Battle_VO_Conversation".lower() in dialogue_event_mixer.lower():
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " contains Battle_VO_Conversation.")
                bnk_name = "Battle_VO_Conversational"
            elif "Battle_VO_Order".lower()  in dialogue_event_mixer.lower():
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " contains Battle_VO_Order.")
                bnk_name = "Battle_VO_Orders"
            elif "Campaign_VO_CS".lower()  in dialogue_event_mixer.lower():
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " contains Campaign_VO_CS.")
                bnk_name = "Campaign_VO_Conversational"
            elif "Campaign_VO".lower()  in dialogue_event_mixer.lower():
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " contains Campaign_VO.")
                bnk_name = "Campaign_VO"
            elif "Frontend_VO".lower()  in dialogue_event_mixer.lower():
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " contains Frontend_VO.")
                bnk_name = "Frontend_VO"
            elif dialogue_event_mixer.lower()  == "Battle_Individual_Melee_Weapon_Hit".lower():
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " is Battle_Individual_Melee_Weapon_Hit.")
                bnk_name = "Battle_VO_Conversational"
            elif dialogue_event_mixer.lower()  == "gotrek_felix_arrival".lower()  or dialogue_event_mixer.lower()  == "gotrek_felix_departure".lower():
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " is gotrek_felix_arrival or gotrek_felix_departure.")
                bnk_name = "Campaign_VO"
            else:
                print("dialogue_event_mixer: " + str(dialogue_event_mixer) + " does not belong anywhere? How lonely... We should find him a home.")

            dialogue_event_mixer_path = f"\\Actor-Mixer Hierarchy\\Default Work Unit\\{bnk_name}\\{dialogue_event_mixer}"
            
            culture_mixer = find_key_at_relative_depth(import_data, dialogue_event_mixer, culture_folder_relative_depth)
            culture_mixer_path = f"{dialogue_event_mixer_path}\\{culture_mixer}"
        
            author_mixer = find_key_at_relative_depth(import_data, dialogue_event_mixer, author_folder_relative_depth)
            author_mixer_path = f"{culture_mixer_path}\\{author_mixer}"
            
            unit_mixer = find_key_at_relative_depth(import_data, dialogue_event_mixer, unit_folder_relative_depth)
            unit_mixer_path = f"{author_mixer_path}\\{unit_mixer}"

            unit_subfolder_mixer = find_key_at_relative_depth(import_data, dialogue_event_mixer, unit_subfolder_relative_depth)
            next_level_path = f"{unit_mixer_path}\\{unit_subfolder_mixer}"

            def generate_sounds_and_container():  
                print("unit_subfolder_mixer: " + str(unit_subfolder_mixer))              
                # checking if unit mixer has a subfolder plus sounds or just sounds
                if unit_subfolder_mixer == "sounds":
                    random_container_path = unit_mixer_path
                    random_container_name = f"{dialogue_event_mixer}_{culture_mixer}_{author_mixer}_{unit_mixer}"
                    client.call("ak.wwise.core.object.create", create_random_container(random_container_name, unit_mixer_path))
                    wav_paths = get_wav_file_paths(import_data, data_path, dialogue_event_mixer)
                    print("wav_paths: " + str(wav_paths))
                    
                    for wav_path in wav_paths:
                        wav_name = wav_path.split("\\")[-1]
                        sound_path = f"{random_container_path}\\{random_container_name}\\<Sound Voice>{wav_name}"
                        client.call("ak.wwise.core.audio.import", create_sound(sound_path, wav_path))

                else:
                    random_container_path = next_level_path
                    random_container_name = f"{dialogue_event_mixer}_{culture_mixer}_{author_mixer}_{unit_mixer}_{unit_subfolder_mixer}"
                    find_next_level_mixer = client.call("ak.wwise.core.object.get", find_mixer(random_container_path))

                    # unit mixer subfolder check
                    if find_next_level_mixer:
                        client.call("ak.wwise.core.object.create", create_random_container(random_container_name, random_container_path))
                        wav_paths = get_wav_file_paths(import_data, data_path, unit_subfolder_mixer)
                        print("wav_paths: " + str(wav_paths))

                        for wav_path in wav_paths:
                            wav_name = wav_path.split("\\")[-1]
                            sound_path = f"{random_container_path}\\{random_container_name}\\<Sound Voice>{wav_name}"
                            client.call("ak.wwise.core.audio.import", create_sound(sound_path, wav_path))
                    
                    else:
                        print(f"Did not find mixer: {unit_subfolder_mixer}")
                        result = client.call("ak.wwise.core.object.create", create_mixer(unit_mixer_path, unit_subfolder_mixer))
                        
                        if result:
                            print(f"Created Mixer: {unit_subfolder_mixer} with ID: {result['id']}")
                            generate_sounds_and_container()                        
                        else:
                            print(f"Failed to create mixer: {unit_subfolder_mixer}")
        
            find_dialogue_event_mixer = client.call("ak.wwise.core.object.get", find_mixer(dialogue_event_mixer_path))
            if find_dialogue_event_mixer:
                print(f"Found mixer: {dialogue_event_mixer}")

                # create state
                state_group = "\\States\\Default Work Unit\\VO_Actor"
                state_name = next(iter(import_data))
                result = client.call("ak.wwise.core.object.create", create_state(state_group, state_name))

                if result:
                    print(f"Created State: {state_name} with ID: {result['id']}")

                else:
                    print("Either the State exists or there's some other error.")

                # culture mixer check
                find_culture_mixer = client.call("ak.wwise.core.object.get", find_mixer(culture_mixer_path))
                if find_culture_mixer:
                    print(f"Found mixer: {culture_mixer}")

                else:
                    print(f"Did not find mixer: {culture_mixer}")
                    result = client.call("ak.wwise.core.object.create", create_mixer(dialogue_event_mixer_path, culture_mixer))
                
                    if result:
                        print(f"Created Mixer: {culture_mixer} with ID: {result['id']}")
                    
                    else:
                        print(f"Failed to create mixer: {culture_mixer}")

                # author mixer check
                find_author_mixer = client.call("ak.wwise.core.object.get", find_mixer(author_mixer_path))
                if find_author_mixer:
                    print(f"Found mixer: {author_mixer}")

                else:
                    print(f"Did not find mixer: {author_mixer}")
                    result = client.call("ak.wwise.core.object.create", create_mixer(culture_mixer_path, author_mixer))
                    if result:
                        print(f"Created Mixer: {author_mixer} with ID: {result['id']}")
                    
                    else:
                        print(f"Failed to create mixer: {author_mixer}")

                # unit mixer check
                find_unit_mixer = client.call("ak.wwise.core.object.get", find_mixer(unit_mixer_path))
                if find_unit_mixer:
                    generate_sounds_and_container()

                else:
                    print(f"Did not find mixer: {unit_mixer}")
                    result = client.call("ak.wwise.core.object.create", create_mixer(author_mixer_path, unit_mixer))
                    if result:
                        print(f"Created Mixer: {unit_mixer} with ID: {result['id']}")
                        generate_sounds_and_container()
                    
                    else:
                        print(f"Failed to create mixer: {unit_mixer}")
                
            else:
                print(f"Mixer {dialogue_event_mixer} does not exist...")
                
except CannotConnectToWaapiException:
    print("Could not connect to WAAPI: Is Wwise running and Wwise Authoring API enabled?")
except Exception as e:
    print(str(e))