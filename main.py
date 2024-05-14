from fastapi import FastAPI
from config import Settings, get_settings
from fastapi import FastAPI, UploadFile, File
from lib import upload_file_to_s3
# -- START FAST-API INITIAL CONFIG -- #
settings: Settings = get_settings()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": f"World! My app is {settings.app_title}"}



# List the files
from lib import list_files
@app.get("/list-files")
def retrieve_all_files_in_my_bucket():
    bucket_name = "lbs-team-2"
    files = list_files(bucket_name)
    return {"files": files}


from lib import get_client
@app.post("/upload-file")
def upload_file(file: UploadFile = File(...)):
    print(settings.aws_access_key_id)
    s3 = get_client(service='s3', settings=settings)
    object_name = file.filename
    return upload_file_to_s3(
        s3_client=s3,
        bucket_name="lbs-team-2",
        object_name=f"uploaded_{file.filename}",
        file=file)

# retrieve file link
from lib import generate_presigned_url
@app.get("/retrieve-file-link")
def retrieve_a_link(my_file: str):
    return generate_presigned_url(
        bucket_name="lbs-team-2",
        object_name=my_file
    )
