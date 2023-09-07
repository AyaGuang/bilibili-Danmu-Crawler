# bilibili-Danmu-Crawler
本程序利用爬虫B站爬取所需弹幕数据，以搜索关键词“**日本核污染水排海**”，爬取综合排序前**300**的所有视频弹幕。<br>
统计每种弹幕的数量，并输出数量排名前**20**的弹幕，将结果导入.*xlsx*文件中。<br>
对采集的数据集进行可视化表示，制作**词云图**。<br>
本程序分为两个子程序，均由python写成，内附*requirement.txt*文件。  <br>
输出统一储存于output文件夹。  
***
## crawler.py
本程序是爬虫程序，用于爬取弹幕以便数据分析，并将输出导入.*xlsx*文件。<br>
以下介绍程序的参数，必要时可在程序头部修改：
> target : 搜索关键词,string型,默认为"日本核污染水排海"<br>
> total_Num : 爬取的视频数，int型，默认为300<br>
> step : 步长，即每次爬取的视频数，int型，默认为30<br>
> header : 浏览器的请求头，比较重要的是**User_Agent**和**Cookie**<br>
> max_Processing_Num : 爬取操作时使用的最大线程数，int型，实测10以上会遇到403错误、从而需要代理ip，默认为6<br>

以下是程序用到的三个url：<br>
> 搜索栏api：[https://api.bilibili.com/x/web-interface/wbi/search/type](https://api.bilibili.com/x/web-interface/wbi/search/type,"进去看看")<br>
> ibilibili网站：[https://www.ibilibili.com/video/{此处填入BV号}/](https://www.ibilibili.com/video/BV1194y1z7M3/)<br>
> 弹幕网站： [https://api.bilibili.com/x/v1/dm/list.so?oid={此处填入cid号}](https://api.bilibili.com/x/v1/dm/list.so?oid=1244984876)

**注意**:使用搜索栏api时要向request.get()中传入**params**参数，表明搜索信息，否则无法访问，具体见函数get_Target_Video().<br>
输出文件：“*Top_20_danmu.xlsx*”，其sheet1为所有视频中出现次数前20的弹幕及其出现次数，sheet2为所有视频的弹幕及其出现次数。<br>
具体实现细节见**main**函数
***
## generate_Word_Cloud.py
本程序是制作词云图的程序，由爬虫程序生成的.*xlsx*文件中读取数据集并对弹幕分词，最后生成词云图。<br>
以下介绍程序的参数，必要时可在程序头部修改：
> workbook_Name : 要读取的Excel表的名称，string型，默认为crawler.py生成的"*Top_20_danmu.xlsx*"，路径为"output/Top_20_danmu.xlsx"<br>
> sheet_Name : 选择读取的sheet名，string型。<br>
> stop_Word ： 停用词表，list型，为避免一些高频出现的符号和语气词分词影响词云图美观而使用。<br>
> WC_Width  ： 生成的词云图的宽度，int型，默认为1000<br>
> WC_Height ： 生成的词云图的高度，int型，默认为1000<br>
> font_Path ： 词云图使用的字体的路径，string型，默认为"config/msyh.ttc"<br>
> pic_Path  ： 词云图使用的背景图片的路径，string型，默认为"config/m.png"<br>
> output_Path : 生成的词云图的保存路径，string型，默认为"output/word_cloud.png"<br>
***
