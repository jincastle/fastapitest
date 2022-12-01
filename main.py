import shotstack_sdk as shotstack
from dotenv import load_dotenv
import os

from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.video_asset import VideoAsset

from fastapi import FastAPI


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


@app.get("/")
async def root():
    return {"message" : "Hello World"}

@app.get("/shotstack")
async def shotStackGet():
    configuration = shotstack.Configuration(host='https://api.shotstack.io/stage')

    configuration.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")
#
#     # a = load_dotenv(os.path.join(BASE_DIR, "testvd.mp4"))
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        video_asset = VideoAsset(
            src="https://s3-ap-southeast-2.amazonaws.com/shotstack-assets/footage/skater.hd.mp4",
            trim=3.0
        )

        video_clip = Clip(
            asset=video_asset,
            start=0.0,
            length=8.0
        )

        track = Track(clips=[video_clip])

        timeline = Timeline(
            background="#000000",
            tracks=[track]
        )

        output = Output(
            format="mp4",
            resolution="sd"
        )

        edit = Edit(
            timeline=timeline,
            output=output
        )

        try:
            api_response = api_instance.post_render(edit)

            message = api_response['response']['message']
            id = api_response['response']['id']

            print(f"{message}\n")
            print(">> Now check the progress of your render by running:")
            print(f">> python examples/status.py {id}")
        except Exception as e:
            print(f"Unable to resolve API call: {e}")

#앱으로 만든다면
# 실행 명령어 : uvicorn main:my_awesome_api --reload
#
# from fastapi import FastAPI
#
# my_awesome_api = FastAPI()
#
#
# @my_awesome_api.get("/")
# async def root():
#     return {"message": "Hello World"}