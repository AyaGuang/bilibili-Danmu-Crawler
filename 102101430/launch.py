#这个程序可以一键运行之前写的两个子程序
import subprocess

language = 'python'
process_Name_List = ['crawler.py', 'gengerate_Clound.py']
def main():
    for process in process_Name_List:
        subprocess.run([language,process])

if __name__ == "__main__":
    print("程序启动！")
    main()
    print("程序终止")