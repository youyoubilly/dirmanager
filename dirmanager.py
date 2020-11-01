import os
import time

from os.path import join, getsize
import shutil

class Logger():
    def __init__(self, path=None, logID=""):
        if path==None:
            self.path = os.environ['HOME'] + "/log"
        else:
            self.path = path + "/log"
        print("Log will save here: " + self.path)
        self.new_dir(dir_path=self.path)
        self.log_file = self.path+"/log_{}{}.txt".format(time.strftime("%y%m%d", time.localtime()), logID)
        
    def write(self, content, p=False):
        if os.path.exists(self.log_file):
            w = open(self.log_file,'a')
            w.write("\n{}".format(content))
        else:
            w = open(self.log_file,'w')
            w.write(content)
        if p==True:
            print(content)
        w.close()
        
    def new_dir(self, dir_path):
        try:
            os.mkdir(dir_path)
        except:
            pass
        
class DirManager():
    def __init__(self, path, log=False, logID="", p=False):
        self.path = path
        print("Target path: " + self.path)
        self.log=log
        self.p = p
        if self.log==True:
            self.l=Logger(path=path, logID=logID)
    
    #Check the space size of the target directory
    #该目标路径的空间大小
    def size(self):
        size = 0
        for root, dirs, files in os.walk(self.path):
            size += sum([getsize(join(root, name)) for name in files])
        return round(size/1024/1024,2)
    
    #list out all files or alone with their created times of the target directory
    #取得该目标路径下所有文件清单的方法
    def ls(self, ctime=False):
        for root, dirs, files in os.walk(self.path):
            if ctime==False:
                return files
            else:
                return files, [os.path.getctime(join(root, name)) for name in files]

    #delete the oldest or newest file/files of the target directory
    #删除该目标路径下最旧或最新的文件
    def delete(self, num=1, d="old"):
        for i in range(0, num):
            data = self.ls(ctime=True)
            if d=="old":
                index_old = data[1].index(min(data[1]))
            else:
                index_old = data[1].index(max(data[1]))
            find_old = data[0][index_old]
            path_old = "{}/{}".format(self.path, find_old)
            os.remove(path_old)
            if self.log==True:
                self.l.write(content="Delete " + path_old, p=self.p)
            
    ##delete all files of the target directory
    #该目标路径下的所有文件删除
    def clear(self):
        for i in range(0,len(self.ls())):
            self.delete()
        if self.log==True:
            self.l.write(content="Clear ALL files at "+self.path, p=self.p)

#Return the path of a disk having the most space among all usb disks under /media/
#找出有效USB文件夹的方法
def find_valid_usb(min_mb_required=512):
    usbs_list = []
    usbs_sel = []
    tmp = []
    #获取media系统目录下所有usb文件夹
    for i in os.listdir("/media/"):
        if "-" in i and len(i)==9:
            usbs_list.append(i)
    #获取所有usb文件夹的空间大小信息
    for i in usbs_list:
        space_avl = os.statvfs(path+i).f_blocks*os.statvfs(path+i).f_frsize/1024/2014
        space_used = getdirsize(path+i)
        #筛选出有效的usb文件夹
        if space_avl > min_mb_required and space_used > 0:
            usbs_sel.append(i)
            tmp.append(space_avl)
    try:
        valid_usb = "/media/"+usbs_sel[tmp.index(max(tmp))]
    except:
        return "Can't find any usb disks"
    #返回可用空间最大的usb文件夹地址
    return valid_usb

