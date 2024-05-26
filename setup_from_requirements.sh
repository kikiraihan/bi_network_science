rm poetry.lock
rm pyproject.toml

poetry init -n --no-interaction

while IFS= read -r line || [ -n "$line" ]; do poetry add "$line"; done < requirements.txt