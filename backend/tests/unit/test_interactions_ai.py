"""Curated AI-generated unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_interactions_with_matching_item_id() -> None:
    """Test that ALL interactions with matching item_id are returned."""
    interactions = [
        _make_log(id=1, learner_id=1, item_id=5),
        _make_log(id=2, learner_id=2, item_id=5),
        _make_log(id=3, learner_id=3, item_id=5),
        _make_log(id=4, learner_id=1, item_id=3),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 3
    assert all(i.item_id == 5 for i in result)
    assert set(i.id for i in result) == {1, 2, 3}


def test_filter_with_zero_item_id() -> None:
    """Test filtering with item_id=0, a boundary integer value."""
    interactions = [
        _make_log(id=1, learner_id=1, item_id=0),
        _make_log(id=2, learner_id=2, item_id=1),
        _make_log(id=3, learner_id=3, item_id=0),
    ]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 2
    assert all(i.item_id == 0 for i in result)
    assert set(i.id for i in result) == {1, 3}


def test_filter_returns_empty_when_no_matches() -> None:
    """Test filtering when NO interactions match the given item_id."""
    interactions = [
        _make_log(id=1, learner_id=1, item_id=1),
        _make_log(id=2, learner_id=2, item_id=2),
        _make_log(id=3, learner_id=3, item_id=3),
    ]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_preserves_original_order() -> None:
    """Test that filtering preserves the original list order."""
    interactions = [
        _make_log(id=5, learner_id=1, item_id=10),
        _make_log(id=1, learner_id=2, item_id=10),
        _make_log(id=3, learner_id=3, item_id=10),
    ]
    result = _filter_by_item_id(interactions, 10)
    assert len(result) == 3
    assert [i.id for i in result] == [5, 1, 3]
