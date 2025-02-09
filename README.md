# Project Guide

## 1. Install UV - Python Package Manager (better than pip)

- #### For Mac/Linux
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

- #### For Windows
    ```PowerShell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

- To update uv: `uv self update`

## 2. Project Setup
```bash
https://github.com/lkx100/Linear-Programing-Solver.git
cd Linear-Programing-Solver
```

## 3. Install dependencies
```bash
uv sync
```

## 4. Run the project
```bash
uv run manage.py runserver
```  

***

If you need a full guide on how to install uv, you can read my blog [here](https://acecoderbeta.onrender.com/blogpost/post/best-python-package-manager-uv/) or check out for the [official documentation](https://docs.astral.sh/uv/).
