import struct
import os

# If you don't already know what this script does, then reading the below explainations won't help you at all. Go learn some Wwise.

# The input and output paths of your bnks.
# The path (and filename) of the bnk you made in wwise, with all of those DialogueEvents that have their IDs (and arguments) the same as the vanilla versions
# The output bnk will be just like your custom bnk, but with the addition of the vanilla decision tree stuff packed inside each DialogueEvent.
bnk_paths = [
    {"input_bnk" : "C:/Users/george/Downloads/battle_vo_generals_speech_cou_quest_battles.bnk", "output_bnk" : "C:/Users/george/Desktop/battle_vo_generals_speech_cou_quest_battles.bnk"},
    #{"input_bnk" : "C:/Users/george/Downloads/battle_vo_generals_speech_cou_quest_battles2.bnk", "output_bnk" : "C:/Users/george/Desktop/battle_vo_generals_speech_cou_quest_battles2.bnk"},
]

#The path to a folder containing the vanilla bnks you extracted from the vanilla .packs
vanilla_bnk_path = "C:/Users/george/Documents/Modding/Resources/Audio Modding/Vanilla VO Banks/2024.01.23/"

# The path to a folder containing the wem files used in your bnk.
wems_path = "C:/Users/george/Downloads/"

# The specific IDs that need replacing.
ids_to_replace = [
        # The format should be (id_to_replace, replacement_id)
        # You can use the name of the object in Wwise for the id_to_replace e.g. "replace_236083155". 
        
        # Audio Bus IDs
        ("replace_3600304837", 3600304837), # battle
        ("replace_3569007248", 3569007248), # campaign
        ("replace_77155641", 77155641),     # possibly diplomacy related, but used in campaign_vo stuff, maybe... unclear...
        ("replace_4047594850", 4047594850), # frontend

        # Game Parameter IDs
        ("replace_2783412956", 2783412956), # Game Parameter
    ]

