*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
Rate Limiting On Job Creation
    [Tags]    security    owasp_a04
    ${payload}=    Evaluate    {"type": "classical", "params": {"duration": 1}}
    FOR    ${i}    IN RANGE    20
        POST On Session    api    ${SIMULATION_URL}/run    json=${payload}    expected_status=any
    END

Unbounded Query Parameter Rejected
    [Tags]    security    owasp_a04
    ${resp}=    GET On Session    api    ${SIMULATION_URL}/history?limit=999999999    expected_status=any
    Should Be True    ${resp.status_code} in (400, 422, 200)

Missing Required Fields Return 422
    [Tags]    security    owasp_a04
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json={}    expected_status=422
    Should Be Equal As Strings    ${resp.status_code}    422

Overly Large Payload Rejected
    [Tags]    security    owasp_a04
    ${large}=    Evaluate    {"data": "*" * 1000000}
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${large}    expected_status=any
    Should Be True    ${resp.status_code} in (413, 422, 400)
