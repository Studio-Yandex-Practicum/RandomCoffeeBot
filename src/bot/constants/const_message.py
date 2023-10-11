from src.bot.schemas import Action, Attachment

action_yes = Action(id="Yes", name="Да", type="botton", integration={"url": "", "context": {"action": "yes"}}).to_dict()

action_no = Action(id="No", name="Нет", type="botton", integration={"url": "", "context": {"action": "no"}}).to_dict()

every_week_message = Attachment(
    text="Хочешь ли принять участие в random coffee на следующей неделе?", actions=[dict(action_yes), dict(action_no)]
).to_dict()

friday_time_sending_message = "11:00"