# All dialogue events currently in the game (extracted from the core dat file)
dialogue_events = {
    "Battle_Individual_Melee_Weapon_Hit", 
    "battle_vo_conversation_allied_unit_routing", 
    "battle_vo_conversation_clash", 
    "battle_vo_conversation_def_own_army_murderous_prowess_100_percent", 
    "battle_vo_conversation_def_own_army_murderous_prowess_75_percent", 
    "battle_vo_conversation_dissapointment", 
    "battle_vo_conversation_encouragement", 
    "battle_vo_conversation_enemy_army_at_chokepoint", 
    "battle_vo_conversation_enemy_army_black_arks_triggered", 
    "battle_vo_conversation_enemy_army_has_many_cannons", 
    "battle_vo_conversation_enemy_skaven_unit_revealed", 
    "battle_vo_conversation_enemy_unit_at_rear", 
    "battle_vo_conversation_enemy_unit_charging", 
    "battle_vo_conversation_enemy_unit_chariot_charge", 
    "battle_vo_conversation_enemy_unit_dragon", 
    "battle_vo_conversation_enemy_unit_flanking", 
    "battle_vo_conversation_enemy_unit_flying", 
    "battle_vo_conversation_enemy_unit_large_creature", 
    "battle_vo_conversation_enemy_unit_revealed", 
    "battle_vo_conversation_enemy_unit_spell_cast", 
    "battle_vo_conversation_environment_ground_type_forest", 
    "battle_vo_conversation_environment_ground_type_mud", 
    "battle_vo_conversation_environment_in_cave", 
    "battle_vo_conversation_environment_in_water", 
    "battle_vo_conversation_environment_weather_cold", 
    "battle_vo_conversation_environment_weather_desert", 
    "battle_vo_conversation_environment_weather_rain", 
    "battle_vo_conversation_environment_weather_snow", 
    "battle_vo_conversation_hef_own_army_air_units", 
    "battle_vo_conversation_hef_own_army_low_stength", 
    "battle_vo_conversation_lzd_own_army_dino_rampage", 
    "battle_vo_conversation_own_army_at_chokepoint", 
    "battle_vo_conversation_own_army_black_arks_triggered", 
    "battle_vo_conversation_own_army_caused_damage", 
    "battle_vo_conversation_own_army_missile_amount_inferior", 
    "battle_vo_conversation_own_army_missile_amount_superior", 
    "battle_vo_conversation_own_army_peasants_fleeing", 
    "battle_vo_conversation_own_army_spell_cast", 
    "battle_vo_conversation_own_unit_artillery_fire", 
    "battle_vo_conversation_own_unit_artillery_firing", 
    "battle_vo_conversation_own_unit_artillery_reload", 
    "battle_vo_conversation_own_unit_fearful", 
    "battle_vo_conversation_own_unit_moving", 
    "battle_vo_conversation_own_unit_routing", 
    "battle_vo_conversation_own_unit_under_dragon_firebreath_attack", 
    "battle_vo_conversation_own_unit_under_ranged_attack", 
    "battle_vo_conversation_own_unit_wavering", 
    "battle_vo_conversation_proximity", 
    "battle_vo_conversation_siege_attack", 
    "battle_vo_conversation_siege_defence", 
    "battle_vo_conversation_skv_own_unit_spawn_units", 
    "battle_vo_conversation_skv_own_unit_tactical_withdraw", 
    "battle_vo_conversation_skv_own_unit_warpfire_artillery", 
    "battle_vo_conversation_storm_of_magic", 
    "battle_vo_order_attack", 
    "battle_vo_order_attack_alternative", 
    "battle_vo_order_bat_mode_capture_neg", 
    "battle_vo_order_bat_mode_capture_pos", 
    "battle_vo_order_bat_mode_survival", 
    "battle_vo_order_bat_speeches", 
    "battle_vo_order_battle_continue_battle", 
    "battle_vo_order_battle_quit_battle", 
    "battle_vo_order_change_ammo", 
    "battle_vo_order_change_formation", 
    "battle_vo_order_climb", 
    "battle_vo_order_fire_at_will_off", 
    "battle_vo_order_fire_at_will_on", 
    "battle_vo_order_flying_charge", 
    "battle_vo_order_formation_lock", 
    "battle_vo_order_formation_unlock", 
    "battle_vo_order_generic_response", 
    "battle_vo_order_group_created", 
    "battle_vo_order_group_disbanded", 
    "battle_vo_order_guard_off", 
    "battle_vo_order_guard_on", 
    "battle_vo_order_halt", 
    "battle_vo_order_man_siege_tower", 
    "battle_vo_order_melee_off", 
    "battle_vo_order_melee_on", 
    "battle_vo_order_move", 
    "battle_vo_order_move_alternative", 
    "battle_vo_order_move_ram", 
    "battle_vo_order_move_siege_tower", 
    "battle_vo_order_pick_up_engine", 
    "battle_vo_order_select", 
    "battle_vo_order_short_order", 
    "battle_vo_order_skirmish_off", 
    "battle_vo_order_skirmish_on", 
    "battle_vo_order_special_ability", 
    "battle_vo_order_withdraw", 
    "battle_vo_order_withdraw_tactical", 
    "campaign_vo_agent_action_failed", 
    "campaign_vo_agent_action_success", 
    "campaign_vo_attack", 
    "campaign_vo_cam_disband", 
    "campaign_vo_cam_disbanded_neg", 
    "campaign_vo_cam_disbanded_pos", 
    "campaign_vo_cam_skill_weapon_tree", 
    "campaign_vo_cam_skill_weapon_tree_response", 
    "campaign_vo_cam_tech_tree", 
    "campaign_vo_cam_tech_tree_response", 
    "campaign_vo_created", 
    "campaign_vo_cs_city_buildings_damaged", 
    "campaign_vo_cs_city_high_corruption", 
    "campaign_vo_cs_city_other_generic", 
    "campaign_vo_cs_city_own_generic", 
    "campaign_vo_cs_city_public_order_low", 
    "campaign_vo_cs_city_riot", 
    "campaign_vo_cs_city_under_siege", 
    "campaign_vo_cs_confident", 
    "campaign_vo_cs_enemy_region_generic", 
    "campaign_vo_cs_forbidden_workshop_purchase_doomrocket", 
    "campaign_vo_cs_forbidden_workshop_upgrade_doomflayer", 
    "campaign_vo_cs_forbidden_workshop_upgrade_doomwheel", 
    "campaign_vo_cs_forbidden_workshop_upgrade_weapon_teams", 
    "campaign_vo_cs_hellforge_accept", 
    "campaign_vo_cs_hellforge_customisation_category", 
    "campaign_vo_cs_hellforge_customisation_unit", 
    "campaign_vo_cs_in_forest", 
    "campaign_vo_cs_in_mountains", 
    "campaign_vo_cs_in_rain", 
    "campaign_vo_cs_in_snow", 
    "campaign_vo_cs_intimidated", 
    "campaign_vo_cs_monster_pens_dilemma_ghrond", 
    "campaign_vo_cs_monster_pens_dilemma_lustria", 
    "campaign_vo_cs_monster_pens_dilemma_naggaroth", 
    "campaign_vo_cs_monster_pens_dilemma_old_world", 
    "campaign_vo_cs_monster_pens_event", 
    "campaign_vo_cs_near_sea", 
    "campaign_vo_cs_neutral", 
    "campaign_vo_cs_on_sea", 
    "campaign_vo_cs_other_character_details_panel_low_loyalty", 
    "campaign_vo_cs_other_character_details_panel_neutral", 
    "campaign_vo_cs_other_character_details_panel_positive", 
    "campaign_vo_cs_post_battle_captives_enslave", 
    "campaign_vo_cs_post_battle_captives_execute", 
    "campaign_vo_cs_post_battle_captives_release", 
    "campaign_vo_cs_post_battle_close_defeat", 
    "campaign_vo_cs_post_battle_close_victory", 
    "campaign_vo_cs_post_battle_defeat", 
    "campaign_vo_cs_post_battle_great_defeat", 
    "campaign_vo_cs_post_battle_great_victory", 
    "campaign_vo_cs_post_battle_settlement_do_nothing", 
    "campaign_vo_cs_post_battle_settlement_establish_foreign_slot", 
    "campaign_vo_cs_post_battle_settlement_loot", 
    "campaign_vo_cs_post_battle_settlement_occupy", 
    "campaign_vo_cs_post_battle_settlement_occupy_factory", 
    "campaign_vo_cs_post_battle_settlement_occupy_outpost", 
    "campaign_vo_cs_post_battle_settlement_occupy_tower", 
    "campaign_vo_cs_post_battle_settlement_raze", 
    "campaign_vo_cs_post_battle_settlement_reinstate_elector_count", 
    "campaign_vo_cs_post_battle_settlement_sack", 
    "campaign_vo_cs_post_battle_settlement_vassal_enlist", 
    "campaign_vo_cs_post_battle_victory", 
    "campaign_vo_cs_pre_battle_fight_battle", 
    "campaign_vo_cs_pre_battle_retreat", 
    "campaign_vo_cs_pre_battle_siege_break", 
    "campaign_vo_cs_pre_battle_siege_continue", 
    "campaign_vo_cs_proximity", 
    "campaign_vo_cs_sacrifice_to_sotek", 
    "campaign_vo_cs_sea_storm", 
    "campaign_vo_cs_spam_click", 
    "campaign_vo_cs_summon_elector_counts_panel_open_vo", 
    "campaign_vo_cs_tzarkan_calls_and_taunts", 
    "campaign_vo_cs_tzarkan_whispers", 
    "campaign_vo_cs_weather_cold", 
    "campaign_vo_cs_weather_hot", 
    "campaign_vo_cs_wef_daiths_forge", 
    "campaign_vo_diplomacy_negative", 
    "campaign_vo_diplomacy_positive", 
    "campaign_vo_diplomacy_selected", 
    "campaign_vo_level_up", 
    "campaign_vo_mounted_creature", 
    "campaign_vo_move", 
    "campaign_vo_move_garrisoning", 
    "campaign_vo_move_next_turn", 
    "campaign_vo_new_commander", 
    "campaign_vo_no", 
    "campaign_vo_no_short", 
    "campaign_vo_post_battle_defeat", 
    "campaign_vo_post_battle_victory", 
    "campaign_vo_recruit_units", 
    "campaign_vo_retreat", 
    "campaign_vo_selected", 
    "campaign_vo_selected_allied", 
    "campaign_vo_selected_fail", 
    "campaign_vo_selected_first_time", 
    "campaign_vo_selected_neutral", 
    "campaign_vo_selected_short", 
    "campaign_vo_ship_dock", 
    "campaign_vo_special_ability", 
    "campaign_vo_stance_ambush", 
    "campaign_vo_stance_astromancy", 
    "campaign_vo_stance_channeling", 
    "campaign_vo_stance_default", 
    "campaign_vo_stance_double_time", 
    "campaign_vo_stance_land_raid", 
    "campaign_vo_stance_march", 
    "campaign_vo_stance_muster", 
    "campaign_vo_stance_patrol", 
    "campaign_vo_stance_raise_dead", 
    "campaign_vo_stance_set_camp", 
    "campaign_vo_stance_set_camp_raiding", 
    "campaign_vo_stance_settle", 
    "campaign_vo_stance_stalking", 
    "campaign_vo_stance_tunneling", 
    "campaign_vo_yes", 
    "campaign_vo_yes_short", 
    "campaign_vo_yes_short_aggressive", 
    "frontend_vo_character_select", 
    "gotrek_felix_arrival", 
    "gotrek_felix_departure"
}

