# 从爬虫生成的Excel表格中读取数据并生成词云图
import jieba
import openpyxl
import wordcloud
import configparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import stylecloud
from PIL import Image
from collections import Counter
from multiprocessing import Pool

# 定义一些参数，参数的详细介绍见GitHub上的readme.md
config_Section_Name = 'GC_DEFAULT'  # 要读取的配置页名
stop_Word = ['!', '！', ':', '*', '，', ',', '？', '《', '》',
             '。', ' ', '的', '了', '是', '啊', '吗', '吧']  # 停用词表


def read_Danmu():  # 从Excel表中读取数据
    workbook = openpyxl.load_workbook(workbook_Name)
    worksheet = workbook[sheet_Name]  # 当然也可以通过索引读sheet,为了可读性选择用名称
    data = worksheet.iter_rows(values_only=1)
    return data


def cut_words(row):
    # 每行第一列是弹幕，第二列是出现次数
    sentence = row[0]
    count = row[1]
    # 运用jieba 进行分词，将结果储存在Counter中，再将其中词语的出现次数翻count倍
    words = jieba.lcut(sentence)
    cut_Words = pd.Series(words)
    cut_Words = cut_Words[~cut_Words.isin(stop_Word)]  # 去除停用词表中的词
    new_Counter = Counter(cut_Words.tolist())   # 将分词存入计数器中
    for item in new_Counter:
        new_Counter[item] *= count              # 弹幕中词语出现数 = 弹幕出现次数*弹幕中词语出现次数
    return new_Counter


def generate_Word_Cloud(counter):  # 生成词云图
    pic = np.array(Image.open(pic_Path))
    image_colors = wordcloud.ImageColorGenerator(pic)
    word_Cloud = wordcloud.WordCloud(
        font_path=font_Path, mask=pic, width=WC_Width, height=WC_Height, mode="RGBA", background_color='white')
    word_Cloud.generate_from_frequencies(counter)
    plt.imshow(word_Cloud.recolor(color_func=image_colors),
            interpolation='bilinear')
    word_Cloud.to_file(output_Path)
    plt.axis('off')
    plt.show()


def main():
    rows = read_Danmu()
    word_counts = Counter()
    # 利用线程池优化分词速度，在生成所有弹幕的词云图是能节省时间
    with Pool() as pool:
        cut_words_results = pool.map(cut_words, rows)
        for result in cut_words_results:
            word_counts.update(result)

    generate_Word_Cloud(word_counts)


if __name__ == "__main__":
    # 读取参数的配置
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    workbook_Name = config.get(config_Section_Name, 'workbook_name',
                               fallback='output/Top_20_danmu.xlsx')  # 要读取的Excel表的名称，默认为crawler.py生成的文件
    # 要读取的Excel表的页的名称，可从['Top 20', '所有弹幕']中选择
    sheet_Name = config.get(config_Section_Name, 'sheet_Name', fallback='所有弹幕')
    WC_Width = config.getint(
        config_Section_Name, 'WC_Width', fallback=1200)  # 词云图的宽度
    WC_Height = config.getint(
        config_Section_Name, 'WC_Height', fallback=1200)  # 词云图的高度
    font_Path = config.get(config_Section_Name, 'font_Path',
                           fallback="config/msyh.ttc")  # 字体存储路径
    pic_Path = config.get(config_Section_Name, 'pic_Path',
                          fallback="config/m.png")  # 词云背景图路径
    output_Path = config.get(
        config_Section_Name, 'output_Path', fallback="output/word_could.png")
    main()
