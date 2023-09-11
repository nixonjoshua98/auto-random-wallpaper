$currentDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition

$pythonRunScript = Join-Path -Path $currentDirectory -ChildPath '\run.py'

$activateScriptPath = Join-Path -Path $currentDirectory -ChildPath '\venv\scripts\activate.ps1'

Invoke-Expression -Command $activateScriptPath

python $pythonRunScript

deactivate