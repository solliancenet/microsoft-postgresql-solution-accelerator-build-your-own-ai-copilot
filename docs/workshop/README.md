# PostgreSQL Solution Accelerator - Build your own AI Copilot for FSI with PostgreSQL: Hands-on Workshop

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://github.com/codespaces/new?hide_repo_select=true&machine=basicLinux32gb&repo=725257907&ref=main&devcontainer_path=.devcontainer%2Fdevcontainer.json&geo=UsEast)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/azure-samples/contoso-chat)

---

## About the PostgreSQL Solution Accelerator - Build your own AI Copilot for FSI with PostgreSQL

This resource is both a solution accelerator and a learning tool for developers who want to create AI-powered solutions using Azure Database for PostgreSQL and Azure AI Services. The **Woodgrove Bank** solution is an actively updated project that will reflect the latest features and best practices for development of AI-enabled applications and RAG-based copilots on the Azure AI platform.

**The current version of the sample follows this high-level architecture**.

![High-level architecture diagram for the solution](./docs/img/solution-architecture-diagram.png)

## Workshop Guide

The current repository is instrumented with a `docs/workshop/` folder that contains the step-by-step lab guide for developers, covering the entire workflow from resource provisioning to ideation, evaluation, deployment, and usage.

You can view [a hosted version of the workshop guide](https://solliancenet.github.io/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot) on GitHub Pages for quick reference. You can also **preview and extend** the workshop directly from this source by running the [MKDocs](https://www.mkdocs.org/) pages locally:

1. Install the `mkdocs-material` package

    ```bash
    pip install mkdocs-material
    ```

2. Run the `mkdocs serve` command from the `workshop` folder

    ```bash
    cd docs/workshop
    mkdocs serve -a localhost:5000
    ```

This should run the dev server with a preview of the workshop guide on the specified local address. Simply open a browser and navigate to `http://localhost:5000` to view the content.

(Optional) If you want to deploy the workshop guide to a live site, you can use the `mkdocs gh-deploy` command to push the content to a GitHub Pages site.
