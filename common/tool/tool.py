import random
import json


class CommonUtil:

    # 随机生成手机号
    def phoneNORandomGenerator(self):
        prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","176","177","181","183","186","187","188","199"]
        return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))










if __name__ == '__main__':
    c= CommonUtil()
    b = c.phoneNORandomGenerator()
    print(b)
