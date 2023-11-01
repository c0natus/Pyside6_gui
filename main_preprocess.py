import json
import argparse
from pathlib import Path
import pandas as pd
from scipy.special import erfcinv
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def preprocess(args):
    print(f'>Make directories')
    # 전처리된 데이터를 저장할 폴더를 생성한다.
    try:
        Path(f'{args.dataset}/').mkdir()
        Path(f'{args.dataset}/log/').mkdir()
        Path(f'{args.dataset}/data/').mkdir()
        Path(f'{args.dataset}/plot/').mkdir()
        Path(f'{args.dataset}/model/').mkdir()
    except:
        pass
    
    print(f'>Read files')
    # 전처리할 데이터(엑셀 파일)를 불러온다.
    col_input, col_output = ord(args.start_column_input) - 65, ord(args.start_column_output) - 65
    df_input = pd.read_excel(f'{args.filename}.xlsx', sheet_name=args.sheet_input, engine='openpyxl').iloc[:, col_input:]
    df_output = pd.read_excel(f'{args.filename}.xlsx', sheet_name=args.sheet_output, engine='openpyxl').iloc[:, col_output:]
    df = pd.concat([df_input, df_output], axis=1).dropna()  # 값이 없는 행을 제거한다.

    print(f'>>Input shape: {df_input.shape}')
    print(f'>>Output shape: {df_output.shape}')

    input_size = df_input.shape[1]
    output_size = df_output.shape[1]

    df_output = df.iloc[:, input_size:]

    print(f'>Detect outliers using {args.outlier_detector}')
    # 지정된 Outlier Detector를 이용하여 Outlier를 찾는다.
    if args.outlier_detector == 'Mean':
        index = ((df_output > df_output.mean() - args.outlier_detector_param * df_output.std()) & (df_output < df_output.mean() + args.outlier_detector_param * df_output.std())).all(axis=1)
    elif args.outlier_detector == 'Median':
        scaled_mad = (- 1 / (2 ** 0.5 * erfcinv(3 / 2))) * (df_output - df_output.median()).abs().median()
        index = ((df_output > df_output.median() - args.outlier_detector_param * scaled_mad) & (df_output < df_output.median() + args.outlier_detector_param * scaled_mad)).all(axis=1)
    elif args.outlier_detector == 'IF':
        outlier_detector = IsolationForest(contamination=args.outlier_detector_param)
        index = outlier_detector.fit_predict(df_output) == 1

    print(f'>>Number of outliers: {len(df[~index])}')

    # 찾은 Outlier를 저장한 후 제거한다.
    df[~index].to_csv(f'{args.dataset}/log/outlier.csv')
    df = df[index]

    for split_id in range(args.num_splits):
        # 데이터를 train/valid/test split으로 분할한다.
        df_train, df_test = train_test_split(df, train_size=args.train_size, random_state=split_id)
        df_train, df_valid = train_test_split(df_train, test_size=0.125, random_state=split_id)

        # 데이터를 표준화한다.
        scaler = StandardScaler().fit(df_train)
        df_train = pd.DataFrame(scaler.transform(df_train))
        df_valid = pd.DataFrame(scaler.transform(df_valid))
        df_test = pd.DataFrame(scaler.transform(df_test))
        pd.DataFrame([scaler.mean_, scaler.scale_], index=['mean', 'std'], columns=df.columns).to_csv(f'{args.dataset}/log/mean_std_{split_id}.csv')

        # train/valid/test split을 저장한다.
        df_train.to_csv(f'{args.dataset}/data/train_{split_id}.csv')
        df_valid.to_csv(f'{args.dataset}/data/valid_{split_id}.csv')
        df_test.to_csv(f'{args.dataset}/data/test_{split_id}.csv')

    # Inference에 사용할 파일을 생성한다.
    pd.DataFrame(columns=df.columns[:input_size]).to_csv(f'{args.dataset}/input.csv', index=False)
    pd.DataFrame(columns=df.columns[input_size:]).to_csv(f'{args.dataset}/output.csv', index=False)

    print(vars(args))

    # 전처리에 사용한 인자들을 저장한다.
    with open(f'{args.dataset}/log/args.json', 'w') as f:
        json.dump(dict(vars(args), **{'input_size': input_size, 'output_size': output_size}), f)

if __name__ == '__main__':
    # 실행 시 입력한 인자를 파싱한다.
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='data/LearningSet01', type=str)
    parser.add_argument('--sheet_input', default='Input', type=str)
    parser.add_argument('--sheet_output', default='Output', type=str)
    parser.add_argument('--start_column_input', default='C', type=str)
    parser.add_argument('--start_column_output', default='A', type=str)
    parser.add_argument('--outlier_detector', default='IF', type=str, choices=['Mean', 'Median', 'IF'])
    parser.add_argument('--outlier_detector_param', default=0.01, type=float)
    parser.add_argument('--train_size', default=0.8, type=float)
    parser.add_argument('--num_splits', default=1, type=int)
    parser.add_argument('--dataset', default='LearningSet01', type=str)
    args = parser.parse_args()

    if args.dataset is None:
        args.dataset = args.filename

    preprocess(args)