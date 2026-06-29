with open("frontend/src/features/researchSuggestions/api/index.ts", "r") as f:
    content = f.read()

content = content.replace("headers: {", "headers: {\n      'Authorization': `Bearer ${localStorage.getItem('token')}`,")

with open("frontend/src/features/researchSuggestions/api/index.ts", "w") as f:
    f.write(content)
