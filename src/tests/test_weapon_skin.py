from scripts import weapon_skin

def test_normalize__with_full_name():
    result = weapon_skin.normalize("ak47 redline ft")

    assert "ak47" in result
    assert "redline" in result
    assert "field tested" in result

# Ensure that we can match a normalized pattern to the original market hash name
def test_search_skin():
    old_array = weapon_skin.SKIN_ARRAY
    weapon_skin.SKIN_ARRAY = [
        "AK-47 | Redline (Field Tested)",
        "M4A1-S | Howl (Factory New)",
    ]

    try:
        result = weapon_skin.search_skin("ak47 redline ft")
        assert result == "AK-47 | Redline (Field Tested)"
    finally:
        weapon_skin.SKIN_ARRAY = old_array