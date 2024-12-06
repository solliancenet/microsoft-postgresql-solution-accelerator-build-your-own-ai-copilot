#!/bin/sh

# # Create the env-config.js file dynamically from environment variables
# echo "Generating env-config.js..."
# cat <<EOF > /usr/share/nginx/html/env-config.js
# window._env_ = {
#   SERVICE_API_ENDPOINT_URL: "$SERVICE_API_ENDPOINT_URL"
# };
# EOF

# ########################################################################################
# Replace API default URL with environment variable
# ########################################################################################

# Check if SERVICE_API_ENDPOINT_URL is set
if [ -z "$SERVICE_API_ENDPOINT_URL" ]; then
  echo "Error: SERVICE_API_ENDPOINT_URL is not set. Exiting."
  exit 1
fi

# Directory containing the files
TARGET_DIR="/usr/share/nginx/html"

# Old value to replace
OLD_VALUE="http://localhost:4242"

# Replace all instances of the old value with the new value
echo "Replacing '$OLD_VALUE' with '$SERVICE_API_ENDPOINT_URL' in files under $TARGET_DIR..."
find "$TARGET_DIR" -type f -exec sed -i "s|$OLD_VALUE|$SERVICE_API_ENDPOINT_URL|g" {} \;

echo "Replacement complete."

# ########################################################################################
# Start Nginx
# ########################################################################################
echo "Starting Nginx..."
nginx -g "daemon off;"
