*** Settings ***
Resource    ../resources/api_keywords.resource
Test Setup    Create API Session

*** Test Cases ***
List Quantum Backends
    [Tags]    smoke    quantum
    ${backends}=    List Quantum Backends
    Should Not Be Empty    ${backends}

Run QKD Protocol Successfully
    [Tags]    quantum
    ${job_id}=    Run QKD Protocol    BB84    128
    Job Should Complete    ${job_id}    ${QUANTUM_URL}

Run Quantum Teleportation
    [Tags]    quantum
    ${resp}=    POST On Session    api    ${QUANTUM_URL}/teleport    json={}
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    fidelity

Get Quantum Job Status
    [Tags]    quantum
    ${job_id}=    Run QKD Protocol    BB84    64
    ${resp}=    GET On Session    api    ${QUANTUM_URL}/jobs/${job_id}
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    status
