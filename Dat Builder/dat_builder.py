# Add your events to the list.
project_file_example = {
    "Events": [
        "Play_example_event_goes_here_01"
    ],
    "BnkName": "global_movies_test"
}

# Put the path for your dat file here.
output_path = "C:/Users/george/Downloads/"

import struct
import io

class SoundDatFile:
    def __init__(self):
        self.Event0 = []
        self.EnumGroup0 = []
        self.EnumGroup1 = []
        self.VoiceEvents = []
        self.SettingValues = []
        self.Unknown = []

    class EventWithValue:
        def __init__(self, event_name, value):
            self.EventName = event_name
            self.Value = value

def get_as_byte_array(dat_file):
    mem_stream = io.BytesIO()

    # Event0
    mem_stream.write(struct.pack('<I', len(dat_file.Event0)))
    for event in dat_file.Event0:
        mem_stream.write(write_str32(event.EventName))
        mem_stream.write(struct.pack('<f', event.Value))

    # EnumGroup0
    mem_stream.write(struct.pack('<I', len(dat_file.EnumGroup0)))
    for enum in dat_file.EnumGroup0:
        mem_stream.write(write_str32(enum.EnumName))
        mem_stream.write(struct.pack('<I', len(enum.EnumValues)))
        for enum_value in enum.EnumValues:
            mem_stream.write(write_str32(enum_value))

    # EnumGroup1
    mem_stream.write(struct.pack('<I', len(dat_file.EnumGroup1)))
    for enum in dat_file.EnumGroup1:
        mem_stream.write(write_str32(enum.EnumName))
        mem_stream.write(struct.pack('<I', len(enum.EnumValues)))
        for enum_value in enum.EnumValues:
            mem_stream.write(write_str32(enum_value))

    # VoiceEvents
    mem_stream.write(struct.pack('<I', len(dat_file.VoiceEvents)))
    for event in dat_file.VoiceEvents:
        mem_stream.write(write_str32(event.EventName))
        mem_stream.write(struct.pack('<I', len(event.Values)))
        for value in event.Values:
            mem_stream.write(struct.pack('<I', value))

    # SettingValues
    mem_stream.write(struct.pack('<I', len(dat_file.SettingValues)))
    for value in dat_file.SettingValues:
        mem_stream.write(write_str32(value.EventName))
        mem_stream.write(struct.pack('<f', value.MinValue))
        mem_stream.write(struct.pack('<f', value.MaxValue))

    # Unknown
    mem_stream.write(struct.pack('<I', len(dat_file.Unknown)))
    for value in dat_file.Unknown:
        mem_stream.write(write_str32(value))

    return mem_stream.getvalue()

def read_str32(chunk):
    # Implementation for reading a string from the byte chunk.
    str_length = struct.unpack('<I', chunk.read(4))[0]
    return chunk.read(str_length).decode('utf-8')

def write_str32(string):
    # Implementation for writing a string to a byte array.
    encoded_str = string.encode('utf-8')
    return struct.pack('<I', len(encoded_str)) + encoded_str

def build_dat(project_file):
    output_name = f"event_data__{project_file['BnkName']}.dat"
    dat_file = SoundDatFile()

    for wwise_event in project_file['Events']:
        dat_file.Event0.append(SoundDatFile.EventWithValue(wwise_event, 400))

    bytes_data = get_as_byte_array(dat_file)
    # You would replace '/path/to/your/output' with the actual path where you want the file saved
    with open(f"{output_path}{output_name}", 'wb') as file:
        file.write(bytes_data)

    return output_name

output_file = build_dat(project_file_example)
print(f"File saved as: {output_file}")
