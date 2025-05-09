from typing import Optional
from fastapi import HTTPException
import auth.models
import auth.routes
import auth.schemas
import settings, auth
from . import schemas, models
from pathlib import Path

from fastapi import Header

from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session




async def get_song_streaming(db: Session, range: Optional[str] = Header(None)):
    song_path = Path('song.mp3')  
    file_size = song_path.stat().st_size

    start = 0
    end = file_size - 1  # Default to entire file if range is not provided
    if range:
        try:
            range_val = range.replace("bytes=", "")
            start_str, end_str = range_val.split("-")

            start = int(start_str)
            end = int(end_str) if end_str else file_size - 1

        except ValueError:
            return {"error": "Invalid range format"}, 400 # Or perhaps a 416 (Range Not Satisfiable)

    # Ensure the requested range is valid
    if start >= file_size or end < start:
        return {"error": "Invalid range"}, 416  # Range Not Satisfiable

    end = min(end, file_size - 1)  # Cap the end at the file size

    chunk_size = settings.CHUNK_SIZE
    # Asynchronously yield file content in chunks
    async def iterfile():  # (1)
        with open(song_path, mode="rb") as file_like:
            file_like.seek(start)
            while (position := file_like.tell()) <= end:
                remaining = end - position + 1 # Calculate how much to read for current chunk
                length = min(remaining, chunk_size) # Determine chunk size
                data = file_like.read(length)
                if not data: # Break if nothing is read
                    break
                yield data
    headers = {
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(end - start + 1),
    }

    return StreamingResponse(iterfile(), status_code=206 if range else 200, headers=headers, media_type="audio/mp3")


async def create_song(db: Session, token: auth.schemas.TokenGet, song: schemas.SongCreate):
    user_author = auth.routes.user_auth.get_current_user(db=db, token=token.access_token)
    file_name = user_author.login+'@'+song.name
    new_song = models.Song(
        name=song.name,
        file_path='/'+file_name,
        is_download=False,
        author=user_author
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song
    

async def get_song_info(db: Session, song: schemas.SongGet):
    author = db.query(auth.models.User).filter(auth.models.User.login == song.author_name).first()
    if author:
        song = db.query(models.Song).filter(models.Song.name == song.name, models.Song.author == author).first()
        if song:
            return song
        raise HTTPException(status_code=404, detail="Song not found")
    raise HTTPException(status_code=404, detail="User not found")