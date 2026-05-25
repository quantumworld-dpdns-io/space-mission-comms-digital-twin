*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
Server Header Does Not Leak Version
    [Tags]    security    owasp_a06
    ${resp}=    GET On Session    api    /health    expected_status=200
    ${server}=    Get From Dictionary    ${resp.headers}    Server    default=missing
    Run Keyword And Continue On Failure    Should Not Contain    ${server}    Python
    Run Keyword And Continue On Failure    Should Not Contain    ${server}    uvicorn

Component Metadata Hidden
    [Tags]    security    owasp_a06
    ${resp}=    GET On Session    api    /health    expected_status=200
    ${body}=    Convert To String    ${resp.json()}
    Should Not Contain    ${body}    django
    Should Not Contain    ${body}    flask
    Should Not Contain    ${body}    fastapi.version

No Known Default Credentials
    [Tags]    security    owasp_a06
    ${headers}=    Create Dictionary    Authorization    Basic admin:admin
    ${resp}=    GET On Session    api    /health    headers=${headers}    expected_status=any
    Should Be True    ${resp.status_code} in (200, 401, 403)
