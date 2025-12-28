# 📁 Project Files Manifest

Complete list of all files in the AI Video Studio project.

## Root Directory

| File | Description |
|------|-------------|
| `README.md` | Main project documentation (Arabic) |
| `QUICKSTART.md` | Quick start guide for beginners |
| `CONTRIBUTING.md` | Contribution guidelines |
| `LICENSE` | MIT License |
| `docker-compose.yml` | Docker services configuration |
| `setup.sh` | Automated setup script |
| `check.sh` | System verification script |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore rules |

## Backend (`backend/`)

### Main Files
| File | Description |
|------|-------------|
| `main.py` | FastAPI application entry point |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Backend container configuration |
| `.env.example` | Backend environment template |
| `.gitignore` | Backend-specific ignore rules |

### Agents (`backend/agents/`)
| File | Description |
|------|-------------|
| `__init__.py` | Agents module initialization |
| `script_agent.py` | AI script generation (Groq API) |
| `voice_agent.py` | Text-to-speech (Edge-TTS) |
| `video_agent.py` | Video assembly (MoviePy) |

### API (`backend/api/`)
| File | Description |
|------|-------------|
| `__init__.py` | API module initialization |
| `routes.py` | API endpoints and handlers |
| `models.py` | Pydantic data models |

### Config (`backend/config/`)
| File | Description |
|------|-------------|
| `__init__.py` | Config module initialization |
| `settings.py` | Application settings and configuration |

### Services (`backend/services/`)
| File | Description |
|------|-------------|
| `__init__.py` | Services module initialization |
| `groq_service.py` | Groq API integration |
| `tts_service.py` | Edge-TTS integration |

## Frontend (`frontend/`)

### Main Files
| File | Description |
|------|-------------|
| `package.json` | Node.js dependencies and scripts |
| `next.config.js` | Next.js configuration |
| `tsconfig.json` | TypeScript configuration |
| `tailwind.config.js` | Tailwind CSS configuration |
| `postcss.config.js` | PostCSS configuration |
| `Dockerfile` | Frontend container configuration |
| `.env.example` | Frontend environment template |
| `.gitignore` | Frontend-specific ignore rules |

### App (`frontend/app/`)
| File | Description |
|------|-------------|
| `layout.tsx` | Root layout component |
| `page.tsx` | Main dashboard page |
| `globals.css` | Global CSS styles |

### Components (`frontend/components/`)
| Description |
|-------------|
| *Directory for reusable React components* |

## Documentation (`docs/`)

| File | Description |
|------|-------------|
| `API_EXAMPLES.md` | API usage examples and code samples |
| `ARCHITECTURE.md` | System architecture documentation |
| `DEPLOYMENT.md` | Deployment guide for various platforms |

## CI/CD (`.github/workflows/`)

| File | Description |
|------|-------------|
| `ci.yml` | GitHub Actions CI/CD pipeline |

## File Statistics

- **Total Files**: 41
- **Python Files**: 12
- **TypeScript/React Files**: 3
- **Configuration Files**: 8
- **Documentation Files**: 8
- **Shell Scripts**: 2
- **Docker Files**: 3

## Directory Structure Summary

```
ai-video-studio/
├── backend/           # Python FastAPI backend
│   ├── agents/        # Intelligent agents
│   ├── api/           # API routes and models
│   ├── config/        # Configuration
│   └── services/      # External service integrations
├── frontend/          # Next.js frontend
│   ├── app/           # Next.js app router
│   └── components/    # React components
├── docs/              # Documentation
└── .github/           # GitHub configuration
    └── workflows/     # CI/CD workflows
```

---

**Last Updated**: 2024-12-28
**Total Lines of Code**: ~2,700
**Documentation Words**: ~15,000
