################################# INSTRUCTIONS #################################

# The input and output paths of your bnks.
bnk_paths = [
    {"input_bnk" : "C:/bnk/path/goes/here/input.bnk", "output_bnk" : "C:/bnk/path/goes/here/output.bnk"},
    #{"input_bnk" : "C:/bnk/path/goes/here/input_2.bnk", "output_bnk" : "C:/bnk/path/goes/here/output_2.bnk"},
    # Add more as you need
]

# The path to a folder containing the wem files used in your bnk. If scramble_wems is set to True you must provide a path.
wems_path = "C:/wem/folder/path/goes/here/"

# Change this to True / False if you do / don't want to scramble wem IDs. You should do this if you want to avoid potential conflicts with vanilla wems or wems others have made.
scramble_wems = False

# Change this to True if you do / don't want to make sure the language is the english(uk) folder.
make_language_english_uk = True

# The specific IDs that need replacing. This should be any object in the Wwise project with the name replace_some_id.
ids_to_replace = [     
        # The format should be (id_to_replace, replacement_id).
        # You can use the name of the object in Wwise for the id_to_replace e.g. "replace_236083155" for all objects EXCEPT mixers as their IDs aren't derived from hashing the name.
        # To find the mixer ID open the bnk in Wwiser. The id_to_replace is the 'ulID' at the top of the mixer.
    
        # Mixer IDs
        # The mixer ID seems to matter for non-vo audio (at least sometimes) e.g. when escaping from a movie the sound will continue unless the ID matches vanilla...
        (982557232, 659413513),     # Quest Battle Mixer
        (652848367, 848372985),     # Music Container
        (240250814, 698158058),     # Music Container
        (298137004, 1042256876),    # Music Container
        (683666133, 148962132),     # Music Container
        (989137633, 573597124),     # Movie Mixer


        # Audio Bus IDs
        ("replace_236083155", 236083155),       # Quest Battle 
        ("replace_3267614108", 3267614108),     # Music
        ("replace_3128400633", 3128400633),     # Music
        ("replace_3356399930", 3356399930),     # Music
        ("replace_3602921883", 3602921883),     # Movie

        # Game Parameter IDs
        ("replace_583154410", 583154410), # Game Parameter
    ]

################################# SCRIPT #################################

import struct
import os
import re

def get_byte_bits(byte):
    bits = []
    for i in range(8):
        bit = (byte >> i) & 1
        bits.append(bit)
        print(f"Bit {i}: {bit}")  # Print each bit as it's added to the list
    return bits

def get_bit(bits, position):
    if position < 0 or position >= len(bits):
        print("Invalid position")
        return "Invalid position"
    print(f"Bit at position {position}: {bits[position]}")
    return bits[position]

def compute_wwise_hash(name):
    lower = name.lower().strip()
    bytes_data = lower.encode('utf-8')

    hash_value = 2166136261
    for byte_index in range(len(bytes_data)):
        name_byte = bytes_data[byte_index]
        hash_value = (hash_value * 16777619) & 0xFFFFFFFF
        hash_value = hash_value ^ name_byte

    return hash_value

def replace_ids(ids, bnk_path):
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

            # Replace all instances of old ID with new ID
            content = content.replace(old_bytes, new_bytes)
            print("Where found, replaced ID: " + str(old_id) + " with " + str(new_id))

        with open(bnk_path, 'wb') as file:
            file.write(content)

# Gets wem files from the provided path so they can be scrambled.
def get_wem_ids():
    wem_ids = []
    files = os.listdir(wems_path)
    for file in files: 
        if "wem" in file:
            wem_id = re.sub('.wem', '', file)
            wem_ids.append(int(wem_id))

    print("wem_ids: " + str(wem_ids))
    return wem_ids

