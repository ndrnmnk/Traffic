#!/bin/bash

echo "Checking for Python installation..."
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found. Please install it from https://www.python.org/downloads/ and try again."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Installing requirements..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "Creating launch script..."
cat > launch.sh <<EOL
#!/bin/bash
source venv/bin/activate
python3 main.py
EOL

chmod +x launch.sh

echo "Setup complete! Use 'launch.sh' to start the project."
