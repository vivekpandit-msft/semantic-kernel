# Copyright (c) Microsoft. All rights reserved.

from typing import Tuple
from dotenv import dotenv_values


def azure_openai_settings_from_dot_env(include_deployment=True) -> Tuple[str, str, str]:
    """
    Reads the Azure OpenAI API key and endpoint from the .env file.

    Returns:
        Tuple[str, str, str]: The deployment name (or empty), Azure OpenAI API key,
            and the endpoint
    """

    deployment, api_key, endpoint = None, None, None
    config = dotenv_values(".env")
    deployment = config.get("AZURE_OPENAI_DEPLOYMENT_NAME", None)
    api_key = config.get("AZURE_OPENAI_API_KEY", None)
    endpoint = config.get("AZURE_OPENAI_ENDPOINT", None)

    # Azure requires the deployment name, the API key and the endpoint URL.
    if include_deployment:
        assert (
            deployment is not None
        ), "Azure OpenAI deployment name not found in .env file"

    assert api_key is not None, "Azure OpenAI API key not found in .env file"
    assert endpoint is not None, "Azure OpenAI endpoint not found in .env file"

    return deployment or "", api_key, endpoint
