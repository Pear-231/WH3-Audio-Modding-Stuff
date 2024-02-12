import os
import pprint
import re
from waapi import WaapiClient, CannotConnectToWaapiException

# Specify the path of the audio mixer import folder.
audio_mixer_import_path = "C:/path/goes/here"

dir_structure = {}
dialogue_event_folder_depth = 3
culture_folder_relative_depth = -3
author_folder_relative_depth = -2
unit_folder_relative_depth = -4
random_container_depth = 1

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

state_groups_and_states = {
    "Battle_Type": ["Any", "Monster_Hunt", "Normal", "Quest_Battle", "Survival_Battle"],
    "Generic_Actor_TzArkan_Sanity": ["Any", "Gone", "High", "Waning"],
    "VO_Actor": ["Any"],
    "VO_Battle_Conversation_Clash_Type": ["Any", "clash", "clash_combat", "pre_clash"],
    "VO_Battle_Order_Air_Unit": ["Any", "no", "yes"],
    "VO_Battle_Order_Artillery_Range": ["Any", "out_of_range", "within_range"],
    "VO_Battle_Order_Speed": ["Any", "fast", "normal"],
    "VO_Battle_Order_Urgency": ["Any", "heightened", "normal", "threatened"],
    "VO_Battle_Selection": ["Any"],
    "VO_Battle_Special_Ability": ["Any"],
    "VO_Battle_Unit_Type": ["Any", "artillery", "cavalry", "default", "guns", "melee", "ranged"],
    "VO_Battle_Vehicle_Ammo_Type": ["Any", "Artilley_Canister", "Artilley_Explosive"],
    "VO_Campaign_Daiths_Forge": ["Ancillary_Not_Received", "Ancillary_Received", "Ancillary_Upgraded", "Any"],
    "VO_Campaign_Order_Move_Type": ["Any", "land", "sea"],
    "VO_Campaign_Special_Ability": ["Any", "vo_campaign_action_enemy_army", "vo_campaign_action_enemy_character", "vo_campaign_action_enemy_region", "vo_campaign_action_enemy_settlement", "vo_campaign_action_own_army", "vo_campaign_action_own_army_embed_while_specific_character_present", "vo_campaign_action_own_region", "vo_campaign_action_passive", "vo_campaign_action_summon_volcano"],
    "VO_Culture": ["Any"],
    "VO_Faction_Leader": ["Any"]
}

def extract_directory(path):
    for root, dirs, files in os.walk(path):
        # Adjust to make root relative to the starting path to simplify structure
        relative_root = os.path.relpath(root, start=os.path.dirname(path))
        path_elements = relative_root.split(os.sep)
        current_level = dir_structure
        
        # Filter out the '.' from path_elements if it exists
        path_elements = [pe for pe in path_elements if pe != '.']
        
        # Iterate through the path elements to build the directory structure
        for part in path_elements:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        
        # Filter the list of files to include only .wav files
        wav_files = [file for file in files if file.lower().endswith('.wav')]
        
        # Add wav files to the current directory level only if there are any present
        if wav_files:
            current_level['Files'] = wav_files

    # Pretty-print the entire directory structure starting from the target
    pprint.pprint(dir_structure)
    
def determine_bnk_name(dialogue_event_folder):
    # Convert the input to lowercase once to optimize comparisons
    folder_lower = dialogue_event_folder.lower()
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

def get_keys_at_depth(data, depth):
    keys_found = []

    def traverse(node, current_depth=0):
        # Check if the current node is a dictionary
        if isinstance(node, dict):
            # If the current depth matches the target depth, extend keys_found
            if current_depth == depth:
                keys_found.extend(node.keys())
                # Once keys at the target depth are found, don't go deeper in this branch
                return
            # Recursively traverse the dictionary
            for key, value in node.items():
                traverse(value, current_depth + 1)

    traverse(data)

    return keys_found

