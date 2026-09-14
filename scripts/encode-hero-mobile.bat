@echo off
REM ==============================================================================
REM Marnie Aesthetics — Script de Otimizacao de Video Mobile da Hero
REM ==============================================================================

set INPUT="media\versao mobile.mp4"
set OUTPUT_MP4="media\hero-video-mobile.mp4"
set OUTPUT_WEBM="media\hero-video-mobile.webm"
set OUTPUT_THUMB="media\video-preview-thumb-mobile.jpg"

echo [1/3] Gerando versao MP4 mobile otimizada (H.264, sem audio, faststart)...
ffmpeg -i %INPUT% -an -vcodec libx264 -crf 26 -preset slow -movflags +faststart -y %OUTPUT_MP4%

echo [2/3] Gerando versao WebM mobile otimizada (VP9, sem audio)...
ffmpeg -i %OUTPUT_MP4% -an -c:v libvpx-vp9 -crf 32 -b:v 0 -deadline realtime -cpu-used 4 -row-mt 1 -y %OUTPUT_WEBM%

echo [3/3] Extraindo thumbnail mobile...
ffmpeg -ss 00:00:03 -i %OUTPUT_MP4% -frames:v 1 -q:v 2 -y %OUTPUT_THUMB%

echo Otimizacao mobile concluida com sucesso!
echo Arquivos gerados em media/:
dir media\*mobile*
