# GitBook SUMMARY.md 文件生成脚本:
#
# 使用标题等级代替目录等级
# 自动翻译目录结构
# 忽略非标题部分，用作书籍大纲构思注释
import copy


class SummaryLine:
    prefix = ""  # 文件路径
    title = ""  # 文件标题
    content = ""  # 实际待写入内容
    level = 1  # 标题等级


srcfile = open("./preSUMMARY.md", 'r')
dstfile = open("./SUMMARY.md", 'w+')

presl = SummaryLine()
cursl = SummaryLine()
string = srcfile.readline()

if string != "# Summary\n":  # 验证首行格式
    print("Wrong firsr line!")
else:
    dstfile.writelines(string + "\n")
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
        except IndexError:  # 该行为注释
            continue
        if cursl.level == 1:
            cursl.prefix = "./"
        elif cursl.level > presl.level:
            cursl.prefix = cursl.prefix + presl.title + "/"
        else:
            pass
        presl = copy.copy(cursl)
        cursl.content = "    " * (cursl.level - 1) + "* " \
                        + "[" + cursl.title + "]" \
                        + "(" + cursl.prefix + cursl.title + ".md" + ")\n"

        dstfile.writelines(cursl.content)

srcfile.close()
dstfile.close()

print("All Done!", end='')
