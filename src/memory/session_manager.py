"""Session management for maintaining conversation context."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque


@dataclass
class Message:
    """Represents a message in a conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)


@dataclass
class Session:
    """Represents a user session with conversation history."""
    id: str
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    messages: deque = field(default_factory=lambda: deque(maxlen=100))
    metadata: Dict = field(default_factory=dict)
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to the session."""
        self.messages.append(
            Message(
                role=role,
                content=content,
                metadata=metadata or {}
            )
        )
    
    def get_context(self, max_messages: int = 20) -> List[Dict]:
        """Get conversation context for the agent."""
        recent_messages = list(self.messages)[-max_messages:]
        return [
            {"role": msg.role, "content": msg.content}
            for msg in recent_messages
        ]
    
    def compact_context(self, keep_recent: int = 10):
        """Compact context by keeping only recent messages."""
        if len(self.messages) > keep_recent:
            recent = list(self.messages)[-keep_recent:]
            self.messages.clear()
            self.messages.extend(recent)


class SessionManager:
    """Manages user sessions (InMemorySessionService equivalent)."""
    
    def __init__(self, max_sessions: int = 1000):
        self.sessions: Dict[str, Session] = {}
        self.max_sessions = max_sessions
    
    def create_session(self, user_id: str, metadata: Optional[Dict] = None) -> Session:
        """Create a new session for a user."""
        session_id = str(uuid.uuid4())
        session = Session(
            id=session_id,
            user_id=user_id,
            metadata=metadata or {}
        )
        self.sessions[session_id] = session
        
        # Clean up old sessions if needed
        if len(self.sessions) > self.max_sessions:
            self._cleanup_old_sessions()
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get an existing session by ID."""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """Update a session with a new message."""
        session = self.get_session(session_id)
        if session:
            session.add_message(role, content, metadata)
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def _cleanup_old_sessions(self):
        """Remove oldest sessions when limit is reached."""
        if len(self.sessions) <= self.max_sessions:
            return
        
        # Sort by creation time and remove oldest
        sorted_sessions = sorted(
            self.sessions.items(),
            key=lambda x: x[1].created_at
        )
        
        to_remove = len(self.sessions) - self.max_sessions
        for session_id, _ in sorted_sessions[:to_remove]:
            del self.sessions[session_id]

