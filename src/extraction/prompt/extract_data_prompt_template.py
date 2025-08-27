from langchain_core.prompts import ChatPromptTemplate

from .prompts import document_format_prompt, extraction_system_message


class ExtractDataPromptTemplate(ChatPromptTemplate):
    def __init__(self):
        super().__init__(
            [extraction_system_message, document_format_prompt],
            template_format="jinja2",
        )
