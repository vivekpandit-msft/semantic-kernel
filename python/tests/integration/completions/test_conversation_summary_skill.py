# Copyright (c) Microsoft. All rights reserved.

import os

import pytest
from python.tests.conftest import azure_openai_settings
from test_utils import retry

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.core_skills.conversation_summary_skill import (
    ConversationSummarySkill,
)


@pytest.mark.asyncio
async def test_azure_summarize_conversation_using_skill(
    setup_summarize_conversation_using_skill,
):
    kernel, chatTranscript = setup_summarize_conversation_using_skill

    azure_openai_settings = sk.load_settings().azure_openai

    kernel.add_text_completion_service(
        "text_completion",
        sk_oai.AzureTextCompletion(azure_openai_settings.deployment, azure_openai_settings.endpoint, azure_openai_settings.api_key),
    )

    conversationSummarySkill = kernel.import_skill(
        ConversationSummarySkill(kernel), "conversationSummary"
    )

    summary = await retry(
        lambda: kernel.run_async(
            conversationSummarySkill["SummarizeConversation"], input_str=chatTranscript
        )
    )

    output = str(summary).strip().lower()
    print(output)
    assert "john" in output and "jane" in output
    assert len(output) < len(chatTranscript)


@pytest.mark.asyncio
async def test_oai_summarize_conversation_using_skill(
    setup_summarize_conversation_using_skill,
):
    kernel, chatTranscript = setup_summarize_conversation_using_skill

    openai_settings = sk.load_settings().openai

    kernel.add_text_completion_service(
        "davinci-003",
        sk_oai.OpenAITextCompletion(
            "text-davinci-003", openai_settings.api_key, org_id=openai_settings.org_id
        ),
    )

    conversationSummarySkill = kernel.import_skill(
        ConversationSummarySkill(kernel), "conversationSummary"
    )

    summary = await retry(
        lambda: kernel.run_async(
            conversationSummarySkill["SummarizeConversation"], input_str=chatTranscript
        )
    )

    output = str(summary).strip().lower()
    print(output)
    assert "john" in output and "jane" in output
    assert len(output) < len(chatTranscript)