dialogue_event_to_vanilla_bnk = {}
unmatched_dialogue_events = set()

def compute_wwise_hash(name):
    lower = name.lower().strip()
    bytes_data = lower.encode('utf-8')

    hash_value = 2166136261
    for byte_index in range(len(bytes_data)):
        name_byte = bytes_data[byte_index]
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
        hash_value = hash_value ^ name_byte

    return hash_value

# Gets wem files from the provided path
def get_wem_ids():
    wem_ids = []
    files = os.listdir(wems_path)
    for file in files: 
        if "wem" in file:
            wem_id = re.sub('.wem', '', file)
            wem_ids.append(int(wem_id))

    print("wem_ids: " + str(wem_ids))
    return wem_ids

#This tries to update the decision trees of each DialogueEvent within input_bnk
#The update involves taking the decision trees from the same DialogueEvent in a vanilla bnk (above, the dialogue_event_to_vanilla_bnk table)
#And merging the decisions trees together
def merge_vanilla_decision_trees_into_bnk(input_bnk_path, output_bnk_path):
    print("Attempting to merge vanilla decision trees into " + input_bnk_path)
    with open(output_bnk_path, "wb") as output_file:
        with open(input_bnk_path, "rb") as custom_file:
            
            #Reading custom file
            
            #Header
            BKHD = custom_file.read(4).decode('UTF-8')
            assert BKHD == "BKHD", "Invalid header in " + input_bnk_path
            BKHD_e = bytes(BKHD,"UTF-8")
            output_file.write(struct.pack("<%ds" % len(BKHD), BKHD_e))
        
            chunk_size  = struct.unpack("<L", custom_file.read(4))[0]
            output_file.write(struct.pack("<L",chunk_size))
            
            version_thingy = struct.unpack("<L", custom_file.read(4))[0]
            if version_thingy != 2147483784:
                print("Corrected version in header of " + input_bnk_path)
                version_thingy = 2147483784
            output_file.write(struct.pack("<L",version_thingy))
            
            
            bank_id = struct.unpack("<L", custom_file.read(4))[0]
            if bank_id != compute_wwise_hash(os.path.splitext(os.path.basename(output_bnk_path))[0]):
                print("Corrected bank id in header of " + input_bnk_path)
                bank_id = compute_wwise_hash(os.path.splitext(os.path.basename(output_bnk_path))[0])
            output_file.write(struct.pack("<L",bank_id))
            
            chunk = custom_file.read(8)
            output_file.write(chunk)
            
            project_id = struct.unpack("<L", custom_file.read(4))[0]
            if project_id != 2361:
                print("Corrected project id in header of " + input_bnk_path)
                project_id = 2361
            output_file.write(struct.pack("<L", project_id))
            
            chunk = custom_file.read(4)
            output_file.write(chunk)
            
            HIRC = custom_file.read(4).decode('UTF-8')
            assert HIRC == "HIRC", "Invalid header in " + input_bnk_path
            HIRC_e = bytes(HIRC,"UTF-8")
            output_file.write(struct.pack("<%ds" % len(HIRC), HIRC_e))
            
            hirc_chunk_size_offset = output_file.tell()
            chunk_size = struct.unpack("<L", custom_file.read(4))[0] #Needs updating later
            output_file.write(struct.pack("<L",chunk_size))
            
            num_items = struct.unpack("<L", custom_file.read(4))[0]
            output_file.write(struct.pack("<L",num_items))
            
            #All the HIRC items
            for _ in range(num_items):
                hirc_type = struct.unpack("<b", custom_file.read(1))[0]
                output_file.write(struct.pack("<b",hirc_type))
                
                section_size_offset = output_file.tell()
                section_size = struct.unpack("<L", custom_file.read(4))[0] #Needs updating later
                output_file.write(struct.pack("<L",section_size))
                
                id = struct.unpack("<L", custom_file.read(4))[0]
                output_file.write(struct.pack("<L",id))
                
                #If we find the dialogue event in question...
                if (hirc_type == 15):
                    print("Found DialogueEvent " + str(id))
                    if(id in dialogue_event_to_vanilla_bnk):
                        dialogue_event_id = id
                        vanilla_bnk_filename = dialogue_event_to_vanilla_bnk[id]
                        
                        chunk = custom_file.read(1)
                        output_file.write(chunk)
                        
                        custom_tree_depth = struct.unpack("<L", custom_file.read(4))[0]
                        output_file.write(struct.pack("<L",custom_tree_depth))
                        
                        custom_arguments = []
                        for _ in range(custom_tree_depth):
                            arg =  struct.unpack("<L", custom_file.read(4))[0]
                            custom_arguments.append(arg)
                            output_file.write(struct.pack("<L",arg))
                        
                        for _ in range(custom_tree_depth):
                            chunk = custom_file.read(1)
                            output_file.write(chunk)

                        tree_data_size_offset = output_file.tell()
                        tree_data_size = struct.unpack("<L", custom_file.read(4))[0] #Needs updating later
                        output_file.write(struct.pack("<L",tree_data_size))
                        
                        chunk = custom_file.read(1) #This has to be padding or something
                        output_file.write(chunk)
                        
                        #The custom bnk's decision tree
                        assert tree_data_size % 12 == 0, "Decision tree of DialogueEvent " + str(dialogue_event_id) + " is structured wrong"
                        
                        custom_decision_tree_nodes = []
                        for j in range(int(tree_data_size/12)):
                            key = struct.unpack("<L", custom_file.read(4))[0]
                            children_uIdx = struct.unpack("<H", custom_file.read(2))[0]
                            children_uCount = struct.unpack("<H", custom_file.read(2))[0]
                            uWeight = struct.unpack("<H", custom_file.read(2))[0]
                            uProbability = struct.unpack("<H", custom_file.read(2))[0]
                            custom_decision_tree_nodes.append([key, children_uIdx, children_uCount, uWeight, uProbability])
                        
                         
                        #Reading vanilla bnk, return the decision tree of the dialogue event we care about
                        vanilla_decision_tree_nodes = read_and_return_decision_tree(vanilla_bnk_path + vanilla_bnk_filename, dialogue_event_id, custom_tree_depth, custom_arguments)                    
                        
                        
                        #Merge the vanilla and custom decision trees
                        final_tree = merge_decision_trees(custom_decision_tree_nodes, vanilla_decision_tree_nodes, custom_tree_depth)

                        #And finally, write tree
                        def write_node(node):
                            output_file.write(struct.pack("<L",node["key"]))
                            if "audioNodeId" in node:
                                output_file.write(struct.pack("<L",node["audioNodeId"]))
                            else:
                                output_file.write(struct.pack("<H",node["uIdx"]))
                                output_file.write(struct.pack("<H",node["uCount"]))                            
                            output_file.write(struct.pack("<H",node["uWeight"]))
                            output_file.write(struct.pack("<H",node["uProbability"]))
                        
                        for node in final_tree:
                            write_node(node)
                        
                        #Go back and update TreeDataSize
                        bookmark_offset = output_file.tell()
                        tree_data_size = output_file.tell() - tree_data_size_offset - 5 #5? what? its got to be that padding....
                        output_file.seek(tree_data_size_offset)
                        output_file.write(struct.pack("<L",tree_data_size))
                        output_file.seek(bookmark_offset)

                        #Finish off the dialogue event with this
                        chunk = custom_file.read(2)
                        output_file.write(chunk)
                        
                        #Go back and update the DialogueEvent's SectionSize
                        bookmark_offset = output_file.tell()
                        section_size = output_file.tell() - section_size_offset - 4
                        output_file.seek(section_size_offset)
                        output_file.write(struct.pack("<L",section_size))
                        output_file.seek(bookmark_offset)
                        
                        print("   Successful merge?")
                        
                    else:
                        raise Exception("DialogueEvent " + str(id) + " has no entry in the script's dialogue_event_to_vanilla_bnk table")
                        #Really shouldn't skip past this, so raise error
                        #chunk = custom_file.read(section_size - 4)
                        #output_file.write(chunk)
                #If it's not the event we are looking for in the custom bnk, then skip ahead to the next HIRC item
                else:
                    print("Skipping " + str(id) + " since it's not a DialogueEvent")
                    chunk = custom_file.read(section_size - 4)
                    output_file.write(chunk)
                    
            
            #And finally, go back and update the HIRC chunk size
            hirc_chunk_size = output_file.tell() - hirc_chunk_size_offset - 4
            output_file.seek(hirc_chunk_size_offset)
            output_file.write(struct.pack("<L",hirc_chunk_size))
        
        
