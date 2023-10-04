# GUI

- 가상환경 install

```bash
conda env create -f env.yml
```

- Python 명령어로 실행

```bash
python main.py
```

- EXE 파일 만든 후 실행

1. 백신 잠시 멈춤 (실시간 검사가 진행 중이면, 파일이 만들어지자 마자 삭제 됩니다.)
2. pyinstaller로 exe 파일로 만듦.
    ```bash 
    pyinstaller --name="Test" --noconsole --onefile main.py 
    ```
3. dist 폴더 안에 Test.exe가 생성되는데 이것을 main.py가 있는 폴더로 옮긴다.
    - File path(LearningSet01.xlsx, args.json)가 상대경로로 되어 있습니다.
    - 이후 편의를 위해 고칠 수 있는 방법을 찾아봐야 합니다.
        - 절대 경로 입력, pyinstaller로 build 후 spec file 편집 등...
4. Text.exe 실행

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