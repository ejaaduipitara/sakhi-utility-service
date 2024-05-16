import json
from typing import List

import outlines

from app_util import convert_chat_messages
from config_util import get_config_value
from env_manager import ai_class

temperature = float(get_config_value("llm", "temperature"))
chatClient = ai_class.get_client(temperature=temperature)

gpt_model = get_config_value("llm", "gpt_model", None)
instructions = get_config_value('few_shot_config', 'instructions', None)
examples = json.loads(get_config_value('few_shot_config', 'examples', None))


@outlines.prompt
def few_shots(instructions, examples):
    """{{ instructions }}

    Examples
    --------
       {% for item_group, items in examples.items() %}
            {% if items %}
                {% for item in items %}
                    Q: {{ item.question }}
                    A: {{ item.answer }}
                    {% if not loop.last %}

                    {% endif %}
                {% endfor %}
            {% endif %}
       {% endfor %}
    Question
    --------

    Q: user_question
    A:
    """


prompt = few_shots(instructions, examples)


def invokeLLM(question):
    system_rules = prompt.replace("user_question", question)
    print("system_rules::: ", system_rules)

    response = call_chat_model(
        messages=[
            {"role": "system", "content": system_rules},
            {"role": "user", "content": question}
        ]
    )
    print("response::: ", response)
    return response



def call_chat_model(messages: List[dict]) -> str:
    converted_messsages = convert_chat_messages(messages)
    response = chatClient.invoke(input=converted_messsages)
    return response.content
