"""Advanced professional visual asset management system for business websites"""

import asyncio
import aiohttp
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
import hashlib
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ProfessionalAssetManager:
    """
    Advanced asset management system for professional business websites.
    Provides contextual, high-quality images with intelligent fallbacks.
    """
    
    def __init__(self):
        self.cache_dir = Path("app/static/images/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = timedelta(hours=24)
        
        # Professional business image categories
        self.business_categories = {
            "business-team": ["business", "team", "office", "professional"],
            "technology-consulting": ["technology", "consulting", "computer", "business"],
            "business-strategy": ["strategy", "planning", "business", "meeting"],
            "digital-transformation": ["digital", "technology", "innovation", "business"],
            "professional-team": ["team", "business", "professional", "office"],
            "modern-office": ["office", "workspace", "modern", "business"],
            "team-meeting": ["meeting", "business", "team", "conference"],
            "workspace": ["workspace", "office", "desk", "computer"],
            "professional-woman": ["business", "woman", "professional", "portrait"],
            "professional-man": ["business", "man", "professional", "portrait"],
            "business-woman": ["business", "woman", "suit", "professional"],
            "business-consulting": ["consulting", "business", "meeting", "professional"],
            "technology-stack": ["technology", "computer", "software", "coding"],
            "cloud-computing": ["cloud", "technology", "server", "computing"],
            "data-analytics": ["data", "analytics", "chart", "business"],
            "cybersecurity": ["security", "technology", "protection", "cyber"],
            "mobile-development": ["mobile", "app", "development", "technology"],
            "ai-machine-learning": ["artificial intelligence", "machine learning", "technology", "future"],
            "business-meeting": ["meeting", "business", "conference", "professional"],
            "modern-office-space": ["office", "modern", "workspace", "interior"],
            "business-insights": ["business", "insights", "data", "analytics"],
            "technology-trends": ["technology", "trends", "innovation", "future"],
            "business-growth": ["growth", "business", "success", "chart"],
            "digital-innovation": ["digital", "innovation", "technology", "future"]
        }
        
        # Unsplash API configuration
        self.unsplash_access_key = "YOUR_UNSPLASH_ACCESS_KEY"  # Replace with actual key
        self.unsplash_base_url = "https://api.unsplash.com"
        
        # Fallback image services
        self.fallback_services = [
            "https://picsum.photos",
            "https://source.unsplash.com"
        ]
    
    async def get_image(self, category: str, width: int = 800, height: int = 600) -> Optional[str]:
        """
        Get a professional image for the specified category.
        Returns cached image URL or fetches new one with fallbacks.
        """
        try:
            # Generate cache key
            cache_key = self._generate_cache_key(category, width, height)
            cached_url = await self._get_cached_image(cache_key)
            
            if cached_url:
                return cached_url
            
            # Try to fetch from Unsplash
            image_url = await self._fetch_from_unsplash(category, width, height)
            
            if not image_url:
                # Fallback to other services
                image_url = await self._fetch_fallback_image(category, width, height)
            
            if image_url:
                await self._cache_image_url(cache_key, image_url)
                return image_url
            
            # Final fallback to local placeholder
            return self._get_local_placeholder(width, height)
            
        except Exception as e:
            logger.error(f"Error fetching image for category {category}: {e}")
            return self._get_local_placeholder(width, height)
    
    async def get_image_gallery(self, categories: List[str], width: int = 400, height: int = 300) -> List[str]:
        """Get multiple images for a gallery"""
        tasks = [self.get_image(category, width, height) for category in categories]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None values
        images = [img for img in results if isinstance(img, str) and img]
        return images
    
    async def _fetch_from_unsplash(self, category: str, width: int, height: int) -> Optional[str]:
        """Fetch image from Unsplash API"""
        try:
            if not self.unsplash_access_key or self.unsplash_access_key == "YOUR_UNSPLASH_ACCESS_KEY":
                return None
            
            keywords = self.business_categories.get(category, [category])
            query = " ".join(keywords)
            
            headers = {"Authorization": f"Client-ID {self.unsplash_access_key}"}
            params = {
                "query": query,
                "orientation": "landscape",
                "per_page": 1,
                "order_by": "relevant"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.unsplash_base_url}/search/photos",
                    headers=headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("results"):
                            photo = data["results"][0]
                            return f"{photo['urls']['raw']}&w={width}&h={height}&fit=crop&crop=center"
            
        except Exception as e:
            logger.error(f"Error fetching from Unsplash: {e}")
        
        return None
    
    async def _fetch_fallback_image(self, category: str, width: int, height: int) -> Optional[str]:
        """Fetch image from fallback services"""
        try:
            keywords = self.business_categories.get(category, [category])
            
            # Try source.unsplash.com with keywords
            if keywords:
                keyword = keywords[0].replace(" ", "-")
                fallback_url = f"https://source.unsplash.com/{width}x{height}/?{keyword}"
                
                # Test if URL is accessible
                async with aiohttp.ClientSession() as session:
                    async with session.head(fallback_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status == 200:
                            return fallback_url
            
            # Final fallback to Lorem Picsum
            return f"https://picsum.photos/{width}/{height}?random={hash(category) % 1000}"
            
        except Exception as e:
            logger.error(f"Error with fallback services: {e}")
            return f"https://picsum.photos/{width}/{height}?random={hash(category) % 1000}"
    
    def _generate_cache_key(self, category: str, width: int, height: int) -> str:
        """Generate cache key for image"""
        key_string = f"{category}_{width}_{height}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    async def _get_cached_image(self, cache_key: str) -> Optional[str]:
        """Get cached image URL if still valid"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cached_time < self.cache_duration:
                    return cache_data['url']
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
        
        return None
    
    async def _cache_image_url(self, cache_key: str, url: str):
        """Cache image URL with timestamp"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            cache_data = {
                'url': url,
                'timestamp': datetime.now().isoformat()
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            logger.error(f"Error writing cache: {e}")
    
    def _get_local_placeholder(self, width: int, height: int) -> str:
        """Get local placeholder image"""
        # Create a simple placeholder URL that can be handled by CSS
        return f"/static/images/placeholder-{width}x{height}.svg"
    
    def create_placeholder_svg(self, width: int, height: int, text: str = "Professional Image") -> str:
        """Create SVG placeholder"""
        return f"""
        <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#f8f9fa"/>
            <rect x="2" y="2" width="{width-4}" height="{height-4}" fill="none" stroke="#dee2e6" stroke-width="2"/>
            <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="16" fill="#6c757d" text-anchor="middle" dy=".3em">{text}</text>
        </svg>
        """