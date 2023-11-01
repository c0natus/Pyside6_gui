import json
import argparse
import pandas as pd
import torch
import torch.utils.data as data
from model import MLP, ResNet, Transformer

MODELS = {'MLP': MLP, 'ResNet': ResNet, 'Transformer': Transformer}

def test(args):
    device = torch.device(f'cuda:{args.cuda}' if torch.cuda.is_available() else 'cpu')  # 실행 장치 설정

    # 저장된 모델의 학습 인자를 불러온다.
    with open(f'{args.dataset}/model/{args.model}_{args.split_id}_args.json', 'r') as f:
        args_model = json.load(f)
    ##args = argparse.Namespace(**(args_model | vars(args)))
    args = argparse.Namespace(**(dict(args_model, **vars(args))))
    input_size = args.input_size

    # 평가에 사용할 데이터를 불러온다.
    datasets = {}
    for split in ['train', 'valid', 'test']:
        df = pd.read_csv(f'{args.dataset}/data/{split}_{args.split_id}.csv', index_col=0)
        tensor = torch.tensor(df.to_numpy(), dtype=torch.float, device=device)
        num_data = args.train_size if split == 'train' else len(tensor)
        datasets[split] = data.TensorDataset(tensor[:num_data, :input_size], tensor[:num_data, input_size:])
    output_size = datasets['train'].tensors[1].shape[1]

    # 저장된 모델을 불러온다.
    model = MODELS[args.model](input_size, output_size, args.num_hidden_layers, args.hidden_size, args.dropout)
    model.load_state_dict(torch.load(f'{args.dataset}/model/{args.model}_{args.split_id}.pt', map_location=device))
    model.to(device)

    # 전처리 전 데이터의 평균과 표준편차를 불러온다.
    mean_std = pd.read_csv(f'{args.dataset}/log/mean_std_{args.split_id}.csv', index_col=0).iloc[:, input_size:]
    mean = torch.tensor(mean_std.loc['mean'].to_numpy(), dtype=torch.float, device=device)
    std = torch.tensor(mean_std.loc['std'].to_numpy(), dtype=torch.float, device=device)

    ######
    # +++++++++
    # 유사도 관련한 결과 x의 거리와 y의 거리를 그래프로 그리기 y는 각각 따로 x는 모아서 normalize
    ####

    # ### 모델 평가 ###########################################################################
    model.eval()
    metrics = {}
    with torch.no_grad():
        for split in ['train', 'valid', 'test']:
            x, y = datasets[split].tensors
            y, y_pred = (y * std) + mean, (model(x) * std) + mean  # 표준화된 값을 역으로 변환한다.

            metrics[f'{split}_mae'] = (y - y_pred).abs().mean(0).detach().cpu().numpy()  # MAE 계산
            metrics[f'{split}_mape'] = ((y - y_pred).abs() / y.abs().clamp(min=1e-3)).mean(0).detach().cpu().numpy()  # MAPE 계산
            metrics[f'{split}_r2_score'] = (1 - ((y - y_pred) ** 2).sum(0) / ((y - y.mean(0)) ** 2).sum(0)).detach().cpu().numpy()  # R2 Score 계산
    # ######################################################################### 모델 평가 #####

    # 평가 결과를 저장한다.
    df = pd.DataFrame.from_dict(metrics, orient='index', columns=mean_std.columns)
    df.to_csv(f'{args.dataset}/log/metrics_{args.model}_{args.split_id}.csv')

if __name__ == '__main__':
    # 실행 시 입력한 인자를 파싱한다.
    parser = argparse.ArgumentParser()
    parser.add_argument('--cuda', default=0, type=int)
    parser.add_argument('--dataset', default='LearningSet01', type=str)
    parser.add_argument('--split_id', default=0, type=int)
    parser.add_argument('--model', default='ResNet', type=str, choices=MODELS.keys())
    args = parser.parse_args()

    test(args)