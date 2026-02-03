"""
Vercel entry point for the API.
Maps to /api/summarize endpoint.
"""

from api.summarize import app as handler

# Vercel expects this export
__all__ = ['handler']
