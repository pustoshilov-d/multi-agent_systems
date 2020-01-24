import numpy as np
import random
import math

class BeeSwarm:
    def __init__(self, func, n_param):
        self.func = func
        self.n_param = n_param
        self.e = 0.001

        self.startX = [0.0] * self.n_param
        self.startRad = 100.0
        self.startRegionX = [self.startRad] * self.n_param

        self.n_beesBestRegions = 5
        self.n_beesOtherRegions = 2

        self.n_bestRegions = 2
        self.n_otherRegions = 3
        self.localSearchRad = 10.0

        self.n_bees = self.n_beesBestRegions * self.n_bestRegions + self.n_beesOtherRegions * self.n_otherRegions
        self.n_res = self.n_bees + self.n_bestRegions + self.n_otherRegions

        self.X_ways = np.array([0.0]*(self.n_res)*self.n_param).reshape(self.n_res,self.n_param)
        self.F_res = np.array([0.0]*self.n_res)
        self.F_resArg = np.array([0]*self.n_res)
        self.X_waysNew = np.array([0.0]*self.n_bees*self.n_param).reshape(self.n_bees,self.n_param)

    def r_Evklid(self, X1, X2):
        res = 0.0
        for i in range(self.n_param):
            res += math.pow(X1[i] - X2[i], 2)
        return math.sqrt(res)


    def getRandX(self, x0, rad):
        x1 = np.array([0.0]*self.n_param)
        for i in range(self.n_param):
            x1[i] = 2*rad*random.random()+ x0[i] - rad
        return x1


    def eval(self):
        # Разведывательный поиск
        for i in range(self.n_bees):
            self.X_ways[i] = self.getRandX(self.startX, self.startRad)
        for i in range(self.n_bestRegions):
            self.X_ways[i+self.n_bees] = self.startRegionX
        for i in range(self.n_otherRegions):
            self.X_ways[i+self.n_bees+self.n_bestRegions] = self.startRegionX

        epoche = 0
        Ostanov = False
        while not Ostanov:
            #Счёт целевой функции по предудущему массиву решений
            for i in range(self.n_bees + self.n_bestRegions + self.n_otherRegions):
                self.F_res[i] = self.func(self.X_ways[i])
            self.F_resArg = np.argsort(-1 * self.F_res)

            #Условие останова
            if (np.all(self.X_ways[self.F_resArg[0]] != self.X_ways[self.F_resArg[1]]) and
                    self.r_Evklid(self.X_ways[self.F_resArg[0]], self.X_ways[self.F_resArg[1]]) < self.e):
                self.result = self.X_ways[self.F_resArg[0]]
                break

            #Новые случайные точки для лучших регионов
            for i in range(self.n_bestRegions):
                self.X_ways[self.n_bees + i] = self.X_ways[self.F_resArg[i]]

                for j in range(self.n_beesBestRegions):
                    self.X_waysNew[j + self.n_beesBestRegions * i] = self.getRandX(
                        self.X_ways[self.F_resArg[i]], self.localSearchRad)

            #Новые случайные точки для преспективных регионов
            shift = self.n_bestRegions * self.n_beesBestRegions
            for i in range(self.n_otherRegions):
                self.X_ways[self.n_bees + self.n_bestRegions + i] = self.X_ways[
                    self.F_resArg[i+self.n_bestRegions]]

                for j in range(self.n_beesOtherRegions):
                    self.X_waysNew[j + self.n_beesOtherRegions * i + shift] = self.getRandX(
                        self.X_ways[self.F_resArg[i+self.n_bestRegions]], self.localSearchRad)

            self.localSearchRad /= 1 + self.e
            self.X_ways[:self.n_bees] = self.X_waysNew
            epoche += 1



        print(self.result, self.func(self.result))
        print(epoche)



if __name__ == '__main__':
    from main import func

    beeSwarm = BeeSwarm(func, 2)
    beeSwarm.eval()
