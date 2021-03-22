# Считывание токена из файла
def read_token(filename: str):
    with open(filename) as f:
        return f.read().strip()
