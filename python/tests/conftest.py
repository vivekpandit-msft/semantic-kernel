# Copyright (c) Microsoft. All rights reserved.

import os

import pytest

import semantic_kernel as sk
from semantic_kernel.settings import AzureOpenAISettings, KernelSettings, OpenAISettings, load_settings


@pytest.fixture()
def create_kernel():
    kernel = sk.Kernel()
    return kernel


@pytest.fixture()
def kernel_settings() -> KernelSettings:
    """Settings used for testing.

    NOTE: See the `tests/unit/test_settings.py::test_load_settings` test for a test that
    ensures that we can load the settings in the test environment. If that test fails,
    then any test depending on this fixture will also fail.
    """
    return load_settings()


@pytest.fixture()
def openai_settings(kernel_settings: KernelSettings) -> OpenAISettings:
    """OpenAI settings used for testing."""
    return kernel_settings.openai


@pytest.fixture()
def azure_openai_settings(kernel_settings: KernelSettings) -> AzureOpenAISettings:
    """Azure OpenAI settings used for testing."""
    return kernel_settings.azure_openai
