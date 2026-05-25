*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
Empty Authorization Header
    [Tags]    security    owasp_a07
    ${headers}=    Create Dictionary    Authorization=
    ${resp}=    GET On Session    api    /health    headers=${headers}
    Should Be Equal As Strings    ${resp.status_code}    200

Malformed JWT Token
    [Tags]    security    owasp_a07
    ${headers}=    Create Dictionary    Authorization=Bearer invalid.jwt.token
    ${resp}=    GET On Session    api    /health    headers=${headers}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200

Weak Credentials Simulation
    [Tags]    security    owasp_a07
    ${params}=    Create Dictionary    username=admin    password=admin
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${params}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200
