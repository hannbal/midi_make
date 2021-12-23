# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 16:22:27 2021

@author: tony
"""


#https://mido.readthedocs.io/en/latest/官方文档
#https://zhuanlan.zhihu.com/p/384830252 乐器列表加一些说明
#https://blog.csdn.net/qq_41556318/article/details/86304765 在这里找到了mixer 混音使用方法


from mido import Message,MidiFile,MidiTrack
from pygame import mixer

class my_tracks:
    def __init__(self):
        self.mid =MidiFile()
        self.track =[]

        self.filepath=''
        
    #添加音符    
    def add_messages(self,message_type,message_value,start_time,end_time,velocity,channel):
        if message_type=='program_change':
            #选择声音的种类
            self.track[channel].append(Message(message_type,program = message_value,time=0,channel = channel))
        elif message_type=='note':
            #添加音符
            self.track[channel].append(Message('note_on',note = message_value,time=start_time,channel = channel,velocity=velocity))
            self.track[channel].append(Message('note_off',note = message_value,time=end_time,channel = channel,velocity=velocity))
    
    #mid对象添加track对象
    def track_to_mid(self):
        for x in self.track:
            self.mid.tracks.append(x)
        
    
    #保存midi文件
    def mid_save(self,file_name):
        self.mid.save(file_name)
        self.filepath = file_name
    
    #用mixer运行midi文件
    def mixer_play(self):
        mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        mixer.music.load(self.filepath)
        mixer.music.play()
    
    #打印midi文件内容    
    def print_track(self):
        print(self.mid)

#一分钟节拍转换为豪秒
class my_beats:
    
    def __init__(self,bpm):
        self.beat = 1000*60/bpm      
    def set_beat(self,bpm):
        self.beat= 1000*60/bpm

class voice():
    def __init__(self):
        self.data = {'do':60,'ra':61,'mi':62,'fa':63,'so':64,'la':65,"xi":66,"do'":67,
                     '1':60,'2':61,'3':62,'4':63,'5':64,'6':65,"7":66,"1'":67,"2'":68,"3'":69,"4'":70,"5'":71,"6'":72}
    
    def get_voice(self,shengdiao,yinfu):
        try:
            if shengdiao.upper() in 'CDEFGAB':
                change = 'CDEFGAB'.index(shengdiao.upper())
                return (self.data[yinfu]+change)
            else:
                raise ValueError('音调错误')
        except Exception as e:
            return e
        
def make_midi(my_track,bpm,myprogram,mylist,shengdiao,velocity,channel):
    '''传人my_track 对象，音乐的速度，myprogram 乐器类型（可填0-127），mylist 乐谱，shengdiao 声调，velocity 音量，channel 声道，filepath 生成的midi文件地址'''
    #定义一分钟多少节拍
    beats = my_beats(bpm)
    
    my_voice = voice()
    
    # print(my_beats.beat,type(my_beats.beat))
    track = MidiTrack()
    if len(my_track.track) > channel:
        my_track.track[channel] = track
    else:
        my_track.track.append(track)
    my_track.add_messages("program_change",  myprogram, 0, 0,0,channel)
 
    start_time =0
    for track in mylist:
        temp = my_voice.get_voice(shengdiao,track[0])
        my_track.add_messages("note", temp, 0,int(beats.beat/track[1]),velocity, channel)
        start_time +=int(beats.beat/track[1])
    my_track.track_to_mid()
    my_track.print_track()

if __name__ == "__main__":

####直接使用
    mid =MidiFile()
    
    #创建两个音轨对象
    track1 = MidiTrack()
    track2 = MidiTrack()
    
    #配置乐器
    track1.append(Message('program_change',program = 0,time=0,channel = 0))
    #note_on 与note_off组成一个音
    track1.append(Message('note_on',channel=0,note=63,velocity=64,time=0))
    track1.append(Message('note_off',channel=0,note=63,velocity=64,time=480))
    
    track1.append(Message('note_on',channel=0,note=63,velocity=64,time=480))
    track1.append(Message('note_off',channel=0,note=63,velocity=64,time=480))

    track2.append(Message('program_change',program = 30,time=0,channel = 2))
    track2.append(Message('note_on',channel=2,note=60,velocity=64,time=0))
    track2.append(Message('note_off',channel=2,note=60,velocity=64,time=480))

    track2.append(Message('note_on',channel=2,note=60,velocity=64,time=480))
    track2.append(Message('note_off',channel=2,note=60,velocity=64,time=480))
    
    #把两个音轨加入mid对象
    mid.tracks.append(track1)
    mid.tracks.append(track2)
    print(mid)
    
    mid.save('D://test1.mid')
    #mixer的初始化，channels选择2 可以混音播放
    mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    mixer.music.load('D://test1.mid')
    mixer.music.play()
    

#######    同一个旋律多少部播放
   #  my_track1 = my_tracks()
    
    
   # # track_list 是乐谱
   #  track_list=[['do',1],["la",1],["la",4],["la",.5],['do',1],["do'",1],['so',4],["la",1]]
    
   #  #生成音轨，可以生成多个音轨 ，
   #  make_midi(my_track1,80,102,track_list,'c',50,0)
   #  make_midi(my_track1,80,0,track_list,'f',50,1)
   #  make_midi(my_track1,80,46,track_list,'a',60,2)
    
   #  my_track1.mid_save('D://test1.mid')
   #  my_track1.mixer_play()
    
    
 # ####同一首歌的两个旋律合并播放   
 #    my_track2 = my_track()
 #    track_list2=[["3'",2],["2'",2],["1'",2],["3'",1],
 #                  ["2'",2],["1'",2],["3'",1],
 #                  ["2'",2],["1'",2],["3'",1],
 #                  ["2'",2],["1'",2],["3'",1],
 #                  ["2'",2],["2'",2],["2'",2],["2'",2],
 #                  ["2'",2],["3'",2],["2'",2],["7",.5],
 #                  ["3'",2],["2'",2],["1'",2],["3'",1],
 #                  ["2'",2],["1'",2],["3'",1],
 #                  ["2'",2],["1'",2],["3'",1],
 #                  ["2'",2],["1'",2],["3'",1],
 #                  ["4'",2],["4'",2],["4'",2],["4'",2],
 #                  ["4'",2],["5'",2],["3'",2],["4'",.5]             ]
 #    track_list3=[["1'",2],["7",2],["6",2],["1'",1],
 #                  ["7",2],["6",2],["1'",1],
 #                  ["7",2],["6",2],["1'",1],
 #                  ["7",2],["6",2],["1'",1],
 #                  ["7",2],["7",2],["7",2],["7",2],
 #                  ["7",2],["1'",2],["7",2],["5",.5],
 #                  ["1'",2],["7",2],["6",2],["1'",1],
 #                  ["7",2],["6",2],["1'",1],
 #                  ["7",2],["6",2],["1'",1],
 #                  ["7",2],["6",2],["1'",1],
 #                  ["2'",2],["2'",2],["2'",2],["2'",2],
 #                  ["2'",2],["3'",2],["1'",2],["2'",.5],
 #                  ]
    
 #    make_midi(my_track2,170,86,track_list2,'A',30,0)
 #    make_midi(my_track2,170,91,track_list3,'g',30,1)
    
 #    my_track2.mid_save('D://test1.mid')
 #    my_track2.mixer_play()
    
  