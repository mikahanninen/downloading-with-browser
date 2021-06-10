*** Settings ***
Library  RPA.Browser.Selenium

*** Variables ***
${website}   https://downloads.robocorp.com/rcc/releases/index.html
${DOWNLOAD_TIMEOUT}   30



*** Keywords ***
Check Downloaded Items
    ${result}=  Execute Javascript   return document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;
    [Return]  ${result}

*** Keywords ***
Are All Downloads Complete
    ${items}=   Check Downloaded Items
    ${all_done}=  Set Variable  ${TRUE}
    FOR  ${item}   IN   @{items}
        IF  "${item}[state]" != "COMPLETE"
            ${all_done}=  Set Variable  ${FALSE}
            Exit For Loop
        END
    END
    ${returnable}=  Create Dictionary  all_done=${all_done}   items=${items}
    [Return]  ${returnable}


*** Tasks ***
Minimal Task
    # ROBOT_ROOT - basically current directory
    # ROBOT_ARTIFACTS - directory defined in robot.yaml with `artifactsDir`
    Set Download Directory  %ROBOT_ARTIFACTS%
    Open Available Browser  ${website}   browser_selection=chrome
    Wait Until Element Is Visible    (//ul//li/a)[1]
    Click Element    (//ul//li/a)[1]
    Execute Javascript  window.open('about:blank','_blank');
    Switch Window       NEW
    Go To   chrome://downloads
    FOR   ${_}  IN RANGE  ${DOWNLOAD_TIMEOUT}
        ${result}=   Are All Downloads Complete
        IF   ${result}[all_done]
            Exit For Loop
        ELSE
            Log  Downloading...
        END
        Sleep  1s

    END
