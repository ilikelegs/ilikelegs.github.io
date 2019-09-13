from PIL import Image
import os
import uuid
import json

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
    # 遍历文件数量生成名字
    path = os.walk("./photos")
    for root, dirs, files in path:
        for f in files: 
            fname = uuid.uuid5(uuid.NAMESPACE_DNS, f)
            temp_dict = {}
            temp_dict['title'] = ""
            temp_dict['url'] = "photos_compress/" + str(fname) + ".jpg"
            temp_dict['href'] = "photos/" + str(fname) + ".jpg"
            temp_dict['content'] = ""
            temp_dict['name'] = str(fname) + ".jpg"
            result.append(temp_dict)
    # 写入json文件
    with open("./data/photos.json", 'w') as f:
        json.dump(result, f)

    # 遍历重命名
    path = os.walk("./photos")
    count = 0
    for root, dirs, files in path:
        for f in files: 
            os.rename(os.path.join(root, f),os.path.join(root,result[count]["name"]))
            count+=1
    # 遍历删除压缩图片
    path = os.walk("./photos_compress")
    for root, dirs, files in path:
        for f in files:
            os.remove(os.path.join(root, f))
    # 遍历压缩图片
    path = os.walk("./photos")
    for root, dirs, files in path:
        for f in files: 
            compress_image(os.path.join(root, f),os.path.join("./photos_compress/", f))