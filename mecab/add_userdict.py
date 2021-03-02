import os
import subprocess
from pathlib import Path
from contextlib import contextmanager

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

@contextmanager
def change_directory(directory):
    original = os.path.abspath(os.getcwd())

    os.chdir(directory)
    yield

    os.chdir(original)

# def check_add_userdic_sh(root_dir):
#     """check add_userdic.sh
#     python-mecab-ko 패키지는 mecab 실행파일의 경로를 /usr/libexec/mecab으로 잡고 있음.
    
#     반면, mecab-ko-dic은 mecab의 기본 실행 경로를 /usr/local/libexec/mecab으로 가정하고 동작함.
    
#     그러므로, python-mecab-ko 패키지와 add-userdic.sh을 함께 사용하기 위해서는 실행파일의 경로를 /usr/libexec/mecab으로 바꿔줘야됨.
#     """
#     fn = str(list(root_dir.glob('*/mecab-ko-dic*/tools/add-userdic.sh'))[0])
#     with open(fn) as f:
#         scripts = f.read().split('\n')
    
#     for line in scripts:
#         if '/usr/libexec/mecab' in line:
#             print('tools/add-userdic.sh is already replaced.')
#             return 
    
#     replace_dir = str(list(root_dir.glob('*/mecab-ko-dic*/tools'))[0])
#     subprocess.run(f'cp {DIRECTORY}/add-userdic.sh {replace_dir}', check=True)
#     print('Replace tools/add-userdic.sh')
#     return
    

def update_custom_dictionary(custom_path:str) -> None:
    # check add-userdic.sh
    root_dir = Path('/tmp')
#     check_add_userdic_sh(root_dir)
    
    # mv custom dictionary
    custom_path = os.path.abspath(custom_path)
    user_dict = str(list(root_dir.glob("*/mecab-ko-dic*/user-dic"))[0])
    subprocess.Popen(f'cp {custom_path} {user_dict}', shell=True)
    
    # ./tools/add-userdic.sh
    dict_dir = [str(d) for d in root_dir.glob("*/mecab-ko-dic*/") if d.is_dir()][0]
    with change_directory(dict_dir):
        try:
            subprocess.run(['./tools/add-userdic.sh'], check=True)
        except:
            pass
    
    # make install
    with change_directory(dict_dir):
        try:
            subprocess.run(['make', 'install'], check=True)
        except:
            pass
    