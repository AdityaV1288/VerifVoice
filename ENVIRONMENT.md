# VerifVoice — Environment Setup (Person 1 + Person 2)

Everything below is **pre-event environment preparation** (allowed). No submission code is here.

## 1. Activate the environment (Windows / PowerShell)

**One step (recommended):** dot-source the helper — it activates the venv AND puts ffmpeg/ffprobe on PATH:
```powershell
cd C:\Aditya\verifvoice_hackathon
. .\activate.ps1
```

**Manual equivalent:**
```powershell
cd C:\Aditya\verifvoice_hackathon
.\.venv\Scripts\Activate.ps1     # if execution policy blocks it, see note below
$env:PATH = "C:\Aditya\verifvoice_hackathon\tools\ffmpeg;" + $env:PATH
python --version                 # should print Python 3.12.7
```

**Execution policy note:** if `Activate.ps1` is blocked, run once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
(or use the CMD activate: `.\.venv\Scripts\activate.bat`)

## 2. Verify the install (smoke test)

```powershell
python -c "import numpy, scipy, pandas, librosa, soundfile, pydub, sklearn, onnx, onnxruntime, skl2onnx, torch, torchaudio, transformers, faster_whisper, fastapi, uvicorn, pydantic, httpx, imageio_ffmpeg, tqdm; print('ALL IMPORTS OK')"
```

## 3. ffmpeg / ffprobe (for mp3/m4a decoding + Whisper)

There is **no system ffmpeg**. A full static build is installed at
`C:\Aditya\verifvoice_hackathon\tools\ffmpeg\` containing **`ffmpeg.exe` + `ffprobe.exe`** (gyan.dev
release-essentials + BtbN shared build, ffmpeg 7.1). It is wired into the environment by `. .\activate.ps1`
(adds `tools\ffmpeg` to `PATH`).

> **Important:** `pydub` resolves `ffmpeg`/`ffprobe` by searching `PATH` (not the `AudioSegment.converter`
> attribute in this version), so **PATH is the reliable method** — use `activate.ps1`. `librosa`/`soundfile`
> read WAV with no ffmpeg at all, and `faster-whisper` decodes via its bundled PyAV (`av`), so ffmpeg is
> optional for the core WAV path.

> `tools\ffmpeg\` is **gitignored** (binaries don't belong in the repo). Team members recreate it by either
> re-downloading the gyan.dev/BtbN build or relying on `import imageio_ffmpeg; imageio_ffmpeg.get_ffmpeg_exe()`
> (bundled ffmpeg, no ffprobe).

## 4. What's installed (and who uses it)

| Area | Packages | Used by |
|---|---|---|
| Core | numpy, scipy, pandas, python-dotenv | all |
| Audio | librosa, soundfile, pydub, resampy | **Person 1** |
| ML | scikit-learn, joblib | P1 fallback classifier, P2 optional classifier |
| ONNX | onnx, onnxruntime, skl2onnx | **Person 1** (LinuxONE/zDLC path) |
| Deep learning | torch, torchaudio, transformers | P1 (AASIST-family) |
| ASR | faster-whisper | P2 (optional transcription) |
| ffmpeg | imageio-ffmpeg | audio decoding |
| Backend | fastapi, uvicorn, pydantic, httpx | Person 3 (integration testing) |
| Utils | tqdm | all |

## 4.5 ASR model download (faster-whisper) + HuggingFace mirror

`faster-whisper` needs a model checkpoint on first use. **`huggingface.co` is unreachable from this network**
(connection timeout), so downloads go through **`https://hf-mirror.com`** instead. This is already wired in:

- `activate.ps1` sets `HF_ENDPOINT=https://hf-mirror.com` for the session.
- `semantic_model._get_model()` calls `os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")` as a
  fallback, so transcription works even if you forgot to source `activate.ps1`.

To pre-download the model now (one-time, ~140 MB → caches under `~/.cache/huggingface`):

```powershell
$env:HF_ENDPOINT = "https://hf-mirror.com"
.\.venv\Scripts\python.exe -c "from faster_whisper import WhisperModel; WhisperModel('base', device='cpu', compute_type='int8'); print('cached')"
```

> If ASR can't be set up on a given machine (e.g. LinuxONE s390x), **it is not a blocker**: Person 2's rule
> engine runs on **scripted transcripts** (`input_type="text"`) — a first-class supported path.

**Known incompatibility (worked around):** `faster-whisper 1.2.1` + `av >= 15` — faster-whisper's built-in
`av.decode_audio()` passes a `metadata_errors=` kwarg that newer PyAV removed, raising a `TypeError`. Our
`transcribe()` **bypasses this** by decoding audio with `librosa` and passing a numpy array to faster-whisper
(which then skips its own `av` decoder). No `av` downgrade needed — leave `av==19.0.1`.

## 5. Add a package later

```powershell
.\.venv\Scripts\python.exe -m pip install <package>
.\.venv\Scripts\python.exe -m pip freeze > requirements.lock.txt
```

## 6. IMPORTANT — LinuxONE (s390x) is a DIFFERENT machine

This venv is your **laptop** (Windows x86_64). The assigned **LinuxONE Community Cloud VM is s390x** —
some wheels (especially **PyTorch**) may not exist there. Person 3 must verify on the VM:

```bash
uname -m            # confirm s390x
python3 --version
which podman docker # container tooling?
```

**Fallback plan (already agreed):**
- If **torch/AASIST** won't run on s390x → Person 1 uses the **MFCC + sklearn** fallback (numpy/sklearn are
  portable) or marks audio authenticity as a labeled future module; the **semantic model (Person 2, rules-only)
  becomes primary**.
- If **librosa/soundfile** won't install on s390x → pre-extract features on the laptop, send feature vectors
  to the server (keep the boundary explicit in the demo).
- Keep the risk engine, token service, and payment simulator on LinuxONE regardless.

## 7. Reproducibility

- `requirements.txt` = curated, human-readable list.
- `requirements.lock.txt` = exact installed versions (generated via `pip freeze`) — commit this so the whole
  team runs identical versions.
