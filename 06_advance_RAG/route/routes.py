# flake8: noqa


from fastapi import APIRouter, Query,Path
from queue_RQ.connection import queue
from queue_RQ.worker import process_query
from dotenv import load_dotenv
load_dotenv()

user = APIRouter()

@user.post("/user-query")
def user_query(query: str = Query(...)):
    print('1')
    # Query ko queue me daalo
    job = queue.enqueue(process_query, query)
    # User ko bolo your job received
    return {"status": "queued", "job_id": job.id}


@user.get("/job-status/{job_id}")
def get_job_id_data(job_id : str = Path(...,description='job_id')):
    job_ids = queue.get_job_ids(0,5)
    print(job_ids)
    job_id_data = queue.fetch_job(job_id=job_id)
    result = job_id_data.return_value()
    
    return {
        'result':result
    }
    