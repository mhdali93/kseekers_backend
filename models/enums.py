from enum import Enum


class ExceptionMessage(Enum):
    # Currently used values

    db_connection_error = 'Error in connecting to host database'
    db_cursor_fetch_error = 'Error in fetching results from database'
    fail_to_create = "Some error occurred"
    member_not_found = "Member Not Found"
    
    # Unused values (commented out)
    # aws_connecion_error = 'Error in connecting to AWS resources'
    # aws_s3_write_exception = 'Error in writing to S3 bucket'
    # aws_s3_download_exception = 'Error in generating download link'
    # token_not_found = 'Token generation failed'
    # duplicate_name_entry = "Name already exist"
    # mapping_not_exist = 'No mapping exist'
    # no_data_found = "No data found"
    # conflicts_occurred = 'Some conflicts occurred'
    # look_up_not_found = "lookup Not Found"
    # no_match_found = "No Match Found"
    # headers_not_found = "No Headers Found"


class HTTPStatus(Enum):
    # Currently used values
    success = (200, 'success')
    created = (201, 'created')
    bad_request = (400, 'bad_request')
    unauthorized = (401, 'unauthorized request')
    not_found = (404, 'resource not found')
    error = (500, 'application error occured')
    
    # Unused values (commented out)
    # accepted = (202, 'accepted')
    # no_content = (204, 'no content')
    # unauthorized_new = (402, 'unauthorized request')
    # conflict = (409, 'duplicate conflict')
    # unprocessable_entity = (422, 'Unprocessable Entity')
    # method_failure = (420, 'Method Failure')
    # existing_session = (435, 'session already exists')

    @classmethod
    def from_code(cls, code):
        for member in cls:
            if member.value[0] == code:
                return member
        return None


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
    # Currently used values
    access_token = "Token generated successfully"
    request_data_error = "Sending Incorrect  Request payload format"
    key_missing_error = "{} key Required field"
    key_none_error = "{} key None"
    incorrect_data_error = "{} data incorrect "
    some_thing_went_wrong = "Something Went Wrong"
    permission_denied = "Permission Denied"
    
    # Unused values (commented out)
    # submitted_message = "Answers Submitted Successfully"
    # deleted_message = "Deleted Successfully"
    # update_message = "Info Updated Successfully"
    # data_added = "Data Added Successfully"
    # document_uploaded = "File Uploaded Successfully"
    # change_req_sent = "Change Request Sent"
    # cache_data = "Data Found From Cache"
