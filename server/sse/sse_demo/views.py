import math

from django.shortcuts import render
from django.views import View
from django.http import StreamingHttpResponse
import time
from uuid import uuid4
import json
from concurrent.futures import ProcessPoolExecutor
import datetime


# BASIC STREAMING VIEW
class StreamingView(View):

    GLOBAL_COUNTER = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request):
        streaming_response = StreamingHttpResponse(self.event_stream_generator())
        streaming_response["Content-Type"] = 'text/event-stream'
        streaming_response['Cache-Control'] = 'no-cache'
        streaming_response['Connection'] = 'keep-alive'
        return streaming_response

    def event_stream_generator(self):
        signature = uuid4()
        initial_data = {"counter": 1, "global_counter": 0}

        while True:
            # with open("/home/iquanti/Documents/Iquanti_related_work/POC/POC_server_sent_events/POC_approach_1/global.json", "r+") as f:
            #     data = json.load(f)
            data=dict(global_counter= "dummy value")
            # Please note: the id is appended below message data by the server, to ensure that lastEventId is updated after the message is received.
            initial_data["counter"] += 1
            initial_data["global_counter"] = data["global_counter"]
            yield f"\nevent: event1\ndata: {initial_data}\nid:{str(signature)}\n\n"
            time.sleep(1)


# ADVANCED STREAMING VIEW
class AdvancedStreamingView(View):

    def get(self, request):

        user = User(request)
        Authenticator.authenticate(user)
        response_stream = Stream.subscribe(user)
        return response_stream


class User:
    def __init__(self, request):

        self.role = request.GET.get("role").lower()


class Authenticator:
    def authenticate(user: User):
        return True


class Stream:
    
    @staticmethod
    def subscribe(user: User):
        role = user.role
        generator_fn = StreamFactory.get_stream(for_role=role)
        streaming_http_res = StreamingHttpResponse(generator_fn())
        streaming_http_res["Content-Type"] = 'text/event-stream'
        streaming_http_res['Cache-Control'] = 'no-cache'
        streaming_http_res['Connection'] = 'keep-alive'
        return streaming_http_res


class LeadStream:
    """
    Lead Stream Impl.
    """
    COUNTER = 0

    @staticmethod
    def get():

        user_data = dict()
        global_data = dict()

        while True:
            with open("/home/iquanti/Documents/Iquanti_related_work/POC/POC_server_sent_events/POC_approach_1/global_1.json", "r+") as f:
                global_processs_data = json.load(f)

            # Please note: the id is appended below message data by the server, to ensure that lastEventId
            # is updated after the message is received.
            LeadStream.COUNTER += 1
            user_data["local_process_value"] = LeadStream.COUNTER 
            global_data["global_process_value"] = global_processs_data["global_process_1"]

            with open("lead_stream_payload_storage.json", "r+") as f:
                payload_data: dict = json.load(f)
                if payload_data.get("floating_point_numbers"):
                    payload_data["floating_point_numbers"].append(global_data["global_process_value"])
                else:
                    payload_data["floating_point_numbers"] = [global_data["global_process_value"]]

                payload_data.update(LeadStream.get_changed_dict(global_data["global_process_value"]))
                f.seek(0)
                json.dump(payload_data, f)
                f.truncate()

            data = dict(
                timestamp=datetime.datetime.now(),
                user_data=user_data,
                global_data=global_data,
                payload_data=payload_data
            )
            yield f"\ndata: {data}\nid:some ref value\n\n"
            time.sleep(1)

    @staticmethod
    def get_changed_dict(float_value: float):
        float_part, integer_part = math.modf(float_value)
        return {float_value: dict(float_part=float_part, integer_part=integer_part)}


class SoftwareEngineerStream:
    """
    Lead Stream Impl.
    """
    COUNTER = 0

    @staticmethod
    def get():

        user_data = dict(
        )
        global_data = dict(
        )

        while True:
            message_id = str(uuid4())

            with open("/home/iquanti/Documents/Iquanti_related_work/POC/POC_server_sent_events/POC_approach_1/global_2.json", "r+") as f:
                global_processs_data = json.load(f)

            # Please note: the id is appended below message data by the server, to ensure that lastEventId is updated after the message is received.
            SoftwareEngineerStream.COUNTER += 1
            user_data["local_process_value"] = SoftwareEngineerStream.COUNTER 
            global_data["global_process_value"] = global_processs_data["global_process_2"]

            with open("se_stream_delta_storage.json", "r+") as f:
                delta_record: dict = json.load(f)
                new_delta = dict(
                    message_id=message_id,
                    numbers=[global_data["global_process_value"]],
                    odd=[global_data["global_process_value"]] if global_data["global_process_value"] % 2 != 0 else [],
                    even=[global_data["global_process_value"]] if global_data["global_process_value"] % 2 == 0 else []
                )
                delta_record[message_id] = new_delta

                f.seek(0)
                json.dump(delta_record, f)
                f.truncate()

            yield f"\ndata: {new_delta}\nid:{message_id}\n\n"
            time.sleep(1)


class StreamFactory:

    # storage of references of generator functions
    STREAM_MAP = dict(
        lead=LeadStream.get,
        se=SoftwareEngineerStream.get
    )

    @staticmethod
    def get_stream(for_role):
        """
        This function LeadStream decides which stream to return based on credentials
        """
        return StreamFactory.STREAM_MAP.get(for_role)

    def register_stream(self):
        """
        This function is for future use to register a stream with this class
        """
        pass