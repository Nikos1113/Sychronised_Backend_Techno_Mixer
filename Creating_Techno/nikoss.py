"""FastAPI application for managing songs and kick audio samples."""
import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, Response, status
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
JSON_WITH_KICKS = BASE_DIR / "audios_kicks_mix.json"


app = FastAPI()


@app.get("/")
def read_root():
    """Return a greeting for the root endpoint."""
    return {"message": "Hello World"}


class Songs(BaseModel):
    """Represents a song entry in the library."""
    id: int
    name: str
    artist: str
    bpm: int


songs: List[Songs] = []


@app.post("/songs/", status_code=201)
def add_a_song(song: Songs, response: Response):
    """Create a new song entry and return it."""
    songs.append(song)
    response.status_code = status.HTTP_201_CREATED
    return song


@app.get("/songs/", status_code=200)
def read_the_songs(response: Response):
    """List all songs in the API."""
    response.status_code = status.HTTP_200_OK
    return songs


@app.put("/songs/{song_id}", status_code=200)
def changes_for_a_song(song_id: int, changed_song: Songs, response: Response):
    """Update an existing song entry by id."""
    for index, song in enumerate(songs):
        if song.id == song_id:
            songs[index] = changed_song
            response.status_code = status.HTTP_200_OK
            return changed_song
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Song not found"}


@app.delete("/songs/{song_id}", status_code=204)
def delete_a_song(song_id: int, response: Response):
    """Delete a song entry by id."""
    for index, song in enumerate(songs):
        if song.id == song_id:
            songs.remove(song)
            response.status_code = status.HTTP_204_NO_CONTENT
            return None
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Song not found"}


@app.get("/kicks/", status_code=200)
def read_file_of_kicks(response: Response):
    """Return the kick data stored in the JSON file."""
    try:
        with open(JSON_WITH_KICKS, "r", encoding="utf-8") as file:
            data = json.load(file)
            response.status_code = status.HTTP_200_OK
            return data
    except FileNotFoundError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "File not found"}


@app.post("/kicks/", status_code=201)
def add_kick_sample(kick: dict, response: Response):
    """Add a kick sample to the JSON file."""
    try:
        with open(JSON_WITH_KICKS, "r", encoding="utf-8") as file:
            kicks_data = json.load(file)

        kicks_data.append(kick)

        with open(JSON_WITH_KICKS, "w", encoding="utf-8") as file:
            json.dump(kicks_data, file, indent=4)

        response.status_code = status.HTTP_201_CREATED
        return kick
    except FileNotFoundError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "File not found"}


@app.delete("/kicks/{kick_id}", status_code=204)
def delete_a_kick(kick_id: int, response: Response):
    """Delete a kick sample."""
    try:
        with open(JSON_WITH_KICKS, "r", encoding="utf-8") as file:
            kicks_data = json.load(file)

        for kick in kicks_data:
            if kick["id"] == kick_id:
                kicks_data.remove(kick)
                with open(JSON_WITH_KICKS, "w", encoding="utf-8") as file:
                    json.dump(kicks_data, file, indent=4)
                    response.status_code = status.HTTP_204_NO_CONTENT
                    return None
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Kick not found"}
    except FileNotFoundError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "File not found"} 
