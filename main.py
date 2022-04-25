import datetime
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import streamlit as st

class Game:
    def __init__(self, matrix, iter):
            self.matrix = []
            for i in matrix:
                stratgy = []
                for _ in i:
                    stratgy.append(float(_))
                self.matrix.append(stratgy)
            self.strategy1 = len(self.matrix)
            self.strategy2 = len(self.matrix[0])
            self.strategy1_count = []
            self.strategy2_count = []
            self.choosen_strategy_1 = None
            self.choosen_strategy_2 = None
            self.errors = []
            self.iter = iter
            self.k = 0
            self.alpha_k = 0
            self.beta_k = 0
            self.v_k = 0
            self.all_vK = []
            self.delta_k = None
            self.epsilon_k = None
            self.mins = [min(i) for i in self.matrix]
            self.maxmin_index = self.mins.index(max(self.mins))+1
            self.maxmin = max(self.mins)
            self.table_fields = ['k', 'i']
            for q in range(self.strategy2):
                self.strategy2_count.append(0)
                name = 'b_'+str(q+1)
                self.table_fields.append(name)
            self.table_fields.append('alpha_k')
            self.table_fields.append('J')
            for q in range(self.strategy1):
                self.strategy1_count.append(0)
                name = 'a_'+str(q+1)
                self.table_fields.append(name)
            self.table_fields.append('beta_k')
            self.table_fields.append('v_k')
            self.table_fields.append('delta_k')
            self.table_fields.append('epsilon_k')
            self.sum_of_plat_1 = []
            self.sum_of_plat_2 = []


    def table_field(self):
        return self.table_fields

def plott(data, name, y_label, x_label):
    plt.plot(data)
    plt.title(name)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.grid()

def culc(matrix, count):
    start = datetime.datetime.now()
    x = Game(matrix, count)
    print(x.matrix)
    table = PrettyTable()
    table.field_names = x.table_field()
    for i in range(1, x.iter+1):
        if i == 1:
            info = [i, x.maxmin_index]
            x.strategy1_count[x.maxmin_index-1] += 1
            for _ in x.matrix[x.maxmin_index-1]:
                info.append(_)
                x.sum_of_plat_1.append(_)
            x.alpha_k = min(x.sum_of_plat_1)/i
            info.append(x.alpha_k)
            x.strategy2 = x.sum_of_plat_1.index(min(x.sum_of_plat_1)) + 1
            x.strategy2_count[x.strategy2-1] += 1
            info.append(x.strategy2)
            for _ in x.matrix:
                info.append(_[x.strategy2-1])
                x.sum_of_plat_2.append(_[x.strategy2-1])
            x.beta_k = max(x.sum_of_plat_2)/i
            info.append(x.beta_k)
            x.v_k = (x.beta_k+x.alpha_k)/2
            x.all_vK.append(x.v_k)
            info.append(x.v_k)
            info.append('-')
            info.append('-')
            table.add_row(info)
        else:
            x.choosen_strategy_1 = x.sum_of_plat_2.index(max(x.sum_of_plat_2))
            x.strategy1_count[x.choosen_strategy_1] += 1
            info = [i, x.choosen_strategy_1+1]
            sum_pl_1 = []
            sum_pl_2 = []
            for prev, now in zip(x.matrix[x.choosen_strategy_1], x.sum_of_plat_1):
                at_moment = prev+now
                info.append(at_moment)
                sum_pl_1.append(at_moment)
            x.sum_of_plat_1 = sum_pl_1
            x.alpha_k = min(x.sum_of_plat_1)/i
            info.append(x.alpha_k)
            x.strategy2 = x.sum_of_plat_1.index(min(x.sum_of_plat_1))
            x.strategy2_count[x.strategy2] += 1
            info.append(x.strategy2+1)
            for now, prev in zip(x.matrix, x.sum_of_plat_2):
                at_moment = prev + now[x.strategy2]
                info.append(at_moment)
                sum_pl_2.append(at_moment)
            x.sum_of_plat_2 = sum_pl_2
            x.beta_k = max(x.sum_of_plat_2)/i
            info.append(x.beta_k)
            v_k = (x.beta_k+x.alpha_k)/2
            x.delta_k = abs(v_k - x.v_k)
            x.v_k = (x.beta_k+x.alpha_k)/2
            x.all_vK.append(x.v_k)
            info.append(x.v_k)
            info.append(x.delta_k)
            try:
                x.epsilon_k = str(abs(x.delta_k/x.v_k)*100)+'%'
                info.append(x.epsilon_k)
                x.errors.append(round(float(x.epsilon_k.replace('%', '')), 3))
            except ZeroDivisionError:
                info.append('-')
            table.add_row(info)
    #print(table)
    table_concl = PrettyTable()
    table_concl.field_names = ['x-*', 'y-*', 'v-*', 'x*', 'y*', 'v*', 'ушло времени']
    #print(x.strategy2_count, x.strategy1_count, sum(x.all_vK)/len(x.all_vK))
    x_ = [f'{i}/{x.iter}' for i in x.strategy1_count]
    y_ = [f'{i}/{x.iter}' for i in x.strategy2_count]
    v_ = sum(x.all_vK)/len(x.all_vK)
    x__ = [round(i/x.iter, 2) for i in x.strategy1_count]
    y__ = [round(i/x.iter, 2) for i in x.strategy2_count]
    v__ = round(sum(x.all_vK)/len(x.all_vK), 2)
    #table_concl.add_row([x_, y_, v_, x__, y__, v__, datetime.datetime.now()-start])
    #print(table_concl)
    st.latex(f'X^* - {x__}')
    st.latex(f'Y^* - {y__}')
    st.latex(f'V^*  - {v__}')
    #st.write([x_, y_, v_, x__, y__, v__, datetime.datetime.now()-start])
    col1, col2 = st.columns(2)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    col1.pyplot(plott(x.all_vK, 'Зависимость цены игры от количества итераций', 'Цена игры', f'Итерации - {x.iter}'))
    col2.pyplot(plott(x.errors, 'Зависимость ошибкок от количества итераций', 'значение ошибки EPSILON_K', f'Итерации - {x.iter}'))

# if __name__ == '__main__':
#     culc()