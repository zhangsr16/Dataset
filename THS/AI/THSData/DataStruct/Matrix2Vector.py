import os
import math
import numpy as np
import torch
import pandas as pd
import copy

# 打开Excel文件
dataframe = pd.read_excel('1.xlsx', engine='openpyxl')
dataframe = dataframe.drop(columns=['项目名称', '项目名称-英文', 'date'])
dataframe2 = pd.read_excel('2.xlsx', engine='openpyxl')
dataframe2 = dataframe2.drop(columns=['序号', '地区', 'date'])

# 将 DataFrame 转换为 NumPy 数组
numpy_array = dataframe.values
numpy_array2 = dataframe2.values
# 将 NumPy 数组转换为 PyTorch 一维张量
tensor = torch.tensor(numpy_array, dtype=torch.float32)
tensor2 = torch.tensor(numpy_array2, dtype=torch.float32)
original_shape = tensor.shape
original_shape2 = tensor2.shape
tensor = tensor.reshape(-1)
tensor2 = tensor2.reshape(-1)
tensorLen = tensor.shape[0]
tensorLen2 = tensor2.shape[0]

# 拼接
tensor3 = torch.cat((tensor, tensor2), dim=0)

# 打印拼接后的 PyTorch 张量
print("\n转换后的 PyTorch 张量:")
print(tensor3)

# 拆分
tensorRe = tensor3[:tensorLen]
tensorRe2 = tensor3[tensorLen:(tensorLen + tensorLen2)]

# 打印恢复后的 PyTorch 张量
print("\n恢复后的 PyTorch 张量:")
print(tensorRe.reshape(original_shape))

# 升维
tensor2d = torch.stack((tensor3, tensor3 * 2, tensor3 * 3, tensor3 * 4), dim=0)
print(tensor2d.shape)
tensor3d = torch.stack((tensor2d, tensor2d * 2, tensor2d * 3, tensor2d * 4), dim=0)
print(tensor3d.shape)

# PredNN
# perameter
SeqDim = 4
SeqLen = 310
SeqRnnLen = 310

# data
src = tensor3d
tgt = tensor3d
# model
Embedding = nn.Linear(SeqDim, 4)
TF = Transformer(4, 4, 5, 7)
Cnn = ConvNet(4, [2, 3], [8, 4], [1, 4])
Rnn = RecNet(4, 4)
Pos = PositionalEncoding(4, SeqLen)
PosCnn = PositionalEncoding(4, SeqLen)
PosRnn = PositionalEncoding(4, SeqLen)