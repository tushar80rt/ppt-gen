import os
import time
from dotenv import load_dotenv
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.messages import BaseMessage
from camel.toolkits import PPTXToolkit
from camel.types import RoleType, ModelPlatformType


load_dotenv("api.env")
os.environ["PEXELS_API_KEY"] = os.getenv("PEXELS_API_KEY", "")


model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type="gpt-4o",
    model_config_dict={"temperature": 0.3, "max_tokens": 2048}
)


ppt_toolkit = PPTXToolkit()
tools = ppt_toolkit.get_tools()

SYSTEM_PROMPT = (
    "You are an expert AI assistant that creates professional, well-structured PowerPoint presentations using the PPTXToolkit.\n"
    "Your task is to generate a complete presentation using ONLY the provided tools. Do not ignore or skip any required step.\n\n"
    "Strictly follow this step-by-step workflow:\n"
    "1. Start by calling create_presentation(filename='output.pptx').\n"
    "2. For each slide, use add_slide(title='...', content='...'):\n"
    "   - Use an engaging and specific title (avoid generic titles like 'Introduction' or 'Conclusion').\n"
    "   - Use bullet points for clarity (separate them with '\\n').\n"
    "   - If applicable, include comparison data in table format:\n"
    "     Example:\n"
    "     | Metric     | Option A | Option B |\n"
    "     |------------|----------|----------|\n"
    "     | Speed      | Fast     | Medium   |\n"
    "     | Cost       | Low      | High     |\n"
    "3. To enhance visuals, you MUST call at least ONE of the following (not optional):\n"
    "   - search_image(keyword='...')\n"
    "   - add_image_to_slide(image_url='...', title='...', content='...')\n"
    "   - add_shape_to_slide(shape='pentagon', title='...', content='...') ← THIS IS MANDATORY at least once\n"
    "     ✅ Example:\n"
    "     add_shape_to_slide(shape='pentagon', title='Implementation Steps', content='>> Step 1: Define Goals\\n>> Step 2: Choose Tools\\n>> Step 3: Build\\n>> Step 4: Review\\n>> Step 5: Launch')\n"
    "4. You MUST include at least one pentagon slide using add_shape_to_slide with shape='pentagon'.\n"
    "   - Use the '>> Step X: ...' format for each bullet in the pentagon slide.\n"
    "5. End by calling save_presentation(file_path='output.pptx').\n\n"
    "⚠️ Important Rules:\n"
    "- Do NOT return plain text explanations.\n"
    "- Do NOT skip save_presentation.\n"
    "- Use ONLY the PPTXToolkit tools provided.\n"
    "- Organize slides logically: include a proper introduction, body, comparisons/visuals, and conclusion.\n"
    "- Slide titles must be clear, specific, and compelling — avoid vague or one-word titles."
)




def run_ppt_task(task: str) -> str:
    try:
        agent = ChatAgent(
            system_message=BaseMessage(
                role_name="assistant",
                role_type=RoleType.ASSISTANT,
                content=SYSTEM_PROMPT,
                meta_dict={}
            ),
            model=model,
            tools=tools
        )

        user_msg = BaseMessage(
            role_name="user",
            role_type=RoleType.USER,
            content=task,
            meta_dict={}
        )

        current_msg = user_msg
        output_file = f"presentation_{int(time.time())}.pptx"
        already_saved = False

        print("Current working directory:", os.getcwd())

        for step in range(10):
            result = agent.step(current_msg)
            print(f"Step {step} response:", result.msg.content)

            tool_calls = result.info.get("tool_calls", [])
            if not tool_calls:
                print("No more tool calls.")
                break

            for call in tool_calls:
                if call.tool_name == "save_presentation":
                    already_saved = True
                    print("Presentation saved. Ending loop.")
                    break

            if already_saved:
                break

            current_msg = result.msg

        # Rename and return final presentation path
        pptx_files = [f for f in os.listdir() if f.endswith(".pptx")]
        print("Found pptx files:", pptx_files)
        if pptx_files:
            latest_file = max(pptx_files, key=os.path.getmtime)
            os.rename(latest_file, output_file)
            print(f"Renamed '{latest_file}' to '{output_file}'")
            return os.path.abspath(output_file)
        else:
            print("No .pptx file found in current directory.")
            return None

    except Exception as e:
        print("Error in run_ppt_task:", e)
        return None
