import torch
import torch.nn as nn
import numpy as np


# Linear Layer를 겹겹이 쌓은 일반적인 구조의 모델
class MLP(nn.Module):
    def __init__(self, input_size, output_size, num_hidden_layers, hidden_size, dropout):
        super().__init__()
        self.layer_i = nn.Sequential(nn.Linear(input_size, hidden_size), nn.ReLU(), nn.Dropout(dropout))
        self.layer_h = nn.ModuleList([
            nn.Sequential(nn.Linear(hidden_size, hidden_size), nn.ReLU(), nn.Dropout(dropout)) for _ in range(num_hidden_layers)])
        self.layer_o = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.layer_i(x)
        for layer in self.layer_h:
            x = layer(x)
        x = self.layer_o(x)
        return x


# MLP에 Residual Connection을 추가한 구조의 모델
class ResNet(nn.Module):
    def __init__(self, input_size, output_size, num_hidden_layers, hidden_size, dropout):
        super().__init__()
        self.layer_i = nn.Linear(input_size, hidden_size)
        self.layer_h = nn.ModuleList([
            nn.Sequential(nn.BatchNorm1d(hidden_size), nn.Linear(hidden_size, hidden_size), nn.ReLU(), nn.Dropout(dropout),
                          nn.Linear(hidden_size, hidden_size), nn.Dropout(0)) for _ in range(num_hidden_layers)])
        self.layer_o = nn.Sequential(nn.BatchNorm1d(hidden_size), nn.ReLU(), nn.Linear(hidden_size, output_size))
        
        ##added
        self.reverse = False
        self.input_size = input_size
        self.optimal_input = torch.nn.Parameter(torch.randn(1,input_size))
        
        #from sklearn.neighbors import NearestNeighbors
        #_, train_y = _train.tensors
        #nbrs = NearestNeighbors(n_neighbors=n_nbrs, algorithm='ball_tree').fit(train_y.cpu())

    def forward(self, x):
        #print(type(x), x.size())
        x = self.layer_i(x)
        for layer in self.layer_h:
            x = x + layer(x)
        x = self.layer_o(x)
        return x

    ## New feature
    def init_optimal_input(self, batch, device, y = None):
        if self.n_nbrs != 0:
            if self.weighted_nbrs == 0:
                return self.init_optimal_input_near (batch, device, y)
            else:
                return self.init_optimal_input_near_weighted (batch, device, y)
        self.optimal_input = torch.nn.Parameter(torch.randn(batch, self.input_size, device=device))
        return
    
    def init_optimal_input_near (self, batch, device, y):
        #knn의 평균
        dists, inds = self.nbrs.kneighbors(y.cpu())
        init_input = torch.mean(self.train_x[inds],1)
        self.optimal_input = torch.nn.Parameter(init_input)
        return
    
    def init_optimal_input_near_weighted (self, batch, device, y):
        ## random이 아닌 y랑 가까운 x train을 인자로 받기
        dists, inds = self.nbrs.kneighbors(y.cpu())
        e_dists = np.exp(-dists)
        weight = torch.tensor(e_dists/np.sum(e_dists,1)[:,None], dtype=torch.float).to(device)
        init_input = torch.sum(weight[:,:,None]*self.train_x[inds],1)
        self.optimal_input = torch.nn.Parameter(init_input)
        return
    
    ## New feature
    def set_reverse(self, _set = True, n_nbrs = 0, _train = None, weighted_nbrs = 0):
        self.n_nbrs = n_nbrs
        self.weighted_nbrs = weighted_nbrs
        train_x, train_y = _train.tensors
        self.train_x = train_x
        if n_nbrs != 0:
            from sklearn.neighbors import NearestNeighbors
            _, train_y = _train.tensors
            self.nbrs = NearestNeighbors(n_neighbors=n_nbrs, algorithm='ball_tree').fit(train_y.cpu())
        
        def freeze_module(module, freeze = True):
            for param in module.parameters():
                param.requires_grad = not freeze
            return
        freeze_module(self.layer_i, freeze = _set)
        for layer in self.layer_h:
            freeze_module(layer, freeze = _set)
        return

    ## New feature    
    def reverse_forward(self):
        x = self.optimal_input
        #if x.size()[0] != 1:
        #    raise Exception(f'Wrong input. Input must have the size [1, {self.input_size}]')
        x = self.layer_i(x)
        for layer in self.layer_h:
            x = x + layer(x)
        x = self.layer_o(x)
        return x
    

class FeatureTokenizer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.parameter.Parameter(torch.randn(in_features, out_features))
        self.bias = nn.parameter.Parameter(torch.randn(in_features, out_features))

    def forward(self, x):
        return x[..., None] * self.weight + self.bias


class MHSA(nn.Module):
    def __init__(self, hidden_size, dropout):
        super().__init__()
        self.attn = nn.MultiheadAttention(hidden_size, 8, dropout=dropout, batch_first=True)

    def forward(self, x):
        return self.attn(x, x, x)[0]


# 자연어 처리에 자주 사용되는 Transformer를 Tabular 데이터에 맞게 수정한 구조의 모델
class Transformer(nn.Module):
    def __init__(self, input_size, output_size, num_hidden_layers, hidden_size, dropout):
        super().__init__()
        self.ft = FeatureTokenizer(input_size, hidden_size)
        self.cls = nn.parameter.Parameter(torch.randn(hidden_size))
        self.block_mhsa = nn.ModuleList([
            nn.Sequential(nn.LayerNorm(hidden_size), MHSA(hidden_size, dropout), nn.Dropout(0)) for _ in range(num_hidden_layers)])
        self.block_ffn = nn.ModuleList([
            nn.Sequential(nn.LayerNorm(hidden_size), nn.Linear(hidden_size, hidden_size), nn.ReLU(), nn.Dropout(dropout),
                          nn.Linear(hidden_size, hidden_size), nn.Dropout(0)) for _ in range(num_hidden_layers)])
        self.pred = nn.Sequential(nn.LayerNorm(hidden_size), nn.ReLU(), nn.Linear(hidden_size, output_size))
        del self.block_mhsa[0][0]

    def forward(self, x):
        x = self.ft(x)
        x = torch.cat([self.cls.repeat(len(x), 1, 1), x], 1)
        for mhsa, ffn in zip(self.block_mhsa, self.block_ffn):
            x = x + mhsa(x)
            x = x + ffn(x)
        x = self.pred(x[:, 0])
        return x
