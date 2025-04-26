from typing import List, Dict, Any, Optional, Protocol

class LLM(Protocol):
    """AI service gateway interface for interacting with AI services"""
    
    async def ask(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send chat request to AI service
        
        Args:
            messages: List of messages, including conversation history
            tools: Optional list of tools for function calling
            response_format: Optional response format configuration
            
        Returns:
            Response message from AI service
        """
        pass 