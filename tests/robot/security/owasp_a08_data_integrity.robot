*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
No Unsigned Deserialization Endpoints
    [Tags]    security    owasp_a08
    ${headers}=    Create Dictionary    Content-Type    application/x-python-serialize
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    data=cos.system\n(S'ls'\ntR.    headers=${headers}    expected_status=any
    Should Be True    ${resp.status_code} in (400, 415, 422, 404)

Content-Type Enforced
    [Tags]    security    owasp_a08
    ${headers}=    Create Dictionary    Content-Type    text/html
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    data=<xml>bad</xml>    headers=${headers}    expected_status=any
    Should Be True    ${resp.status_code} in (400, 415, 422)

No Cache Busting On Sensitive Data
    [Tags]    security    owasp_a08
    ${resp}=    GET On Session    api    ${SIMULATION_URL}/history    expected_status=any
    ${cache}=    Get From Dictionary    ${resp.headers}    Cache-Control    default=missing
    Run Keyword And Continue On Failure    Should Not Contain    ${cache}    no-store
