import pytest
from unittest.mock import MagicMock
from app.bot.handlers.feed import format_candidate_card
@pytest.mark.asyncio
async def test_format_candidate_card_with_all_fields():
    candidate = MagicMock()
    candidate.name = "Alex"
    candidate.age = "17"
    candidate.about = "bLA"
    result = await format_candidate_card(candidate)
    assert "<b>Alex</b>" in result 
    assert ", 17" in result
    assert "<i>bLA</i>" in result
@pytest.mark.asyncio
async def test_format_candidate_card_without_optional_fields():
    candidate = MagicMock()
    candidate.name = "Mary"
    candidate.age = None
    candidate.about = None
    result = await format_candidate_card(candidate)
    assert result == "<b>Mary</b>"