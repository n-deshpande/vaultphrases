"""Tests for derivation logic."""

import pytest
from vaultphrases.derive import derive_master_key, derive_child_key
from vaultphrases.constants import LABEL_HOT, LABEL_COLD


def test_derive_master_key_deterministic():
    """Master key derivation should be deterministic."""
    root_phrase = "correct horse battery staple"
    
    key1 = derive_master_key(root_phrase, test_mode=True)
    key2 = derive_master_key(root_phrase, test_mode=True)
    
    assert key1 == key2
    assert len(key1) == 32


def test_derive_master_key_normalisation():
    """Root phrase normalisation should be consistent."""
    # Different whitespace and casing should produce same key
    phrase1 = "correct horse battery staple"
    phrase2 = "  Correct   Horse  Battery   Staple  "
    phrase3 = "CORRECT HORSE BATTERY STAPLE"
    
    key1 = derive_master_key(phrase1, test_mode=True)
    key2 = derive_master_key(phrase2, test_mode=True)
    key3 = derive_master_key(phrase3, test_mode=True)
    
    assert key1 == key2 == key3


def test_derive_master_key_different_phrases():
    """Different root phrases should produce different keys."""
    key1 = derive_master_key("correct horse battery staple", test_mode=True)
    key2 = derive_master_key("incorrect horse battery staple", test_mode=True)
    
    assert key1 != key2


def test_derive_child_key_deterministic():
    """Child key derivation should be deterministic."""
    master_key = derive_master_key("test phrase", test_mode=True)
    
    child1 = derive_child_key(master_key, LABEL_HOT)
    child2 = derive_child_key(master_key, LABEL_HOT)
    
    assert child1 == child2
    assert len(child1) == 32


def test_derive_child_key_domain_separation():
    """Different labels should produce different child keys."""
    master_key = derive_master_key("test phrase", test_mode=True)
    
    hot_key = derive_child_key(master_key, LABEL_HOT)
    cold_key = derive_child_key(master_key, LABEL_COLD)
    
    assert hot_key != cold_key


def test_derive_child_key_independence():
    """Child keys from different master keys should be different."""
    master1 = derive_master_key("phrase one", test_mode=True)
    master2 = derive_master_key("phrase two", test_mode=True)
    
    child1 = derive_child_key(master1, LABEL_HOT)
    child2 = derive_child_key(master2, LABEL_HOT)
    
    assert child1 != child2
