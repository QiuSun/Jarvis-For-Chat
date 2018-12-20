from jieba import posseg as psg
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import os
import cv2

from database import *


def generateErrorImg(image_save_path):
    '''
    向指定路径生成错误图片
    :param image_save_path:
    :return:
    '''
    error_img_path = 'images/error.jpg'
    image = cv2.imread(error_img_path)
    image_save_dir = os.path.split(image_save_path)[0]

    if not os.path.exists(image_save_dir):
        os.makedirs(image_save_dir)

    cv2.imwrite(image_save_path, image)
    print('[+]错误图片保存成功{}'.format(os.path.abspath(image_save_path)))


def getWordWeight(wordflag):
    '''
    根据词的词性获取词的权重
    :param wordflag:
    :return:
    '''
    weight = 1
    # 赋予机构团体名2的权重
    if wordflag == 'nt':
        weight = 2
    # 赋予人名5的权重(排除姓氏)
    elif wordflag in ['nr', 'nr2', 'nrj', 'nrf']:
        weight = 2
    # 赋予英文3的权重(暂时不解决英文词性的问题)
    elif wordflag == 'eng':
        weight = 3
    return weight

def getFrequencyDict(message_list):
    '''
    根据消息列表生成词频统计词典
    :param message_list: 消息列表
    :return: 词频统计词典
    '''
    # 加载停用词表
    with open("stopwords.txt", encoding='utf-8') as f:
        stopwords={}.fromkeys(f.read().split("\n"))


    print("[ ]开始生成词频统计词典")
    frequency_dict = {}

    for message in message_list:
        for word, flag in psg.cut(message):
            # 目前只考虑名词 以及英文单词
            if flag[0] == 'n' or flag == 'en':
            # if True:
                # 如果是停用词 或者为空字符 或者长度仅为1 忽略
                if word in stopwords or word==" " or len(word)==1:
                    continue 

                # print('[ ]{:10} {}'.format(word, flag))

                old_weight = frequency_dict.get(word, 0)
                # frequency_dict[word] = old_weight + getWordWeight(flag)
                frequency_dict[word] = old_weight + 1
                
    print("[+]词频统计词典生成完成")

    for key in frequency_dict:
        print("{}  {}".format(key, frequency_dict[key]))

    return frequency_dict


def generateWordCloud(message_list, image_save_path, image_mask_path):
    '''
    根据消息列表生成词云图
    :param message_list: 消息列表
    :param image_save_path: 词云图的保存路径（相对）
    :param image_mask_path: 词云图所使用的蒙版路径
    :return: 无返回值
    '''
    map_mask = np.array(Image.open(image_mask_path))
    frequency_dict = getFrequencyDict(message_list)

    wc = WordCloud(background_color="white", max_words=1000, mask=map_mask, font_path='simsun.ttf')
    # generate word cloud
    wc.generate_from_frequencies(frequency_dict)

    save_dir_path = os.path.split(image_save_path)[0]
    if not os.path.exists(save_dir_path):
        print('[+]创建目录{}'.format(os.path.abspath(save_dir_path)))
        os.makedirs(save_dir_path)

    wc.to_file(image_save_path)
    print('[+]图片保存成功{}'.format(os.path.abspath(image_save_path)))


def getWordCloud(userid, wxid, msg_group, msg_time_start, msg_time_end, image_save_path, image_mask_path='map.png'):
    '''
    根据时段、群聊生成词云 并返回该时段内群聊消息的总数
    :param userid:
    :param wxid:
    :param msg_group:
    :param msg_time_start: 筛选消息的起始时间 以整形传入 例20181212235900
    :param msg_time_end: 筛选消息的终止时间 以整形传入 例20181212235900
    :param image_save_path: 图片保存路径
    :param image_mask_path: 蒙版路径
    :return: 该时段内群聊消息的总数
    '''
    message_list = filterMessage(userid, wxid , msg_group, msg_time_start, msg_time_end)
    if len(message_list) == 0:
        print('[-]该时间段内收集到的消息数为0 生成错误图片中')
        generateErrorImg(image_save_path)
        return 0
    generateWordCloud(message_list, image_save_path, image_mask_path)
    return len(message_list)

if __name__ == "__main__":
    getWordCloud('13038011192', '13038011192', '有趣', 20181129220300, 20180129220700, 'result/1.jpg')