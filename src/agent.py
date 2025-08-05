# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random

from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from dotenv import load_dotenv
import os

load_dotenv()  # 會自動從當前目錄或上層尋找 .env 並載入
print("USE_VERTEXAI =", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("PROJECT =", os.getenv("GOOGLE_CLOUD_PROJECT"))
print("LOCATION =", os.getenv("GOOGLE_CLOUD_LOCATION"))
print("CREDENTIALS =", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))



root_agent = Agent(
    model='gemini-2.0-flash',
    name='analyze_and_recommend',
    description=(
        '你是一個分析問題並給出建議的助手，主要是要接收計畫書與graylog的日誌。'
        '計劃書可以幫助你理解這些graylog資料的意義。'
        'graylog的日誌主要要根據MSGID來追蹤問題發生順序。'
    ),
    instruction="""
      1. 接收計畫書與graylog的日誌。
      2. 分析計畫書與日誌，找出問題發生可能原因。
      3. 給出解決建議。
      4. 如果需要更多資訊，反饋使用者請他做下一次的查詢計畫。
      5. 如果資訊充足，請給出定論。
    """,
    tools=[
 
    ],
    # planner=BuiltInPlanner(
    #     thinking_config=types.ThinkingConfig(
    #         include_thoughts=True,
    #     ),
    # ),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)

a2a_app = to_a2a(root_agent, port=8001)

if __name__ == "__main__":
    print("Starting analyze_and_recommend agent on port 8001...")
    a2a_app.run(host="0.0.0.0", port=8001)
