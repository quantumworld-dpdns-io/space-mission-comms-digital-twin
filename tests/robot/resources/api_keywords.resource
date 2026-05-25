*** Settings ***
Resource    common.resource

*** Keywords ***
Run Classical Simulation
    [Arguments]    ${tx_power}=10    ${frequency}=8    ${distance}=1000000
    ${params}=    Create Dictionary    tx_power=${tx_power}    frequency=${frequency}    distance=${distance}
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${params}
    Should Be Equal As Strings    ${resp.status_code}    200
    ${job_id}=    Get From Dictionary    ${resp.json()}    job_id
    RETURN    ${job_id}

Get Simulation Result
    [Arguments]    ${job_id}
    ${resp}=    GET On Session    api    ${SIMULATION_URL}/result/${job_id}
    Should Be Equal As Strings    ${resp.status_code}    200
    RETURN    ${resp.json()}

List Quantum Backends
    ${resp}=    GET On Session    api    ${QUANTUM_URL}/backends
    Should Be Equal As Strings    ${resp.status_code}    200
    RETURN    ${resp.json()}

Run QKD Protocol
    [Arguments]    ${protocol}=BB84    ${num_bits}=256
    ${params}=    Create Dictionary    protocol=${protocol}    num_bits=${num_bits}
    ${resp}=    POST On Session    api    ${QUANTUM_URL}/qkd    json=${params}
    Should Be Equal As Strings    ${resp.status_code}    200
    ${job_id}=    Get From Dictionary    ${resp.json()}    job_id
    RETURN    ${job_id}

Run Route Optimization
    [Arguments]    ${graph}    ${source}    ${target}
    ${params}=    Create Dictionary    graph=${graph}    source=${source}    target=${target}
    ${resp}=    POST On Session    api    ${OPTIMIZATION_URL}/route    json=${params}
    Should Be Equal As Strings    ${resp.status_code}    200
    RETURN    ${resp.json()}
