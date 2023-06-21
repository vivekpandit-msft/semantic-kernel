# Copyright (c) Microsoft. All rights reserved.

from dataclasses import dataclass, field
from typing import List
import pydantic as pdt

class CompletionConfig(pdt.BaseModel):
    temperature: float = pdt.Field(0.0, description="The temperature for generating completions.")
    top_p: float = pdt.Field(1.0, description="The top-p value for generating completions.")
    presence_penalty: float = pdt.Field(0.0, description="The presence penalty for generating completions.")
    frequency_penalty: float = pdt.Field(0.0, description="The frequency penalty for generating completions.")
    max_tokens: int = pdt.Field(256, description="The maximum number of tokens for generating completions.")
    number_of_responses: int = pdt.Field(1, description="The number of completions to generate.")
    stop_sequences: List[str] = pdt.Field([], description="The list of stop sequences for generating completions.")


class InputParameter(pdt.BaseModel):
    name: str = pdt.Field("", description="The name of the input parameter.")
    description: str = pdt.Field("", description="The description of the input parameter.")
    default_value: str = pdt.Field("", description="The default value of the input parameter.")


class InputConfig(pdt.BaseModel):
    parameters: List["InputParameter"] = pdt.Field(default_factory=list, description="The list of input parameters.")


class PromptTemplateConfig(pdt.BaseModel):
    schema_alias: int = pdt.Field(1, alias="schema")
    type: str = pdt.Field("completion")
    description: str = pdt.Field("")

    completion: "CompletionConfig" = pdt.Field(default_factory=CompletionConfig)
    default_services: List[str] = pdt.Field(default_factory=list)
    input: "InputConfig" = pdt.Field(default_factory=InputConfig)

    @staticmethod
    def from_dict(data: dict) -> "PromptTemplateConfig":
        config = PromptTemplateConfig()
        config.schema_alias = data.get("schema")
        config.type = data.get("type")
        config.description = data.get("description")

        # Some skills may not have all completion parameters defined
        config.completion = CompletionConfig()
        completion_dict = data["completion"]
        config.completion.temperature = completion_dict.get("temperature")
        config.completion.top_p = completion_dict.get("top_p")
        config.completion.presence_penalty = completion_dict.get("presence_penalty")
        config.completion.frequency_penalty = completion_dict.get("frequency_penalty")
        config.completion.max_tokens = completion_dict.get("max_tokens")
        config.completion.number_of_responses = completion_dict.get(
            "number_of_responses"
        )
        config.completion.stop_sequences = completion_dict.get("stop_sequences", [])
        config.default_services = data.get("default_services", [])

        # Some skills may not have input parameters defined
        config.input = InputConfig()
        config.input.parameters = []
        if data.get("input") is not None:
            for parameter in data["input"]["parameters"]:
                if "name" in parameter:
                    name = parameter["name"]
                else:
                    raise Exception(
                        f"The input parameter doesn't have a name (function: {config.description})"
                    )

                if "description" in parameter:
                    description = parameter["description"]
                else:
                    raise Exception(
                        f"Input parameter '{name}' doesn't have a description (function: {config.description})"
                    )

                if "defaultValue" in parameter:
                    defaultValue = parameter["defaultValue"]
                else:
                    raise Exception(
                        f"Input parameter '{name}' doesn't have a default value (function: {config.description})"
                    )

                config.input.parameters.append(
                    InputParameter(
                        name,
                        description,
                        defaultValue,
                    )
                )
        return config

    @staticmethod
    def from_json(json_str: str) -> "PromptTemplateConfig":
        import json

        return PromptTemplateConfig.from_dict(json.loads(json_str))

    @staticmethod
    def from_completion_parameters(
        temperature: float = 0.0,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        max_tokens: int = 256,
        number_of_responses: int = 1,
        stop_sequences: List[str] = [],
    ) -> "PromptTemplateConfig":
        config = PromptTemplateConfig()
        config.completion.temperature = temperature
        config.completion.top_p = top_p
        config.completion.presence_penalty = presence_penalty
        config.completion.frequency_penalty = frequency_penalty
        config.completion.max_tokens = max_tokens
        config.completion.number_of_responses = number_of_responses
        config.completion.stop_sequences = stop_sequences
        return config
