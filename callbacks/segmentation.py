from dash import callback, Input, Output, State, no_update, ctx
from dash.exceptions import PreventUpdate
from utils.annotations import Annotations
from utils.data_utils import data
import numpy as np
import os
import uuid
import requests
import time

MODE = os.getenv("MODE", "")

DEMO_WORKFLOW = {
    "user_uid": "high_res_user",
    "job_list": [
        {
            "mlex_app": "high-res-segmentation",
            "description": "test_1",
            "service_type": "backend",
            "working_directory": "/data/mlex_repo/mlex_tiled/data",
            "job_kwargs": {
                "uri": "mlexchange1/random-forest-dc:1.1",
                "type": "docker",
                "cmd": 'python random_forest.py data/seg-results/spiral/image-train data/seg-results-test/spiral/feature data/seg-results/spiral/mask data/seg-results-test/spiral/model \'{"n_estimators": 30, "oob_score": true, "max_depth": 8}\'',
                "kwargs": {
                    "job_type": "train",
                    "experiment_id": "123",
                    "dataset": "name_of_dataset",
                    "params": '{"n_estimators": 30, "oob_score": true, "max_depth": 8}',
                },
            },
        },
        {
            "mlex_app": "high-res-segmentation",
            "description": "test_1",
            "service_type": "backend",
            "working_directory": "/data/mlex_repo/mlex_tiled/data",
            "job_kwargs": {
                "uri": "mlexchange1/random-forest-dc:1.1",
                "type": "docker",
                "cmd": "python segment.py data/data/20221222_085501_looking_from_above_spiralUP_CounterClockwise_endPointAtDoor_0-1000 data/seg-results-test/spiral/model/random-forest.model data/seg-results-test/spiral/output '{\"show_progress\": 1}'",
                "kwargs": {
                    "job_type": "train",
                    "experiment_id": "124",
                    "dataset": "name_of_dataset",
                    "params": '{"show_progress": 1}',
                },
            },
        },
    ],
    "host_list": ["vaughan.als.lbl.gov"],
    "dependencies": {"0": [], "1": [0]},
    "requirements": {"num_processors": 2, "num_gpus": 0, "num_nodes": 1},
}


@callback(
    Output("output-details", "children"),
    Output("submitted-job-id", "data"),
    Input("run-model", "n_clicks"),
    State("annotation-store", "data"),
    State("project-name-src", "value"),
)
def run_job(n_clicks, annotation_store, project_name):
    """
    This callback collects parameters from the UI and submits a job to the computing api.
    If the app is run from "dev" mode, then only a placeholder job_uid will be created.
    The job_uid is saved in a dcc.Store for reference by the check_job callback below.

    # TODO: This callback should also save the user's annotations to the Tiled server in
    mask format, so that the path can be submitted as part of the API request.

    """
    if n_clicks:
        if MODE == "dev":
            job_uid = uuid.uuid4()
            return (
                f"Workflow has been succesfully submitted with uid: {job_uid}",
                job_uid,
            )
        else:
            job_submitted = requests.post(
                "http://job-service:8080/api/v0/workflows", json=DEMO_WORKFLOW
            )
            job_uid = job_submitted.json()
            if job_submitted.status_code == 200:
                return (
                    f"Workflow has been succesfully submitted with uid: {job_uid}",
                    job_uid,
                )
            else:
                return (
                    f"Workflow presented error code: {job_submitted.status_code}",
                    job_uid,
                )
    return no_update, no_update


@callback(
    Output("output-details", "children", allow_duplicate=True),
    Output("submitted-job-id", "data", allow_duplicate=True),
    Input("submitted-job-id", "data"),
    Input("model-check", "n_intervals"),
    prevent_initial_call=True,
)
def check_job(job_id, n_intervals):
    """
    This callback checks to see if a job has completed successfully and will only
    update if there is a job_id present in the submitted-job-id dcc.Store. Will
    wait 3sec in "dev" mode to simulate.

    # TODO: Connect with the computing API when not in "dev" mode
    """
    if MODE == "dev":
        if job_id:
            time.sleep(3)
            return (
                f"Workflow {job_id} completed successfully. Click button below to view segmentation results.",
                None,
            )
        raise PreventUpdate
    else:
        # TODO - connect with API
        raise PreventUpdate