#Look through bnk_path, find a dialogue_event, check it against expected_tree_depth and expected_arguments, and then return it
def read_and_return_decision_tree(bnk_path, dialogue_event_id, expected_tree_depth=None, expected_arguments=None):
    with open(bnk_path, "rb") as file:
        
        #Header
        BKHD = file.read(4).decode('UTF-8')
        assert BKHD == "BKHD", "Invalid header in " + bnk_path
        chunk_size  = struct.unpack("<L", file.read(4))[0]
        file.read(chunk_size)
        HIRC = file.read(4).decode('UTF-8')
        assert HIRC == "HIRC", "Invalid header in " + bnk_path
        chunk_size = struct.unpack("<L", file.read(4))[0]
        num_items = struct.unpack("<L", file.read(4))[0]
        
        #All the HIRC items
        decision_tree_nodes = []
        for _ in range(num_items):
            hirc_type = struct.unpack("<b", file.read(1))[0]
            section_size = struct.unpack("<L", file.read(4))[0]
            id = struct.unpack("<L", file.read(4))[0]
            
            
            #If we find the dialogue event in question...
            if (hirc_type == 15) and (id == dialogue_event_id):
                
                file.read(1)
                tree_depth = struct.unpack("<L", file.read(4))[0]
                if expected_tree_depth is not None:
                    assert tree_depth == expected_tree_depth, "Tree depths do not match for DialogueEvent " + str(dialogue_event_id)
                
                arguments = []
                for _ in range(tree_depth):
                    arg =  struct.unpack("<L", file.read(4))[0]
                    arguments.append(arg)
                
                if expected_arguments is not None:
                    assert arguments == expected_arguments, "Arguments do not match for DialogueEvent " + str(dialogue_event_id)
        
        
                for _ in range(tree_depth):
                    file.read(1)
                    
                tree_data_size = struct.unpack("<L", file.read(4))[0]
                file.read(1)
                
                #The bnk's decision tree
                assert tree_data_size % 12 == 0, "Decision tree of DialogueEvent " + str(dialogue_event_id) + " is structured wrong"
                
                for _ in range(int(tree_data_size/12)):
                    key = struct.unpack("<L", file.read(4))[0]
                    children_uIdx = struct.unpack("<H", file.read(2))[0]
                    children_uCount = struct.unpack("<H", file.read(2))[0]
                    uWeight = struct.unpack("<H", file.read(2))[0]
                    uProbability = struct.unpack("<H", file.read(2))[0]
                    decision_tree_nodes.append([key, children_uIdx, children_uCount, uWeight, uProbability])
                    
                #file.read(2)
                break #don't need to keep reading
                
            #Otherwise, skip ahead to the next HIRC itrm
            else:
                file.read(section_size - 4)
        
        return decision_tree_nodes

