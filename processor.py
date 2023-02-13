from TelegramFunction.features import Tool
import BotScript

class TelegramBot(Tool):
    def run_process(self,event):
        """
        To catch and deconstruct the data response from Telegram Server.

        params:
            *event : dict : user message from Telegram server.
        """
        try:
            if event.get('message'):
                event = event['message']
                self.content = event['text']
            elif event.get('callback_query'):
                event = event['callback_query']
                self.content = event['data']
            else:
                print('Error(run_process): Nothing')
        except Exception as err:
            print('Error(run_process): ',event,err)

        # Assign to variable
        self.chat_id = event['from']['id']
        self.first_name = event['from']['first_name']
    
    def run_data(self):
        uid = self.chat_id
        input_text = self.content
        feedback = BotScript.dialog(input_text,uid)
        # feedback will be wrapped
        # data = super().tool_to_json(chat_id=self.chat_id,text=self.content)
        data = super().tool_to_json(chat_id=self.chat_id,text=feedback)
        to_msg = super().tool_to_dict(type='sendMessage', data=data, files='')
        return super().send_msg([to_msg])