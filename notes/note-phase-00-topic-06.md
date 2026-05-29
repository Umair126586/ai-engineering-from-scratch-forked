## Some rough commands (which I ran sequentially)
```bash
uv init my-ai-project
cd my-ai-project/
uv add numpy
uv add matplotlib

[project.optional-dependencies]
llm = ["anthropic>=0.39", "openai>=1.50"]

[tool.uv]
index-url = "https://pypi.org/simple"
extra-index-url = ["https://download.pytorch.org/whl/cpu"]

uv add torch --index-strategy unsafe-best-match
uv pip install -e ".[llm]"

uv pip compile pyproject.toml -o requirements.lock --index-strategy unsafe-best-match
uv pip install -r requirements.lock  --index-strategy unsafe-best-match
```

## Logical Understanding 
```bash
: '
This command launches a new python project with three files i.e., main.py, pyproject.toml and README.md
'
uv init my-ai-project

cd my-ai-project

: '
# Till now .venv does not exist. To make a virtual environment:
# 1. Run `uv add pkg-name` OR
# 2. RUn `uv venv`
'
uv add numpy matplotlib     #This also syncs with the pyproject.toml

: '
A little problem occurs on torch, if we simply run `uv add torch`, it will install torch with cuda
What if we need a cpu version of torch ?
It means we also need a registry or index URL here. 
'
uv add torch --index https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match    #This also adds the given index url to pyproject.toml file

: '
Now, using this command we basically compile the dependencies to one .lock file, from which we can reinstall. But again, here we will use --index-strategy unsafe-best-match to avoid uv looking into one registry for all dependencies
'
uv pip compile pyproject.toml -o requirements.lock --index-strategy unsafe-best-match

: '
Given below command does not only use requirements.lock file but behind the scenes, it also requires pyproject.toml file
'
uv pip install -r requirements.lock  --index-strategy unsafe-best-match
```

## Key Take aways
1. Conda env may be good if you want to manage some non-python libraries, for example, if you don't want to use a system-wide cuda-toolkit, you can create a conda environment and then install you own cuda-toolkit
2. When working in a conda environment, always install all the libraries with 'conda' first and then move to 'pip' only libraries
3. uv is the recommended way generally
4. Pytorch CUDA version must be smaller than Nvidia-cuda version
e.g.,
```bash
nvidia-smi                # shows driver CUDA version (e.g., 12.4)
python -c "import torch; print(torch.version.cuda)"  # shows PyTorch CUDA version
```