#Extra thing for an audio bus with no known name
def replacement_hack(ids, bnk_path):
    if ids != None:
        with open(bnk_path, 'rb') as file:
            content = file.read()

# Assuming int32 is 4 bytes
        for id in ids:
            old_id = id[0]
            new_id = id[1]

            if isinstance(old_id, str):
                old_bytes = struct.pack('<L', compute_wwise_hash(old_id)) 
            else:
                old_bytes = struct.pack('<L', old_id)

            new_bytes = struct.pack('<L', new_id)

            # Replace all instances of old_value with new_value
            content = content.replace(old_bytes, new_bytes)
            print("Where found, replaced ID: " + str(old_id) + " with " + str(new_id))

        with open(bnk_path, 'wb') as file:
            file.write(content)

#Merges dialogue event decision trees
#Order is a little bit important, the decision_tree_nodes2 get "merged into" decision_tree_nodes1
#So if there is ever a duplicate node, it will use decision_tree_nodes1's probabilities and weights
#But those are almost always a default value, so not a real issue if you get it backwards
def merge_decision_trees(decision_tree_nodes1, decision_tree_nodes2, tree_depth):
    def parse_tree(node_list, depth, current_index=0):
        node = node_list[current_index]
        if depth == 0:
            foobar = struct.unpack('<L', b''.join(struct.pack('<H', value) for value in [node[1], node[2]]))[0]
            return {"key": node[0], "audioNodeId": foobar, "uWeight": node[3], "uProbability": node[4]}
                         
        #secondary checks, since a leaf can (rarely) occur before max depth
        if (node[1] > len(node_list) #Impossibly large amout of children
        or node[2] > len(node_list)  #Impossibly large index
        or node[1] < current_index):                   #Index goes "backwards", also impossible
            foobar = struct.unpack('<L', b''.join(struct.pack('<H', value) for value in [node[1], node[2]]))[0]
            return {"key": node[0], "audioNodeId": foobar, "uWeight": node[3], "uProbability": node[4]}
            
        children_index = node[1]
        children_count = node[2]
        
        result = {"key": node[0], "uWeight": node[3], "uProbability": node[4], "children": []}
        
        for i in range(children_count):
            # Recursively traverse each child
            child_node = parse_tree(node_list, depth - 1, children_index + i)
            result["children"].append(child_node)
        
        return result       

    
    #parse the custom tree into some structure
    parsed_tree1 = parse_tree(decision_tree_nodes1, tree_depth)

    
    #parse the vanilla tree into some structure
    parsed_tree2 = parse_tree(decision_tree_nodes2, tree_depth)
    
    
    #combine the two trees
    def combine_tree(node1, node2):
        children1 = node1.get("children", [])
        children2 = node2.get("children", [])

        combined_children = []
        combined_keys = set()

        # Iterate over children of both trees
        for child1 in children1:
            key1 = child1["key"]
            combined_keys.add(key1)
            matching_child2 = next((child2 for child2 in children2 if child2["key"] == key1), None)

            if matching_child2:
                # Recursively combine nodes with the same key
                combined_child = combine_tree(child1, matching_child2)
                combined_children.append(combined_child)
            else:
                # If key is not present in tree2, include the node from tree1
                combined_children.append(child1)

        # Include nodes from tree2 that do not have a matching key in tree1
        for child2 in children2:
            if child2["key"] not in combined_keys:
                combined_children.append(child2)

        if combined_children == []:
            return {
                "key": node1["key"],
                "audioNodeId": node1["key"],
                "uWeight": node1["uWeight"],
                "uProbability": node1["uProbability"],
            }
        else:
            return {
                "key": node1["key"],
                "uWeight": node1["uWeight"],
                "uProbability": node1["uProbability"],
                "children": combined_children
            }
            

    combined_parsed_tree = combine_tree(parsed_tree1, parsed_tree2)
    
    
    #Sort of the combined tree
    def sort_tree(node):
        if "audioNodeId" in node:
            # Leaf node, nothing to sort
            return node

        sorted_children = sorted(node.get("children", []), key=lambda x: x["key"])
        sorted_children = [sort_tree(child) for child in sorted_children]

        return {
            "key": node["key"],
            "uWeight": node["uWeight"],
            "uProbability": node["uProbability"],
            "children": sorted_children
        }

    sorted_combined_tree = sort_tree(combined_parsed_tree)
    
    
    #Assign indices to tree ("siblings-first-depth-second" traversal order)
    count = 0
    def assign_indices(node):
        nonlocal count

        #Assign index to current node if it doesn't have one (root node only, I think?)
        if "index" in node:
            pass #do nothing
        else:
            node["index"] = count 
            count+=1
        
        #Assign indices to children if they don't have one (they never should, I think?)
        if "children" in node:
            for child in node["children"]:
                if "index" in child:
                    raise Exception("Child somehow already had an index, huh?")
                else:
                    child["index"] = count 
                    count+=1
        
            #Then we can recurse into the children
            node["children"] = [assign_indices(child) for child in node["children"]]
            
        return node
                

    indexed_tree = assign_indices(sorted_combined_tree)
        
    
    #Each parent should then have a record of the index of their first child, and how many children
    def update_parents(node):
        if "children" in node:
            if "uIdx" in node:
                raise Exception("Node somehow already had a uIdx, huh?")
            else:
                node["uIdx"] = node["children"][0]["index"]
                
            if "uCount" in node:
                raise Exception("Node somehow already had a uCount, huh?")
            else:
                node["uCount"] = len(node["children"])
                
            #Then we can recurse into the children
            node["children"] = [update_parents(child) for child in node["children"]]
            
        else:
            pass #do nothing
        
        return node
            
            
    updated_tree = update_parents(sorted_combined_tree)
    
    
    #Linearize tree
    def linearize_tree(node):
        if "children" in node:
            children = node["children"]
            node_ = node
            node_.pop("children", None)
            output = [node_]
            for child in children:
                output.extend(linearize_tree(child))
                
            return output
        else:
            return [node]
    linearized_tree = linearize_tree(updated_tree)
    
    
    #Sort linearize tree by index
    sorted_linearized_tree = sorted(linearized_tree, key=lambda x: x["index"])
    
    return sorted_linearized_tree




