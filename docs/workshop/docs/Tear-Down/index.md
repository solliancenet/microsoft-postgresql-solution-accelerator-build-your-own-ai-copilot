# Cleanup Resources

## 1. Give us a ⭐️ on GitHub

!!! task "FOUND THIS WORKSHOP AND SAMPLE USEFUL? MAKE SURE YOU GET UPDATES."

The **[PostgreSQL Solution Accelerator: Build Your Own AI Copilot](https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot)** sample is an actively updated project that will reflect the latest features and best practices for code-first development of RAG-based copilots on the Azure AI platform. **[Visit the repo](https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot)** or click the button below, to give us a ⭐️.

<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot" data-color-scheme="no-preference: light; light: light; dark: dark;" data-size="large" data-show-count="true" aria-label="Star solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot on GitHub"> Give the PostgreSQL Solution Accelerator a Star!</a>

---

## 2. Provide Feedback

Check that the right tab is selected for your session, and complete the steps!

=== "Self-Guided"

    !!! task "Reminder 1: Give us Feedback"

        Have feedback that can help us make this lab better for others? [Open an issue](https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot/issues/new) and let us know.

<!--
=== "Microsoft AI Tour"

    !!! task "Reminder 1: Give us Feedback"

        Visit [aka.ms/MicrosoftAITour/Survey](https://aka.ms/MicrosoftAITour/Survey) to give us feedback on this session (#WRK550)
      
    !!! danger "Reminder 2: End the Skillable Session"

        Visit the Skillable Lab page and click `End Session` to end the session and release all resources. This allows the lab to be run again without quota issues for others.

    
=== "Microsoft Ignite"

    !!! success "Reminder 1: Please Give us Feedback"

        Visit [aka.ms/MicrosoftIgniteEvals](https://aka.ms/MicrosoftIgniteEvals) to give us feedback on this session (LAB401)
      
    !!! warning "Reminder 2: End the Skillable Session"

        Visit the Skillable Lab page and click `End Session` to end the session and release all resources. This allows the lab to be run again without quota issues for others.
-->
---

## 3. Clean-up

Once you have completed this workshop, delete the Azure resources you created. You are charged for the configured capacity, not how much the resources are used. Follow these instructions to delete your resource group and all resources you created for this solution accelerator.

1. In VS Code, open a new integrated terminal prompt.

2. At the terminal prompt, execute the following command to delete the resources created by the deployment script:

    ```bash title=""
    azd down --purge
    ```

    !!! tip "The `--purge` flag purges the resources that provide soft-delete functionality in Azure, including Azure KeyVault and Azure OpenAI. This flag is required to remove all resources completely."

3. In the terminal window, you will be shown a list of the resources that will be deleted and prompted about continuing. Enter "y" at the prompt to being the resource deletion.

## 4. Persist changes to GitHub

If you want to save any changes you have made to files, use the Source Control tool in VS Code to commit and push your changes to your fork of the GitHub repo.
