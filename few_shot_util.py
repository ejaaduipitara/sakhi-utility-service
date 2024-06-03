import json
from typing import List

import outlines

from env_manager import llm_class
from logger import logger
from utils import get_from_env_or_config, convert_chat_messages

temperature = float(get_from_env_or_config("llm", "temperature"))
chatClient = llm_class.get_client(temperature=temperature)

instructions = get_from_env_or_config('few_shot_config', 'instructions', None)
examples = json.loads(get_from_env_or_config('few_shot_config', 'examples', None))


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
    logger.debug("system_rules::: ", system_rules)

    response = call_chat_model(
        messages=[
            {"role": "system", "content": system_rules},
            {"role": "user", "content": question}
        ]
    )
    logger.debug("response::: ", response)
    return response


def call_chat_model(messages: List[dict]) -> str:
    converted_messages = convert_chat_messages(messages)
    response = chatClient.invoke(input=converted_messages)
    return response.content
