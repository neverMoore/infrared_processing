import sys
sys.path.insert(0, r'G:\app')
import numpy as np
from CFrame import CFrameInfo

class CRawDataParser(object):
    def __init__(self, file_name = [],frame_info = []):
        self.file_name = file_name
        self.frame_header = frame_info.header
        self.frame_length = frame_info.frame_length_with_header # 完整的一帧数据长度
        self.frame_row = frame_info.frame_row
        self.frame_col = frame_info.frame_col
        self.total_frames = 0
    def __KMP__(self, text, pattern):
        '''
        KMP 算法，用来查找帧头。
        '''
        pattern = list(pattern)
        length = len(pattern)
        shifts = [1] * (length + 1)
        shift = 1
        for pos, pat in enumerate(pattern):
            while shift <= pos and pat != pattern[pos-shift]:
                shift += shifts[pos-shift]
            shifts[pos+1] = shift
        start_pos = 0
        match_len = 0
        for c in text:
            while match_len == length or match_len >= 0 and pattern[match_len] != c:
                start_pos += shifts[match_len]
                match_len -= shifts[match_len]
            match_len += 1
            if match_len == length:
                yield start_pos
    def __get_file_info(self):
        '''
        用来获取文件的大小，总帧数，第一帧的起始位置等信息
        '''
        try:
            fobj = open(self.file_name, 'rb')
        except Exception as e:
            print('can not open the file' + self.name)
            print(e)
            return
        
        flag_pos_a = fobj.tell()
        fobj.seek(os.SEEK_SET, os.SEEK_END)
        flag_pos_b = fobj.tell()
        fobj.seek(os.SEEK_SET, flag_pos_a) # set to the begin of opened file.
        self.data_size = flag_pos_b - flag_pos_a
#        print('pos flag')
        frame = CFrameInfo()
#        print(flag_pos_a, flag_pos_b, flag_pos_b/(frame.data_byte * frame.length),fobj.tell())
        
        self.total_frames = int(np.floor(self.data_size/(frame.data_byte * frame.frame_with_header_length)))
        # read the file of 2 frame_size length
        
#        fobj.seek(where) # read from where
        
        bit_to_be_read = frame.data_byte * frame.frame_with_header_length *2
        try:
            raw_data = fobj.read(bit_to_be_read)
            if len(raw_data) < bit_to_be_read:
                fobj.close()
                raise ReadFileERROR('Not having enough bits of the reading file !')
        except ReadFileERROR as e:
            print (e.error_info)
            raise
            
#        global data_stream
        data_stream = [(a << 8) + b for a,b in zip(raw_data[0::2], raw_data[1::2])]
#        print(len(raw_data), len(data_stream))
#        zstr1 = str(raw_data)
        pos = [a*2 for a in self.__KMP__(data_stream, frame.header)]
#        print('begin_pos = %d', pos)
#        print(data_stream[int(pos[0]/2):int(pos[0]/2)+8])
#        print(data_stream[int(pos[1]/2):int(pos[1]/2)+8])
        self.first_frame_pos = int(pos[0])
        fobj.close()
    def __get_data(self, frames2read = 2, frames_offset = 0, flag = True):
        '''
        从指定的位置(frame_offset)开始读取 frames2read 帧的数据，flag 用来指示返回的数据格式。返回的数据不包含帧头。
        若 flag == True, 则表示返回的 frames2read 帧的数据，
        flag == False 返回的的是 frames2read 帧的平均值。
        '''
        frames_info = CFrameInfo()
        where = frame_offset * frames_info.frame_length
        try:
            fobj = open(self.file_name, where)
        except Exception as e:
            print('Can not open the file' = self.file_name)
            print(e)
            raise
        fobj.seek(self.first_frame_pos + where) # 读取文件的起始位置
        # 判断能否读取所给定的的帧数，如果不能，则读取文件从给定位置到结束的所有帧，并返回读取内容和帧数
        if frames2read + frame_offset > self.total_frames:
            frames2read = self.total_frames - frame_offset
        else:
             frames2read = frames2read
        bytes2read = int(frames2read * self.frame_length)
        try:
            raw_data = fobj.read(bytes2read)
        except Exception as e:
            print(e)
            raise
        fobj.close()

        # 数据调整
        data_stream = [(a << 8) + b for a,b in zip(bytes2read[0::2], bytes2read[1::2])]
        pos = [ a for a in self.__KMP__(data_stream, frames_info.header) ] # pos 保存 data_stream 中每帧的起始位置
        data = np.zeros( (frames_info.frames_length, frames2read) )
        for index in range(frames2read):
            pos_begin = pos[index] + frames_info.header_length
            pos_end = pos_begin + frames_info.frames_length
            data[:, index] = data_stream[pos_begin:pos_end]
        if flag:
            return data, frames2read
        else:
            template_sum = np.ones((frames2read,1)) # 列矩阵，用来对 data 的每行 进行求和。
            mean_value = np.zeros((bkg_data.shape[0],1), dtype = 'float32')
            mean_value = np.dot( data, template_sum )
            mean_value = mean_value / frames2read
            return sum_data
            
    def set_file_name(self, file_name):
        self.file_name = file_name
    def set_frame_name(self, header):
        self.frame_header = header

if __name__ == '__main__':
    parser = CRawDataParser()
    parser.set_file_name('G\app\123.dat')
    total_frames = parser.total_frames
    