def get_key_at_relative_depth(data, target_key, relative_depth):
    # Helper function to find the path to the target key
    def find_path(current_data, current_path=[]):
        if target_key in current_data:
            return current_path + [target_key]
        for key, value in current_data.items():
            if isinstance(value, dict):
                new_path = find_path(value, current_path + [key])
                if new_path:
                    return new_path
        return []

    # Find the path to the target key
    path_to_key = find_path(data)

    if not path_to_key:
        return None  # Target key not found

    # Calculate the index for the relative depth
    if relative_depth < 0:
        # Navigate upwards
        target_index = len(path_to_key) + relative_depth
        if 0 <= target_index < len(path_to_key):
            return path_to_key[target_index]
    elif relative_depth > 0:
        # Navigate downwards is limited to direct children for simplicity
        target_data = data
        for key in path_to_key:
            target_data = target_data[key]
        if isinstance(target_data, dict) and relative_depth == 1:
            return next(iter(target_data.keys()), None)

    return None

def find_immediate_child_folders(data, target_key):
    # Helper function to search recursively for the target_key
    def search(data, target_key, found=False):
        if target_key in data:
            # Return the immediate child folders of the target_key
            return list(data[target_key].keys())
        for key, value in data.items():
            if isinstance(value, dict):
                result = search(value, target_key, found)
                if result is not None:
                    return result
        return None

    return search(data, target_key)
    
def get_wav_file_paths(directory_path):
    # List all entries in the directory
    all_entries = os.listdir(directory_path)
    
    # Filter out directories and non-.wav files, keep only .wav files
    # Concatenate the directory path with each .wav file name to get the full path
    wav_file_paths = [os.path.join(directory_path, entry) for entry in all_entries if os.path.isfile(os.path.join(directory_path, entry)) and entry.endswith('.wav')]
    
    return wav_file_paths

