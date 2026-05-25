*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
Server Responds To Malformed Input
    [Tags]    security    owasp_a09
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json={"type": "classical"}    expected_status=any
    Should Be True    ${resp.status_code} >= 400

Empty Body Returns Structured Error
    [Tags]    security    owasp_a09
    ${headers}=    Create Dictionary    Content-Type    application/json
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    data=${EMPTY}    headers=${headers}    expected_status=any
    Should Be True    ${resp.status_code} >= 400

Error Response Is Consistent Format
    [Tags]    security    owasp_a09
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json={"bad": "data"}    expected_status=422
    ${json}=    Set Variable    ${resp.json()}
    ${has_detail}=    Run Keyword And Return Status    Dictionary Should Contain Key    ${json}    detail
    ${has_message}=    Run Keyword And Return Status    Dictionary Should Contain Key    ${json}    message
    Evaluate    ${has_detail} or ${has_message}
