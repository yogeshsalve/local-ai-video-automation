# System Architecture

The Local AI Video Automation Platform converts a user-provided script
into a YouTube-ready video using locally running open-source technologies.

## High-Level Flow

Script
  ↓
AI Scene Planner
  ↓
Text-to-Speech
  ↓
Visual Generation
  ↓
Caption Generation
  ↓
Video Assembly
  ↓
MP4

## Planned Components

- Laravel
- Python
- FastAPI
- Ollama
- Local LLM
- Text-to-Speech
- Whisper
- FFmpeg
- PostgreSQL
- Redis
- Docker