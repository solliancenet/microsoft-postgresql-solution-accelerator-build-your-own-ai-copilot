# Exit on error
$ErrorActionPreference = "Stop"

# Download model from Hugging Face
Write-Output "Downloading bge-reranker-v2-m3 model from Hugging Face.."
$MODEL_DIR = "./scripts/aml/model_asset/model"
New-Item -ItemType Directory -Force -Path $MODEL_DIR


$FILES = @(
 "config.json"
 "model.safetensors"
 "sentencepiece.bpe.model"
 "special_tokens_map.json"
 "tokenizer.json"
 "tokenizer_config.json"
)
$BASE_URL = "https://huggingface.co/BAAI/bge-reranker-v2-m3/resolve/main"

foreach ($FILE in $FILES) {
  $FILE_PATH = Join-Path $MODEL_DIR $FILE
  if (-Not (Test-Path $FILE_PATH)) {
    try {
        $content = Invoke-WebRequest -Uri "$BASE_URL/$FILE" -OutFile "$FILE_PATH"
        Write-Output "- $FILE downloaded successfully."
    } catch {
        Write-Error "Failed to download $FILE from $BASE_URL"
    }
  } else {
    Write-Output "- $FILE already exists - skipping download."
  }
}

# Deploy model to Azure Machine Learning Workspace
az account set --subscription "$env:AZURE_SUBSCRIPTION_ID"

# create variable for AML Deployment Name
$DEPLOYMENT_NAME = "bgev2m3-v1"
$DEPLOYMENT_YML = "./scripts/aml/model_asset/deployment.yml"
az ml online-deployment create --name "$DEPLOYMENT_NAME" --endpoint "$env:AZURE_AML_ENDPOINT_NAME" -f "$DEPLOYMENT_YML" --all-traffic --resource-group "$env:AZURE_RESOURCE_GROUP" --workspace-name "$env:AZURE_AML_WORKSPACE_NAME"