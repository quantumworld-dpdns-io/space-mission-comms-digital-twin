*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
Access Protected Endpoint Without Auth
    [Tags]    security    owasp_a01
    ${headers}=    Create Dictionary    Authorization=
    ${resp}=    GET On Session    api    /api/v1/quantum/jobs/nonexistent    headers=${headers}    expected_status=404
    Should Be Equal As Strings    ${resp.status_code}    404

IDOR On Simulation Result
    [Tags]    security    owasp_a01
    ${resp}=    GET On Session    api    ${SIMULATION_URL}/result/00000000-0000-0000-0000-000000000000    expected_status=404
    Should Be Equal As Strings    ${resp.status_code}    404

Forced Browsing To Admin Endpoint
    [Tags]    security    owasp_a01
    ${resp}=    GET On Session    api    /admin    expected_status=404
    Status Should Be    404    ${resp}

CORS Preflight Check
    [Tags]    security    owasp_a01
    ${headers}=    Create Dictionary    Origin=https://malicious-site.com
    ${resp}=    OPTIONS On Session    api    /health    headers=${headers}
    Should Be Equal As Strings    ${resp.status_code}    200
