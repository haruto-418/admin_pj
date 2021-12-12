from typing import List
import random
import string

def read_file(path:str,arr:List[str])->None:
    """
    外部ファイルを読み込み、配列に組み込む関数。
    """
    with open (path,'r')as f:
        while True:
            line=f.readline()
            if not line:
                break
            arr.append(line)

def create_random_strings(is_digit:bool,characters:int):
    """
    ランダムな文字列を生成する関数。
    """
    empty_str:str=""
    if is_digit:
        return empty_str.join([random.choice(string.ascii_letters+string.digits) for _ in range(characters)])
    else:
        return empty_str.join([random.choice(string.ascii_letters) for _ in range(characters)])

def extract_from_file(path:str)->None:
    """
    外部ファイルを読み込み、配列に組み込む関数。
    """
    arr=[]
    with open (path,'r')as f:
        while True:
            line=f.readline()
            if not line:
                break
            arr.append(line)
    return random.choice(arr)


    
if __name__=='__main__':
    a=create_random_strings(True,6)
    print(a)