def read_file(path:str,arr:List[str])->None:
    """
    外部ファイルを読み込み、配列に組み込む関数。
    """
    with open (path,'r')as f:
        while True:
            line=readline()
            if not line:
                break
            arr.append(line)
    
if __name__='__main__':
    read_file()