def assert_lists_of_objects_equal_ignore_attr(l1, l2, ignore_attr):
  """
  Assert that two lists of objects are equal, ignoring a specific attribute.
  """
  assert len(l1) == len(l2)
  for idx, expected_adj in enumerate(l1):
    assert all(
      [v == vars(l2[idx])[k] for k, v in vars(expected_adj).items() if k != ignore_attr]
    )
