# web-scrapper

### Installation
You need `python 3.12`

1. Install `Poetry`
For Linux, macOS, Windows (WSL) run:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Create a poetry shell with a python 3.12 executable.
```bash
poetry en use <path-to-python3.12-executable>/bin/python
```

3. Create a poetry shell
```bash
poetry shell
```

4. Install dependencies
```bash
poetry install
```

5. Install pre-commit
```bash
poetry run pre-commit install
```

6. Install `chromedriver`

7.  Create a `.env` file at the root of the repository and add your OPENAI API KEY
```.env
OPENAI_API_KEY=<your-api-key>
```

8. Run the `main.py` script:
```bash
poetry run python main.py
```

The extracted offers will be saved to `extracted_offers.json`
