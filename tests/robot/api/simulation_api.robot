*** Settings ***
Resource    ../resources/api_keywords.resource
Test Setup    Create API Session

*** Test Cases ***
Run Classical Simulation Successfully
    [Tags]    smoke    simulation
    ${job_id}=    Run Classical Simulation
    Job Should Complete    ${job_id}    ${SIMULATION_URL}
    ${result}=    Get Simulation Result    ${job_id}
    Should Not Be Empty    ${result}

Simulation Returns Job ID
    [Tags]    simulation
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json={}
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    job_id

List Simulation History
    [Tags]    simulation
    ${resp}=    GET On Session    api    ${SIMULATION_URL}/history
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    simulations

Get Nonexistent Simulation Returns 404
    [Tags]    negative
    ${resp}=    GET On Session    api    ${SIMULATION_URL}/status/nonexistent-id    expected_status=404
    Should Be Equal As Strings    ${resp.status_code}    404
