# API setup

## Access via Microsoft Entra ID RBAC

TODO: Steps to set up RBAC access to the API and backend services (e.g., PostgreSQL)

https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-configure-sign-in-azure-ad-authentication

## Create a Python virtual environment

Virtual environments in Python are essential for maintaining a clean and organized development space, allowing individual projects to have their own set of dependencies, isolated from others. This prevents conflicts between different projects and ensures consistency in your development workflow. By using virtual environments, you can manage package versions easily, avoid dependency clashes, and keep your projects running smoothly. It's a best practice that keeps your coding environment stable and dependable, making your development process more efficient and less prone to issues.

1. Using Visual Studio Code, open the folder into which you cloned the solution accelerator code repository for **Microsoft PostgreSQL Solution Accelerator - Build Your Own Copilot**.

2. In Visual Studio Code, open a new terminal window and change directories to the `src/api` folder.

3. Create a virtual environment named `.venv` by running the following command at the terminal prompt:

    ```bash
    python -m venv .venv 
    ```

    The above command will create a `.venv` folder under the `api` folder, which will provide a dedicated Python environment for the exercises in this lab.

4. Activate the virtual environment by selecting the appropriate command for your OS and shell from the table below and executing it at the terminal prompt.

    | Platform | Shell | Command to activate virtual environment |
    | -------- | ----- | --------------------------------------- |
    | POSIX | bash/zsh | `source .venv/bin/activate` |
    | | fish | `source .venv/bin/activate.fish` |
    | | csh/tcsh | `source .venv/bin/activate.csh` |
    | | pwsh | `.venv/bin/Activate.ps1` |
    | Windows | cmd.exe | `.venv\Scripts\activate.bat` |
    | | PowerShell | `.venv\Scripts\Activate.ps1` |

5. Install the libraries defined in `requirements.txt` by running the following:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file contains the set of Python libraries needed to run the solution accelerator.

    | Library | Version | Description |
    | ------- | ------- | ----------- |
    | `azure-identity` | 1.19.0 | Azure Identity SDK for Python |
    | `fastapi` | 0.115.6 | Web framework for building APIs with Python |
    | `langchain` | 0.3.13 | Framework for developing applications powered by large language models (LLMs) |
    | `langchain-openai` | 0.2.14 | LangChain library for connecting to and interacting with Azure OpenAI |
    | `openai` | 1.58.1 | Provides access to the Azure OpenAI REST API from Python apps. |
    | `pydantic` | 2.10.4 | Data validation using Python type hints. |
    | `requests` | 2.32.3 | Send HTTP requests. |
    | `uvicorn` | 0.34.0 | An ASGI web server implementation for Python. |

## Implement RAG with LangChain

TODO: Add steps for creating functions for communicating with the database via LangChain function calling (structured tools).

