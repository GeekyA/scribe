from setuptools import setup, find_packages

setup(
    name='scribe',            # Package name
    version='0.0.1',          # Version of the package
    packages=find_packages(), # Automatically find packages
    install_requires=[        # Dependencies
        'click==8.1.7',
        'anthropic==0.34.2'
    ],
    author='Ansh Chadha',       # Package author
    author_email='anshchadha9211@gmail.com', # Author email
    description='scribe is an AI coding assistant, it allows an LLM to talk to your codebase directly from your terminal',
    # python_requires='>=3.8.1',    # Python version requirement
    entry_points={
        'console_scripts': [
            'scribe=scribe_cli.scribe:main',
        ],
    },
)