# Get the IDs of objects we don't want to scramble due to their significance e.g. event names in dat files or that their IDs are definitively replaced e.g. mixers.
def get_non_scramble_ids(bnk_path):
    object_ids = []
    with open(bnk_path, "rb") as file:
        # Header
        BKHD = file.read(4).decode('UTF-8')
        assert BKHD == "BKHD", "Invalid header in " + bnk_path
        dwChunkSize  = struct.unpack("<L", file.read(4))[0]
        file.read(dwChunkSize)
        HIRC = file.read(4).decode('UTF-8')
        assert HIRC == "HIRC", "Invalid header in " + bnk_path
        struct.unpack("<L", file.read(4))[0]
        numReleasableHircItem = struct.unpack("<L", file.read(4))[0]
        
        # Hirc items
        for _ in range(numReleasableHircItem):
            eHircType = struct.unpack("<b", file.read(1))[0]
            section_size = struct.unpack("<L", file.read(4))[0]
            ulID = struct.unpack("<L", file.read(4))[0]
            print("eHircType: " + str(eHircType))
            
            # If the object is not a mixer add it to the list
            if (eHircType != 4 and eHircType != 7 and eHircType != 12 and eHircType != 13): # 0x04 [Event], 0x07 [Actor-Mixer] = 7, 0x0C [Music Switch] = 12, 0x0D [Music Random Sequence] = 13 (can be found by viewing a bnk in wwiser)
                print("Adding ulID " + str(ulID) + " to object_ids")
                object_ids.append(ulID)
                
            # Skip ahead to next Hirc Item
            file.read(section_size - 4)
        
    return object_ids

# Scramble the IDs. This is necessary to prevent any conflicts arising.
def scramble_hirc_ids(bnk_path):
    object_ids = get_non_scramble_ids(bnk_path)    
    replacement_pairs = []
    for object_id in object_ids:
        new_id = compute_wwise_hash(os.path.splitext(os.path.basename(bnk_path))[0] + str(object_id))
        print("Renaming " + str(object_id) + " to " + str(new_id))
        replacement_pairs.append((object_id, new_id))

    replace_ids(replacement_pairs, bnk_path)

def scramble_wem_ids(bnk_path):
    wem_ids = get_wem_ids()
    replacement_pairs = []
    for wem_id in wem_ids:
        new_id = compute_wwise_hash(os.path.splitext(os.path.basename(bnk_path))[0] + str(wem_id))
        replacement_pairs.append((wem_id, new_id))
        print("Renaming " + str(wem_id) + " to " + str(new_id))
        os.rename(wems_path + str(wem_id) + ".wem", wems_path + str(new_id) + ".wem")

    replace_ids(replacement_pairs, bnk_path)

