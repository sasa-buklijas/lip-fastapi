import os
import pytest
from model.creature import Creature 
# Set this before data import below
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from service import creature as code # noqa: E402
from errors import Missing # noqa: E402

sample = Creature(name="Yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
        )

def test_create():
    resp = code.create(sample) 
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Yeti") 
    assert resp == sample

def test_get_missing():
    with pytest.raises(Missing):
        code.get_one("boxturtle") 