def get_wav_files(audio_mixer_import_path):
    try:
        return [file for file in os.listdir(audio_mixer_import_path) if os.path.isfile(os.path.join(audio_mixer_import_path, file))]
    except FileNotFoundError:
        return []

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
    dialogue_event_folders = get_keys_at_depth(dir_structure, dialogue_event_folder_depth)

    for dialogue_event_folder in dialogue_event_folders:
        print(f"Key at depth {dialogue_event_folder_depth} is: {dialogue_event_folder}")
        bnk_name = determine_bnk_name(dialogue_event_folder)

        if bnk_name:
            print(f"bnk_name: {bnk_name}")
            dialogue_event_mixer_path = f"\\Actor-Mixer Hierarchy\\Default Work Unit\\{bnk_name}\\{dialogue_event_folder}"
            find_dialogue_event_mixer = client.call("ak.wwise.core.object.get", find_object(dialogue_event_mixer_path))

            culture_folder = get_key_at_relative_depth(dir_structure, dialogue_event_folder, culture_folder_relative_depth)
            culture_folder_path = f"{dialogue_event_mixer_path}\\{culture_folder}"
        
            author_folder = get_key_at_relative_depth(dir_structure, dialogue_event_folder, author_folder_relative_depth)
            author_folder_path = f"{culture_folder_path}\\{author_folder}"
            
            unit_mixer = get_key_at_relative_depth(dir_structure, dialogue_event_folder, unit_folder_relative_depth)
            unit_mixer_path = f"{author_folder_path}\\{unit_mixer}"

            def generate_sounds_and_container():  
                random_containers = find_immediate_child_folders(dir_structure, dialogue_event_folder)
                
                for random_container in random_containers:
                    result = client.call("ak.wwise.core.object.create", create_random_container(random_container, unit_mixer_path))

                    if result:
                            print(f"Created Random Container: {random_container} with ID: {result['id']}")

                    else:
                        print(f"Failed to create Sound: {random_container}")

                    directory_path = f"{audio_mixer_import_path}/{culture_folder}/{author_folder}/{dialogue_event_folder}/{random_container}"
                    wav_paths = get_wav_file_paths(directory_path)
                    print("wav_paths: " + str(wav_paths))
                    
                    for wav_path in wav_paths:
                        wav_name = wav_path.split("\\")[-1]
                        wav_extension_removed = wav_name.replace('.wav', '')
                        sound_path = f"{unit_mixer_path}\\{random_container}\\<Sound Voice>{wav_extension_removed}"
                        client.call("ak.wwise.core.audio.import", create_sound(sound_path, wav_path))

            if find_dialogue_event_mixer:
                print(f"Found mixer: {dialogue_event_folder}")
                find_culture_folder = client.call("ak.wwise.core.object.get", find_object(culture_folder_path))

                if find_culture_folder:
                    print(f"Found mixer: {culture_folder}")

                else:
                    print(f"Did not find mixer: {culture_folder}")
                    result = client.call("ak.wwise.core.object.create", create_mixer(dialogue_event_mixer_path, culture_folder))
                
                    if result:
                        print(f"Created Mixer: {culture_folder} with ID: {result['id']}")
                    
                    else:
                        print(f"Failed to create mixer: {culture_folder}")

                find_author_folder = client.call("ak.wwise.core.object.get", find_object(author_folder_path))
                if find_author_folder:
                    print(f"Found mixer: {author_folder}")

                else:
                    print(f"Did not find mixer: {author_folder}")
                    result = client.call("ak.wwise.core.object.create", create_mixer(culture_folder_path, author_folder))
                    if result:
                        print(f"Created Mixer: {author_folder} with ID: {result['id']}")
                    
                    else:
                        print(f"Failed to create mixer: {author_folder}")

                find_unit_mixer = client.call("ak.wwise.core.object.get", find_object(unit_mixer_path))
                if find_unit_mixer:
                    generate_sounds_and_container()

                else:
                    print(f"Did not find mixer: {unit_mixer}")
                    result = client.call("ak.wwise.core.object.create", create_mixer(author_folder_path, unit_mixer))
                    if result:
                        print(f"Created Mixer: {unit_mixer} with ID: {result['id']}")
                        generate_sounds_and_container()
                    
                    else:
                        print(f"Failed to create mixer: {unit_mixer}")

        else:
            print(f"No bnk_name determined for {dialogue_event_folder}.")

def generate_states():
    def get_states_from_folder(random_container_folder):
        # Pattern to match text within brackets
        pattern = r"\[(.*?)\]"
        # Find all matches
        states = re.findall(pattern, random_container_folder)
        return states

    dialogue_event_folders = get_keys_at_depth(dir_structure, dialogue_event_folder_depth)

    for dialogue_event_folder in dialogue_event_folders: # Battle_VO_Conversation_Clash
        print(f"Key at depth {dialogue_event_folder_depth} is: {dialogue_event_folder}")
        random_containers = find_immediate_child_folders(dir_structure, dialogue_event_folder)
        
        for random_container in random_containers: 
            states_work_unit = []
            print(f"Random Container: {random_container}") # [ovn_vo_culture_Albion][ovn_vo_actor_Dural_Durak][Any][Any][Any][Any]
            
            states = get_states_from_folder(random_container)
            print(f"States: {states}") # ['ovn_vo_culture_Albion', 'ovn_vo_actor_Dural_Durak', 'Any', 'Any', 'Any', 'Any']

            state_groups = dialogue_event_state_groups[dialogue_event_folder.lower()]
            print(f"State Groups: {state_groups}") # ['VO_Culture', 'VO_Actor', 'VO_Battle_Selection', 'VO_Battle_Conversation_Clash_Type', 'VO_Culture', 'VO_Actor']

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

try:
    with WaapiClient() as client:
        extract_directory(audio_mixer_import_path)
        generate_mixer_hierarchy()
        generate_states()
        
except CannotConnectToWaapiException:
    print("Could not connect to WAAPI: Is Wwise running and Wwise Authoring API enabled?")

except Exception as e:
    print(str(e))