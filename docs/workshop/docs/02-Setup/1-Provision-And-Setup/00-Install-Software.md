# Install Software

You will need to install the required software locally and provision the Azure infrastructure yourself, as described on the tabs below.

## 1. Install Software

The required development environment uses a Visual Studio (VS) Code editor with a Python runtime. To complete this lab on your own computer, you must install the following required software. On completing this step, you should have installed:

- [X] Azure command-line tools
- [X] Git
- [X] Python 3.11+
- [X] Node.js
- [X] Docker desktop
- [X] Visual Studio Code and required extensions
- [X] pgAdmin

## **1.1 Install Azure command-line tools**

!!! note "In this task, you will install both the Azure CLI and the Azure Developer CLI (`azd`)."

    - The Azure CLI enables you to execute Azure CLI commands from a command prompt or VS Code terminal on your local machine.
    - The Azure Developer CLI (`azd`) is an open-source tool that accelerates provisioning and deploying app resources on Azure.

1. Install or upgrade to the latest version of the [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest) by following the instructions for your OS at <https://learn.microsoft.com/cli/azure/install-azure-cli>

    !!! info "Upgrade to latest version of Azure CLI"

        If you already have the Azure CLI installed, you'll need to be sure to upgrade to the latest version. This guide required v2.69.0 or greater. You can use this command to upgrade to the latest version:

        ```azurecli title=""
        az upgrade
        ```

2. Once installed, open a command prompt on your machine and verify the installation by running the following:

    ```azurecli title=""
    az version
    ```

3. Next, install the `ml` extension to the Azure CLI.

    !!! info "About the ml extension"

        The `ml` extension to the Azure CLI is the enhanced interface for Azure Machine Learning. It enables you to train and deploy models from the command line, with features that accelerate scaling data science up and out while tracking the model lifecycle.

    To install the `ml` extension you should first remove any existing installation of the extension and also the CLI v1 `azure-cli-ml` extension:

    ```azurecli title=""
    az extension remove -n azure-cli-ml
    az extension remove -n ml
    ```

    Then, run the following to install the latest version of the `ml` extension:

    ```azurecli title=""
    az extension add -n ml
    ```

4. Install or upgrade Azure Developer CLI to the latest version by following the instructions for your OS at <https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd>.

    !!! info "Upgrade to latest version of Azure Developer CLI"

        If you already have the Azure Developer CLI installed, you'll need to be sure to upgrade to the latest version. This guide required v1.12 or greater.

5. Execute the following command from a terminal prompt to verify the tools were installed:
    
    ```bash title=""
    azd version
    ```

## **1.2 Install Git**

Git enables you to manage your code by tracking changes, maintaining a version history, and facilitating collaboration with others. This helps in organizing and maintaining the integrity of your project's development.

1. Download Git from <https://git-scm.com/downloads>.

2. Run the installer using the default options.

## **1.3 Install Python**

Python is the programming used to build the backend API for the solution. By utilizing Python's versatile programming capabilities and Azure Database for PostgreSQL's generative AI and vector search capabilities, you can create powerful and efficient AI copilots and streamlining complex workflows.

1. Download Python 3.11+ from <https://python.org/downloads>.

2. Run the installer using the default options.

3. Use the following command from a terminal prompt to verify Python was installed:

    ```bash title=""
    python --version
    ```

## **1.4 Install Node.js**

Node.js is an open-source runtime environment that lets you run JavaScript code outside of a browser. It's ideal for building scalable network applications and works seamlessly with REACT single-page applications by providing a backend environment to handle server-side logic and API requests. This allows for efficient development and smooth interactions between the frontend and backend.

1. Download Node.js from <https://nodejs.org/en/download/>, ensuring you select the most recent LTS version and your correct OS.

2. Run the installer using the default options.

## **1.5 Install Docker Desktop**

Docker Desktop is an application that allows you to build, share, and run containerized applications on your local machine. It provides a user-friendly interface to manage Docker containers, images, and networks. By streamlining the containerization process, Docker Desktop helps you develop, test, and deploy applications consistently across different environments.

1. Download and install Docker Desktop for your OS using instructions provided on the <https://docs.docker.com/desktop/>:

        - [Linux](https://docs.docker.com/desktop/setup/install/linux/)
        - [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
        - [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

## **1.6 Install Visual Studio Code (and extensions)**

Visual Studio Code is a versatile, open-source code editor that combines powerful features with an intuitive interface to help you efficiently write, debug, and customize projects.

1.  Download and install from <https://code.visualstudio.com/download>.

    - Use the default options in the installer.

2.  After installation completed, launch Visual Studio Code.

3.  In the **Extensions** menu, search for and install the following extensions from Microsoft:

    - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

4.  Close VS Code.

## **1.7 Install pgAdmin**

Throughout this workshop, you will use pgAdmin to run queries against your PostgreSQL database. pgAdmin is the leading Open Source management tool for Postgres.

1.  Download pgAdmin from <https://www.pgadmin.org/download/>.

2.  Run the installer using the default options.

---
