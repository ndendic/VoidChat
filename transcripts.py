from youtube_transcript_api import YouTubeTranscriptApi
from pydantic_ai import Agent
from pydantic import BaseModel

class ResultWithTitle(BaseModel):
    """Response structure for the agent"""
    explanation: str
    title: str


vids = ['4x9wtrDOXac', 'X_m7qz5LteY', 'kEGQSamwpuU', 'HO1gmouGEVI', 'w_YltetZc3M', '83tbt5lEUgI', 'Dnu39sQCV3k', 'lA-KvHeFJkI', 'ObliDyAdRx8', '5ZPFC_Xnz8A', 'AvItkLCD7v8', 'rr-59PLkIdY']
yta = Agent(
    'openai:gpt-4o-mini',
    result_type=ResultWithTitle,
    name="YT Agent Title suggestion-er",
    system_prompt="You are a helpful assistant that can suggest a title for a youtube video based on the transcript of the video.",
)

i = 1
results = []
for vid in vids:
    print("Processing video " + str(i) + " of " + str(len(vids)))
    transcript =   YouTubeTranscriptApi.get_transcript(vid)
    texts_only = [t['text'] for t in transcript]
    print("Calling agent...")
    result = yta.run_sync(
        """Can you please suggest at least a meaningfull title for a video based on the transcript of the video. 
        Title should be a short sentence that summarizes the video content.
        Transcript: """ + "\n".join(texts_only)
    )
    print("Agent says: " + result.data.title)
    results.append("Lesson " + str(i) + ": " + result.data.title)
    i += 1

print("\n".join(results))