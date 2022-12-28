# GitBook SUMMARY.md 文件生成脚本:
#
# 功能：使用格式更简单，内容更灵活的预生成文件preSummary.md来生成SUMMARY.md
#
# preSummary.md文件相比原文件的优势：
# * 使用标题等级代替目录等级，摆脱繁杂的MD目录语法
# * 自动根据标题等级关系生成子目录路径，规范化书籍文件路径
# * 非标题部分内容不参与生成，可将其用作书籍大纲的注释，辅助构思书籍结构
#
# preSummary.md文件内容的注意事项：
# * 推荐编辑器：Typora
# * 强调标题语法：对应数量的#后应该加上一个空格作为语法与正文的分割，而Typora的标题快捷键会自动帮你添加该空格
# * 首行内容必须为：正文为Summary的一级标题，即：# Summary
# * 除首行外，文件中不应含有任何一级标题，最高为二级标题
# * 首个二级标题为书籍介绍，对应生成书籍根目录下的README.md,该标题不应有子标题
# * 目录生成规则：
#       无子标题的标题，生成 title_name.md 文件
#       有子标题的标题，生成 title_name 文件夹，并在该文件夹下生成README文件
#       子标题会生成 title_name.md 文件，存储于其父标题所生成的文件夹下


import copy


class SummaryLine:
    prefix = ""  # 文件路径
    title = ""  # 文件标题
    content = ""  # 实际待写入内容
    level = 1  # 标题等级


srcfile = open("preSummary.md", 'r')
dstfile = open("./SUMMARY.md", 'w+')

presl = SummaryLine()
cursl = SummaryLine()
string = srcfile.readline()

introFlag = 1
errFlag = False

presl.content = string + "\n"

if string != "# Summary\n":  # 验证首行格式
    print("Error: Wrong first line!")
    errFlag = True
else:
    while True:
        string = srcfile.readline()
        if string == '':
            break
        elif string == "\n":
            continue
        try:
            res = string.split("# ")
            cursl.level = res[0].count('#')
            cursl.title = res[1].split("\n")[0]
        except IndexError:
            continue
        if cursl.level == 1:
            cursl.prefix = "./"
        if cursl.level > presl.level:
            if introFlag >= 0:
                print("Error: Introduction should not have a subtitle!")
                errFlag = True
                break
            cursl.prefix = presl.prefix = cursl.prefix + presl.title + "/"
            presl.content = presl.content.replace("/" + presl.title + ".md", "/" + presl.title + "/README.md")
        cursl.content = "    " * (cursl.level - 1) + "* " \
                        + "[" + cursl.title + "]" \
                        + "(" + cursl.prefix + cursl.title + ".md" + ")\n"
        if introFlag == 1:
            cursl.content = cursl.content.replace("/" + cursl.title + ".md", "/README.md")
        introFlag -= 1
        dstfile.writelines(presl.content)
        presl = copy.copy(cursl)
    dstfile.writelines(presl.content)

srcfile.close()
dstfile.close()
if not errFlag:
    print("All Done!")
