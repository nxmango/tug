# Slightly modified by nxmango from https://github.com/Adubbz/Tinfoil/blob/master/tools/usb_install_pc.py

import struct

CMD_ID_EXIT = 0
CMD_ID_FILE_RANGE = 1
CMD_TYPE_RESPONSE = 1

def send_response_header(out_ep, cmd_id, data_size):
    out_ep.write(b'TUC0')  # Tinfoil USB Command 0
    out_ep.write(struct.pack('<B', CMD_TYPE_RESPONSE))
    out_ep.write(b'\x00' * 3)
    out_ep.write(struct.pack('<I', cmd_id))
    out_ep.write(struct.pack('<Q', data_size))
    out_ep.write(b'\x00' * 0xC)

def file_range_cmd(nsp_dir, in_ep, out_ep, data_size):
    file_range_header = in_ep.read(0x20)

    range_size = struct.unpack('<Q', file_range_header[:8])[0]
    range_offset = struct.unpack('<Q', file_range_header[8:16])[0]
    nsp_name_len = struct.unpack('<Q', file_range_header[16:24])[0]
    nsp_name = bytes(in_ep.read(nsp_name_len)).decode('utf-8')

    send_response_header(out_ep, CMD_ID_FILE_RANGE, range_size)

    with open(nsp_name, 'rb') as f:
        f.seek(range_offset)
        curr_off = 0x0
        end_off = range_size
        read_size = 0x800000
        while curr_off < end_off:
            if curr_off + read_size >= end_off:
                read_size = end_off - curr_off
            buf = f.read(read_size)
            out_ep.write(data=buf, timeout=0)
            curr_off += read_size

def poll_commands(nsp_dir, in_ep, out_ep):
    while True:
        cmd_header = bytes(in_ep.read(0x20, timeout=0))
        magic = cmd_header[:4]

        if magic != b'TUC0':  # Tinfoil USB Command 0
            continue
        cmd_id = struct.unpack('<I', cmd_header[8:12])[0]
        data_size = struct.unpack('<Q', cmd_header[12:20])[0]

        if cmd_id == CMD_ID_EXIT:
            break
        elif cmd_id == CMD_ID_FILE_RANGE:
            file_range_cmd(nsp_dir, in_ep, out_ep, data_size)

def send_nsp_list(nsp_dir, out_ep):
    nsp_path_list = list()
    nsp_path_list_len = 0

    # Add all files with the extension .nsp in the provided dir
    for nsp_path in [f for f in nsp_dir.iterdir() if f.is_file() and f.suffix == '.nsp']:
        nsp_path_list.append(nsp_path.__str__() + '\n')
        nsp_path_list_len += len(nsp_path.__str__()) + 1

    out_ep.write(b'TUL0')  # Tinfoil USB List 0
    out_ep.write(struct.pack('<I', nsp_path_list_len))
    out_ep.write(b'\x00' * 0x8)  # Padding

    for nsp_path in nsp_path_list:
        out_ep.write(nsp_path)
