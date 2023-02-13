class QuestionPaser:

    '''構建實體節點'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函數'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'shop_relative':
                sql = self.sql_transfer(question_type, entity_dict.get('shop'))

            elif question_type == 'shop_accompany':
                sql = self.sql_transfer(question_type, entity_dict.get('shop'))

            elif question_type == 'shop_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('shop'))

            elif question_type == 'food_do_shop':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'shop_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('shop'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''針對不同問題分開進行處理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查詢語句
        sql = []

        # 查詢商店可以吃的東西
        if question_type == 'shop_do_food':
            sql1 = ["MATCH (m:Shop)-[r:has]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            # sql2 = ["MATCH (m:Shop)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1

        # 已知食物查商店(關係不完善，需要增加)
        # elif question_type == 'food_do_shop':
        #     sql1 = ["MATCH (m:Shop)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Shop)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2

        # 查詢相似店家
        elif question_type == 'shop_relative':
            sql1 = ["MATCH (m:Shop)-[r:is_similar_to]->(n:Shop) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1

        # 查詢連鎖店家
        elif question_type == 'shop_accompany':
            sql1 = ["MATCH (m:Shop)-[r:franchise]->(n:Shop) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1
        
        # 查詢店家的介紹
        elif question_type == 'shop_desc':
            sql = ["MATCH (m:Shop) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
