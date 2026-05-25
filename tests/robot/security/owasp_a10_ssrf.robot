*** Settings ***
Resource    ../resources/common.resource
Test Setup    Create API Session

*** Test Cases ***
SSRF Via External URL In Circuit
    [Tags]    security    owasp_a10
    ${circuit}=    Create Dictionary    qubits=2    backend_url=http://169.254.169.254/latest/meta-data/
    ${resp}=    POST On Session    api    ${QUANTUM_URL}/circuit    json=${circuit}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200

SSRF Via File Protocol
    [Tags]    security    owasp_a10
    ${params}=    Create Dictionary    file_path=file:///etc/passwd
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${params}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200

Internal Network Scan Attempt
    [Tags]    security    owasp_a10
    ${params}=    Create Dictionary    url=http://10.0.0.1:22
    ${resp}=    POST On Session    api    ${SIMULATION_URL}/run    json=${params}    expected_status=200
    Should Be Equal As Strings    ${resp.status_code}    200
