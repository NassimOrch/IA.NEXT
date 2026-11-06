@echo off
setlocal
cd /d "%~dp0"
echo NGeGenBrain v3 archives are single-part releases; no reassembly is required.
echo If a future release is split, concatenate parts in listed order and verify SHA-256.
exit /b 0
