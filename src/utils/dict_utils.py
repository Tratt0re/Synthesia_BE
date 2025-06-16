def safe_merge_dictionaries(dicts: list[dict | None]) -> dict:
    """
    Merges a list of dictionaries into a single dictionary, preserving duplicate keys by
    storing values in lists.

    Args:
        dicts: A list of dictionaries to merge.

    Returns:
        A single dictionary where duplicate keys have lists of values.
    """
    merged_dict = {}
    for d in dicts:
        if d:
            for key, value in d.items():
                if key in merged_dict:
                    # If the key exists, append to the list
                    if isinstance(merged_dict[key], list):
                        merged_dict[key].append(value)
                    else:
                        merged_dict[key] = [merged_dict[key], value]
                else:
                    merged_dict[key] = value
    return merged_dict