#Look through bnk_path, return a list of the DialogueEvent ids contained within
def read_and_return_dialogue_event_ids(bnk_path):
    dialouge_event_ids = []
    with open(bnk_path, "rb") as file:
        #Header
        BKHD = file.read(4).decode('UTF-8')
        assert BKHD == "BKHD", "Invalid header in " + bnk_path
        chunk_size  = struct.unpack("<L", file.read(4))[0]
        file.read(chunk_size)
        HIRC = file.read(4).decode('UTF-8')
        assert HIRC == "HIRC", "Invalid header in " + bnk_path
        chunk_size = struct.unpack("<L", file.read(4))[0]
        num_items = struct.unpack("<L", file.read(4))[0]
        
        #All the HIRC items
        decision_tree_nodes = []
        for _ in range(num_items):
            hirc_type = struct.unpack("<b", file.read(1))[0]
            section_size = struct.unpack("<L", file.read(4))[0]
            id = struct.unpack("<L", file.read(4))[0]
            
            
            #If we find a dialogue event, add to list
            if (hirc_type == 15):
                dialouge_event_ids.append(id)
                
            #Skip ahead to next
            file.read(section_size - 4)
        
    return dialouge_event_ids


def return_dialogue_event_chunk(bnk_path, dialogue_event_id):
    with open(bnk_path, "rb") as file:
        #Header
        BKHD = file.read(4).decode('UTF-8')
        assert BKHD == "BKHD", "Invalid header in " + bnk_path
        chunk_size  = struct.unpack("<L", file.read(4))[0]
        file.read(chunk_size)
        HIRC = file.read(4).decode('UTF-8')
        assert HIRC == "HIRC", "Invalid header in " + bnk_path
        chunk_size = struct.unpack("<L", file.read(4))[0]
        num_items = struct.unpack("<L", file.read(4))[0]
        
        #All the HIRC items
        for _ in range(num_items):
            hirc_type = struct.unpack("<b", file.read(1))[0]
            section_size = struct.unpack("<L", file.read(4))[0]
            id = struct.unpack("<L", file.read(4))[0]
            
            #If we find a dialogue event, add to list
            if (hirc_type == 15) and (id == dialogue_event_id):
                file.seek(-9,1) #go back 9
                return file.read(section_size + 5)
                
            #Skip ahead to next
            file.read(section_size - 4)

