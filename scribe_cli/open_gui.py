
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk

def show_multi_gui(responses):
    # Initialize tkinter window
    root = tk.Tk()
    root.title("Generated Code and Explanations")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    for response in responses:
  
        # Create a frame for each file
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=response['file_path'])

        # Create a scrolled text widget for displaying the code
        code_label = tk.Label(frame, text="Generated Code:")
        code_label.pack()
        code_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
        code_text.insert(tk.END, response['code'])
        code_text.configure(state='disabled')
        code_text.pack()

        # Create a scrolled text widget for displaying the explanation
        explanation_label = tk.Label(frame, text="Explanation:")
        explanation_label.pack()
        explanation_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=10)
        explanation_text.insert(tk.END, response['explanation'])
        explanation_text.configure(state='disabled')
        explanation_text.pack()

        # Accept button
        def accept(file_path=response['file_path'], code=response['code']):
            with open(file_path, 'w') as f:
                f.write(code)
            messagebox.showinfo("Success", f"Code accepted and written to {file_path}")

        # Reject button
        def reject(file_path=response['file_path']):
            messagebox.showinfo("Cancelled", f"Code was not written to {file_path}")

        # Add buttons for Accept and Reject
        accept_button = tk.Button(frame, text="Accept", command=accept)
        accept_button.pack(side=tk.LEFT, padx=10, pady=10)

        reject_button = tk.Button(frame, text="Reject", command=reject)
        reject_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

def show_gui(code, explanation, file_path):
    show_multi_gui([{'file_path': file_path, 'code': code, 'explanation': explanation}])
