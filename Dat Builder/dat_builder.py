# Put the path for your dat file here.
dat_path= "C:/path/to/your/example.dat"

# Add your events to the list.
events = [
    "Play_example_event_goes_here_01",
    "Play_example_event_goes_here_02",
    # Add more strings as needed.
]

def create_dat_file(strings_to_add, dat_path):
    # Create the binary data.
    header = bytearray(b"\x25\x00\x00\x00")
    data = header

    for string in strings_to_add:
        length = len(string).to_bytes(4, byteorder='little') # Length of the current string.
        utf8_string = string.encode('utf-8') # Current string encoded in utf-8.
        padding = bytearray(b"\x00\x00\xc8\x43")  # 00 00 C8 43

        data += length  
        data += utf8_string  
        data += padding

    footer = bytearray(b"\x00\x00\x00\x00") * 5 
    data += footer

    # Write the data to a DAT file.
    with open(dat_path, "wb") as file:
        file.write(data)

    print(f"Woo dat file '{dat_path}' created successfully.")

create_dat_file(events, dat_path)