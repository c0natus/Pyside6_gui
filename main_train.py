import math
import copy
import json
import argparse
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
from model import MLP, ResNet, Transformer

MODELS = {'MLP': MLP, 'ResNet': ResNet, 'Transformer': Transformer}


def train(args):
    print(vars(args))  # 인자 출력
    device = torch.device(f'cuda:{args.cuda}' if torch.cuda.is_available() else 'cpu')  # 실행 장치 설정

    # 입력 데이터의 Feature 수를 불러온다.
    with open(f'{args.dataset}/log/args.json', 'r') as f:
        input_size = json.load(f)['input_size']

    # 학습에 사용할 데이터의 개수를 계산한다.
    num_train_data = len(pd.read_csv(f'{args.dataset}/data/train_{args.split_id}.csv', index_col=0))
    args.train_size = min(int(args.train_size), num_train_data) if args.train_size > 1 else int(args.train_size * num_train_data)

    # 학습 및 평가에 사용할 데이터를 불러온다.
    datasets = {}
    for split in ['train', 'valid', 'test']:
        df = pd.read_csv(f'{args.dataset}/data/{split}_{args.split_id}.csv', index_col=0)
        tensor = torch.tensor(df.to_numpy(), dtype=torch.float, device=device)
        num_data = args.train_size if split == 'train' else len(tensor)
        datasets[split] = data.TensorDataset(tensor[:num_data, :input_size], tensor[:num_data, input_size:])
    # dataloader = data.DataLoader(datasets['train'], batch_size=args.batch_size, shuffle=True)
    output_size = datasets['train'].tensors[1].shape[1]

    # 모델, 손실 함수, 옵티마이저, 스케쥴러를 지정한다.
    model = MODELS[args.model](input_size, output_size, args.num_hidden_layers, args.hidden_size, args.dropout).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, args.num_epochs)

    scores_best = {'epoch': 0, 'train': 0, 'valid': 0, 'test': 0, 'model': copy.deepcopy(model.state_dict())}
    for epoch in range(1, args.num_epochs + 1):
        # ### 모델 학습 ###########################################################################
        model.train()
        loss_train = 0
        index_batches = torch.randperm(len(datasets['train']), device=device).split(args.batch_size)
        for indices in index_batches:
            x, y = [tensor[indices] for tensor in datasets['train'].tensors]
            if len(x) == 1:
                continue
            loss = criterion(model(x), y)  # MSE Loss 계산

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            loss_train += loss.item() * len(x) / len(datasets['train'])
        # ######################################################################### 모델 학습 #####

        if math.isnan(loss_train):
            break

        # ### 모델 평가 ###########################################################################
        model.eval()
        scores = {'epoch': epoch, 'model': None}
        with torch.no_grad():
            for split in ['train', 'valid', 'test']:
                x, y = datasets[split].tensors
                scores[split] = (1 - ((y - model(x)) ** 2).sum(0) / ((y - y.mean(0)) ** 2).sum(0)).mean().item()  # R2 Score 계산
        # ######################################################################### 모델 평가 #####

        # 중간 결과 출력
        if not args.quiet:
            print(f'[Epoch {epoch:3}/{args.num_epochs}]', end=' ')
            print(f'Loss: {loss_train:6.4f}', end=' | ')
            print(f'Score: {scores["train"]:6.4f} {scores["valid"]:6.4f} {scores["test"]:6.4f}')

        # Validation 성능을 기준으로 Best 결과 업데이트
        if scores_best['valid'] < scores['valid']:
            scores_best = scores
            if not args.quiet:
                scores_best['model'] = copy.deepcopy(model.state_dict())
        scheduler.step()

    # Best 결과 출력
    print('[BEST CHECKPOINT]', end=' ')
    print(f'Epoch: {scores_best["epoch"]:3}', end=' | ')
    print(f'Score: {scores_best["train"]:6.4f} {scores_best["valid"]:6.4f} {scores_best["test"]:6.4f}')

    # Best 모델 저장
    if not args.quiet:
        torch.save(scores_best['model'], f'{args.dataset}/model/{args.model}_{args.split_id}.pt')
        with open(f'{args.dataset}/model/{args.model}_{args.split_id}_args.json', 'w') as f:
            ##json.dump(vars(args) | {'input_size': input_size}, f)
          json.dump(dict(vars(args), **{'input_size': input_size}), f)

    del scores_best['model']
    ##return vars(args) | scores_best
    return dict(vars(args), **scores_best)


if __name__ == '__main__':
    # 실행 시 입력한 인자를 파싱한다.
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--cuda', default=0, type=int)
    parser.add_argument('--dataset', default='LearningSet01', type=str)
    parser.add_argument('--split_id', default=0, type=int)
    parser.add_argument('--train_size', default=1.0, type=float)
    parser.add_argument('--batch_size', default=1024, type=int)
    parser.add_argument('--model', default='ResNet', type=str, choices=MODELS.keys())
    parser.add_argument('--num_hidden_layers', default=3, type=int)
    parser.add_argument('--hidden_size', default=512, type=int)
    parser.add_argument('--dropout', default=0.2, type=float)
    parser.add_argument('--learning_rate', default=1e-3, type=float)
    parser.add_argument('--weight_decay', default=5e-6, type=float)
    parser.add_argument('--num_epochs', default=200, type=int)
    args = parser.parse_args()

    result = train(args)
