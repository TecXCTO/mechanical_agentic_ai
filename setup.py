from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mechanical_agent_ai",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A mechanical agentic AI model for automation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mechanical-agentic-ai", # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.8',
    install_requires=[
        # Add your core dependencies here, matching requirements.txt
        # e.g., 'numpy>=1.20.0',
        # 'pandas>=1.3.0',
        'PyYAML>=5.4.1',
        # 'pytest',
        # 'matplotlib',
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
            "jupyter",
            "matplotlib",
            # Add other development dependencies here
        ],
        "ml": [
            # "tensorflow",
            # "torch",
            # "scikit-learn",
        ]
    },
    entry_points={
        # If you have command-line scripts, you can define them here
        # 'console_scripts': [
        #     'run-agent=src.cli:main',
        # ],
    },
)
