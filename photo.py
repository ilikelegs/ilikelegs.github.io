from PIL import Image
import os,shutil
import uuid
import json

#图片压缩批处理
def compressImage(srcPath,dstPath):
    for filename in os.listdir(srcPath):
        #如果不存在目的目录则创建一个，保持层级结构
        if not os.path.exists(dstPath):
                os.makedirs(dstPath)
 
        #拼接完整的文件或文件夹路径
        srcFile=os.path.join(srcPath,filename)
        dstFile=os.path.join(dstPath,filename)
 
        # 如果是文件就处理
        if os.path.isfile(srcFile):
            try:
                #打开原图片缩小后保存，可以用if srcFile.endswith(".jpg")或者split，splitext等函数等针对特定文件压缩
                sImg=Image.open(srcFile)
                w,h=sImg.size
                dImg=sImg.resize((int(w/2),int(h/2)),Image.ANTIALIAS)  #设置压缩尺寸和选项，注意尺寸要用括号
                dImg.save(dstFile) #也可以用srcFile原路径保存,或者更改后缀保存，save这个函数后面可以加压缩编码选项JPEG之类的
                print (dstFile+" 成功！")
            except Exception:
                print(dstFile+"失败！！！！！！！！！！！！！！！！！！！！！！！！！！！！")
 
        # 如果是文件夹就递归
        if os.path.isdir(srcFile):
            compressImage(srcFile, dstFile)

def compress_image(infile, outfile='', mb=140, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

if __name__ == '__main__':
    # json数组
    result = []
    # 遍历待加入图片
    path = os.walk("./photos_prepare")
    for root, dirs, files in path:
        for f in files: 
            fname = str(uuid.uuid5(uuid.NAMESPACE_DNS, f)) + ".jpg"
            os.rename(os.path.join(root, f),os.path.join(root,fname))                           #重命名
            shutil.move(os.path.join(root,fname),os.path.join('./photos',fname))                #移动文件
    
    dir_list = os.listdir("./photos")
    # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序降序排列
    # os.path.getmtime() 函数是获取文件最后修改时间
    # os.path.getctime() 函数是获取文件最后创建时间
    dir_list = sorted(dir_list,key=lambda x: os.path.getmtime(os.path.join("./photos", x)), reverse=True)
    for file in dir_list:
        temp_dict = {}
        temp_dict['title'] = ""
        temp_dict['url'] = "photos_compress/" + file
        temp_dict['href'] = "photos/" + file
        temp_dict['content'] = ""
        temp_dict['name'] = file
        result.append(temp_dict)

    # # 遍历文件数量生成名字
    # path = os.walk("./photos")
    # for root, dirs, files in path:
    #     for f in files: 
    #         temp_dict = {}
    #         temp_dict['title'] = ""
    #         temp_dict['url'] = "photos_compress/" + f
    #         temp_dict['href'] = "photos/" + f
    #         temp_dict['content'] = ""
    #         temp_dict['name'] = f
    #         result.append(temp_dict)

    # 写入json文件
    with open("./data/photos.json", 'w') as f:
        json.dump(result, f)

    # # 遍历重命名
    # path = os.walk("./photos")
    # count = 0
    # for root, dirs, files in path:
    #     for f in files: 
    #         os.rename(os.path.join(root, f),os.path.join(root,result[count]["name"]))
    #         count+=1

    # 遍历删除压缩图片
    path = os.walk("./photos_compress")
    for root, dirs, files in path:
        for f in files:
            os.remove(os.path.join(root, f))
    # 遍历压缩图片
    compressImage("./photos","./photos_compress")

    # path = os.walk("./photos")
    # for root, dirs, files in path:
    #     for f in files: 
    #         compress_image(os.path.join(root, f),os.path.join("./photos_compress/", f))