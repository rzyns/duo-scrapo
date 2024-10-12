from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory


kernel = Kernel()

chat_completion_service = kernel.get_service(type=AzureChatCompletion)

svc = AzureChatCompletion(
    api_key="828e89e4bcec4d50bb4cf92bbe8640dc",
    endpoint="https://forserial.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview",
    # service_id="",
    deployment_name="gpt-4o",
)

history = ChatHistory()

kernel.add_service(svc)
