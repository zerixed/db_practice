import pytest
from crud import save_reaction
@pytest.mark.asyncio
async def test_save_reaction_mutual_match(db_session):
    user_1_id = 1001
    user_2_id = 2002
    is_match_first = await save_reaction(
        db_session,from_id=user_1_id, to_id=user_2_id,is_like=True
    )
    assert is_match_first is False
    is_match_second = await save_reaction(
        db_session,from_id=user_2_id, to_id=user_1_id,is_like=True
    )
    assert is_match_second is True