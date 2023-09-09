import unittest
from generate_StyleCloud import *
#终端输入 python -m unittest  test\Test_generate_StyleCloud.py开始测试
class TestReadDanmu(unittest.TestCase):
    #测试正常运行的情况
    def test_Regular_Runing(self): 
        path = "test/Top_20_danmu.xlsx"
        test_Sheet = "Top 20"
        data = read_Danmu(path, test_Sheet)
        self.assertIsNotNone(data)
    #测试找不到工作表的情况
    def test_Flie_NotFound(self):
        path = ""
        test_Sheet = "Top 20"
        with self.assertRaises(StopIteration):#检测是否返回了空迭代器
            result = read_Danmu(path, test_Sheet)
            next(result)
    #测试找不到工作页的情况
    def test_Sheet_NotFound(self):
        path = "test/Top_20_danmu.xlsx"
        test_Sheet = ""
        with self.assertRaises(StopIteration):#检测是否返回了空迭代器
            result = read_Danmu(path, test_Sheet)
            next(result)

class TestCutWord(unittest.TestCase):
    #输入iter元素不正确时的处理
    def test_Unexpect_Input(self):
        input = ('',0)
        output = cut_words(input)
        self.assertEqual(output, Counter())
    #检测停用词表是否正常运作
    def test_StopWords_Runing(self):
        input = ('你我他是啊吧的了吗！？',2)
        output = cut_words(input)
        self.assertEqual(output, Counter())

class TestGenerateWordCloud(unittest.TestCase):
    #检测传入计数器为空时的处理
    def test_Empty_Counter(self):
        input = Counter()
        except_output = "输入的词频为空！"
        self.assertEqual(generate_Word_Cloud(input),except_output)