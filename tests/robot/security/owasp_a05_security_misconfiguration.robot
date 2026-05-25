*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
No Debug Endpoints Exposed
    [Tags]    security    owasp_a05
    ${resp}=    GET On Session    api    /debug    expected_status=any
    Should Be True    ${resp.status_code} in (404, 405, 403)
    ${resp}=    GET On Session    api    /debug/vars    expected_status=any
    Should Be True    ${resp.status_code} in (404, 405, 403)

HTTP Methods Enforced
    [Tags]    security    owasp_a05
    ${resp}=    PUT On Session    api    /health    expected_status=any
    Should Be True    ${resp.status_code} in (405, 404, 400)
    ${resp}=    DELETE On Session    api    /health    expected_status=any
    Should Be True    ${resp.status_code} in (405, 404, 400)

Default Error Content Type Is Json
    [Tags]    security    owasp_a05
    ${resp}=    GET On Session    api    /nonexistent-route-xyz    expected_status=any
    ${content_type}=    Get From Dictionary    ${resp.headers}    Content-Type    default=text/html
    Should Contain    ${content_type}    json

CORS Methods Restricted
    [Tags]    security    owasp_a05
    ${headers}=    Create Dictionary    Origin=https://evil.com
    ${resp}=    OPTIONS On Session    api    /health    headers=${headers}    expected_status=any
    Run Keyword And Continue On Failure    Should Be True    ${resp.status_code} in (200, 204, 400)
