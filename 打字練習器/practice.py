from configparser import ConfigParser
from datetime import datetime
from mimetypes import init
import os


def loadConfig():
    config_object = ConfigParser()
    config_object.read("config.ini")
    practice_info = config_object["PRACTICE_INFO"]
    return practice_info


def loadKeywords():
    with open("kw.txt", "r") as f:
        lstKeywords = f.readlines()
    return lstKeywords


def choiceKeywords(lstKeywords):
    keyword = "abcdefghijklmnopqrstuvwxyz"
    description = ""
    for i in range(len(lstKeywords)):
        lstKeywords[i] = lstKeywords[i].strip("\n")
        description += str(i+1) + " : " + lstKeywords[i] + "\n"
    Index = int(input("請決定練習的題目:\n" + description))
    if Index < len(lstKeywords):
        keyword = lstKeywords[Index-1]
    # else:
    #     expect = "abcdefghijklmnopqrstuvwxyz"

    return keyword


# 結束匯出報告
def diffIndex(expect, actual):
    lstDiffIndex = []
    for i in range(len(expect)):
        if expect[i] != actual[i]:
            lstDiffIndex.append(i)
    return lstDiffIndex


def diffMsg(expect, lstDiffIndex):
    text = "diff :  "
    lstText = []
    for i in range(len(expect)):
        lstText.append(" ")
    # print(lstText)
    for idx in lstDiffIndex:
        lstText[idx] = "^"

    for s in lstText:
        text += s
    text += " -> "

    for i in range(len(lstDiffIndex)):
        text += "'" + expect[lstDiffIndex[i]] + "'"
        if i < len(lstDiffIndex)-1:
            text += ","
    return text


def report(
                count,
                correctCount,
                practiceTime,
                startTime,
                endTime,
                expect):

    expectTime = practiceTime
    actualTime = count
    correctTime = correctCount
    errorTime = count - correctCount
    correctRate = (correctCount / count) * 100
    totalTime = (endTime - startTime).total_seconds()
    speedRate = totalTime / count
    reportText = """
{0}
------
+ Expect Practice Count : {1}
+ Actual Practice Count : {2}
+ Correct Number : {3}
+ Error Number : {4} 
+ Correct Rate : {5:.2f} %
+ Practice Time : {6:.2f}
+ Average Speed : {7:.2f}
+ Start Time : {8}
+ End Time : {9}
    """.format(
        expect,
        expectTime,
        actualTime,
        correctTime,
        errorTime,
        correctRate,
        totalTime,
        speedRate,
        stratTime.strftime("%Y-%m-%d, %H:%M:%S"),
        endTime.strftime("%Y-%m-%d, %H:%M:%S"),
        ""
    )
    print(reportText)
    return reportText


def export(reportText, exportPath):
    fileName = datetime.now().strftime("report_%Y%m%d_%H%M%S")
    if len(exportPath) > 0:
        pathText = exportPath + os.path.sep + fileName + '.md'
    else:
        pathText = fileName + '.md'

    with open(pathText, 'w') as f:
        f.write(reportText)
    print("練習報告輸出路徑 : ", pathText)


def practice_process():
    configInfo = loadConfig()
    # actual = "123"
    practiceTime = int(configInfo["practice_time"])
    exportPath = configInfo["export_path"]

    lstKeywords = loadKeywords()

    expect = choiceKeywords(lstKeywords)
    print("請輸入: ", expect)

    isRun = True
    count = 0
    correctCount = 0

    stratTime = datetime.now()
    endTime = datetime.now()
    totalTime = 0

    while (isRun):
        # print(stratTime)
        # actual = input("\r 請輸入" + expect + ": \n",end="")
        actual = input("練習第{}次 \n".format(count+1))

        # time.sleep(0.5)
        if expect == actual:
            print("input: ", expect, "->", "正確 \n")
            correctCount += 1
        else:
            print("input: ", actual, "->", "錯誤")
            if len(expect) == len(actual):
                lstDiffIndex = diffIndex(expect, actual)
                # print(lstDiffIndex)
                text = diffMsg(expect, lstDiffIndex)
                print(text + "\n")
                # print("diff : ", expect, "->", "Length mismatch \n")
            else:
                print("diff :  " + expect + "-> Length mismatch\n")

        count += 1
        if count >= practiceTime:
            isRun = False
            # 輸出練習的結果報告
        elif actual == "exit":
            isRun = False

        if isRun == False:
            endTime = datetime.now()
            totalTime = (endTime - stratTime).total_seconds()
            reportText = report(
                expect,
                count,
                correctCount,
                practiceTime,
                stratTime,
                endTime,
            )
            export(reportText, exportPath)

if __name__ == '__main__':
    practice_process()