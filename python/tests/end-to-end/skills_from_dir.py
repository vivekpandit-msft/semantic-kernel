# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from python.tests.conftest import azure_openai_settings

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai

kernel = sk.Kernel()

useAzureOpenAI = False
model = "text-davinci-002"
service_id = model

# Configure AI service used by the kernel
if useAzureOpenAI:
    azure_openai_settings = sk.load_settings().azure_openai
    kernel.add_text_completion_service(
        service_id, sk_oai.AzureTextCompletion(model, azure_openai_settings.api_key, azure_openai_settings.endpoint)
    )
else:
    openai_settings = sk.load_settings().openai
    kernel.add_text_completion_service(
        service_id,
        sk_oai.OpenAITextCompletion(
            model, openai_settings.api_key, openai_settings.org_id
        ),
    )

# note: using skills from the samples folder
skills_directory = os.path.join(__file__, "../../../../samples/skills")
skill = kernel.import_semantic_skill_from_directory(skills_directory, "FunSkill")

result = asyncio.run(
    kernel.run_async(skill["Joke"], input_str="time travel to dinosaur age")
)
print(result)
