#!/usr/bin/python
# encoding: utf-8

"""
multi-lang.py
Created by funpig on 2017-11-16.
Copyright (c) 2017 __MyCompanyName__. All rights reserved.
"""

import imp
import sys
import os
import re
import time
from pypinyin import lazy_pinyin

imp.reload(sys)
sys.setdefaultencoding('utf-8')   # 设置默认编码

validsuffixs = [".m"]
validRex = ur'@\"[^\"]*[\u4E00-\u9FA5]+[^\"\n]*?\"'  # 查找 @"汉字"
ignoreRex = [r"NSLocalizedString",
              r"MobClick",
              r"TalkingData",
              r"uploadUserStartAction",
              r"NSLog",
              r"imageNamed",
              r"//",
              r"DEBUG_Log",
              r"DDLogDebug",
              r"V4.0-"
              ]

ignoreDir = [r"Pods",
              r"build",
              r"Carthage",
              r"3rdparty",
              r"Util"
              ]

ignoreDirSuffixs = [
                    r".git",
                    r".framework"
                    ]

translatedRex = ur'=\s*\"[^\"]*[\u4E00-\u9FA5]+[^\"]*?\";'  # 用来解析.strings文件

translateString = "RRUUNSLocalizedString(@\"%s\", %s)"

stringsFileName = 'Localizable.strings'
translatedWords = {}  # 已翻译好的文字
needTranslatedWords = {}  # 需要翻译的文字
willProcessFils = {}  # 实际需要处理的文件，有文件已经处理过了
needProcessFiles = []

hasConflict = False  # 有没有key冲突
onlyShowProcessResult = False  # 如果你只想查看翻译效果，设置为 True


# 已翻译好的文字，从.strings读取
def gettranslatedwords(path):
    filepath = os.path.join(path, stringsFileName)
    if os.path.isfile(filepath):
        try:
            f = open(filepath)
            pattern = re.compile(translatedRex)
            while 1:
                lines = f.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    # "visitor" = "游客";
                    line_utf8 = line.decode('utf8')
                    searchobj = pattern.search(line_utf8)
                    if searchobj:
                        array = line_utf8.split(' = ')
                        key = array[1].strip()[1:-2]
                        value = array[0].strip()[1:-1]
                        translatedWords[key] = value
        finally:
            f.close()


# 遍历所有文件，列出需要查找的文件路径
def getallprocessfiles(rootpath):
    for filename in os.listdir(rootpath):
        path = os.path.join(rootpath, filename)
        if os.path.isdir(path):
            hasignor = False
            for ignor in ignoreDirSuffixs:
                if ignor in filename:
                    hasignor = True
                    break
            if hasignor or filename in ignoreDir:
                pass
            else:
                getallprocessfiles(path)
        else:
            suffix = os.path.splitext(path)
            if suffix[1] in validsuffixs:
                needProcessFiles.append(path)


# 按行查找汉字
def findhanzi(line):
    pattern = re.compile(validRex)
    line_utf8 = line.decode('utf8')
    searchobj = pattern.search(line_utf8)  # 查找汉字
    if searchobj:
        needadd = True
        for rex in ignoreRex:  # 排除 不符合要求 或 已经翻译 或 不需要翻译 的汉字
            pattern = re.compile(rex)
            obj = pattern.search(line_utf8)
            if obj:
                needadd = False
                break
        return needadd, searchobj.group()
    else:
        return False, ""


# 查找符合要求的汉字
def processfile(filepath):
    try:
        f = open(filepath)
        translatedWords.values()
        while 1:
            lines = f.readlines(100000)
            if not lines:
                break
            for line in lines:
                needadd, word = findhanzi(line)
                if needadd:
                    willProcessFils[filepath] = filepath
                    word = word[2:-1]  # @"汉字" -> 汉字
                    if translatedWords.get(word) is None and needTranslatedWords.get(word) is None:
                        # pypinyin转换中文为拼音
                        needTranslatedWords[word] = '-'.join(lazy_pinyin(word))
                        # needTranslatedWords 格式：{"汉字" : "hanzi"}

    finally:
        f.close()


# 查找并替换文件里面所有符合要求的文字
def replacestringinfile(filepath):
    file_data = ""
    try:
        f = open(filepath)
        while 1:
            lines = f.readlines(100000)
            if not lines:
                break
            for line in lines:
                needmodify, word = findhanzi(line)
                if needmodify:
                    key = word[2:-1]  # @"汉字" -> 汉字
                    value = translatedWords.get(key)
                    if value is None:
                        value = needTranslatedWords.get(key)
                    newstr = translateString % (value, word)
                    line = line.replace(word, newstr)
                file_data += line

        # filepath = filepath + '_back'
        f2 = open(filepath, 'w')
        f2.write(file_data)
    finally:
        f.close()
        f2.close()


def modifylocalizablefile():
    if len(needTranslatedWords.keys()) == 0:
        return
    try:
        f = open(stringsFileName, 'a')
        f.write('\n')
        datestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        datestr = '//append new translate words at ' + datestr
        f.write(datestr)
        f.write('\n')
        # needTranslatedWords 格式：{"汉字" : "hanzi"}
        for key, value in needTranslatedWords.items():
            f.write('\n')
            f.write('"' + value + '" = "' + key + '";')
            f.write('\n')
    finally:
        f.close()


def main():
    print 'begin processing...'
    root = os.getcwd()
    # 获取.strings文件里面已经翻译好的文字
    gettranslatedwords(root)

    # 获取所有需要处理的文件
    getallprocessfiles(root)
    for filepath in needProcessFiles:
        processfile(filepath)  # 遍历所有的文件，查找需要翻译的文字

    if not onlyShowProcessResult:
        # 实际需要处理的文件，这些文件里才有字符串需要处理
        for filepath in willProcessFils:
            replacestringinfile(filepath)

        # 增加新翻译的文字到.strings文件
        modifylocalizablefile()

    p = os.path.join(root, 'out.txt')
    try:
        f = open(p, 'a')
        for key, value in needTranslatedWords.items():
            f.write('"' + value + '" = "' + key + '";')
            f.write('\n')
    except BaseException, e:
        print e.message
    finally:
        f.close()

    print 'processing successful...'

if __name__ == '__main__':
    main()