def patch_bnk(input_bnk_path, output_bnk_path):
    print("Correcting header of " + input_bnk_path)
    new_data = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) # Music data added in V136 bnks
    
    with open(output_bnk_path, "wb") as output_file:
        with open(input_bnk_path, "rb") as input_file:
            # Reading and rewriting header
            BKHD = input_file.read(4).decode('UTF-8')
            assert BKHD == "BKHD", "Invalid header in " + input_bnk_path
            BKHD_e = bytes(BKHD,"UTF-8")
            output_file.write(struct.pack("<%ds" % len(BKHD), BKHD_e))
        
            dwChunkSize  = struct.unpack("<L", input_file.read(4))[0]
            output_file.write(struct.pack("<L", dwChunkSize))
            
            dwBankGeneratorVersion = struct.unpack("<L", input_file.read(4))[0]
            if dwBankGeneratorVersion != 2147483784:
                dwBankGeneratorVersion = 2147483784
                print("Changed dwBankGeneratorVersion in header to " + str(dwBankGeneratorVersion))
            output_file.write(struct.pack("<L", dwBankGeneratorVersion))
            
            dwSoundBankID = struct.unpack("<L", input_file.read(4))[0]
            if dwSoundBankID != compute_wwise_hash(os.path.splitext(os.path.basename(output_bnk_path))[0]):
                dwSoundBankID = compute_wwise_hash(os.path.splitext(os.path.basename(output_bnk_path))[0])
                print("Changed dwSoundBankID in header to " + str(dwSoundBankID))
            output_file.write(struct.pack("<L", dwSoundBankID))

            dwLanguageID = struct.unpack("<L", input_file.read(4))[0]
            if dwLanguageID != 550298558 and make_language_english_uk == True:
                dwLanguageID = 550298558
                print("Changed dwLanguageID in header to " + str(dwLanguageID))
            output_file.write(struct.pack("<L", dwLanguageID))
            
            chunk = input_file.read(4)
            output_file.write(chunk)
            
            dwProjectID = struct.unpack("<L", input_file.read(4))[0]
            if dwProjectID != 2361:
                dwProjectID = 2361
                print("Changed dwProjectID in header to " + str(dwProjectID))
            output_file.write(struct.pack("<L", dwProjectID))
            
            chunk = input_file.read(4)
            output_file.write(chunk)
            
            HIRC = input_file.read(4).decode('UTF-8')
            assert HIRC == "HIRC", "Invalid header in " + input_bnk_path
            HIRC_e = bytes(HIRC,"UTF-8")
            output_file.write(struct.pack("<%ds" % len(HIRC), HIRC_e))
            
            hirc_dwChunkSize = struct.unpack("<L", input_file.read(4))[0]
            hirc_dwChunkSize_pos = output_file.tell()  # Remember the position of dwChunkSize in the output file
            print("hirc_dwChunkSize: " + str(hirc_dwChunkSize))
            output_file.write(struct.pack("<L", hirc_dwChunkSize))
            
            numReleasableHircItem = struct.unpack("<L", input_file.read(4))[0]
            print("numReleasableHircItem: " + str(numReleasableHircItem))
            output_file.write(struct.pack("<L", numReleasableHircItem))
            
            # Initialize a variable to track the total size increase for all HIRC items
            total_size_increase = 0
            hirc_item = 0

            # Reading and writing all HIRC items
            for _ in range(numReleasableHircItem):
                hirc_item += 1
                print("Reading and writing HIRC item: " + str(hirc_item))
                
                eHircType = struct.unpack("<b", input_file.read(1))[0]
                print("eHircType: " + str(eHircType))
                output_file.write(struct.pack("<b", eHircType))

                dwSectionSize = struct.unpack("<L", input_file.read(4))[0]
                dwSectionSize_pos = output_file.tell()  # Remember the position of dwChunkSize in the output file
                print("dwSectionSize: " + str(dwSectionSize))
                output_file.write(struct.pack("<L", dwSectionSize))

                ulID = struct.unpack("I", input_file.read(4))[0]
                print("ulID: " + str(ulID))
                output_file.write(struct.pack("<I",ulID))
                read_size = 4


                # Patch any Music Switch or Music Random Sequence Container objects if found.
                if eHircType == 12 or eHircType == 13:  # 0x0C [Music Switch] = 12, 0x0D [Music Random Sequence] = 13
                    print("Found Music Random Sequence Container " + str(ulID))
                    
                    uFlags = struct.unpack("<b", input_file.read(1))[0]
                    print("uFlags: " + str(uFlags))
                    output_file.write(struct.pack("<b", uFlags))

                    bIsOverrideParentFX = struct.unpack("<b", input_file.read(1))[0]
                    print("bIsOverrideParentFX: " + str(bIsOverrideParentFX))
                    output_file.write(struct.pack("<b", bIsOverrideParentFX))

                    uNumFx = struct.unpack("<b", input_file.read(1))[0]
                    print("uNumFx: " + str(uNumFx))
                    output_file.write(struct.pack("<b", uNumFx))

                    bOverrideAttachmentParams = struct.unpack("<b", input_file.read(1))[0]
                    print("bOverrideAttachmentParams: " + str(bOverrideAttachmentParams))
                    output_file.write(struct.pack("<b", bOverrideAttachmentParams))

                    overrideBusId = struct.unpack("<L", input_file.read(4))[0]
                    print("overrideBusId: " + str(overrideBusId))
                    output_file.write(struct.pack("<L", overrideBusId))

                    directParentID = struct.unpack("<L", input_file.read(4))[0]
                    print("directParentID: " + str(directParentID))
                    output_file.write(struct.pack("<L", directParentID))


                    byBitVector = struct.unpack("<b", input_file.read(1))[0]
                    print("byBitVector: " + str(byBitVector))
                    output_file.write(struct.pack("<b", byBitVector))

                    cProps = struct.unpack("<b", input_file.read(1))[0]
                    print("cProps:", cProps)
                    output_file.write(struct.pack("<b", cProps))
                    read_size += 14
                    
                    for _ in range(cProps):
                        pID = struct.unpack("<b", input_file.read(1))[0]
                        print("pID:", pID)
                        output_file.write(struct.pack("<b", pID))
                        read_size += 1
                        
                    for _ in range(cProps):    
                        pValue = struct.unpack("<f", input_file.read(4))[0]
                        print("pValue:", pValue)
                        output_file.write(struct.pack("<f", pValue))
                        read_size += 4

                    cProps = struct.unpack("<b", input_file.read(1))[0]
                    print("cProps:", cProps)
                    output_file.write(struct.pack("<b", cProps))
                    read_size += 1
                    
                    for _ in range(cProps):
                        pID = struct.unpack("<b", input_file.read(1))[0]
                        print("pID:", pID)
                        output_file.write(struct.pack("<b", pID))
                        read_size += 1
                        
                    for _ in range(cProps):    
                        pValue = struct.unpack("<f", input_file.read(4))[0]
                        print("pValue:", pValue)
                        output_file.write(struct.pack("<f", pValue))
                        read_size += 4

                    # PositioningParams
                    uBitsPositioning = struct.unpack("<b", input_file.read(1))[0]
                    print("uBitsPositioning:", uBitsPositioning)
                    output_file.write(struct.pack("<b", uBitsPositioning))
                    read_size += 1

                    if uBitsPositioning != 0:
                        some_other_positioning_stuff = struct.unpack("<b", input_file.read(1))[0] # e.g. uBits3d
                        print("some_other_positioning_stuff:", some_other_positioning_stuff)
                        output_file.write(struct.pack("<b", some_other_positioning_stuff))
                        read_size += 1
                    
                    # AuxParams
                    byBitVector = struct.unpack("<b", input_file.read(1))[0]
                    print("byBitVector:", byBitVector)
                    output_file.write(struct.pack("<b", byBitVector))
                    read_size += 1

                    if get_bit(get_byte_bits(byBitVector), 3) == 1:
                        auxID1 = struct.unpack("<L", input_file.read(4))[0]
                        print("auxID1: " + str(auxID1))
                        output_file.write(struct.pack("<L", auxID1))

                        auxID2 = struct.unpack("<L", input_file.read(4))[0]
                        print("auxID2: " + str(auxID2))
                        output_file.write(struct.pack("<L", auxID2))

                        auxID3 = struct.unpack("<L", input_file.read(4))[0]
                        print("auxID3: " + str(auxID3))
                        output_file.write(struct.pack("<L", auxID3))

                        auxID4 = struct.unpack("<L", input_file.read(4))[0]
                        print("auxID4: " + str(auxID4))
                        output_file.write(struct.pack("<L", auxID4))
                        read_size += 16
                        
                    reflectionsAuxBus = struct.unpack("<L", input_file.read(4))[0]
                    print("reflectionsAuxBus: " + str(reflectionsAuxBus))
                    output_file.write(struct.pack("<L", reflectionsAuxBus))
                    read_size += 4

                    # AdvSettingsParams
                    byBitVector = struct.unpack("<b", input_file.read(1))[0]
                    print("byBitVector:", byBitVector)
                    output_file.write(struct.pack("<b", byBitVector))

                    eVirtualQueueBehavior = struct.unpack("<b", input_file.read(1))[0]
                    print("eVirtualQueueBehavior:", eVirtualQueueBehavior)
                    output_file.write(struct.pack("<b", eVirtualQueueBehavior))
                    
                    u16MaxNumInstance = struct.unpack("<H", input_file.read(2))[0]
                    print("u16MaxNumInstance:", u16MaxNumInstance)
                    output_file.write(struct.pack("<H", u16MaxNumInstance))
                    
                    eBelowThresholdBehavior = struct.unpack("<b", input_file.read(1))[0]
                    print("eBelowThresholdBehavior:", eBelowThresholdBehavior)
                    output_file.write(struct.pack("<b", eBelowThresholdBehavior))
                    
                    byBitVector = struct.unpack("<b", input_file.read(1))[0]
                    print("byBitVector:", byBitVector)
                    output_file.write(struct.pack("<b", byBitVector))
                    read_size += 6

                    ## StateChunk
                    ulNumStateProps = struct.unpack("<b", input_file.read(1))[0]
                    print("ulNumStateProps:", ulNumStateProps)
                    output_file.write(struct.pack("<b", ulNumStateProps))
                    
                    ulNumStateGroups = struct.unpack("<b", input_file.read(1))[0]
                    print("ulNumStateGroups:", ulNumStateGroups)
                    output_file.write(struct.pack("<b", ulNumStateGroups))
                    read_size += 2

                    # InitialRTPC
                    ulNumRTPC = struct.unpack("<H", input_file.read(2))[0]
                    print("ulNumRTPC:", ulNumRTPC)
                    output_file.write(struct.pack("<H", ulNumRTPC))
                    read_size += 2

                    # Children    
                    ulNumChilds = struct.unpack("<L", input_file.read(4))[0]
                    print("ulNumChilds: " + str(ulNumChilds))
                    output_file.write(struct.pack("<L", ulNumChilds))
                    read_size += 4

                    for _ in range(ulNumChilds):                    
                        ulChildID = struct.unpack("<L", input_file.read(4))[0]
                        print("ulChildID: " + str(ulChildID))
                        output_file.write(struct.pack("<L", ulChildID))
                        read_size += 4

                    # AkMeterInfo
                    fGridPeriod = struct.unpack("<d", input_file.read(8))[0]
                    print("fGridPeriod: " + str(fGridPeriod))
                    output_file.write(struct.pack("<d", fGridPeriod))
                    
                    fGridOffset = struct.unpack("<d", input_file.read(8))[0]
                    print("fGridOffset: " + str(fGridOffset))
                    output_file.write(struct.pack("<d", fGridOffset))
                    
                    fTempo = struct.unpack("<f", input_file.read(4))[0]
                    print("fTempo: " + str(fTempo))
                    output_file.write(struct.pack("<f", fTempo))
                    
                    uTimeSigNumBeatsBar = struct.unpack("<b", input_file.read(1))[0]
                    print("uTimeSigNumBeatsBar:", uTimeSigNumBeatsBar)
                    output_file.write(struct.pack("<b", uTimeSigNumBeatsBar))
                    
                    uTimeSigBeatValue = struct.unpack("<b", input_file.read(1))[0]
                    print("uTimeSigBeatValue:", uTimeSigBeatValue)
                    output_file.write(struct.pack("<b", uTimeSigBeatValue))
                    
                    bMeterInfoFlag = struct.unpack("<b", input_file.read(1))[0]
                    print("bMeterInfoFlag:", bMeterInfoFlag)
                    output_file.write(struct.pack("<b", bMeterInfoFlag))
                    
                    numStingers = struct.unpack("<L", input_file.read(4))[0] # Might have to do something with this it appears to be a list, but current examples have 0 items in the list
                    print("numStingers: " + str(numStingers)) 
                    output_file.write(struct.pack("<L", numStingers))
                    
                    numRules = struct.unpack("<L", input_file.read(4))[0]
                    print("numRules: " + str(numRules)) 
                    output_file.write(struct.pack("<L", numRules))
                    read_size += 31

                    for _ in range(numRules):   
                        # AkMusicTransitionRule
                        uNumSrc = struct.unpack("<L", input_file.read(4))[0]
                        print("uNumSrc: " + str(uNumSrc)) 
                        output_file.write(struct.pack("<L", uNumSrc))
                        
                        srcID = struct.unpack("<i", input_file.read(4))[0]
                        print("srcID: " + str(srcID)) 
                        output_file.write(struct.pack("<i", srcID))
                        
                        uNumDst = struct.unpack("<L", input_file.read(4))[0]
                        print("uNumDst: " + str(uNumDst)) 
                        output_file.write(struct.pack("<L", uNumDst))
                        
                        dstID = struct.unpack("<i", input_file.read(4))[0]
                        print("dstID: " + str(dstID)) 
                        output_file.write(struct.pack("<i", dstID))
                        read_size += 16

                        # AkMusicTransSrcRule
                        transitionTime = struct.unpack("<i", input_file.read(4))[0]
                        print("transitionTime: " + str(transitionTime)) 
                        output_file.write(struct.pack("<i", transitionTime))
                        
                        eFadeCurve = struct.unpack("<L", input_file.read(4))[0]
                        print("eFadeCurve: " + str(eFadeCurve)) 
                        output_file.write(struct.pack("<L", eFadeCurve))
                        
                        iFadeOffset = struct.unpack("<i", input_file.read(4))[0]
                        print("iFadeOffset: " + str(iFadeOffset)) 
                        output_file.write(struct.pack("<i", iFadeOffset))
                        
                        eSyncType = struct.unpack("<L", input_file.read(4))[0]
                        print("eSyncType: " + str(eSyncType)) 
                        output_file.write(struct.pack("<L", eSyncType))
                        
                        uCueFilterHash = struct.unpack("<L", input_file.read(4))[0]
                        print("uCueFilterHash: " + str(uCueFilterHash)) 
                        output_file.write(struct.pack("<L", uCueFilterHash))
                        
                        bPlayPostExit = struct.unpack("<b", input_file.read(1))[0]
                        print("bPlayPostExit: " + str(bPlayPostExit)) 
                        output_file.write(struct.pack("<b", bPlayPostExit))
                        read_size += 21

                        # AkMusicTransDstRule
                        transitionTime = struct.unpack("<i", input_file.read(4))[0]
                        print("transitionTime: " + str(transitionTime)) 
                        output_file.write(struct.pack("<i", transitionTime))
                        
                        eFadeCurve = struct.unpack("<L", input_file.read(4))[0]
                        print("eFadeCurve: " + str(eFadeCurve)) 
                        output_file.write(struct.pack("<L", eFadeCurve))
                        
                        iFadeOffset = struct.unpack("<i", input_file.read(4))[0]
                        print("iFadeOffset: " + str(iFadeOffset)) 
                        output_file.write(struct.pack("<i", iFadeOffset))
                        
                        uCueFilterHash = struct.unpack("<L", input_file.read(4))[0]
                        print("uCueFilterHash: " + str(uCueFilterHash)) 
                        output_file.write(struct.pack("<L", uCueFilterHash))
                        
                        uJumpToID = struct.unpack("<L", input_file.read(4))[0]
                        print("uJumpToID:", uJumpToID)
                        output_file.write(struct.pack("<L", uJumpToID))
                        
                        eJumpToType = struct.unpack("<H", input_file.read(2))[0]
                        print("eJumpToType:", eJumpToType)
                        output_file.write(struct.pack("<H", eJumpToType))
                        
                        eEntryType = struct.unpack("<H", input_file.read(2))[0] 
                        print("eEntryType:", eEntryType)
                        output_file.write(struct.pack("<H", eEntryType))
                        
                        bPlayPreEntry = struct.unpack("<b", input_file.read(1))[0]
                        print("bPlayPreEntry: " + str(bPlayPreEntry))  
                        output_file.write(struct.pack("<b", bPlayPreEntry))
                        
                        bDestMatchSourceCueName = struct.unpack("<b", input_file.read(1))[0]
                        print("bDestMatchSourceCueName: " + str(bDestMatchSourceCueName)) 
                        output_file.write(struct.pack("<b", bDestMatchSourceCueName))
                        read_size += 26

                        # This the v136 stuff we've been after! 
                        allocTransObjectFlag = struct.unpack("<b", input_file.read(1))[0]
                        print("allocTransObjectFlag: " + str(allocTransObjectFlag)) 
                        output_file.write(struct.pack("<b", allocTransObjectFlag))
                        read_size += 1

                        # Adds the new data in.
                        output_file.write(new_data) 
                        total_size_increase += len(new_data)
                        print("total size increase at this point is: " + str(total_size_increase))

                    # Calculate remaining size and read the rest of the HIRC item
                    remaining_size = dwSectionSize - read_size
                    if remaining_size > 0:
                        print("Writing rest_of_hirc bytes: " + str(remaining_size))
                        rest_of_hirc = input_file.read(remaining_size)
                        output_file.write(rest_of_hirc)

                        # Update dwSectionSize with size of new data added
                        dwSectionSize += len(new_data)
                        output_file.seek(dwSectionSize_pos)
                        output_file.write(struct.pack("<L", dwSectionSize))
                        output_file.seek(0, os.SEEK_END)
                        
                    else:
                        print("No more data to read for this HIRC item.")
                        break

                else:
                    print("This is not the hirc_type you're looking for...")
                    chunk = input_file.read(dwSectionSize - 4)
                    output_file.write(chunk)
            
            # Update dwChunkSize with size of new data added
            hirc_dwChunkSize += total_size_increase
            output_file.seek(hirc_dwChunkSize_pos)
            print("New hirc_dwChunkSize is: " + str(hirc_dwChunkSize))
            output_file.write(struct.pack("<L", hirc_dwChunkSize))

