
import yaml
import os



class HandleYaml:
    """获取yaml里边的数据，参数化读取，修改直接改yaml
    """
    def __init__(self, filename=None):
        if filename is None:
            CONF_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            filename = os.path.join(CONF_PATH, r"conf/base.yaml")
            with open(filename, encoding="utf-8") as file:
                self.config_data = yaml.full_load(file)
        else:
            CONF_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            filename = os.path.join(CONF_PATH, filename)
            with open(filename, encoding="utf-8") as file:
                self.config_data = yaml.full_load(file)


    def get_data(self, section, option):
        """
        读取配置文件数据
        :param section: 区域名
        :param option: 选项名
        :return: 值
        """
        return self.config_data[section][option]

    def get_all_data(self, section):
        """
        读取配置文件某个区域下的所有数据
        :param section:
        :return: 值
        """
        return self.config_data[section]


if __name__ == '__main__':
    do_yaml = HandleYaml("conf\\base.yaml")
    print(do_yaml.get_data("base_url","admin"))
    print(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

