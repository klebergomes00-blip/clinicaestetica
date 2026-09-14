#!/usr/bin/env bash
# ==============================================================================
# Marnie Aesthetics — Script de Otimização e Remoção de Áudio de Vídeo da Hero
# ==============================================================================
set -e

INPUT="media/Design sem nome (7).mp4"
OUTPUT_MP4="media/hero-video-final.mp4"
OUTPUT_WEBM="media/hero-video-final.webm"

echo "[1/2] Gerando versao MP4 otimizada (H.264, sem audio, faststart)..."
ffmpeg -i "$INPUT" -an -vcodec libx264 -crf 26 -preset slow -movflags +faststart -y "$OUTPUT_MP4"

echo "[2/2] Gerando versao WebM otimizada (VP9, sem audio)..."
ffmpeg -i "$OUTPUT_MP4" -an -c:v libvpx-vp9 -crf 32 -b:v 0 -deadline realtime -cpu-used 4 -row-mt 1 -y "$OUTPUT_WEBM"

echo "Otimizacao concluida com sucesso!"
ls -lh media/hero-video-final.*
