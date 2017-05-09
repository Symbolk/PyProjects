#!/usr/bin/env python
# -*- coding: utf-8 -*-
# who i am
import time, os
import threading
import sys
import datetime
import math

def readFile(filePath):
    file = 0
    try:
        file = open(filePath)
    except:
        print "read file" + filePath + " error"
        return
    lines = []
    while True:
        line = file.readline().decode("utf-8-sig").encode("utf-8")

        if not line:
            break
        line = line.strip()
        if len(line) == 0:
            break
        lines.append(line)
    return lines

def getOracle(filePath):
    idConMap = {}
    lines = readFile(filePath)
    for line in lines:
        words = line.split("\t")
        try:
            id = int(words[0].strip())
            con = words[1].strip()
            # if id in idConMap.keys():
            #     print "id already exist: " + str(id)
            if id not in idConMap.keys():
                idConMap[id] = []
            idConMap[id].append(con)
        except:
            continue

    return idConMap

def getMyCondition(filePath):
    idConListMap = {}
    lines = readFile(filePath)
    for line in lines:
        words = line.split("\t")
        try:
            id =  int(words[0].strip())
            var = words[1].strip()
            predicate = words[2].strip()

            con = predicate.replace('$', var)
            if id not in idConListMap.keys():
                idConListMap[id] = []
            idConListMap[id].append(con)

        except:
            continue

    return idConListMap

def getPrecision(params):
    oracle_path = params['input_path'] + params['project'] + '/' + params['project'] + '_' + params['bugid'] + '.orc.csv'
    my_result_patch = params['output_path'] + params['project'] + '/' + params['project'] + '_' + params[
        'bugid'] + '.joint.csv'
    #该文件只记录oracle只有一个条件表达式，rank,num比如2,3表示oracle在预测的列表里排名第2的有3个
    one_con_precision_path = params['output_path'] + params['project'] + '/' + params['project'] + '_' + params[
        'bugid'] + '.one_con_precision.csv'
    #该文件只记录oracle有两个表达式，预测列表只包含其中的一个，id,rank比如100,2表示编号为2的oracle两个表达式中的某个在预测列表中排名第2
    two_con_one_predicate_precision_path = params['output_path'] + params['project'] + '/' + params['project'] + '_' + params[
        'bugid'] + '.two_con_one_predicate_precision.csv'
    # 该文件只记录oracle有两个表达式，预测列表含其中的两个，id,rank1,rank2比如100,2,3表示编号为2的oracle两个表达式在预测列表中分别排名第2,第3
    two_con_two_predicate_precision_path = params['output_path'] + params['project'] + '/' + params['project'] + '_' + params[
        'bugid'] + '.two_con_two_predicate_precision.csv'

    oracleIdConMap = getOracle(oracle_path)
    myIdConListMap = getMyCondition(my_result_patch)


    oneConOrderMap = {}
    twoConOrderMap = {}

    for key in oracleIdConMap.keys():
        if key not in myIdConListMap.keys():
            continue

        oracleConList = oracleIdConMap[key]
        myConList = myIdConListMap[key]

        myConListSize = len(myConList)
        oracleConListSize = len(oracleConList)

        if oracleConListSize == 1:
            for i in range(0, myConListSize):
                if myConList[i] == oracleConList[0]:
                    order = i + 1
                    if order not in oneConOrderMap.keys():
                        oneConOrderMap[order] = 0

                    oneConOrderMap[order] = oneConOrderMap[order] + 1
                    break

        elif oracleConListSize == 2:
            for i in range(0, oracleConListSize):
                for j in range(0, myConListSize):
                    if oracleConList[i] == myConList[j]:
                        if key not in twoConOrderMap.keys():
                            twoConOrderMap[key] = []
                        twoConOrderMap[key].append(j + 1)
                        break

    fOut = file(one_con_precision_path, "w")
    fOut.write("rank\tnum\n")
    for key in oneConOrderMap.keys():
        fOut.write(str(key) + "\t" + str(oneConOrderMap[key]) + "\n")
    fOut.close()

    fOut = file(two_con_one_predicate_precision_path, "w")
    fOut.write("id\trank\n")
    for key in twoConOrderMap.keys():
        value = twoConOrderMap[key]
        if len(value) == 1:
            fOut.write(str(key) + "\t" + str(value[0]) + "\n")
    fOut.close()


    fOut = file(two_con_two_predicate_precision_path, "w")
    fOut.write("id\trank1\trank2\n")
    for key in twoConOrderMap.keys():
        value = twoConOrderMap[key]
        if len(value) == 2:
            fOut.write(str(key) + "\t" + str(value[0]) + "\t" + str(value[1]) + "\n")
    fOut.close()

    print "总共预测数目:" + str(len(myIdConListMap))
if __name__ == '__main__':
    params ={
        'project':'RxJava',
        'bugid':'',
        'type': 'expr',
        'expr_frequency': 10,
        'model_path': 'model/',
        'input_path':'input/',
        'output_path':'output/',
        'gen_expr_top': 10
    }
    getPrecision(params)








