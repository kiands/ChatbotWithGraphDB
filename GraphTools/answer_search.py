from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123"))
        self.num_limit = 20

    '''執行cypher查詢，並返回相應結果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根據對應的qustion_type，調用相應的回覆模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        # 商店介紹
        elif question_type == 'shop_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},據我所知：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        # 商店加盟關係
        elif question_type == 'shop_accompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的加盟店有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 類似的商店
        elif question_type == 'shop_relative':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的相似店家有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 商店可以吃什麼（變數名稱需要優化）
        elif question_type == 'shop_do_food':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}可以吃到：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()