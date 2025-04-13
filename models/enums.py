from enum import Enum


class ExceptionMessage(Enum):
    token_not_found = 'Token generation failed'
    aws_connecion_error = 'Error in connecting to AWS resources'
    aws_s3_write_exception = 'Error in writing to S3 bucket'
    aws_s3_download_exception = 'Error in generating download link'
    # DB #
    db_connection_error = 'Error in connecting to host database'
    db_cursor_fetch_error = 'Error in fetching results from database'
    # some Error occurred
    fail_to_create = "Some error occurred"
    # five 9 errors
    fail_to_dispose = "Error in setting the call disposition. Please dispose from the dialer window."
    fail_to_disconnect = "Error in disconnecting the call. Please disconnect from the dialer window."
    call_disconnect_success = "Call disconnected"
    call_dispose_success = "Call disposed"
    duplicate_name_entry = "Name already exist"
    call_disposition_saved = "Call disposition saved"
    mapping_not_exist = 'No mapping exist'
    pcp_details_not_found = "PCP Name Not Found"
    cache_msg = "No data found in visit_data_cache table"
    sp_msg = "No data found in SP"
    no_data_found = "No data found"
    member_not_found = "Member Not Found"
    no_tests_found = "No test results found"


    # conflicts
    conflicts_occurred = 'Some conflicts occurred'
    members_not_found = "Members Not Found"
    mapping_list_not_found = "Mapping List Not Found"
    look_up_not_found = "lookup Not Found"
    state_not_found = "State Not Found"
    pcp_not_found = "PCP Not Found"
    healthplan_not_found = "Healthplan Not  Found"
    account_not_found = "Account Not Found"
    call_not_created = "Call Not Created"
    call_history_not_found = "Call History Not Found"
    disposition_not_found = "Disposition Not Found"
    member_visit_info_not_found = "Visit Info Not Found"
    member_info_not_found = "Member Info Not Found"
    call_already_finished = "Call Already Finished"
    call_not_found = "Call not Found"
    no_match_found = "No Match Found"
    headers_not_found = "No Headers Found"
    pvs_authentication_error = "Invalid Credentials"
    physician_not_found = "Physician not Found"
    dialPad_message="DialPad :"

    agent_not_authorized_for_call = "Agent is not authorized to make a call"
    interaction_id_call_ended = 'Call with this interaction id has already ended'
    dialpad_call_dispose_error = 'Error in disposing the call'
    dialpad_call_ongoing = 'Error : Dialpad call still ongoing.'



class HTTPStatus(Enum):
    success = (200, 'success')
    created = (201, 'created')
    accepted = (202, 'accepted')
    no_content = (204, 'no content')
    bad_request = (400, 'bad_request')
    unauthorized = (401, 'unauthorized request')
    unauthorized_new = (402, 'unauthorized request')
    not_found = (404, 'resource not found')
    conflict = (409, 'duplicate conflict')
    unprocessable_entity = (422, 'Unprocessable Entity')
    method_failure = (420, 'Method Failure')
    error = (500, 'application error occured')
    existing_session = (435, 'session already exists')


class AppStatus(Enum):
    success = {'code': 200, 'message': 'success'}
    logging_error = {'code': 900, 'message': 'error in logging request'}


class TypeOfErrorEnum(Enum):
    json_invalid_error = "json_invalid"
    value_error_missing = "value_error.missing"
    value_error_none = "value_error.none"
    value_error_max_length = "value_error.any_str.max_length"
    value_error_min_length = "value_error.any_str.min_length"
    type_error_list = "type_error.list"
    type_error = "type_error"
    type_error_none_not_allowed = "type_error.none.not_allowed"


class UniversalMessage(Enum):
    access_token = "Token generated successfully"
    request_data_error = "Sending Incorrect  Request payload format"
    key_missing_error = "{} key Required field"
    key_none_error = "{} key None"
    incorrect_data_error = "{} data incorrect "
    submitted_message = "Answers Submitted Successfully"
    deleted_message = "Deleted Successfully"
    some_thing_went_wrong = "Something Went Wrong"
    permission_denied = "Permission Denied"
    update_message = "Info Updated Successfully"
    data_added = "Data Added Successfully"
    document_uploaded = "File Uploaded Successfully"
    change_req_sent = "Change Request Sent"
    mapping_created = "Education Material Mapping has been created successfully"
    cache_data = "Data Found From Cache"
    sp_data = "Data Found From SP"
    not_found = "Data Not Found From SP"
    task_disposition = "Task Disposed Successfully"
    pcp_info_edit = "PCP Information updated Successfully"
    notes_saved_successfully = 'Note Saved successfully'
