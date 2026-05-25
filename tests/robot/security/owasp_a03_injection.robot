*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
SQL Injection Attempt On Simulation
    [Tags]    security    owasp_a03
    ${params}=    Create Dictionary    query=1' OR '1'='1
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${params}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200

Command Injection In Parameters
    [Tags]    security    owasp_a03
    ${params}=    Create Dictionary    tx_power=10; whoami
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${params}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200

XSS In Simulation Endpoint
    [Tags]    security    owasp_a03
    ${params}=    Create Dictionary    name=<script>alert('xss')</script>
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${params}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200

JSON Injection In Quantum Circuit
    [Tags]    security    owasp_a03
    ${circuit}=    Create Dictionary    qubits=0    operations=${EMPTY}
    ${resp}=    POST On Session    api    ${QUANTUM_URL}/circuit    json=${circuit}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200
