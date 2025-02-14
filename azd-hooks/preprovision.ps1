# Get the user principal name of the signed-in user and write it to the .env file for the azd environment
$env:AZURE_PRINCIPAL_NAME = $(az ad signed-in-user show --query 'userPrincipalName' -o tsv)

# write AZURE_PRINCIPAL_NAME to azd environment variables
azd env set "AZURE_PRINCIPAL_NAME" "$env:AZURE_PRINCIPAL_NAME"