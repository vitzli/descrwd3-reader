#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#
# Descr.WD3 reader in python, uses python 3
# Descr.WD3 file are made by Metaproducts Offline Explorer
#

import struct
import sys
import os.path

def _parse_mp_date(date_string):
    pass

def _read_wd3_buf(buf):
    
    """a: Total record size: 4 bytes (signed integer)
    b: File name record size: 4 bytes (signed integer)
    c: URL record size: 4 bytes (signed integer, unused, always zero
    d: File name as on disk: b bytes (text)
    e: URL name: c bytes (text, zero length)
    f: Version: 4 bytes (signed integer?)
    g: Modification date: 31 byte, g[0]: length of the actual
       string in the following 30 bytes (byte+text)
    h: MIME type: 36 bytes, g[0]: length of the actual string,
       following 35 bytes are a text string (byte+text),
       of which only g[0] matter 
    i: Original file length before parsing: 4 bytes (signed integer)
    j: NeedPrimary: 1 byte, 0 if Primary is needed, 1 - if not
    """
    out = dict()
    x = buf.read(12)
    
    if len(x) != 12:
        raise IOError
    
    data_size, fn_size, url_size  = struct.unpack('<iii', x)
    
    if url_size != 0:
        raise IOError
    
    filename = buf.read(fn_size).decode(encoding='ascii')
    version= struct.unpack('i', buf.read(4))[0]
    
    f_date_length=struct.unpack('b', buf.read(1))
    f_date_data=buf.read(30)
    
    modification_date = f_date_data[0:f_date_length[0]].decode(encoding='ascii')
    if modification_date is '':
        modification_date = None
    
    f_mime_length=struct.unpack('b', buf.read(1))
    f_mime_data=buf.read(35)
    
    mime_type = f_mime_data[0:f_mime_length[0]].decode(encoding='ascii')
    
    file_size = struct.unpack('i', buf.read(4))[0]
    
    need_primary = True if struct.unpack('b', buf.read(1))[0]==0 else False
    
    return data_size, (filename, mime_type, file_size, modification_date)

def read_wd3_file(file_object):
    out = []
    pos = 0
    while True:
        try:
            k = _read_wd3_buf(fp)
            out.append(k[1])
            n = k[0]
            pos += n
            fp.peek(pos)
        except IOError:
            break
    
    return out    

if __name__=='__main__':
    if len(sys.argv) == 1:
        print('Usage: descrwd3-reader.py FILENAME')
        sys.exit(1)

    file_path = sys.argv[1]
        
    if os.path.isfile(file_path):
        fp = open(file_path, mode='rb')
        parsed_wd3 = read_wd3_file(fp)
        for line in parsed_wd3:
            print("\t".join(map(str, line)))
        fp.close()
    else:
        print('File does not exist', file=sys.stderr)
        sys.exit(1)

    sys.exit(1)