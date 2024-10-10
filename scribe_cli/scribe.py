
import click
from scribe_cli.prompt_gen import create_prompt, multi_parse
from scribe_cli.open_gui import show_gui, show_multi_gui
from scribe_cli.llm_infer import get_resp
import json
import os

@click.group()
def main():
    pass

@click.command()
def init():
    """Initialize the project and create the scribeconfig directory."""
    codepath = os.getcwd()
    language = input("What language is this codebase written in?: ")
    
    # Create the scribeconfig directory
    try:
        os.mkdir('scribeconfig')
        click.echo('scribeconfig dir created')
    except FileExistsError:
        click.echo('codebase already initialized')

    # Write the configuration file
    config_data = {
            'path': codepath,
            'language': language
        }
    with open(os.path.join(codepath, 'scribeconfig', 'scribe_config.json'), 'w') as f:
        json.dump(config_data, f, indent=4)

    # Check if .gitignore exists and add scribeconfig if it's not already there
    gitignore_path = os.path.join(codepath, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r+') as gitignore_file:
            content = gitignore_file.read()
            if 'scribeconfig' not in content:
                gitignore_file.write('\nscribeconfig\n')
                click.echo('Added scribeconfig to .gitignore')
            else:
                click.echo('scribeconfig already in .gitignore')
    else:
        with open(gitignore_path, 'w') as gitignore_file:
            gitignore_file.write('scribeconfig\n')
            click.echo('Created .gitignore and added scribeconfig')

@click.command()
@click.argument('file_path', type=click.Path(exists=False, writable=True))
@click.option('--prompt', help='Prompt for the write command')
@click.option('--references', multiple=True, type=click.Path(exists=True), help='Add references to other files if required')
def write(file_path, prompt, references):
    """Write to a file"""
    refs = []
    with open(file_path, 'r') as f:
        in_text=f.read()
    
    if prompt is None:
        prompt = input("Enter prompt: ")

    if references:
        for i, ref in enumerate(references):
            with open(ref, 'r') as rf:
                refs.append(
                    f"<reference_{i} input_path={ref}>\n{rf.read()}\n</reference_{i}>"
                )
    
    final_prompt = create_prompt(in_text,file_path,prompt, refs)
    click.echo("scribe AI is thinking...")

    resp = get_resp(final_prompt, "clean_resp")    
    show_gui(resp['code'], resp['explanation'], file_path)

@click.command()
@click.argument('file_paths', nargs=-1, type=click.Path(exists=False, writable=True))
@click.option('--prompt', help='Prompt for the multi-write command')
@click.option('--references', multiple=True, type=click.Path(exists=True), help='Add references to other files if required')
def multi_write(file_paths, prompt, references):
    """Write to multiple files"""
    if not file_paths:
        click.echo("No files specified. Please provide at least one file path.")
        return

    if prompt is None:
        prompt = input("Enter prompt for all files: ")
    
    files = []
    for i, file in enumerate(file_paths):
        with open(file, 'r') as rf:
                files.append(
                    f"<file_{i} input_path={file}>\n{rf.read()}\n</file_{i}>"
                )


    prompt = multi_parse(files,prompt)
    init_resp = get_resp(prompt,"clean_multi_resp")
    

    refs = []
    responses = []
    for file in init_resp:
        with open(file['file_path'], 'r') as f:
            in_text = f.read()
        
        if references:
            for i, ref in enumerate(references):
                with open(ref, 'r') as rf:
                    refs.append(
                        f"<reference_{i} input_path={ref}>\n{rf.read()}\n</reference_{i}>"
                    )
        
        final_prompt = create_prompt(in_text, file['file_path'], file['instruction'], refs)
        click.echo(f"scribe AI is thinking for {file['file_path']}...")

        resp = get_resp(final_prompt, "clean_resp")
        responses.append({'file_path': file['file_path'], 'code': resp['code'], 'explanation': resp['explanation']})

        # Add the current file as a reference for the next iterations
        refs.append(f"<reference_{len(refs)} input_path={file['file_path']}>\n{resp['code']}\n</reference_{len(refs)}>")

    show_multi_gui(responses)


main.add_command(init)
main.add_command(write)
main.add_command(multi_write)

if __name__ == '__main__':
    main()
