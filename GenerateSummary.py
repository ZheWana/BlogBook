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


srcfile = open("./preSummary.md", 'r')
dstfile = open("./SUMMARY.md", 'w+')

presl = SummaryLine()
cursl = SummaryLine()
string = srcfile.readline()

presl.content = string + "\n"

if string != "# Summary\n":  # 验证首行格式
    print("Wrong first line!")
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
        except IndexError:  # 该行为注释
            continue
        if cursl.level == 1:
            cursl.prefix = "./"
        if cursl.level > presl.level:
            cursl.prefix = presl.prefix = cursl.prefix + presl.title + "/"
            presl.content = "    " * (presl.level - 1) + "* " \
                            + "[" + presl.title + "]" \
                            + "(" + presl.prefix + "README.md" + ")\n"
        cursl.content = "    " * (cursl.level - 1) + "* " \
                        + "[" + cursl.title + "]" \
                        + "(" + cursl.prefix + cursl.title + ".md" + ")\n"
        dstfile.writelines(presl.content)
        presl = copy.copy(cursl)

srcfile.close()
dstfile.close()

print("All Done!")
