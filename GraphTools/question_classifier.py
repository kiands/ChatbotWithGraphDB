import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特徵詞路徑
        self.shop_path = os.path.join(cur_dir, 'dict/shop.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        # 加載特徵詞
        self.shop_wds= [i.strip() for i in open(self.shop_path) if i.strip()]
        self.food_wds= [i.strip() for i in open(self.food_path) if i.strip()]
        self.region_words = set(self.food_wds + self.shop_wds)
        # 構造領域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 構建詞典
        self.wdtype_dict = self.build_wdtype_dict()
        # 問句疑問詞
        self.accompany_qwds = ['連鎖','加盟']
        self.food_qwds = ['飲食', '飲用', '吃', '食', '伙食', '膳食', '喝', '菜' , '食譜', '菜單', '食用', '食物', '好吃的']
        self.relative_qwds = ['類似','像','差不多','相似']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集問句當中所涉及到的實體類型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 加盟
        if self.check_words(self.accompany_qwds, question) and ('shop' in types):
            question_type = 'shop_accompany'
            question_types.append(question_type)

        # 相似
        if self.check_words(self.relative_qwds, question) and ('shop' in types):
            question_type = 'shop_relative'
            question_types.append(question_type)

        # 有什麼食品
        if self.check_words(self.food_qwds, question) and 'shop' in types:
            # deny_status = self.check_words(self.deny_words, question)
            # if deny_status:
            #     question_type = 'shop_not_food'
            # else:
            question_type = 'shop_do_food'
            question_types.append(question_type)

        # 已知食物找店家
        if self.check_words(self.food_qwds, question) and 'food' in types:
            # deny_status = self.check_words(self.deny_words, question)
            # if deny_status:
            #     question_type = 'food_not_disease'
            # else:
            question_type = 'food_do_shop'
            question_types.append(question_type)

        # 若没有查到相關的外部查詢信息，那麼將該店家的描述信息返回
        if question_types == [] and 'shop' in types:
            question_types = ['shop_desc']

        # 將多個分類結果進行合併處理，組裝成一個字典
        data['question_types'] = question_types

        return data

    '''構造詞對應的類型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.shop_wds:
                wd_dict[wd].append('shop')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
        return wd_dict

    '''構造actree，加速過濾'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''語句過濾'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基於特徵詞進行分類'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)