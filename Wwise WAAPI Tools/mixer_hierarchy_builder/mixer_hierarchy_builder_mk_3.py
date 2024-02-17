import os
import json
from waapi import WaapiClient, CannotConnectToWaapiException

# The path to the submission folder you want to import
audio_mixer_import_path = "C:/path/to/folder"
# The path to the json within the submission folder you want to import
audio_mixer_import_json_path = "C:/path/to/the.json"

dialogue_event_state_groups = {
    "battle_vo_conversation_own_unit_under_ranged_attack" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_enemy_unit_chariot_charge" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_hef_own_army_low_stength" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_army_missile_amount_inferior" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_enemy_unit_flanking" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_dissapointment" : ["VO_Culture", "VO_Actor", "VO_Culture"],
    "battle_vo_conversation_enemy_unit_flying" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_skv_own_unit_warpfire_artillery" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_enemy_unit_charging" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_environment_weather_snow" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_enemy_army_has_many_cannons" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_environment_in_water" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_unit_fearful" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_hef_own_army_air_units" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_unit_under_dragon_firebreath_attack" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_own_unit_artillery_reload" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_enemy_unit_revealed" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_own_army_caused_damage" : ["VO_Culture", "VO_Battle_Selection", "VO_Actor"],
    "battle_vo_conversation_own_army_peasants_fleeing" : ["VO_Actor"],
    "battle_vo_conversation_enemy_army_black_arks_triggered" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_skv_own_unit_tactical_withdraw" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_clash" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Conversation_Clash_Type", "VO_Culture", "VO_Actor"],
    "battle_vo_conversation_environment_in_cave" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_unit_artillery_firing" : ["VO_Culture", "VO_Battle_Selection"],
    "battle_vo_conversation_siege_defence" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Conversation_Clash_Type"],
    "battle_vo_conversation_environment_weather_cold" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_storm_of_magic" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_lzd_own_army_dino_rampage" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_encouragement" : ["VO_Culture", "VO_Actor", "VO_Culture"],
    "battle_vo_conversation_own_unit_routing" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_environment_ground_type_forest" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_def_own_army_murderous_prowess_75_percent" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_allied_unit_routing" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_enemy_skaven_unit_revealed" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_skv_own_unit_spawn_units" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_army_spell_cast" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_siege_attack" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Conversation_Clash_Type"],
    "battle_vo_conversation_def_own_army_murderous_prowess_100_percent" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_unit_moving" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_environment_weather_desert" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_enemy_unit_at_rear" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_enemy_unit_large_creature" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_own_army_black_arks_triggered" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_environment_weather_rain" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_army_at_chokepoint" : ["VO_Culture", "VO_Battle_Selection", "VO_Actor"],
    "battle_vo_conversation_enemy_unit_spell_cast" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_own_army_missile_amount_superior" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_own_unit_artillery_fire" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_environment_ground_type_mud" : ["VO_Culture", "VO_Actor"],
    "battle_vo_conversation_enemy_army_at_chokepoint" : ["VO_Culture", "VO_Battle_Selection", "VO_Actor"],
    "battle_vo_conversation_own_unit_wavering" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_enemy_unit_dragon" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_conversation_proximity" : ["VO_Actor", "VO_Actor"],
    "battle_vo_order_bat_mode_survival" : ["VO_Actor"],
    "battle_vo_order_guard_on" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_bat_mode_capture_pos" : ["VO_Actor", "Battle_Type"],
    "battle_vo_order_halt" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_special_ability" : ["VO_Culture", "VO_Actor", "VO_Battle_Special_Ability", "VO_Battle_Selection", "VO_Battle_Order_Urgency"],
    "battle_vo_order_battle_continue_battle" : ["VO_Actor"],
    "battle_vo_order_climb" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_withdraw_tactical" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_pick_up_engine" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_move_alternative" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_withdraw" : ["VO_Culture", "VO_Actor", "VO_Battle_Order_Urgency"],
    "battle_vo_order_move_siege_tower" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_change_ammo" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Vehicle_Ammo_Type"],
    "battle_vo_order_attack" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Unit_Type", "VO_Battle_Order_Urgency", "VO_Faction_Leader", "VO_Battle_Order_Artillery_Range"],
    "battle_vo_order_skirmish_off" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_generic_response" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Unit_Type", "VO_Battle_Order_Urgency"],
    "battle_vo_order_fire_at_will_on" : ["VO_Culture", "VO_Actor", "VO_Battle_Order_Urgency", "VO_Battle_Selection"],
    "battle_vo_order_short_order" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_change_formation" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_formation_lock" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_move" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Order_Speed", "VO_Battle_Order_Urgency", "VO_Battle_Order_Air_Unit", "VO_Faction_Leader"],
    "battle_vo_order_fire_at_will_off" : ["VO_Culture", "VO_Actor", "VO_Battle_Order_Urgency", "VO_Battle_Selection"],
    "battle_vo_order_man_siege_tower" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_move_ram" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_group_created" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_group_disbanded" : ["VO_Culture", "VO_Actor"],
    "battle_vo_order_skirmish_on" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_melee_off" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_flying_charge" : ["VO_Culture"],
    "battle_vo_order_attack_alternative" : ["VO_Culture", "VO_Actor", "VO_Battle_Unit_Type", "VO_Battle_Order_Urgency"],
    "battle_vo_order_melee_on" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_battle_quit_battle" : ["VO_Actor"],
    "battle_vo_order_bat_speeches" : ["VO_Actor"],
    "battle_vo_order_formation_unlock" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_guard_off" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection"],
    "battle_vo_order_bat_mode_capture_neg" : ["VO_Actor"],
    "battle_vo_order_select" : ["VO_Culture", "VO_Actor", "VO_Battle_Selection", "VO_Battle_Order_Urgency", "VO_Faction_Leader"],
    "campaign_vo_cs_enemy_region_generic" : ["VO_Actor"],
    "campaign_vo_cs_hellforge_customisation_category" : ["VO_Actor"],
    "campaign_vo_cs_intimidated" : ["VO_Culture", "VO_Actor", "VO_Culture"],
    "campaign_vo_cs_hellforge_customisation_unit" : ["VO_Actor"],
    "campaign_vo_cs_tzarkan_calls_and_taunts" : ["VO_Actor", "Generic_Actor_TzArkan_Sanity"],
    "campaign_vo_cs_near_sea" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_victory" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_vassal_enlist" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_forbidden_workshop_purchase_doomrocket" : ["VO_Actor"],
    "campaign_vo_cs_in_forest" : ["VO_Actor"],
    "campaign_vo_cs_summon_elector_counts_panel_open_vo" : ["VO_Actor"],
    "campaign_vo_cs_monster_pens_dilemma_lustria" : ["VO_Actor"],
    "campaign_vo_cs_weather_hot" : ["VO_Actor"],
    "campaign_vo_cs_pre_battle_siege_break" : ["VO_Actor"],
    "campaign_vo_cs_city_public_order_low" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_great_victory" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_captives_release" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_wef_daiths_forge" : ["VO_Actor", "VO_Campaign_Daiths_Forge"],
    "campaign_vo_cs_other_character_details_panel_low_loyalty" : ["VO_Actor"],
    "campaign_vo_cs_spam_click" : ["VO_Actor"],
    "campaign_vo_cs_in_mountains" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_raze" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_pre_battle_siege_continue" : ["VO_Actor"],
    "campaign_vo_cs_other_character_details_panel_neutral" : ["VO_Actor"],
    "campaign_vo_cs_city_under_siege" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_proximity" : ["VO_Actor", "VO_Actor"],
    "campaign_vo_cs_forbidden_workshop_upgrade_weapon_teams" : ["VO_Actor"],
    "campaign_vo_cs_city_riot" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_loot" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_occupy" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_do_nothing" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_weather_cold" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_great_defeat" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_city_other_generic" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_close_defeat" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_captives_enslave" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_sea_storm" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_in_snow" : ["VO_Actor"],
    "campaign_vo_cs_city_buildings_damaged" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_defeat" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_neutral" : ["VO_Actor"],
    "campaign_vo_cs_forbidden_workshop_upgrade_doomwheel" : ["VO_Actor"],
    "campaign_vo_cs_tzarkan_whispers" : ["VO_Actor"],
    "campaign_vo_cs_forbidden_workshop_upgrade_doomflayer" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_occupy_factory" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_monster_pens_event" : ["VO_Actor"],
    "campaign_vo_cs_monster_pens_dilemma_ghrond" : ["VO_Actor"],
    "campaign_vo_cs_pre_battle_fight_battle" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_occupy_outpost" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_close_victory" : ["VO_Actor"],
    "campaign_vo_cs_confident" : ["VO_Culture", "VO_Actor", "VO_Culture"],
    "campaign_vo_cs_post_battle_captives_execute" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_pre_battle_retreat" : ["VO_Actor"],
    "campaign_vo_cs_sacrifice_to_sotek" : ["VO_Actor"],
    "campaign_vo_cs_on_sea" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_sack" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_city_high_corruption" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_other_character_details_panel_positive" : ["VO_Actor"],
    "campaign_vo_cs_monster_pens_dilemma_naggaroth" : ["VO_Actor"],
    "campaign_vo_cs_monster_pens_dilemma_old_world" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_reinstate_elector_count" : ["VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_occupy_tower" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_hellforge_accept" : ["VO_Actor"],
    "campaign_vo_cs_in_rain" : ["VO_Actor"],
    "campaign_vo_cs_city_own_generic" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_cs_post_battle_settlement_establish_foreign_slot" : ["VO_Culture", "VO_Actor"],
    "frontend_vo_character_select" : ["VO_Actor"],
    "campaign_vo_stance_default" : ["VO_Actor"],
    "campaign_vo_no" : ["VO_Actor"],
    "campaign_vo_stance_stalking" : ["VO_Actor"],
    "campaign_vo_selected_allied" : ["VO_Actor"],
    "campaign_vo_post_battle_defeat" : ["VO_Culture", "VO_Actor"],
    "campaign_vo_level_up" : ["VO_Actor"],
    "campaign_vo_yes" : ["VO_Actor"],
    "campaign_vo_stance_settle" : ["VO_Actor"],
    "campaign_vo_retreat" : ["VO_Actor"],
    "campaign_vo_recruit_units" : ["VO_Actor"],
    "campaign_vo_yes_short" : ["VO_Actor"],
    "campaign_vo_agent_action_success" : ["VO_Actor"],
    "campaign_vo_stance_astromancy" : ["VO_Actor"],
    "campaign_vo_ship_dock" : ["VO_Actor", "VO_Campaign_Order_Move_Type"],
    "campaign_vo_post_battle_victory" : ["VO_Actor"],
    "campaign_vo_mounted_creature" : ["VO_Culture"],
    "campaign_vo_stance_patrol" : ["VO_Actor"],
    "gotrek_felix_departure" : ["VO_Actor"],
    "campaign_vo_move_garrisoning" : ["VO_Actor"],
    "campaign_vo_move_next_turn" : ["VO_Actor"],
    "campaign_vo_stance_tunneling" : ["VO_Actor"],
    "campaign_vo_new_commander" : ["VO_Actor"],
    "campaign_vo_diplomacy_negative" : ["VO_Actor"],
    "campaign_vo_stance_channeling" : ["VO_Actor"],
    "campaign_vo_created" : ["VO_Actor"],
    "campaign_vo_selected_fail" : ["VO_Actor"],
    "campaign_vo_stance_land_raid" : ["VO_Actor"],
    "campaign_vo_agent_action_failed" : ["VO_Actor"],
    "campaign_vo_selected_first_time" : ["VO_Actor"],
    "campaign_vo_move" : ["VO_Actor", "VO_Campaign_Order_Move_Type"],
    "campaign_vo_attack" : ["VO_Actor", "VO_Campaign_Order_Move_Type"],
    "campaign_vo_cam_tech_tree_response" : ["VO_Actor"],
    "campaign_vo_cam_disband" : ["VO_Actor"],
    "campaign_vo_stance_muster" : ["VO_Actor"],
    "campaign_vo_stance_double_time" : ["VO_Actor"],
    "campaign_vo_cam_disbanded_pos" : ["VO_Actor"],
    "campaign_vo_special_ability" : ["VO_Actor", "VO_Campaign_Special_Ability"],
    "campaign_vo_stance_ambush" : ["VO_Actor"],
    "campaign_vo_stance_raise_dead" : ["VO_Actor"],
    "campaign_vo_selected_neutral" : ["VO_Actor"],
    "campaign_vo_stance_march" : ["VO_Actor"],
    "campaign_vo_cam_disbanded_neg" : ["VO_Actor"],
    "gotrek_felix_arrival" : ["VO_Actor"],
    "campaign_vo_no_short" : ["VO_Actor"],
    "campaign_vo_cam_skill_weapon_tree" : ["VO_Actor"],
    "campaign_vo_stance_set_camp_raiding" : ["VO_Actor"],
    "campaign_vo_diplomacy_positive" : ["VO_Actor"],
    "campaign_vo_diplomacy_selected" : ["VO_Actor"],
    "campaign_vo_yes_short_aggressive" : ["VO_Actor"],
    "campaign_vo_stance_set_camp" : ["VO_Actor"],
    "campaign_vo_cam_skill_weapon_tree_response" : ["VO_Actor"],
    "campaign_vo_selected_short" : ["VO_Actor"],
    "campaign_vo_cam_tech_tree" : ["VO_Actor"],
    "campaign_vo_selected" : ["VO_Actor"]
}

