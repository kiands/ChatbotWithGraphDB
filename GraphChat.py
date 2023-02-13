from GraphTools.question_classifier import *
from GraphTools.question_parser import *
from GraphTools.answer_search import *

'''問答類'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，不好意思我不是很理解這個問題或者不知道解答。今後將繼續改進！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    # while 1:
    #     question = input('用戶:')
    #     answer = handler.chat_main(question)
    #     print('Bot:', answer)

