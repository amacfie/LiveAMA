from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI()

# Data models
class Reply(BaseModel):
    author: str
    comment: str

class Comment(BaseModel):
    id: UUID
    author: str
    comment: str
    upvotes: int = 0
    replies: list[Reply] = []

class CreateComment(BaseModel):
    author: str
    comment: str

# In-memory storage
comments: list[UUID] = []

# Endpoint to fetch all comments
@app.get("/api/comments")
async def get_comments() -> list[Comment]:
    return sorted(comments, key=lambda c: c.upvotes, reverse=True)

# Endpoint to add a new comment
@app.post("/api/comment")
async def add_comment(comment: CreateComment) -> Comment:
    ret = Comment(
        author=comment.author,
        comment=comment.comment,
        id=uuid4(),
    )
    comments.append(ret)
    return ret

# Endpoint to add a reply to a comment
@app.post("/api/comment/{comment_id}/reply")
async def add_reply(comment_id: UUID, reply: Reply) -> Reply:
    try:
        the_comment = next(c for c in comments if c.id == comment_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Comment not found")
    the_comment.replies.append(reply)
    return reply

# Endpoint to upvote a comment
@app.post("/api/comment/{comment_id}/upvote")
async def upvote_comment(comment_id: UUID) -> Comment:
    try:
        the_comment = next(c for c in comments if c.id == comment_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Comment not found")
    the_comment.upvotes += 1
    return the_comment

# Serve the HTML file
@app.get("/", response_class=HTMLResponse)
def index():
    with open("index.html") as f:
        return f.read()

