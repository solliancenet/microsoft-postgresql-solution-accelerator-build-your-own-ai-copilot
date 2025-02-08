# Prerequisites

Select the tab of your chosen track for details about what you need to do before starting the workshop, what you are expected to know beforehand, and what you can expect to take away after completing it.

=== "Self-Guided"

    Expand each block below and review the requirements within each.

    ???+ info "1. What You Need"   

        1. **Your own computer.**
            - Any computer capable of running Visual Studio Code, Docker Desktop, and a modern web browser will do.
            - You must have the ability to install software on the computer.
            - We recommend installing a recent version of Edge, Chrome, or Safari.
        2. **A GitHub Account.**
            - This is required to create a copy (known as a fork) of the sample repository.
            - We recommend using a personal (vs. enterprise) GitHub account for convenience.
            - If you don't have a GitHub account, [sign up for a free one](https://github.com/signup) now. (It takes just a few minutes.)
        3. **An Azure Subscription.**
            - This is needed to provision the Azure infrastructure for your AI project.
            - If you don't have an Azure account, [sign up for a free one](https://aka.ms/free) now. (It takes just a few minutes.)
        4. **Sufficient Azure ML Online Endpoint CPU quota**
            - To run the solution accelerator's **Semantic Ranker** element, you must have at least 32 **Standard DASv4 Family Cluster Dedicated vCPUs** cores available within your subscription. Detailed instructions are provided in the setup section to verify this in your subscription.
            
    ??? info "2. What You Should Know (expand to view)"   

        **Recommended knowledge and experience**

        1. **Familiarity with Visual Studio Code** 
            - The default editor used in this workshop is Visual Studio Code. You will configure your VS Code development environment with the required extensions and code libraries.
            - The workshop requires Visual Studio Code and other tools to be installed on your computer. You will be running the solution code from your local computer.    
        2. **Familiarity with the Azure portal**
            - The workshop assumes you are familiar with navigating to resources within the Azure portal.
            - You will use the Azure portal to retrieve endpoints, keys, and other values associated with the resources you deploy for this workshop.
        3. **Familiarity with PostgreSQL**
            - The workshop assumes you are familiar with basic SQL syntax.
            - You will be executin SQL statements to alter tables, create extensions, and run queries against tables.

        **Preferred knowledge and experience**

        4. **Familiarity with `git` operations**
            - You will be forking the sample repository into your GitHub account.
            - You will be committing code changes to your forked repo.
        5. **Familiarity with the `bash` shell**.
            - If needed, you will use `bash` in the VS Code terminal to run post-provisioning scripts.
            - You will also use it to run Azure CLI and Azure Developer CLI commands during setup. 
        6.  **Familiarity with Python and JavaScript UI frameworks**.
            - You will modify REACT JavaScript and Python code to implement changes to the starter solution.
            - In some steps, you will create and run Python code from the command line and VS Code.
            - You will select a Python kernel and run pre-existing scripts in some steps.

    ??? info "3. What You Will Take Away (expand to view)"   

        After completing this workshop, you will have:
        
        7.  A personal fork (copy) of the [Build Your Own AI Copilot for FSI with PostgreSQL](https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot) repository in your GitHub profile. This repo contains all the materials you need to reproduce the workshop later (e.g., as a _Self-Guided_ session).
        8.  Hands-on understanding of the [Azure AI Foundry](https://ai.azure.com) portal and relevant developer tools (e.g., Azure Developer CLI, Prompty, FastAPI) to streamline end-to-end development workflows for your own AI apps.
        9.  An understanding of how Azure AI services can be integrated into applications to create powerful AI-enabled applications.

=== "Instructor-Led Workshop"

    Expand each block below and review the requirements within each.

    <!-- ???+ info "1. What You Need"   
    
        The instructor-guided labs are set up with everything you need to get started. To get the most from this session, please review the recommended and preferred knowledge and experience in the blocks below. _If you revisit the workshop later at home, use the [Self-Guided version](./../1-Provision-And-Setup/03-Self-Guided.md) instead_. -->

    ???+ info "1. What You Need"   

        1. **Your own computer.**
            - Any computer capable of running Visual Studio Code, Docker Desktop, and a modern web browser will do.
            - You must have the ability to install software on the computer.
            - We recommend installing a recent version of Edge, Chrome, or Safari.
        2. **A GitHub Account.**
            - This is required to create a copy (known as a fork) of the sample repository.
            - We recommend using a personal (vs. enterprise) GitHub account for convenience.
            - If you don't have a GitHub account, [sign up for a free one](https://github.com/signup) now. (It takes just a few minutes.)
        3. **An Azure Subscription.**
            - This is needed to provision the Azure infrastructure for your AI project.
            - If you don't have an Azure account, [sign up for a free one](https://aka.ms/free) now. (It takes just a few minutes.)
        4. **Sufficient Azure ML Online Endpoint CPU quota**
            - To run the solution accelerator's **Semantic Ranker** element, you must have at least 32 **Standard DASv4 Family Cluster Dedicated vCPUs** cores available within your subscription. Detailed instructions are provided in the setup section to verify this in your subscription.

    ??? info "2. What You Should Know (expand to view)"   

        **Recommended knowledge and experience**

        1. **Familiarity with Visual Studio Code** 
            - The default editor used in this workshop is Visual Studio Code. You will configure your VS Code development environment with the required extensions and code libraries.
            - The workshop requires Visual Studio Code and other tools to be installed on your computer. You will be running the solution code from your local computer.    
        2. **Familiarity with the Azure portal**
            - The workshop assumes you are familiar with navigating to resources within the Azure portal.
            - You will use the Azure portal to retrieve endpoints, keys, and other values associated with the resources you deploy for this workshop.
        3. **Familiarity with PostgreSQL**
            - The workshop assumes you are familiar with basic SQL syntax.
            - You will be executin SQL statements to alter tables, create extensions, and run queries against tables.

        **Preferred knowledge and experience**

        4. **Familiarity with `git` operations**
            - You will be forking the sample repository into your GitHub account.
            - You will be committing code changes to your forked repo.
        5. **Familiarity with the `bash` shell**.
            - If needed, you will use `bash` in the VS Code terminal to run post-provisioning scripts.
            - You will also use it to run Azure CLI and Azure Developer CLI commands during setup. 
        6.  **Familiarity with Python and JavaScript UI frameworks**.
            - You will modify REACT JavaScript and Python code to implement changes to the starter solution.
            - In some steps, you will create and run Python code from the command line and VS Code.
            - You will select a Python kernel and run pre-existing scripts in some steps.

    ??? info "3. What You Will Take Away (expand to view)"   

        After completing this workshop, you will have:
        
        7.  A personal fork (copy) of the [Build Your Own AI Copilot for FSI with PostgreSQL](https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot) repository in your GitHub profile. This repo contains all the materials you need to reproduce the workshop later (e.g., as a _Self-Guided_ session).
        8.  Hands-on understanding of the [Azure AI Foundry](https://ai.azure.com) portal and relevant developer tools (e.g., Azure Developer CLI, Prompty, FastAPI) to streamline end-to-end development workflows for your own AI apps.
        9.  An understanding of how Azure AI services can be integrated into applications to create powerful AI-enabled applications.
