import struct
import json


class Package():
    def pack_header(self, header):
        '''
        parameter: 
            header: a dic which contain the infomation
        fuction: 
            pack the header
        return:
            the packed package which is encode in byte
        '''
        header_json = json.dumps(header)
        header_json_byte = header_json.encode('utf-8')
        header_len = len(header_json_byte)
        header_struct = struct.pack('i', header_len)
        return header_struct + header_json_byte

    def pack_message(self, header, message):
        '''
        parameter: 
            header: a dic which contain the infomation
                    can not have key is message_length
            message: string in utf-8
        fuction: 
            pack the header
        return:
            the packed package which is encode in byte
        '''
        if type(message) == type(b''):
            header['message_length'] = len(message)
        elif type(message) == type(''):
            message = message.encode('utf-8')
            header['message_length'] = len(message)
        elif type(message) == type({}):
            message_json = json.dumps(message)
            message_json_byte = message_json.encode('utf-8')
            header['message_length'] = len(message_json_byte)
            message = message_json_byte
        header_info = self.pack_header(header)
        return header_info + message.encode('utf-8')

    def unpack_header_size(self, size_struct):
        return struct.unpack('i', size_struct)[0]

    def unpack_header(self, header_byte):
        '''
        parameter: 
            header_byte: the byte of header
        fuction: 
            unpack the header
        return:
            dic of header
        '''
        return json.loads(header_byte.decode('utf-8'))

    def unpack_message(self,message,mode):
        if mode == 'utf-8':
            

