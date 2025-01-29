import os

class PromptService:
    def __init__(self):
        # Set the prompt directory path to the prompts folder in this project
        self.prompt_directory = os.path.join(os.path.dirname(__file__), "../prompts")
        # Create a dictionary from the content of the files in the prompt directory
        self.prompts = self.__load_prompts()
        
    def __load_prompts(self):
        """Load the prompts from text files in the prompts directory."""
        # Initialize an empty dictionary to store the prompts
        prompts = {}
        # Iterate over the files in the prompt directory
        for filename in os.listdir(self.prompt_directory):
            # Check if the file is a text file
            if filename.endswith(".txt"):
                # Get the name of the prompt from the filename, minus its extension
                prompt_name = filename.replace('.txt', '')
                # Open the file and read the content
                with open(os.path.join(self.prompt_directory, filename), "r") as file:
                    # Add the content to the prompts dictionary with the filename (without extension) as the key
                    prompts[prompt_name] = file.read()
        return prompts
    
    def get_prompt(self, name: str):
        """Gets a prompt by name."""
        # Return the prompt from the repository
        return self.prompts.get(name)