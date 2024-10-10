import json
import anthropic
from anthropic import HUMAN_PROMPT, AI_PROMPT
import re




def clean_resp(resp_text):
    code_pattern = r"--output_code_by_claude_start--.*--output_code_by_claude_end--"
    code_match = re.findall(code_pattern, resp_text, re.DOTALL)
    code_match = code_match[0].replace('--output_code_by_claude_start--','').replace('--output_code_by_claude_end--','') if len(code_match) > 0 else None
    explanation_pattern = r"--code_explanation_by_claude_start--.*--code_explanation_by_claude_end--"
    explanation = re.findall(explanation_pattern, resp_text, re.DOTALL)
    explanation = explanation[0].replace('--code_explanation_by_claude_start--','').replace('--code_explanation_by_claude_end--','') if len(explanation) > 0 else None
    if code_match != None and explanation != None:
        return {
            "code": code_match,
            "explanation": explanation

        }


def clean_multi_resp(resp_text):
    '''file_orders = r"--file_ordering_start--.*--file_ordering_stop--"
    file_orders = re.findall(file_orders, resp_text, re.DOTALL)
    file_orders = file_orders[0].replace('--file_ordering_start--','').replace('--file_ordering_stop--','') if len(file_orders) > 0 else None
    file_instructions = r"--file_instruction_start--.*--file_instruction_stop--"
    file_instructions = re.findall(file_instructions, resp_text, re.DOTALL)
    file_instructions = file_instructions[0].replace('--file_instruction_start--','').replace('--file_instruction_stop--','') if len(file_orders) > 0 else None

    return {
        "files_ordered": file_orders,
        "file_instructions": file_instructions
    }'''
    return json.loads(resp_text)

def get_resp(prompt, function):
    resp = anthropic.Anthropic().messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        messages=[
            {"role": "user", "content": prompt}
    ]
)

    if resp:
        resp = resp.content[0].text
        return eval(f"{function}(resp)")
    
    return {}


