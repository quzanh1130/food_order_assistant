import uuid
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from core.exception import QuestionNotProvidedException
from core.logger import logger
from database.db import save_conversation, save_feedback
from core.rag import rag, rag_conversation

router = APIRouter()

@router.get("/")
async def index():
    return FileResponse('./static/index.html')

@router.post("/question")
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
        save_conversation(
            conversation_id=conversation_id,
            question=question,
            answer_data=answer_data,
        )

        return JSONResponse(content=result)
    except QuestionNotProvidedException as e:
        raise e

@router.post("/conversation")
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
        save_conversation(
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

@router.post("/feedback")
async def handle_feedback(request: Request):
    try:
        data = await request.json()
        conversation_id = data.get("conversation_id")
        feedback = data.get("feedback")

        if not conversation_id or feedback not in [1, -1]:
            logger.error(f"Invalid input: {data}")
            raise HTTPException(status_code=400, detail="Invalid input")

        logger.info(f"Received feedback for conversation {conversation_id}: {feedback}")
        
        save_feedback(
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