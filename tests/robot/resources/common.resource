*** Variables ***
${BASE_URL}          http://localhost:8000
${API_PREFIX}        /api/v1
${TIMEOUT}           30s
${SIMULATION_URL}    ${BASE_URL}${API_PREFIX}/simulation
${QUANTUM_URL}       ${BASE_URL}${API_PREFIX}/quantum
${OPTIMIZATION_URL}  ${BASE_URL}${API_PREFIX}/optimization
${HEALTH_URL}        ${BASE_URL}/health

*** Keywords ***
Create API Session
    Create Session    api    ${BASE_URL}    timeout=${TIMEOUT}

Health Check Should Succeed
    ${resp}=    GET On Session    api    /health
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    status

Job Should Complete
    [Arguments]    ${job_id}    ${endpoint}
    ${resp}=    GET On Session    api    ${endpoint}/status/${job_id}
    Should Be Equal As Strings    ${resp.status_code}    200
    ${status}=    Get From Dictionary    ${resp.json()}    status
    Should Be Equal    ${status}    completed
