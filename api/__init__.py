"""
Vercel serverless function handler.
"""

from api.summarize import app

# Export for Vercel
__all__ = ['app']
