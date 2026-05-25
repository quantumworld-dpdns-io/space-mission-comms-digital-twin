*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
Health Endpoint Returns 200
    [Tags]    smoke    health
    Health Check Should Succeed

Root Endpoint Returns API Info
    [Tags]    smoke
    ${resp}=    GET On Session    api    /
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    message

Metrics Endpoint Returns Data
    [Tags]    smoke    metrics
    ${resp}=    GET On Session    api    /metrics
    Should Be Equal As Strings    ${resp.status_code}    200
