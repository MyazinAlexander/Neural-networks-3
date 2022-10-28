import os
from sys import argv
import math

def dfs(v, colorDict, d):
    colorDict[v] = 'grey'
    for y in d[v]:
        if colorDict[y] == 'white':
            dfs(y, colorDict, d)
        if colorDict[y] == 'grey':
            print('Ошибка, обнаружен цикл!')
            exit()
    colorDict[v] = 'black'

if (len(argv) == 1):
    print('Не было передано аргументов!')
    exit()

sourcePath = argv[1][7::]
operationsFilePath = argv[2][7::]
destinationPath = argv[3][8::]

if (not os.path.isfile(sourcePath)):
    print("Не удалось открыть файл-источник, такого файла нет!")
    exit()

else:
    source = open(sourcePath, 'r')
    edges = []
    for x in source.read().split(sep='), '):
        edges.append(x[1:].split(sep=', '))

    edgesAmount = len(edges)
    edges[edgesAmount - 1][2] = edges[edgesAmount - 1][2][:-1:]

    for i in range(0, edgesAmount - 1):
        edge1 = edges[i]
        for edge2 in edges:
            if edge1 != edge2:
                if edge1[1] == edge2[1] and edge1[2] == edge2[2]:
                    print("Ошибка формата! Строка:", i + 1)
                    exit()

    edges.sort(key=lambda i: (i[1], i[2]))

    vertexList = []
    for i in range(edgesAmount):
        vertexList.append(edges[i][0])
        vertexList.append(edges[i][1])
    vertexList.sort()
    uniqueVertexList = []
    for x in vertexList:
        if x not in uniqueVertexList:
            uniqueVertexList.append(x)

    # тут начинается 2 задание
    d = {} # в d положим список смежности

    for vertex in uniqueVertexList:
        tempList = []
        for edge in edges:
            if edge[1] == vertex:
                tempList.append(edge[0])
        d[vertex] = tempList

    # проверим, есть ли в графе цикл
    colorDict = {}
    for vertex in uniqueVertexList:
        colorDict[vertex] = 'white'
    for vertex in uniqueVertexList:
        dfs(vertex, colorDict, d)

    # если нет, то продолжаем
    # найдем стоки
    drains = []
    for vertex in uniqueVertexList:
        isDrain = True
        for edge in edges:
            if edge[0] == vertex:
                isDrain = False
        if isDrain:
            drains.append(vertex)

    def calculateGraphFun(x, graphFun): # вычисление функции графа
        if len(d[x]) == 0:
            return graphFun
        graphFun += '('
        i = 0
        for y in d[x]:
            if i != 0:
                graphFun += ', '
            graphFun += f'{y}'
            graphFun = calculateGraphFun(y, graphFun)
            i += 1
        graphFun += ')'

        return graphFun

    # тут начинается 3 задание

    operationsFile = open(operationsFilePath, 'r')
    dNew = {} # это будет словарь, где вершинам будут сопоставлены значения или операции
    for x in operationsFile.read().split(sep='\n'):
        pos = x.find(':')
        vertexTemp = x[:pos - 1:]
        valueTemp = x[pos + 2::]
        dNew[vertexTemp] = valueTemp

    destination = open(destinationPath, "w+")

    def calculateValueOfGraphFun(graphFun): # вычисление значения функции графа
        while True:
            start = graphFun.rfind('(')
            if start == -1: # если скобки закончились, то выводим ответ
                return graphFun
            end = graphFun.find(')', start) # допускаем, что для каждой левой скобки найдется её правая

            numbers = graphFun[start + 1:end:]
            operation = ''
            stringToReplace = ''
            if graphFun[start - 1] == '*':
                operation = '*'
                stringToReplace = graphFun[start - 1:end + 1:]
            elif graphFun[start - 1] == '+':
                operation = '+'
                stringToReplace = graphFun[start - 1:end + 1:]
            elif graphFun[start - 3:start:] == 'exp':
                operation = 'exp'
                stringToReplace = graphFun[start - 3:end + 1:]
            tempResult = str(calculateValueOfGraphFunAuxiliary(graphFun[start + 1:end:], operation))
            graphFun = graphFun.replace(stringToReplace, tempResult)

    def calculateValueOfGraphFunAuxiliary(graphFun, operation):
        numbers = [int(x) for x in graphFun.split(', ')]
        if operation == 'exp':
            return math.exp(numbers[0])
        elif operation == '+':
            result = 0
            for x in numbers:
                result += x
            return result
        else:
            result = 1
            for x in numbers:
                result *= x
            return result

    for drain in drains:
        graphFun = calculateGraphFun(drain, f'{drain}')
        result = graphFun + ' = '

        for i in uniqueVertexList:
            graphFun = graphFun.replace(i, dNew[i])
        result += graphFun + ' = ' + calculateValueOfGraphFun(graphFun)
        destination.write(result + '\n')

    # test = "*(+(1, 2), *(3, 4))"
    # print(calculateValueOfGraphFun(test))

# 1
# *(5, +(3, *(1, 2), 4))

# 2
# exp(*(1, 2))

# 3
# *(+(1, 2), *(3, 4))





