# GUI

## 1. 가상환경 install

```bash
conda env create -f env.yml
```

## 2.1. Python 명령어로 실행

```bash
python main.py
```

## 2.2. EXE 파일 만든 후 실행

- pyinstaller는 virus issue가 많아 적합하지 않아 보입니다.
- cx_Freeze와 nuitka를 자주 사용합니다.
    - cx_Freeze는 decompile이 쉽게 돼서 exe파일로 code를 복구하는 게 쉽다는 단점이 있습니다.
    - nuitka는 python을 c code로 바꾼다음 compile을 진행하기 때문에 compile할 때의 속도가 느리다는 단점이 있습니다. 그렇지만, decompile이 어렵고 실행 속도가 빠르다는 장점이 있습니다.

1. nuitka로 exe 파일로 만듦.
    ```bash 
    python -m nuitka \
        --standalone \
        --enable-plugin=pyside6 \
        --disable-console \
        --include-data-files=./LearningSet01/log/args.json=args.json \
        main.py
    ```
    - `--standalone`: python interpreter 없이도 실행 가능하도록 binary file을 만듦.
        - `--onefile`: `--standalone`과 유사한 역할을 하지만, 모든 것을 *.exe에 때려 박지만, virus로 인식된다.
    - `--enable-plugin`: UI를 사용하려면 enable-plugin option을 사용해야 한다.
    - `--disable-console`: UI를 사용하기 때문에 console 창이 열릴 필요가 없다.
    - `--include-data-files`: argument가 저장된 파일을 exe 파일이 있는 폴더에 생성한다.
        - 상대 경로를 이용해 argument를 저장하고 불러올 수 있다.
        - main.dist 폴더 안에 args.json 파일이 생성되고 저장이 된다.
2. main.dist 폴더 안에 main.exe 파일이 생성되는데 이것을 실행한다.
    - 배경화면에 main.exe 바로가기를 만들면 폴더에 접근하지 않고 실행할 수 있습니다.

## 3. 의논 해봐야 할 것
- args에 저장된 것을 불러올 때, dataset filename은 불러오지 않는 방향...?
    - UI 상으로 filename은 사용자가 편집 불가능하고 어떤 file을 선택했는지만 보여주는 방향...?
- pre-processing된 file들을 저장할 위치도 사용자에게 입력을 받을지...?
    - 그렇지 않으면 상대 경로에 따라 main.dist에 LearningSet01 폴더가 생성되고 pre-processing된 file들이 저장됨.

```bash
📦code  
 ┣ 📂data  
 ┃ ┗ 📜LearningSet01.xlsx  
 ┣ 📂LearningSet01  
 ┃ ┣ 📂data  
 ┃ ┃ ┣ 📜test_0.csv  
 ┃ ┃ ┣ 📜train_0.csv  
 ┃ ┃ ┗ 📜valid_0.csv  
 ┃ ┣ 📂log  
 ┃ ┃ ┣ 📜args.json  # 해당 파일에 arg를 저장하고 불러옴. 이후 .ini 파일로 대체하면 될 듯 합니다.
 ┃ ┃ ┣ 📜mean_std_0.csv  
 ┃ ┃ ┗ 📜outlier.csv  
 ┃ ┣ 📂model  
 ┃ ┣ 📂plot  
 ┃ ┣ 📜input.csv  
 ┃ ┗ 📜output.csv  
 ┣ 📜.gitignore  
 ┣ 📜env.yml        # 가상환경
 ┣ 📜main.py
 ┣ 📜mainwindow.py  # .ui를 .py로 만든 것.
 ┣ 📜mainwindow.ui  # GUI 파일, mainwindow.py가 있다면 없어도 됨.
 ┣ 📜preprocess.py  
 ┗ 📜README.md
 ```