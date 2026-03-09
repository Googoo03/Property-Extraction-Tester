import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.cluster_rebalance_weights import cluster_rebalance_weights

# Property: preserves_length
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            cluster_rebalance_weights(current, target, damping=damping)
    else:
        result = cluster_rebalance_weights(current, target, damping=damping)
        assert len(result) == len(current)

# Property: branch_specific_behavior (shape mismatch)
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_specific_behavior_shape_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            cluster_rebalance_weights(current, target, damping=damping)

# Property: branch_specific_behavior (empty weights)
@given(
    current=st.lists(st.floats(), min_size=0, max_size=0),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_specific_behavior_empty_weights(current, target, damping):
    with pytest.raises(ValueError, match="empty weights"):
        cluster_rebalance_weights(current, target, damping=damping)

# Property: loop_invariant
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_loop_invariant(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            cluster_rebalance_weights(current, target, damping=damping)
    else:
        result = cluster_rebalance_weights(current, target, damping=damping)
        assert all(
            c + (t - c) * damping == u
            for c, t, u in zip(current, target, result)
        )

# Property: return_postcondition
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_return_postcondition(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            cluster_rebalance_weights(current, target, damping=damping)
    else:
        result = cluster_rebalance_weights(current, target, damping=damping)
        assert result is not None