import pytest
from crud import get_random_candidate

@pytest.mark.asyncio
async def test_get_random_candidate_empty_db(db_session):
    user_id = 12345
    candidate = await get_random_candidate(db_session, user_id)
    
    assert candidate is None