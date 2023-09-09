import unittest
from multiprocessing import Pool
from crawler import *
#终端输入 python -m unittest  test\Test_crawler.py 开始测试
class TestGetResponse(unittest.TestCase):
    def test_get_Response_invalid(self):
        url = 'https://www.0d000721.gov'  #测试url 不存在的情况
        response = get_Response(url)
        self.assertEqual(response, None)
    def test_get_Response(self):          #测试正常上不去，要翻墙才能上去的网站的情况
        # url = 'https://www.google.com'    #这个因为不翻墙上不去，所以这个测试会非常占用时间
        response = get_Response('')      #若你开启翻墙可以用self.assertEqual(response.status_code, 200)判断
        self.assertEqual(response, None)

class TestGetCid(unittest.TestCase):      #因为主程序编写的原因，Bv号是爬取下来的
    def test_Get_Cid(self):               #不会出现空输入的情况，也不会出现不存在的bv
        Bv = "BV1v14y1z7MV"               #用主程序没使用过的BV号测试能否正确解析cid
        cid = get_Cid(Bv)
        self.assertEqual(cid,'1212521934')
    def test_Get_Cid_UnusualBv(self):
        BV = "BV"                        #虚空捏一个不可能的BV号看看情况
        cid = get_Cid(BV)
        self.assertEqual(cid,None)

class TestGetDanmaku(unittest.TestCase):
    def test_get_Danmaku(self):                 # 测试能否正确爬取弹幕并计数
        pool = Pool(2)                          # 测试返回值的格式是否是含计数器的列表
        BVs = ["BV1AZ4y1L7Ks", "BV1UJ411w7KC"]
        results = pool.map(get_Danmaku, BVs)
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Counter)
        self.assertIsInstance(results[1], Counter)
        pool.close()
        pool.join()
    def test_get_Danmaku_Pool(self):
        # 测试并发运行多个任务时是否会产生竞争条件或死锁
        pool = Pool(10)     #这个测试也可以测试max_processing_num的上限
        BVs = ["BV1AZ4y1L7Ks","BV1UJ411w7KC",'BV1yF411C7ZJ', 'BV1Sm4y1T7VL', 'BV1vN411i73M', 'BV1t94y147Fk', 'BV1Ap4y1E718', 'BV19h411N7rS', 'BV1M8411B7cE', 'BV1EN4y1o7c3']
        results = pool.map(get_Danmaku, BVs)
        self.assertEqual(len(results), 10)
        pool.close()
        pool.join()
    def test_get_Danmuku_NoBv(self):            #测试能否正确处理Bv号有误的情况
        BV = "BV"
        results = get_Danmaku(BV)
        self.assertEqual(results,None)
    
class TestGetTargetVideo(unittest.TestCase):
    def test_get_Target_Video_Step(self):            #测试返回值数量是否正确
        Cookie = 'i-wanna-go-back=-1; buvid4=B4C50C10-9B84-829C-550D-419C5FA4126D63704-022012116-tKxIwyBtfce6CxQ0ElglAw%3D%3D; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; LIVE_BUVID=AUTO5016571134973707; fingerprint3=c5c219316d0ccb004373ae81c1fccd50; rpdid=|(JlRYJ~Yk)k0J\'uYY)l~kJlm; hit-new-style-dyn=1; CURRENT_PID=01c3a640-cd15-11ed-be2f-b9d6f8fcd3c4; FEED_LIVE_VERSION=V8; buvid3=69F5EB42-E69A-FE9E-7403-89217946A89D91721infoc; b_nut=1688646492; _uuid=F38573DB-92FE-685E-E4110-CDD12936C28495998infoc; hit-dyn-v2=1; CURRENT_QUALITY=80; b_ut=5; header_theme_version=CLOSE; fingerprint=347a82351e94d7a58ecc0fb8a9c7eff7; CURRENT_FNVAL=4048; home_feed_column=5; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQwOTY5MDYsImlhdCI6MTY5MzgzNzcwNiwicGx0IjotMX0.z334MNCOGLvZKPDOo41gKoOsiwLXDtcen17hEnloQ-E; bili_ticket_expires=1694096906; browser_resolution=1707-917; buvid_fp=347a82351e94d7a58ecc0fb8a9c7eff7; SESSDATA=959e95a3%2C1709474725%2Cfa205%2A9247T3X6UVfRmt2Q14XTH_gosu6lH1BvPuuVlKcbVJv64tO74rYwvS8zlT8XnN0KmFRweMJAAAGwA; bili_jct=08c90b43a4f60a67a47cf85922b0a8eb; DedeUserID=65993927; DedeUserID__ckMd5=a4ecada1426e7447; sid=73zq6pro; bp_video_offset_65993927=837879399983349907; PVID=4; b_lsid=3FBAC57F_18A6612D649'
        target = '蔡徐坤'
        arg = (1,target,30,Cookie)
        results = get_Target_Video(arg)
        self.assertEqual(len(results),30)
    def test_get_Target_Video_content(self):        # 测试返回值是否是含列表的列表
        pool = Pool(2)
        Cookie = 'i-wanna-go-back=-1; buvid4=B4C50C10-9B84-829C-550D-419C5FA4126D63704-022012116-tKxIwyBtfce6CxQ0ElglAw%3D%3D; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; LIVE_BUVID=AUTO5016571134973707; fingerprint3=c5c219316d0ccb004373ae81c1fccd50; rpdid=|(JlRYJ~Yk)k0J\'uYY)l~kJlm; hit-new-style-dyn=1; CURRENT_PID=01c3a640-cd15-11ed-be2f-b9d6f8fcd3c4; FEED_LIVE_VERSION=V8; buvid3=69F5EB42-E69A-FE9E-7403-89217946A89D91721infoc; b_nut=1688646492; _uuid=F38573DB-92FE-685E-E4110-CDD12936C28495998infoc; hit-dyn-v2=1; CURRENT_QUALITY=80; b_ut=5; header_theme_version=CLOSE; fingerprint=347a82351e94d7a58ecc0fb8a9c7eff7; CURRENT_FNVAL=4048; home_feed_column=5; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQwOTY5MDYsImlhdCI6MTY5MzgzNzcwNiwicGx0IjotMX0.z334MNCOGLvZKPDOo41gKoOsiwLXDtcen17hEnloQ-E; bili_ticket_expires=1694096906; browser_resolution=1707-917; buvid_fp=347a82351e94d7a58ecc0fb8a9c7eff7; SESSDATA=959e95a3%2C1709474725%2Cfa205%2A9247T3X6UVfRmt2Q14XTH_gosu6lH1BvPuuVlKcbVJv64tO74rYwvS8zlT8XnN0KmFRweMJAAAGwA; bili_jct=08c90b43a4f60a67a47cf85922b0a8eb; DedeUserID=65993927; DedeUserID__ckMd5=a4ecada1426e7447; sid=73zq6pro; bp_video_offset_65993927=837879399983349907; PVID=4; b_lsid=3FBAC57F_18A6612D649'
        target = '蔡徐坤'
        arg = [(1,target,30,Cookie),(2,target,30,Cookie)]
        results = pool.map(get_Target_Video,arg)
        self.assertEqual(len(results),2)
        self.assertIsInstance(results[0],list)
        pool.close()
        pool.join()
    def test_get_Target_Video_WrongCookie(self):      # 测试Cookie不正确时的情况处理
        Cookie = ''
        target = '蔡徐坤'
        arg = (1,target,30,Cookie)
        results = get_Target_Video(arg)
        self.assertEqual(results, list())