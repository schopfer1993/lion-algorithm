import random
import math
import k_mean
from operator import attrgetter
import matplotlib.pyplot as plt

class Lion:
    def __init__(self, x):
        self.x = x
        self.fitness = self.x + 10*math.sin(5*self.x) + 7*math.cos(4*self.x)
    
    def mutation(self, maxvalue, minvalue):
        mutation_value = random.uniform(-1, 1) * (maxvalue - minvalue)

        while(self.x + mutation_value < minvalue or self.x + mutation_value > maxvalue): #若突變後x不在[minvalue, maxvalue]之間，則重新算新的
            mutation_value = random.uniform(-1, 1) * (maxvalue - minvalue)
        else:
            self.x = self.x + mutation_value
            self.__fitness_update()

    def __fitness_update(self):
        self.fitness = self.x + 10*math.sin(5*self.x) + 7*math.cos(4*self.x)
    
#形成獅群
nomads = [] 
generate_nomad_time = 10 #產生流浪獅子10隻
x = 0 #解的範圍最小值
y = 9 #最大值
age = 5 #小獅子成熟年齡(用來計算防禦幾次)
mating_round = 1 #想交配幾次(一次交配有兩個子代)
raw_cubs = [] #未分群幼兒
boy_cubs =[] #男幼獅
girl_cubs =[] #女幼獅
train_times = 500 #最大訓練次數
campare_history = 20 
counter = 0 #等資料有campare_history筆後，取後面數來第campare_history筆和現在這筆最佳解差值是否<容忍值
acceptance_error = 0.0005 #容忍值
best_x_history = [] #紀錄最佳x歷史紀錄
mutation_ratio = 0.25 #突變率

#繁衍後代
#隨機產生一隻公母獅來交配
selected_male =   Lion(random.uniform(x, y))
selected_female = Lion(random.uniform(x, y))

while(len(best_x_history) < train_times):#達到最大訓練次數
    while(len(raw_cubs) ==  0):#若公獅被流浪獅子殺死取代，取流浪獅子跟母獅交配，重新一輪
        #交配
        for i in range(mating_round):
            ratio = random.random()
            raw_cubs.append(Lion(selected_male.x * ratio + selected_female.x * (1 - ratio)))
            raw_cubs.append(Lion(selected_female.x * ratio + selected_male.x * (1 - ratio)))

        #選擇幾隻突變
        selected_mutation_cubs =random.sample(raw_cubs, int(len(raw_cubs)*mutation_ratio))
        for i in selected_mutation_cubs:
            i.mutation(maxvalue = y, minvalue = x)
 
        #k_mean分群
        common_gender_cubs = k_mean.k_mean(raw_cubs, 2, 10)
        boy_cubs = common_gender_cubs[0]
        girl_cubs = common_gender_cubs[1]

        #刪除多餘弱小的子代
        diff = len(boy_cubs) - len(girl_cubs)
        if diff > 0:
            for i in range(diff):
                boy_cubs.remove(min(boy_cubs, key=attrgetter('fitness')))
        else:
            for i in range(-diff):
                girl_cubs.remove(min(girl_cubs, key=attrgetter('fitness')))    

        #領土防禦
        for meow in range(generate_nomad_time): #產生流浪獅子
            nomads.append(Lion(random.uniform(x, y)))

        ra_nomads = random.sample(nomads, age) #隨機選age隻流浪獅子

        for nomad in ra_nomads: #若流浪公獅適應力較強，取代公獅，且清除所有幼兒，跳出循環
            if nomad.fitness > selected_male.fitness:
                boy_cubs.clear()
                girl_cubs.clear()
                raw_cubs.clear()
                nomads.clear()
                selected_male = nomad
                break
        else:
            #領土防禦後換領土爭奪，把成長完的幼獅加入親公母獅，選出最強的來當下代交配
            boy_cubs.append(selected_male)
            girl_cubs.append(selected_female)

            selected_male = max(boy_cubs, key=attrgetter('fitness'))
            selected_female = max(girl_cubs, key=attrgetter('fitness'))
            best_x_history.append(max(selected_male.x, selected_female.x))
    else: #
        boy_cubs.clear()
        girl_cubs.clear()
        raw_cubs.clear()
        nomads.clear()
    counter += 1

    #收斂則跳出循環
    if counter >= campare_history and abs(best_x_history[-campare_history] - best_x_history[-1]) < acceptance_error:
        break

plt.title('MaxAug(x + 10sin(5x) + 7cos(4x)) \n x ≈ ' + str(round(best_x_history[-1],4)))
plt.xlabel('time(s)')
plt.ylabel('solution x')
plot_x = range(len(best_x_history))
plot_y = best_x_history
plt.plot(plot_x, plot_y)
plt.show()