#Merge a single dialogue event
def merge_dialogue_event(bnk_path1, bnk_path2, output_file, dialogue_event_id):
    with open(bnk_path1, "rb") as file1:
        #Header
        BKHD = file1.read(4).decode('UTF-8')
        assert BKHD == "BKHD", "Invalid header in " + bnk_path1
        chunk_size  = struct.unpack("<L", file1.read(4))[0]
        file1.read(chunk_size)
        HIRC = file1.read(4).decode('UTF-8')
        assert HIRC == "HIRC", "Invalid header in " + bnk_path1
        chunk_size = struct.unpack("<L", file1.read(4))[0]
        num_items = struct.unpack("<L", file1.read(4))[0]
        
        #All the HIRC items
        for _ in range(num_items):
            hirc_type = struct.unpack("<b", file1.read(1))[0]
            section_size = struct.unpack("<L", file1.read(4))[0]
            id = struct.unpack("<L", file1.read(4))[0]
            
            #If we find the dialogue event
            if (hirc_type == 15) and (id == dialogue_event_id):
                output_file.write(struct.pack("<b",hirc_type))
                
                section_size_offset = output_file.tell()
                output_file.write(struct.pack("<L",0)) #0 for now, update later
                
                output_file.write(struct.pack("<L",id))
                
                chunk = file1.read(1)
                output_file.write(chunk)
                
                tree_depth = struct.unpack("<L", file1.read(4))[0]
                output_file.write(struct.pack("<L",tree_depth))
                
                arguments = []
                for _ in range(tree_depth):
                    arg =  struct.unpack("<L", file1.read(4))[0]
                    arguments.append(arg)
                    output_file.write(struct.pack("<L",arg))
                
                for _ in range(tree_depth):
                    chunk = file1.read(1)
                    output_file.write(chunk)

                tree_data_size_offset = output_file.tell()
                tree_data_size = struct.unpack("<L", file1.read(4))[0] #Needs updating later
                output_file.write(struct.pack("<L",tree_data_size))
                
                chunk = file1.read(1) #This has to be padding or something
                output_file.write(chunk)
                
                #The bnk1's decision tree
                assert tree_data_size % 12 == 0, "Decision tree of DialogueEvent " + str(dialogue_event_id) + " is structured wrong"
                
                decision_tree_nodes1 = []
                for j in range(int(tree_data_size/12)):
                    key = struct.unpack("<L", file1.read(4))[0]
                    children_uIdx = struct.unpack("<H", file1.read(2))[0]
                    children_uCount = struct.unpack("<H", file1.read(2))[0]
                    uWeight = struct.unpack("<H", file1.read(2))[0]
                    uProbability = struct.unpack("<H", file1.read(2))[0]
                    decision_tree_nodes1.append([key, children_uIdx, children_uCount, uWeight, uProbability])
                
                 
                #Reading bnk2, return the decision tree of the dialogue event we care about
                decision_tree_nodes2 = read_and_return_decision_tree(bnk_path2, dialogue_event_id, tree_depth, arguments)                    
                
                
                #Merge the vanilla and custom decision trees
                final_tree = merge_decision_trees(decision_tree_nodes1, decision_tree_nodes2, tree_depth)

                #And finally, write tree
                def write_node(node):
                    output_file.write(struct.pack("<L",node["key"]))
                    if "audioNodeId" in node:
                        output_file.write(struct.pack("<L",node["audioNodeId"]))
                    else:
                        output_file.write(struct.pack("<H",node["uIdx"]))
                        output_file.write(struct.pack("<H",node["uCount"]))                            
                    output_file.write(struct.pack("<H",node["uWeight"]))
                    output_file.write(struct.pack("<H",node["uProbability"]))
                
                for node in final_tree:
                    write_node(node)
                
                #Go back and update TreeDataSize
                bookmark_offset = output_file.tell()
                tree_data_size = output_file.tell() - tree_data_size_offset - 5 #5? what? its got to be that padding....
                output_file.seek(tree_data_size_offset)
                output_file.write(struct.pack("<L",tree_data_size))
                output_file.seek(bookmark_offset)

                #Finish off the dialogue event with this
                chunk = file1.read(2)
                output_file.write(chunk)
                
                #Go back and update the DialogueEvent's SectionSize
                bookmark_offset = output_file.tell()
                section_size = output_file.tell() - section_size_offset - 4
                output_file.seek(section_size_offset)
                output_file.write(struct.pack("<L",section_size))
                output_file.seek(bookmark_offset)            
            else:
                #Skip ahead to next
                file1.read(section_size - 4)

#This takes in two bnks (ideally, custom bnks that haven't been merged with the vanilla decision trees yet)
#And then compiles them into a single bnk that only contains the DialoguEvents
#If it finds the same DialogueEvent in each, then it will merge their decision trees
#It discards any Sound or RandomContainers, etc.
def merge_bnks_together(bnk_path1, bnk_path2, output_bnk_path):
    print("Attempting to merge " + bnk_path1 + " and " + bnk_path2 + " into a single bnk")
    
    #First find all the DialoguEvent ids in file1
    dialogue_event_ids1 = read_and_return_dialogue_event_ids(bnk_path1)
        
    
    #Do the same for file2
    dialogue_event_ids2 = read_and_return_dialogue_event_ids(bnk_path2)

    dialogue_event_ids_combined = dialogue_event_ids1 + dialogue_event_ids2
    dialogue_event_ids_combined = list(set(dialogue_event_ids_combined))
    dialogue_event_ids_combined = sorted(dialogue_event_ids_combined)
        
    with open(output_bnk_path, "wb") as output_file:
            
            #Header
            BKHD_e = bytes("BKHD","UTF-8")
            output_file.write(struct.pack("<%ds" % len("BKHD"), BKHD_e))
        
            chunk_size  = 24
            output_file.write(struct.pack("<L",chunk_size))

            version_thingy = 2147483784
            output_file.write(struct.pack("<L",version_thingy))
            
            bank_id = compute_wwise_hash(os.path.splitext(os.path.basename(output_bnk_path))[0])
            output_file.write(struct.pack("<L",bank_id))
            
            language_id = 550298558
            output_file.write(struct.pack("<L",language_id))
            
            alt_values = 16
            output_file.write(struct.pack("<L",alt_values))
            
            project_id = 2361
            output_file.write(struct.pack("<L", project_id))
            
            padding = 0
            output_file.write(struct.pack("<L", padding))

            HIRC_e = bytes("HIRC","UTF-8")
            output_file.write(struct.pack("<%ds" % len("HIRC"), HIRC_e))
            
            hirc_chunk_size_offset = output_file.tell()
            output_file.write(struct.pack("<L", 0)) #0 for now, will get updated later
            
            hirc_num_items = len(dialogue_event_ids_combined)
            output_file.write(struct.pack("<L",hirc_num_items))
            
            for dialogue_event_id in dialogue_event_ids_combined:
                
                if dialogue_event_id in dialogue_event_ids1:
                    if dialogue_event_id in dialogue_event_ids2:
                        #read file1, merge-in file2's stuff
                        merge_dialogue_event(bnk_path1, bnk_path2, output_file, dialogue_event_id)
                    else:
                        #just copy-over file1's dialogue event, unedited
                        output_file.write(return_dialogue_event_chunk(bnk_path1, dialogue_event_id))
                elif dialogue_event_id in dialogue_event_ids2:
                    #just copy-over file2's dialogue event, unedited
                    output_file.write(return_dialogue_event_chunk(bnk_path2, dialogue_event_id))   
            
            #And finally, go back and update the HIRC chunk size
            hirc_chunk_size = output_file.tell() - hirc_chunk_size_offset - 4
            output_file.seek(hirc_chunk_size_offset)
            output_file.write(struct.pack("<L",hirc_chunk_size))

