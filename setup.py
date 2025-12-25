
from setuptools import setup, find_packages

setup(
    name='mech_agent_ai',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add core dependencies from requirements.txt if desired
    ],
    entry_points={
        'console_scripts': [
            'mech_ai_run = src.main:main', # Example: allows 'mech_ai_run task params'
        ],
    },
    python_requires='>=3.7',
)
