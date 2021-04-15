import random
import numpy as np

def k_mean(elements, class_number = 2 ,times = 10):

    #分類
    classes =[]
    for i in range(class_number):
        classes.append([])

    #在要分類的元素中隨機取2個元素不重複當群心
    random_get_lion = random.sample(elements, class_number)
    keys = []
    for lion in random_get_lion:
        keys.append(lion.x)

    for i in range(times):

        for i in range(class_number):
            classes[i].clear()

        for element in elements: 

            distance_list = []
            for key in keys:
                distance_list.append(abs(element.x - key))

            indexofclass = np.argmin(distance_list)
            classes[indexofclass].append(element)
        
        #群心更新
        sum = 0
        for x in range(class_number):
            for i in classes[x]:
                sum += i.x
            else:
                if(len(classes[x]) != 0):
                    keys[x] = sum/len(classes[x])
                sum = 0
    
    return classes
 