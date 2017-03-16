import sys
sys.path.insert(0, r'G:\app')

class CFrameInfo(object):
    def __init__(self):
        self.byte_width = 2
        self.frame_header = [16383, 515,515, 0, 16383, 515,515, 0]
        self.header_length = len(self.frame_header)
        self.frame_row = 8
        self.frame_col = 640
        self.frame_length = self.frame_row * self.frame_col
        self.frame_length_with_header = self.frame_length + self.header_length
    def set_frame_header(self, header):
        self.frame_header = header
