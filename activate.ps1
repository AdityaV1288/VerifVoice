# VerifVoice — one-step environment activation
# Usage (dot-source so PATH changes persist in your shell):
#   . .\activate.ps1
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1) activate the Python venv
& (Join-Path $root ".venv\Scripts\Activate.ps1")

# 2) put the bundled ffmpeg/ffprobe on PATH
$ff = Join-Path $root "tools\ffmpeg"
if (Test-Path $ff) { $env:PATH = "$ff;" + $env:PATH }

# 3) HuggingFace model downloads via mirror (huggingface.co is unreachable here)
if (-not $env:HF_ENDPOINT) { $env:HF_ENDPOINT = "https://hf-mirror.com" }

# 4) Person 1's audio-authenticity adapter (AASIST ONNX; laptop only — no s390x wheels)
if (-not $env:VERIFVOICE_ADAPTER) { $env:VERIFVOICE_ADAPTER = "aasist_onnx" }

Write-Host ""
Write-Host "VerifVoice environment ready." -ForegroundColor Green
Write-Host ("  python  : " + (Get-Command python -ErrorAction SilentlyContinue).Source)
Write-Host ("  ffmpeg  : " + (Get-Command ffmpeg -ErrorAction SilentlyContinue).Source)
Write-Host ("  ffprobe : " + (Get-Command ffprobe -ErrorAction SilentlyContinue).Source)
Write-Host ("  adapter : " + $env:VERIFVOICE_ADAPTER)
Write-Host ""
