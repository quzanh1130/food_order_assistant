import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException

import db
from logger import logger
from rag import rag, rag_conversation
from exception import QuestionNotProvidedException

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse('static/index.html')

@app.exception_handler(QuestionNotProvidedException)
async def question_not_provided_exception_handler(request: Request, exc: QuestionNotProvidedException):
    logger.error(f"QuestionNotProvidedException: {exc.detail}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

@app.post("/question")
async def handle_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question")

        if not question:
            raise QuestionNotProvidedException(detail="No question provided")

        conversation_id = str(uuid.uuid4())

        logger.info(f"Received question: {question}")
        
        answer_data = rag(question)

        result = {
            "conversation_id": conversation_id,
            "question": question,
            "answer": answer_data["answer"],
        }

        logger.info(f"Stored conversation: {conversation_id}")
        db.save_conversation(
            conversation_id=conversation_id,
            question=question,
            answer_data=answer_data,
        )

        return JSONResponse(content=result)
    except QuestionNotProvidedException as e:
        raise e
    except Exception as e:
        logger.error(f"Error handling question: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/conversation")
async def handle_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question")
        last_conversation = data.get("last_conversation")
        
        if not question:
            logger.error(f"No question provided: {data}")
            raise HTTPException(status_code=400, detail="No question provided")

        conversation_id = str(uuid.uuid4())

        logger.info(f"Received question: {question}")
        
        answer_data = rag_conversation(question, last_conversation)

        result = {
            "conversation_id": conversation_id,
            "question": question,
            "answer": answer_data["answer"],
        }

        logger.info(f"Stored conversation: {conversation_id}")
        db.save_conversation(
            conversation_id=conversation_id,
            question=question,
            answer_data=answer_data,
        )

        return JSONResponse(content=result)
    except QuestionNotProvidedException as e:
        raise e
    except Exception as e:
        logger.error(f"Error handling question: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/feedback")
async def handle_feedback(request: Request):
    try:
        data = await request.json()
        conversation_id = data.get("conversation_id")
        feedback = data.get("feedback")

        if not conversation_id or feedback not in [1, -1]:
            logger.error(f"Invalid input: {data}")
            raise HTTPException(status_code=400, detail="Invalid input")

        logger.info(f"Received feedback for conversation {conversation_id}: {feedback}")
        
        db.save_feedback(
            conversation_id=conversation_id,
            feedback=feedback,
        )

        result = {
            "message": f"Feedback received for conversation {conversation_id}: {feedback}"
        }
        return JSONResponse(content=result)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error handling feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
