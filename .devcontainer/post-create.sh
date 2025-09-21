# Uninstall and reinstall Dapr to ensure the latest version is used
dapr uninstall
dapr init

# Install uv
wget -qO- https://astral.sh/uv/install.sh | sh