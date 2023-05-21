# 画图模块测试
import random
import numpy as np
import matplotlib.pyplot as plt


def loss_acc_fig(loss_A, accuracy_A, loss_B, accuracy_B):
    fig = plt.figure(figsize=(12, 6))
    x=[i+1 for i in range(len(loss_A))]
    plt.subplot(1, 2, 1)
    l1=plt.plot(x,loss_A,'r--',label='loss_A')
    l2=plt.plot(x,accuracy_A,'g--',label='accuracy_A')
    plt.plot(x,loss_A,'ro-',x,accuracy_A,'g+-')
    plt.title('Training and validation accuracy')
    plt.xlabel('n_iter')
    plt.ylabel('loss_A/accuracy_A')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    l3=plt.plot(x,loss_B,'r--',label='loss_B')
    l4=plt.plot(x,accuracy_B,'g--',label='accuracy_B')
    plt.plot(x,loss_B,'ro-',x,accuracy_B,'g+-')
    plt.title('Training and validation accuracy')
    plt.xlabel('n_iter')
    plt.ylabel('loss_B/accuracy_B')
    plt.legend()
    plt.show()
    
config = {
    'n_iter': 40,
    'lambda': 10,
    'lr': 0.005,
    'A_idx': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    'B_idx': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
}

# loss_A = [random.uniform(0, 1) for _ in range(40)]
# accuracy_A = [random.uniform(0, 1) for _ in range(40)]
# loss_B = [random.uniform(0, 1) for _ in range(40)]
# accuracy_B = [random.uniform(0, 1) for _ in range(40)]
loss_A = [1.0/x for x in range(1,41)]
accuracy_A = [1.0/x for x in range(20,60)]
loss_B = [x/60.0 for x in range(1,41)]
accuracy_B = [x/80.0 for x in range(20,60)]

loss_acc_fig(loss_A, accuracy_A, loss_B, accuracy_B)