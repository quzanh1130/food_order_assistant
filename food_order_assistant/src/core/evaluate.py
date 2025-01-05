import json
from core.promt_storage import EVALUATION_PROMT_TEMPLATE
from core.llm import llm

def evaluate_relevance(question, answer):
    prompt = EVALUATION_PROMT_TEMPLATE.format(question=question, answer=answer)
    evaluation, tokens = llm(prompt, model="gpt-4o-mini")

    try:
        json_eval = json.loads(evaluation)
        return json_eval, tokens
    except json.JSONDecodeError:
        result = {"Relevance": "UNKNOWN", "Explanation": "Failed to parse evaluation"}
        return result, tokens