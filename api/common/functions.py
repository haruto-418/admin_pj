from typing import List
import random
import string

class File(object):
    @staticmethod
    def read_file(path:str,arr:List[str])->None:
        with open (path,'r')as f:
            while True:
                line=f.readline()
                if not line:
                    break
                arr.append(line)
    @staticmethod
    def extract_from_file(path:str)->List[str]:
        arr=[]
        File.read_file(path,arr)
        return random.choice(arr)



def create_random_strings(is_digit:bool,characters:int):
    """
    ランダムな文字列を生成する関数。
    """
    if is_digit:
        return "".join([random.choice(string.ascii_letters+string.digits) for _ in range(characters)])
    else:
        return "".join([random.choice(string.ascii_letters) for _ in range(characters)])

    
if __name__=='__main__':
    a=File.extract_from_file('/src/api/assets/order_strings.csv')
    print(a)