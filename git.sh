#!/bin/bash

# Initialize git repo
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: add ollama_starter project"

# Set main branch
git branch -M main

# Add remote (replace placeholders)
git remote add origin https://github.com/your-username/repo-name.git

# Push to GitHub
git push -u origin main

echo "Project pushed to GitHub successfully."
