# 从爬虫生成的Excel表格中读取数据并生成词云图
import os
import sys
import PIL
import jieba
import openpyxl
import wordcloud
import configparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from multiprocessing import Pool

# 定义一些参数，参数的详细介绍见GitHub上的readme.md
config_file = 'config/config.ini'
config_Section_Name = 'GC_DEFAULT'  # 要读取的配置页名
stop_Word = ['!', '！', ':', '*', '，', ',', '？','《','》',
             '。', ' ', '的', '了', '是', '啊', '吗', '吧','这','你','我','他','就']  # 停用词表


def read_Danmu(workbook_Name, sheet_Name):  # 从Excel表中读取数据
    try:
        workbook = openpyxl.load_workbook(workbook_Name)
        worksheet = workbook[sheet_Name]  # 当然也可以通过索引读sheet,为了可读性选择用名称
        data = worksheet.iter_rows(values_only=1)
        return data
    #若报错，则返回空迭代器
    except openpyxl.utils.exceptions.InvalidFileException:
        print(f"输入文件的路径或格式错误，请打开{config_file}文件重新配置路径\n")
        return iter(())
    except KeyError:
        print(f"工作表页名错误，请检查Sheet的名字和{config_file}中是否一致\n")
        return iter(())
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"发生错误: {exc_type} - {exc_value}")
        return iter(())


def cut_words(row):
    try:
        # 每行第一列是弹幕，第二列是出现次数
        sentence = row[0]
        count = row[1]
        # 运用jieba 进行分词，将结果储存在Counter中，再将其中词语的出现次数翻count倍
        words = jieba.lcut(sentence)
        # 去除停用词表中的词
        cut_Words = pd.Series(words)
        cut_Words = cut_Words[~cut_Words.isin(stop_Word)]  
        # 将分词存入计数器中
        new_Counter = Counter(cut_Words.tolist())   
        for item in new_Counter:
            new_Counter[item] *= count              # 弹幕中词语出现数 = 弹幕出现次数*弹幕中词语出现次数
        return new_Counter
    except TypeError:
        return Counter()                            #遇见异常输入的情况，返回空计数器。


def generate_Word_Cloud(counter):  # 生成词云图
    try:
        if not counter:  # 如果计数器对象为空，则给出提示并退出函数
            return "输入的词频为空！"
        img = PIL.Image.open(pic_Path).convert('RGBA') # 解决灰度图像ERROR
        pic = np.array(img)
        image_colors = wordcloud.ImageColorGenerator(pic)
        word_Cloud = wordcloud.WordCloud(
            font_path=font_Path, mask=pic, width=WC_Width, height=WC_Height, mode="RGBA", background_color='white')
        word_Cloud.generate_from_frequencies(counter)
        plt.imshow(word_Cloud.recolor(color_func=image_colors),
                interpolation='bilinear')
        word_Cloud.to_file(output_Path)
        plt.axis('off')
        plt.show()
        return f"词云图生成完成，请前往{output_Path}查看"
    except FileNotFoundError : #pic_Path 或 font_Path错误的情况
        return f"图片或字体路径错误，请前往{config_file}核查。"
    except TypeError or ValueError : #WC_Width 或WC_Height类型或数组错误的情况
        return f"图片的Height与Width设置有误，请前往{config_file}核查。"
    except PIL.UnidentifiedImageError :
        return f"不支持该类型的图片，请修改图片路径。"
    except Exception as e:
        return f"生成词云图时发生错误：{e}"


def main():
    rows = read_Danmu(workbook_Name, sheet_Name)
    word_counts = Counter()
    # 利用线程池优化分词速度，在生成所有弹幕的词云图是能节省时间
    with Pool() as pool:
        cut_words_results = pool.map(cut_words, rows)
        for result in cut_words_results:
            word_counts.update(result)

    print(generate_Word_Cloud(word_counts))


if __name__ == "__main__":
    # 读取参数的配置
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        print(f"配置文件 {config_file} 不存在！")
        exit(1)
    config.read(config_file)
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
