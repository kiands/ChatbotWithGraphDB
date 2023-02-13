import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/entities.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123"))

    '''读取文件'''
    def read_nodes(self):
        # 2類節點，格式為[a,b,c,...]
        shops = []
        foods = [] #　食物

        # 一個存放很多dict的list
        shop_infos = []

        # 節點實體關係，格式為[[a,b],[c,d],...]
        rels_food = []
        rels_accompany = []
        rels_relative = []


        count = 0
        # 遍歷每一條json
        for data in open(self.data_path):
            # 這個要進入shop_infos
            shop_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            shop = data_json['name']
            # 店名進入節點列表
            shops.append(shop)
            # 寫入單純的信息
            shop_dict['name'] = shop
            # foods應該沒必要寫在info
            # shop_dict['foods'] = ''
            shop_dict['desc'] = ''
            shop_dict['reput'] = ''

            #理論上food應該可以寫在shop_dict，但是沒有這麼做
            if 'foods' in data_json:
                foods += data_json['foods']
                # 預先寫好準備生成後續的關係
                for food in data_json['foods']:
                    rels_food.append([shop, food])
            
            if 'accompanies' in data_json:
                # 預先寫好準備生成後續的關係
                for accompany in data_json['accompanies']:
                    rels_accompany.append([shop, accompany])
            
            if 'relatives' in data_json:
                for relative in data_json['relatives']:
                    rels_relative.append([shop, relative])

            # 單純寫一下信息
            if 'desc' in data_json:
                shop_dict['desc'] = data_json['desc']

            # 單純寫一下信息
            if 'reput' in data_json:
                shop_dict['reput'] = data_json['reput']

            # inspector
            # print(shop_dict)
            shop_infos.append(shop_dict)
            # print(shop_infos)

        # ！全局標記1！注意變數順序，會影響到下面
        return set(shops), set(foods), shop_infos, rels_food, rels_accompany, rels_relative

    '''建立節點'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''創建知識圖譜中心商店的節點'''
    def create_shops_nodes(self, shop_infos):
        count = 0
        for shop_dict in shop_infos:
            node = Node("Shop", name=shop_dict['name'], desc=shop_dict['desc'],reput=shop_dict['reput'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''創建知識圖譜中心商店的節點schema'''
    def create_graphnodes(self):
        # 有的變數用不到，但是為了統一格式🧵全都讀取進來
        # shop_infos寫在變數最後面就要出錯，按順序寫就沒事
        # 此處變數列表要和！全局標記1！return的一致
        Shops, Foods, shop_infos, rels_food, rels_accompany, rels_relative = self.read_nodes()
        # 商店節點（Shops有意義，但是這邊先用商店信息，Shops這個set暫時打醬油）
        self.create_shops_nodes(shop_infos)
        # 食物節點
        self.create_node('Food', Foods)
        return


    '''創建實體關係邊'''
    def create_graphrels(self):
        # 有的變數用不到，但是為了統一格式🧵全都讀取進來
        # 此處變數列表要和！全局標記1！return的一致
        Shops, Foods, shop_infos, rels_food, rels_accompany, rels_relative = self.read_nodes()
        print(Foods)
        print(rels_food)
        self.create_relationship('Shop', 'Food', rels_food, 'has', '店內食物')
        self.create_relationship('Shop', 'Shop', rels_relative, 'is_similar_to', '相關店鋪')
        self.create_relationship('Shop', 'Shop', rels_accompany, 'franchise', '加盟店鋪')

    '''创建實體關聯邊'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''導出資料'''
    def export_data(self):
        Shops, Foods, shop_infos, rels_food, rels_accompany, rels_relative  = self.read_nodes()
        f_food = open('dict/food.txt', 'w+')
        f_shop = open('dict/shop.txt', 'w+')

        f_shop.write('\n'.join(list(Shops)))
        f_food.write('\n'.join(list(Foods)))

        f_shop.close()
        f_food.close()

        return



if __name__ == '__main__':
    handler = MedicalGraph()
    print("step1:導入圖譜節點中")
    handler.create_graphnodes()
    print("step2:圖譜邊中")      
    handler.create_graphrels()
    print("step3:導出字典中")   
    handler.export_data()