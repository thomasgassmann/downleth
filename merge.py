import os

if __name__ == '__main__':
    room = 'hg-f-1'
    with open('res.ts', 'wb') as res:
        for item in sorted(os.listdir(room), key=lambda x: int(x.split('.')[0])):
            with open(f'{room}/' + item, 'rb') as inp:
                res.write(inp.read())
