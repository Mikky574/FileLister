#描述一下，运行文件主体，输入目标文件夹地绝对路径。会生成两个文件。”路径结构（依据）.txt“，”路径结构（修改后）.txt“
#通过编辑”路径结构（修改后）.txt“，然后运行一边程序主体，便会修改对应文件夹下的文件，并刷新”路径结构（依据）.txt“文件。
#全程”路径结构（依据）.txt“不要人为地去改动



# path=r"C:\Users\Administrator\Desktop\河口海岸防护与修复创新团队附件\附件\骨干成员"

# 显示文件夹树状目录
import os
import os.path

def dfs_showdir(path, depth,s=""):
    if depth == 0:
        s+="root:[" + path + "]+\n"
    for item in os.listdir(path):
        if '.git' not in item:
            s+="|      " * depth + "+--" + item+"\n"
            newitem = path +'/'+ item
            if os.path.isdir(newitem):
                s=dfs_showdir(newitem, depth +1,s)
    return s



def build(path_s):
    s=dfs_showdir(path_s, 0)  # 显示文件夹的树状结构
    f=open("路径结构（依据）.txt","w")
    f.write(s)
    f.close()
    f=open("路径结构（修改后）.txt","w")
    f.write(s)
    f.close()

def get_l(file_path="路径结构（修改后）.txt"):
    s1_sep="|      "
    s2_sep="+--"
    f=open(file_path,"r")
    s=f.read()
    f.close()
    l=[i for i in s.split("\n") if i!=""]
    root=l[0][6:-2]
    file_path=l[1].split(s2_sep)[1]
    depth=len(l[1].split(s2_sep)[0].split(s1_sep))-1
    l_tem=[(len(i.split(s2_sep)[0].split("|      "))-1,i.split(s2_sep)[1]) for i in l[1:]]
    def deal_l(l,num,something):
        try:
            l[num]=something
        except:
            l.append(something)
        return l
    l=[]
    l_path=[]
    for depth,file_path in l_tem:
        l_path=deal_l(l_path,depth,file_path)
        l.append(tuple(l_path[:depth+1]))
    return root,l

class app():
    def __init__(self,workplace):
        self.workplace=workplace
    def run(self):
        while(True):
            comn=input("请输入指令(-help获取帮助):")
            if comn=="b":
                self.app_build()
            elif comn=="c":
                self.app_change()
            elif comn=="w":
                self.write_pre()
            elif comn=="-help":
                print("b:\n  搭建工作目录，没有两个“路径结构”的txt文件时运行这个方法创建，或者打算刷新两个文件时创建。")
                print("c:\n  修改完“路径结构（修改后）.txt”后调用本方法，批量修改文件名称")
                print("w:\n  刷新“路径结构（依据）.txt”文件，原则上不需要，因为程序运行后就不从该文件内读取数据了。该文件仅作为初始目录的一种备份")
    def app_build(self):
        build(self.workplace)
    
    def app_get(self):
        self.root_pre,self.l_pre=get_l("路径结构（依据）.txt")
        self.root,self.l=get_l()
    
    def app_change(self):
        if "root_pre" not in self.__dict__:
            self.app_get()#一般不改变这个
        #读取文件
        root,l=get_l()
        root_pre=self.root_pre
        l_pre=self.l_pre
        if root_pre!=root:
            print("两文件根目录不统一，请刷新“路径结构（依据）.txt”文件")
        elif len(l_pre)!=len(l):
            print("两文件长度不统一，请按照说明使用，或者敲打作者，催作者写好适配")
        else:
            for i in range(len(l)):
                if l_pre[i][-1]!=l[i][-1]:
                    if l[i][:-1]!=():
                        path=os.path.join(*l[i][:-1])
                        path1=os.path.join(root,path,l_pre[i][-1])
                        path2=os.path.join(root,path,l[i][-1])
                    else:
                        path1=os.path.join(root,l_pre[i][-1])
                        path2=os.path.join(root,l[i][-1])
                    os.rename(path1,path2)
                    print("%s-->%s" %(path1,path2))
            self.root_pre=root
            self.l_pre=l
            self.root=root
            self.l=l
    def write_pre(self):#改变依据文件
        s=dfs_showdir(self.workplace, 0)
        f=open("路径结构（依据）.txt","w")
        f.write(s)
        f.close()

if __name__ == '__main__':
    Flag=True
    while(Flag):#判断工作路径是否正确
        workplace=input("请输入目标路径（绝对路径）:")
        if not os.path.exists(workplace):
            print("%s不存在" %(workplace))
        elif not os.path.isdir(workplace):
            print("错误的文件夹，%s是个文件" %(workplace))
        else:
            Flag=False
    a=app(workplace)
    print("successed")
    a.run()