def read_json_file(audio_mixer_import_json_path):
    try:
        with open(audio_mixer_import_json_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"The file {audio_mixer_import_json_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {audio_mixer_import_json_path}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_author(json_data):
    return json_data.get("Audio Mixer Submission", {}).get("Author")

def get_projects(json_data):
    return json_data.get("Project", [])

def get_vo_actor(json_data, project_index):
    projects = get_projects(json_data)
    if project_index < len(projects):
        return projects[project_index].get("VO_Actor")
    return None

def get_vo_culture(json_data, project_index):
    projects = get_projects(json_data)
    if project_index < len(projects):
        return projects[project_index].get("VO_Culture")
    return None

def get_dialogue_event_keys(json_data, project_index):
    dialogue_events = get_dialogue_events(json_data, project_index)
    return list(dialogue_events.keys())

def get_dialogue_events(json_data, project_index):
    projects = get_projects(json_data)
    if project_index < len(projects):
        return projects[project_index].get("Dialogue_Events", {})
    return {}

def get_sounds_for_state(json_data, project_index, event, state):
    dialogue_events = get_dialogue_events(json_data, project_index)
    event_data = dialogue_events.get(event, {})
    # Directly access the sounds list for the specified state within the event
    sounds_list = event_data.get(state, [])
    # Splitting the string into a list if it's not already a list
    if isinstance(sounds_list, str):
        sounds_list = sounds_list.split(', ')
    return sounds_list

def count_project_indexes(data):
    # Check if 'Project' key exists and is a list, then return its length
    if 'Project' in data and isinstance(data['Project'], list):
        return len(data['Project'])
    return 0

def get_state_path(json_data, project_index, event):
    dialogue_events = get_dialogue_events(json_data, project_index)
    event_data = dialogue_events.get(event, {})
    # Return all keys in the event data dictionary
    return list(event_data.keys())

def string_after_pattern(input_string, pattern):    
    # Find the position where the pattern starts
    pattern_start = input_string.find(pattern)
    
    # Check if the pattern was found
    if pattern_start != -1:
        # Calculate the start of the substring after the pattern
        start_of_substring = pattern_start + len(pattern)
        
        # Extract and print the substring
        result_string = input_string[start_of_substring:]

        return result_string
 
def determine_bnk_name(dialogue_event):
    # Convert the input to lowercase once to optimize comparisons
    folder_lower = dialogue_event.lower()
    if "battle_vo_conversation".lower() in folder_lower:
        return "Battle_VO_Conversational"
    elif "battle_vo_order".lower() in folder_lower:
        return "Battle_VO_Orders"
    elif "campaign_vo_cs".lower() in folder_lower:
        return "Campaign_VO_Conversational"
    elif "campaign_vo".lower() in folder_lower:
        return "Campaign_VO"
    elif "frontend_vo".lower() in folder_lower:
        return "Frontend_VO", 
    elif folder_lower == "battle_individual_melee_weapon_hit":
        return "Battle_VO_Conversational"
    elif folder_lower in ["gotrek_felix_arrival", "gotrek_felix_departure"]:
        return "Campaign_VO"
    else:
        return None

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

def find_object(dialogue_event_mixer_path):
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

def generate_mixer_hierarchy():
    for index, project in enumerate(json_data['Project']):
        print(f"Project index is: {index}")

        dialogue_events = get_dialogue_event_keys(json_data, index)
        print(f"Dialogue_Event: {dialogue_events}")

        for dialogue_event in dialogue_events:
            print(f"Processing Dialogue_Event: {dialogue_event}")
            bnk_name = determine_bnk_name(dialogue_event)

            if bnk_name:
                print(f"bnk_name: {bnk_name}")
                dialogue_event_mixer_path = f"\\Actor-Mixer Hierarchy\\Default Work Unit\\{bnk_name}\\{dialogue_event}"
                find_dialogue_event_mixer = client.call("ak.wwise.core.object.get", find_object(dialogue_event_mixer_path))

                vo_culture = get_vo_culture(json_data, index)
                vo_culture_shortened = string_after_pattern(vo_culture, "vo_culture_")
                vo_culture_path = f"{dialogue_event_mixer_path}\\{vo_culture_shortened}"
                print(f"vo_culture_shortened: {vo_culture_shortened}")
            
                author = get_author(json_data)
                author_path = f"{vo_culture_path}\\{author}"
                print(f"Author: {author}")
                
                vo_actor = get_vo_actor(json_data, index)
                pattern = f"vo_actor_{vo_culture_shortened}_"
                vo_actor_shortened = string_after_pattern(vo_actor, pattern)
                vo_actor_path = f"{author_path}\\{vo_actor_shortened}"
                print(f"vo_actor_shortened: {vo_actor_shortened}")

                def convert_state_path(state_path):
                    # Split the string into segments based on the period character
                    segments = state_path.split('.')
                    # Wrap each segment in square brackets
                    wrapped_segments = ['[' + segment + ']' for segment in segments]
                    # Concatenate the modified segments back together
                    converted_path = ''.join(wrapped_segments)
                    # Add the converted string to the list                    
                    return converted_path

                def generate_sounds_and_container(): 
                    state_paths = get_state_path(json_data, index, dialogue_event)
                    print(f"State Paths: {state_paths}") 
                    
                    for random_container in state_paths:
                        mixer_folders = f"[{dialogue_event}][{vo_culture_shortened}][{author}][{vo_actor_shortened}]"
                        random_container_converted = convert_state_path(random_container)
                        random_container_combined = f"{mixer_folders} - {random_container_converted}" 

                        result = client.call("ak.wwise.core.object.create", create_random_container(random_container_combined, vo_actor_path))

                        if result:
                                print(f"Created Random Container: {random_container_combined} with ID: {result['id']}")

                        else:
                            print(f"Failed to create Sound: {random_container_combined}")
                        
                        wav_files = get_sounds_for_state(json_data, index, dialogue_event, random_container)
                        print(f"wav_files: {wav_files}")
                        
                        wav_paths = []
                        for wav_file in wav_files:
                            wav_file_path = os.path.join(audio_mixer_import_path, wav_file)
                            wav_file_path = wav_file_path.replace('\\', '/')
                            wav_file_path = wav_file_path.replace('/', '\\')
                            wav_paths.append(wav_file_path)
                        print("wav_paths: " + str(wav_paths))

                        for wav_path in wav_paths:
                            wav_name = wav_path.split("\\")[-1]
                            wav_extension_removed = wav_name.replace('.wav', '')
                            print(wav_name)
                            print(wav_extension_removed)
                            sound_path = f"{vo_actor_path}\\{random_container_combined}\\<Sound Voice>{wav_extension_removed}"
                            client.call("ak.wwise.core.audio.import", create_sound(sound_path, wav_path))

                if find_dialogue_event_mixer:
                    print(f"Found mixer: {dialogue_event}")
                    find_vo_culture = client.call("ak.wwise.core.object.get", find_object(vo_culture_path))

                    if find_vo_culture:
                        print(f"Found mixer: {vo_culture_shortened}")

                    else:
                        print(f"Did not find mixer: {vo_culture_shortened}")
                        result = client.call("ak.wwise.core.object.create", create_mixer(dialogue_event_mixer_path, vo_culture_shortened))
                    
                        if result:
                            print(f"Created Mixer: {vo_culture_shortened} with ID: {result['id']}")
                        
                        else:
                            print(f"Failed to create mixer: {vo_culture_shortened}")

                    find_author = client.call("ak.wwise.core.object.get", find_object(author_path))
                    if find_author:
                        print(f"Found mixer: {author}")

                    else:
                        print(f"Did not find mixer: {author}")
                        result = client.call("ak.wwise.core.object.create", create_mixer(vo_culture_path, author))
                        if result:
                            print(f"Created Mixer: {author} with ID: {result['id']}")
                        
                        else:
                            print(f"Failed to create mixer: {author}")

                    find_vo_actor = client.call("ak.wwise.core.object.get", find_object(vo_actor_path))
                    if find_vo_actor:
                        generate_sounds_and_container()

                    else:
                        print(f"Did not find mixer: {vo_actor_shortened}")
                        result = client.call("ak.wwise.core.object.create", create_mixer(author_path, vo_actor_shortened))
                        if result:
                            print(f"Created Mixer: {vo_actor_shortened} with ID: {result['id']}")
                            generate_sounds_and_container()
                        
                        else:
                            print(f"Failed to create mixer: {vo_actor_shortened}")

            else:
                print(f"No bnk_name determined for {dialogue_event}.")

def generate_states():
    def get_state_groups_from_path(random_container_folder):
        # Split the string by periods
        states = random_container_folder.split('.')
        return states
    for index, project in enumerate(json_data['Project']):
        print(f"Project index is: {index}")

        dialogue_events = get_dialogue_event_keys(json_data, index)
        print(f"Dialogue_Event: {dialogue_events}")

        for dialogue_event in dialogue_events: # Battle_VO_Conversation_Clash
            state_paths = get_state_path(json_data, index, dialogue_event)
            print(f"State Paths: {state_paths}") 
            
            for random_container in state_paths: 
                states_work_unit = []
                print(f"Random Container: {random_container}") # ovn_vo_culture_Albion.ovn_vo_actor_Dural_Durak.Any.Any.Any.Any
                
                states = get_state_groups_from_path(random_container)
                print(f"States: {states}") # ['ovn_vo_culture_Albion', 'ovn_vo_actor_Dural_Durak', 'Any', 'Any', 'Any', 'Any']

                state_groups = dialogue_event_state_groups[dialogue_event.lower()]
                print(f"State Groups: {state_groups}") # ['VO_Culture', 'VO_Actor', 'VO_Battle_Selection', 'VO_Battle_Conversation_Clash_Type', 'VO_Culture', 'VO_Actor']

                states_number = len(states)
                state_groups_number = len(state_groups)

                if states_number == state_groups_number:
                    # Iterate through both lists simultaneously
                    for state_group, state in zip(state_groups, states):
                        states_work_unit.append({state_group: state})

                    print(states_work_unit)

                    # Iterate through the list of dictionaries
                    for entry in states_work_unit:
                        # Each entry is a dictionary
                        for state_group, state in entry.items():
                            print(f"State Group: {state_group}, State: {state}")
                            state_group_path = f"\\States\\Default Work Unit\\{state_group}"
                            find_state_group = client.call("ak.wwise.core.object.get", find_object(state_group_path))
                            
                            if find_state_group:
                                print(f"Found State Group: {state_group}")
                                state_path = f"{state_group_path}\\{state}"
                                find_state = client.call("ak.wwise.core.object.get", find_object(state_path))

                                if find_state:
                                    print(f"Found State: {state}")

                                else:
                                    if state.lower() != "any":
                                        result = client.call("ak.wwise.core.object.create", create_state(state_group_path, state))
                                        if result:
                                            print(f"Created State: {state} with ID: {result['id']}")

                                        else:
                                            print("Could not create state.")
                            else:
                                print(f"Did not find State Group: {state_group_path}")
                else:
                    print(f"################# ERROR: The number of states is incorrect for the Dialogue_Event: {dialogue_event}")

try:
    with WaapiClient() as client:
        json_data = read_json_file(audio_mixer_import_json_path)

        if json_data is not None:
            print("JSON data successfully read:")
            print(json_data)
        else:
            print("Failed to read JSON data.")

        generate_mixer_hierarchy()
        generate_states()
        
except CannotConnectToWaapiException:
    print("Could not connect to WAAPI: Is Wwise running and Wwise Authoring API enabled?")

except Exception as e:
    print(str(e))