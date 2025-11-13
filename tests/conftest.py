"""
Pytest configuration and shared fixtures.
"""

import pytest
from unittest.mock import AsyncMock

from monitoring.config import monitoring_config


@pytest.fixture(autouse=True)
def reset_config():
    """Reset monitoring config before each test"""
    original_values = {
        'MONITORING_ENABLED': monitoring_config.MONITORING_ENABLED,
        'TELEGRAM_BOT_TOKEN': monitoring_config.TELEGRAM_BOT_TOKEN,
        'TELEGRAM_CHAT_ID': monitoring_config.TELEGRAM_CHAT_ID,
        'MONITORING_ENV': monitoring_config.MONITORING_ENV,
    }
    
    yield
    
    # Restore original values
    for key, value in original_values.items():
        setattr(monitoring_config, key, value)


@pytest.fixture
def mock_redis_adapter():
    """Create mock Redis adapter"""
    mock = AsyncMock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.setex.return_value = True
    mock.delete.return_value = 1
    mock.incr.return_value = 1
    mock.expire.return_value = True
    mock.lpush.return_value = 1
    mock.lrange.return_value = []
    mock.ltrim.return_value = True
    mock.scan.return_value = (0, [])
    mock.ping.return_value = True
    mock.type.return_value = "string"
    mock.zcard.return_value = 0
    mock.llen.return_value = 0
    return mock


@pytest.fixture
def mock_database_adapter():
    """Create mock Database adapter"""
    from monitoring.adapters import DatabaseAdapter
    
    class MockDatabaseAdapter(DatabaseAdapter):
        async def get_new_users_count(self, start_date, end_date):
            return 10
        
        async def get_active_users_count(self, start_date, end_date):
            return 50
        
        async def get_total_users_count(self):
            return 100
        
        async def get_new_projects_count(self, start_date, end_date):
            return 5
        
        async def get_updated_projects_count(self, start_date, end_date):
            return 20
        
        async def get_total_projects_count(self):
            return 50
        
        async def health_check(self, timeout=5.0):
            return True
    
    return MockDatabaseAdapter()


@pytest.fixture
def mock_queue_adapter():
    """Create mock Queue adapter"""
    from monitoring.adapters import QueueAdapter
    
    class MockQueueAdapter(QueueAdapter):
        async def health_check(self):
            return True
        
        async def get_queue_size(self):
            return 0
        
        async def get_last_job_time(self):
            import time
            return time.time()
    
    return MockQueueAdapter()


@pytest.fixture
def configured_monitoring():
    """Configure monitoring for testing"""
    monitoring_config.MONITORING_ENABLED = True
    monitoring_config.TELEGRAM_BOT_TOKEN = "test_bot_token"
    monitoring_config.TELEGRAM_CHAT_ID = "test_chat_id"
    monitoring_config.MONITORING_ENV = "test"
    
    yield monitoring_config


@pytest.fixture
async def mock_telegram_client():
    """Create mock Telegram HTTP client"""
    from unittest.mock import Mock
    
    mock_response = Mock()
    mock_response.json.return_value = {"ok": True, "result": {"message_id": 123}}
    mock_response.raise_for_status = Mock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    
    return mock_client