*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  lauri
    Set Password  lauri574
    Set Password Confirmation  lauri574
    Click Button  Register
    Register Should Succeed


Register With Too Short Username And Valid Password
    Set Username  la
    Set Password  lauri574
    Set Password Confirmation  lauri574
    Click Button  Register
    Register Should Fail With Message  Username too short


Register With Valid Username And Too Short Password
    Set Username  lauri
    Set Password  lauri5
    Set Password Confirmation  lauri5
    Click Button  Register
    Register Should Fail With Message  Password too short

Register With Valid Username And Invalid Password
    Set Username  lauri
    Set Password  lauriiiii
    Set Password Confirmation  lauriiiii
    Click Button  Register
    Register Should Fail With Message  Password must contain letters and numbers

Register With Nonmatching Password And Password Confirmation
    Set Username  lauri
    Set Password  lauri123
    Set Password Confirmation  lauri574
    Click Button  Register
    Register Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  lauri
    Set Password  lauri574
    Set Password Confirmation  lauri574
    Click Button  Register
    Register Should Succeed
    Go To Register Page
    Set Username  lauri
    Set Password  lauri574
    Set Password Confirmation  lauri574
    Click Button  Register
    Register Should Fail With Message  User with username lauri already exists

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

