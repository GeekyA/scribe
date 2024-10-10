

def create_prompt(in_text,in_text_path, instruction, references):
    if in_text.strip() != "":
        op = "modifying input code"
    else:
        op = "write code"

    if references != []:
        references = '\n'.join(references)
        references = "You are provided with the following references to aid your modifications:\n"+references
    else:
        references = ""

    prompt = f"""
    You are an AI assistant tasked with {op} based on a user's instruction. Your goal is to change the provided code accurately and explain your changes. Follow these instructions carefully:

1. First, you will be given the input code and its file path. Review this code carefully:
<input_text file_path={in_text_path}>
{in_text}
</input_text>



2. Next, you will receive an instruction for how to modify this code:

Instruction: {instruction}

{references}

3. Your task is to modify the input code according to this instruction. Make sure your changes are accurate and fulfill the user's request.

4. After modifying the code, you must output your result in the following format:

--output_code_by_claude_start--
your_modified_code
--output_code_by_claude_end--
--code_explanation_by_claude_start--
explanation: your_explanation_of_changes
--code_explanation_by_claude_end--

5. When modifying the code:
   - Ensure that your changes are minimal and targeted to address the instruction.
   - Maintain the overall structure and style of the original code unless explicitly instructed otherwise.
   - If the instruction is unclear or could be interpreted in multiple ways, choose the most likely interpretation based on the context of the code.

6. In your explanation:
   - Clearly describe what changes you made and why.
   - If you made any assumptions or interpretations of the instruction, explain these.
   - Keep your explanation concise but informative.

7. Important rules to follow:
   - The code must be free of syntax errors and must be accurate.
   - Do not include anything in your response other than the JSON object with the 'code' and 'explanation' keys.
   - Do not include anyhting in the code other than the code
   - Make sure the code is properly indented
Remember, the code you provide will be directly pasted into a file, so ensure it is correct and ready for use.
    """

    return prompt



def multi_parse(files, instruction):
    no_of_files = len(files)
    files =  '\n'.join(files)
    prompt = f"""
    You are an AI assistant tasked with creating file-specific instructions for {no_of_files} files based on a high-level user instruction. Each file will have a path and content, and your job is to process these files according to the overarching instruction while accounting for dependencies between them.

1. You will be given the code and file paths for {no_of_files} files. Review the content of each file and the relationships between them:

    {files}
2. Overarching instruction for all files:
    
    Instruction: {instruction}

3. Your task is to:
   - Parse each file individually and create a specific instruction for it, based on the high-level instruction.
   - Reorder the files based on their dependencies. For example, if one file references another or is supposed to reference another (e.g., through function calls or imports), make sure the referenced file is processed first.
   - Ensure that each instruction is tailored to the specific content of the file and its role in the project.

4. Output each file's order and instructions in the following format:

   [
    {{
        "file_path": "Path of file 1",
        "instruction": "instruction for file 1",
    }},
    {{
        "file_path": "Path of file 2",
        "instruction": "instruction for file 2",
    }}
    {{
        "file_path": "Path of file 3",
        "instruction": "instruction for file 3",
    }}
    .
    .
   ]


5. Make sure that:
   - The output is JSON and only JSON, the formate should be absolutely accurate
   - If a file references another (e.g., an import or a function call), that file is processed first and referenced in the instruction.
   - Any assumptions made based on the instruction are clearly stated.
   - Each file’s code is processed correctly and the instructions are minimal but targeted.

   
    """
    
    return prompt
