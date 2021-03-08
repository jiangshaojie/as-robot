# -*- coding: UTF-8 -*-
def run():
    with open("ddd","r",encoding="utf-8") as case:
        for line in case.readlines():
            contents=line.strip().split(" ")

            print(contents)
            for i in contents:
                print(i.strip())
            # contents.remove("''")
            # print(contents)
            # print(contents[1]+contents[2])



if __name__=='__main__':
    run()