def read_and_return_non_dialogue_event_ids(bnk_path):
    event_ids = []
    with open(bnk_path, "rb") as file:
        #Header
        BKHD = file.read(4).decode('UTF-8')
        assert BKHD == "BKHD", "Invalid header in " + bnk_path
        chunk_size  = struct.unpack("<L", file.read(4))[0]
        file.read(chunk_size)
        HIRC = file.read(4).decode('UTF-8')
        assert HIRC == "HIRC", "Invalid header in " + bnk_path
        chunk_size = struct.unpack("<L", file.read(4))[0]
        num_items = struct.unpack("<L", file.read(4))[0]
        
        #All the HIRC items
        decision_tree_nodes = []
        for _ in range(num_items):
            hirc_type = struct.unpack("<b", file.read(1))[0]
            section_size = struct.unpack("<L", file.read(4))[0]
            id = struct.unpack("<L", file.read(4))[0]
            
            
            #If we find a NON dialogue event, add to list
            if (hirc_type != 15): #I think this is correct....
                event_ids.append(id)
                
            #Skip ahead to next
            file.read(section_size - 4)
        
    return event_ids

def scramble_ids(bnk_path):
    event_ids = read_and_return_non_dialogue_event_ids(bnk_path)
    
    replacement_pairs = []
    for event_id in event_ids:
        #Concat the bnk's name and the event_id, then run it through the hash.....
        #Doing it this way so it's deterministic
        new_id = compute_wwise_hash(os.path.splitext(os.path.basename(bnk_path))[0] + str(event_id))
        replacement_pairs.append((event_id, new_id))

    wem_ids = get_wem_ids()
    for wem_id in wem_ids:
        new_id = compute_wwise_hash(os.path.splitext(os.path.basename(bnk_path))[0] + str(wem_id))
        replacement_pairs.append((wem_id, new_id))
        print("Renaming " + str(wem_id) + " to " + str(new_id))
        os.rename(wems_path + str(wem_id) + ".wem", wems_path + str(new_id) + ".wem")
        
    replacement_hack(replacement_pairs, bnk_path)

def match_dialogue_event_to_bnk():
    # Matches dialogue events to their parent bnks.
    for dialogue_event in dialogue_events:
        if "battle_vo_conversation" in dialogue_event:
            print("Dialogue Event: " + str(dialogue_event) + " contains battle_vo_conversation.")
            dialogue_event_id = compute_wwise_hash(dialogue_event)
            dialogue_event_to_vanilla_bnk[dialogue_event_id] = "battle_vo_conversational__core.bnk"
        elif "battle_vo_order" in dialogue_event:
            print("Dialogue Event: " + str(dialogue_event) + " contains battle_vo_order.")
            dialogue_event_id = compute_wwise_hash(dialogue_event)
            dialogue_event_to_vanilla_bnk[dialogue_event_id] = "battle_vo_orders__core.bnk"
        elif "campaign_vo_cs" in dialogue_event:
            print("Dialogue Event: " + str(dialogue_event) + " contains campaign_vo_cs.")
            dialogue_event_id = compute_wwise_hash(dialogue_event)
            dialogue_event_to_vanilla_bnk[dialogue_event_id] = "campaign_vo_conversational__core.bnk"
        elif "campaign_vo" in dialogue_event:
            print("Dialogue Event: " + str(dialogue_event) + " contains campaign_vo.")
            dialogue_event_id = compute_wwise_hash(dialogue_event)
            dialogue_event_to_vanilla_bnk[dialogue_event_id] = "campaign_vo__core.bnk"
        elif "frontend_vo" in dialogue_event:
            print("Dialogue Event: " + str(dialogue_event) + " contains frontend_vo.")
            dialogue_event_id = compute_wwise_hash(dialogue_event)
            dialogue_event_to_vanilla_bnk[dialogue_event_id] = "frontend_vo__core.bnk"
        elif dialogue_event == "Battle_Individual_Melee_Weapon_Hit":
            dialogue_event_id = compute_wwise_hash(dialogue_event)
            dialogue_event_to_vanilla_bnk[dialogue_event_id] = "battle_individual_melee__core.bnk"
        elif dialogue_event == "gotrek_felix_arrival" or dialogue_event == "gotrek_felix_departure":
            dialogue_event_id = compute_wwise_hash(dialogue_event)
            dialogue_event_to_vanilla_bnk[dialogue_event_id] = "campaign_vo__core.bnk"
        else:
            # Hmmm what to do about these??
            print("Hello there! To which bnk do you belong Dialogue Event: " + str(dialogue_event))
            unmatched_dialogue_events.add(str(dialogue_event))

    print("dialogue_event_to_vanilla_bnk: " + str(dialogue_event_to_vanilla_bnk))
    print("unmatched_dialogue_events: " + str(unmatched_dialogue_events))

for i in range(len(bnk_paths)):
    input_bnk = bnk_paths[i]['input_bnk']
    output_bnk = bnk_paths[i]['output_bnk']        
    
    #1 Gets the parent bnks of all dialogue events
    match_dialogue_event_to_bnk()
    
    #2. Merge together custom .bnks
    #Only the audio compatibility mod should do this step
    #It discards all non-DialogueEvent WWise objects
    #merge_bnks_together(custom_bnk1, custom_bnk2, "./combined_foobar.bnk")

    #3. Merge-in the vanilla decision trees
    merge_vanilla_decision_trees_into_bnk(input_bnk, output_bnk)

    #4. Extra find+replace thing for audio buses with no known name
    replacement_hack(ids_to_replace, output_bnk)

    #5. Scramble IDs (you MUST do this)
    #WWise can reuse IDs since they are assigned the moment something is created inside the program
    #So if you, for instance, use someone else's project as a template, all of the existing objects will continue to have the same IDs
    #Run this on your custom bnk to guarentee we don't run into any collisions between bnks
    #This scrambling is deterministic (bnk's name is an input) so you'll get the same output IDs if run twice
    scramble_ids(output_bnk)