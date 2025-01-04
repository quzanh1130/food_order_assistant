from setuptools import setup, find_packages

setup(
    name='food_order_assistant',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pandas",
        "tqdm",
        "openai",
        "sentence-transformers",
        "elasticsearch",
        "psycopg2-binary"
    ],
    entry_points={
        'console_scripts': [
            'start-food-order-assistant=food_order_assistant.main:main',
        ],
    },
    author='Nguyen Quoc Anh (quzanh1130)',
    author_email='anhnq1130@gmail.com',
    description='A food order assistant application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/quzanh1130/food_order_assistant',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)