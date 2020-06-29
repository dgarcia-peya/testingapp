import json
import requests

from .config import *


def get_headers(project_id):
    """Format the http header with the authentication based on the project id

    :param project_id: The FWF Project Id
    :return: Dict
    """
    api_token = [p['token'] for p in FWF_PROJECTS if p['id'] == project_id][0]
    headers = {'Authorization': api_token}
    return headers


def get_projects():
    """Return the FWF projects list

    :return: Project tuples list
    """
    return [(p['id'], p['name']) for p in FWF_PROJECTS]


def get_features_list(project_id):
    """Get the list of the FWF Features configured in a project

    :param project_id: The FWF project identification
    :return: Json Object with the project features
    """
    url = f'{FWF_API_BASE_URL}/features-list/keys'

    response = requests.get(url, headers=get_headers(project_id))
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def get_feature_data(project_id, feature_key):
    """Get the FWF Feature detailed data

    :param project_id: The FWF project identification
    :param feature_key: The FWF Feature key
    :return: Json object with the Feature FWF configuration
    """
    url = f'{FWF_API_BASE_URL}/features/{feature_key}/data'

    response = requests.get(url, headers=get_headers(project_id))
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
