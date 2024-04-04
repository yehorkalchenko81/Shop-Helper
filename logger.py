def logger(text: str):
    with open('logs.txt', 'a') as f:
        f.write(text)
