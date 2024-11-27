from fastapi import HTTPException, status

from app.core.loggers.MyLogger import MyLogger
from app.core.azureOpenAI.azure_openai import client


if MyLogger.logger is None:
    MyLogger.configure()


async def process_audio(file_location: str):
    try:
        deployment_id = "whisper"

        audio_file = open(file_location, "rb")
        result = client.audio.transcriptions.create(
            file=open(file_location, "rb"), model=deployment_id
        )
        audio_file.close()

        print(result)

        # Save file in /uploads file.mp3.txt
        text_audio_location = file_location + ".txt"
        with open(text_audio_location, "w") as file_object:
            file_object.write(result.text)

        return text_audio_location
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        MyLogger.logger.error(f"Error en transcripcion de audio: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en transcripcion de audio: {exc}",
        )
