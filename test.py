# 画图模块测试
import random
import numpy as np
import matplotlib.pyplot as plt


def loss_acc_fig(loss, accuracy):
    x=[i+1 for i in range(len(loss))]
    l1=plt.plot(x,loss,'r--',label='loss')
    l2=plt.plot(x,accuracy,'g--',label='accuracy')
    plt.plot(x,loss,'ro-',x,accuracy,'g+-')
    plt.title('Training and validation accuracy')
    plt.xlabel('n_iter')
    plt.ylabel('loss/accuracy')
    plt.legend()
    plt.show()
    
config = {
    'n_iter': 40,
    'lambda': 10,
    'lr': 0.005,
    'A_idx': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    'B_idx': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
}

loss = [random.uniform(0, 1) for _ in range(40)]
accuracy = [random.uniform(0, 1) for _ in range(40)]
loss_acc_fig(loss, accuracy)