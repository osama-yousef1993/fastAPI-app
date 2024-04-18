# fastAPI-app

## steps to build it to azure
- create resource group
- create postgresql database:
    - username: osama
    - password: osama1234567

- AZURE_WEBAPP_PUBLISH_PROFILE : az webapp deployment list-publishing-profiles --name fast-web-app --resource-group os-fastapi --xml
- AZURE_CREDENTIALS: az ad sp create-for-rbac --name "github-actions" --role contributor --scopes /subscriptions/6bdd5df9-6baf-48df-852c-4cf022de502d/resourceGroups/os-fastapi --sdk-auth