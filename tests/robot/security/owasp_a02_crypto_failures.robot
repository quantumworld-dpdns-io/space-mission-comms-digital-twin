*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
Response Does Not Leak Sensitive Headers
    [Tags]    security    owasp_a02
    ${resp}=    GET On Session    api    /health    expected_status=any
    Dictionary Should Not Contain Key    ${resp.headers}    X-Powered-By
    Dictionary Should Not Contain Key    ${resp.headers}    Server-SSL

API Does Not Expose Stack Traces
    [Tags]    security    owasp_a02
    ${headers}=    Create Dictionary    Content-Type    application/json
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json={"bad": "data"}    expected_status=any
    Should Not Match Regexp    ${resp.text}    Traceback \\(most recent call last\\)

No Plaintext Secrets In Response
    [Tags]    security    owasp_a02
    ${resp}=    GET On Session    api    /health    expected_status=200
    ${body}=    Convert To String    ${resp.json()}
    Should Not Contain    ${body}    password
    Should Not Contain    ${body}    secret
    Should Not Contain    ${body}    token

HTTP Strict Transport Security Header
    [Tags]    security    owasp_a02
    ${resp}=    GET On Session    api    /health    expected_status=200
    ${hsts}=    Get From Dictionary    ${resp.headers}    Strict-Transport-Security    default=missing
    Run Keyword And Continue On Failure    Should Be Equal As Strings    ${hsts}    missing
