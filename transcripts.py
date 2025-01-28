from youtube_transcript_api import YouTubeTranscriptApi
from pydantic_ai import Agent

vids = ['4x9wtrDOXac', 'X_m7qz5LteY', 'kEGQSamwpuU', 'HO1gmouGEVI', 'w_YltetZc3M', '83tbt5lEUgI', 'Dnu39sQCV3k', 'lA-KvHeFJkI', 'ObliDyAdRx8', '5ZPFC_Xnz8A', 'AvItkLCD7v8', 'rr-59PLkIdY']
yta = Agent(
    'openai:gpt-4o-mini',
    name="YT Agent Title suggestion-er",
    system_prompt="You are a helpful assistant that can suggest a title for a youtube video based on the transcript of the video.",
)

for vid in vids:
    transcript =   YouTubeTranscriptApi.get_transcript(vid)
    texts_only = [t['text'] for t in transcript]
    result = yta.run_sync(
        "Can you please suggest at least 3 titles for this video based on the transcript of the video. " + "\n".join(texts_only)
    )
    print(result.data)