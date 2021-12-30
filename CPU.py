import torch
from torch import nn, optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import cnn
import time
import datetime

# 在本机的CPU上运行

# 记录开始运行时间
start = time.perf_counter()

# 定义一些超参数
batch_size = 128
learning_rate = 0.01
num_epoches = 50

# 数据预处理。transforms.ToTensor()将图片转换成PyTorch中处理的对象Tensor,并且进行标准化（数据在0~1之间）
# transforms.Normalize()做归一化。它进行了减均值，再除以标准差。两个参数分别是均值和标准差
# transforms.Compose()函数则是将各种预处理的操作组合到了一起
data_tf = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize([0.5], [0.5])])


# 数据集的下载器
train_dataset = datasets.MNIST(root='./data', train=True, transform=data_tf, download=True)
test_dataset = datasets.MNIST(root='./data', train=False, transform=data_tf)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 选择模型
model = cnn.CNN()
if torch.cuda.is_available():
    print("CUDA is available")
    # model = model.to(device)
    model

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

# 训练模型
for i in range(num_epoches):
    epoch = 0
    for data in train_loader:
        img, label = data
        img = Variable(img)
        if torch.cuda.is_available():
            img,label
        else:
            img = Variable(img)
            label = Variable(label)
        out = model(img)
        loss = criterion(out, label)
        print_loss = loss.data.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        epoch+=1
    # 模型评估
    model.eval()
    eval_loss = 0
    eval_acc = 0
    for data in test_loader:
        img, label = data
        img = Variable(img)
        if torch.cuda.is_available():
            img,label
        out = model(img)
        loss = criterion(out, label)
        eval_loss += loss.data.item()*label.size(0)
        _, pred = torch.max(out, 1)
        num_correct = (pred == label).sum()
        eval_acc += num_correct.item()
    print('EPOCH: ',i+1)
    print('Test Loss: {:.6f}, Acc: {:.6f}'.format(
        eval_loss / (len(test_dataset)),
        eval_acc / (len(test_dataset))
    ))
    i+=1
#保存模型
torch.save(model, 'CNN_for_MNIST.pth')

end =time.perf_counter()
print("total time of CPU"+str(end-start))