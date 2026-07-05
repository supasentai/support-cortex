requests
beautifulsoup4
markdownify
python-dotenv
openai

## Playground sanity check

After running the ingestion pipeline and creating/updating the assistant, verify the
assistant manually in the OpenAI Playground.

Required question:

```txt
How do I add a YouTube video?
```

The answer should use the uploaded docs and cite relevant `Article URL:` lines.
