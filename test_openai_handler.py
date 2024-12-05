from openai_handler import OpenAIHandler

def test_openai_handler_add_message():
    handler = OpenAIHandler()
    assert len(handler.message_history) == 0
    channel_id = 1
    role = "user"
    message = "hello pytest"
    handler.add_message(channel_id, role, message)
    assert len(handler.message_history) == 1