for i in range(len(bnk_paths)):
    input_bnk = bnk_paths[i]['input_bnk']
    output_bnk = bnk_paths[i]['output_bnk']
    print("### Correcting header and replacing IDs for " + str(input_bnk))
    patch_bnk(input_bnk, output_bnk)
    replace_ids(ids_to_replace, output_bnk)
    scramble_hirc_ids(output_bnk)
    if scramble_wems == True:
        scramble_wem_ids(output_bnk)
    print("### New bnk output to " + str(output_bnk))

#Whether it's read(1), read(2), or read(4) etc. corresponds to how many bytes that offset contains.
# e.g. viewing the bnk in wwiser, we can see that the CAkMusicRanSeqCntr has this top section
# 0000011a          u8  eHircType           0x0D [Music Random Sequence]
# 0000011b          u32 dwSectionSize       0xE5
# 0000011f          sid ulID                652848367
                    # 00000123          u8 uFlags           0x06

# The u8 means 1 byte, as there are 8 bits in a byte. So 0x0D is 1 byte.
# Below that it says u32, that means there are 4 bytes, as 4 * 8 is 32. So 0xE5 is 4 bytes.
# sid is slightly different, in practice that is also 4 bytes, but to tell that you can go to the offset 0000011f.
# Then go to the next offset 00000123. Count the pairs between the 2 offsets. There are 4. That means there are 4 bytes.

# "<b" = u8             (1 byte)
# "<H" = u16            (2 bytes)
# "<L" = u32 / tid      (4 bytes) unsigned 32-bit integer (positive numbers)
# "<I" = s32 / sid      (4 bytes) signed 32-bit integer (positive and negative numbers)
# "<f" = f32            (4 bytes)
# "<d" = d64            (8 bytes)