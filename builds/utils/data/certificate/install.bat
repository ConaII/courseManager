@echo off
title Wood Certificate Installer
call :setESC    
call :START


:START
cls
echo.
echo %ESC%[91m ##################################
echo %ESC%[91m #   %ESC%[96mWOOD CERTIFICATE INSTALLER   %ESC%[91m#
echo %ESC%[91m ##################################
echo.
echo %ESC%[31m:: %ESC%[36mThis script will install a windows certificate signature for Wood.
echo %ESC%[31m:: %ESC%[36mIt should allow to execute Wood without falsely prompting your antivirus.
echo %ESC%[31m:: %ESC%[36mSince this is a Self-Asigned digital signature, we need you to allow it to be installed.
echo %ESC%[31m:: %ESC%[36mUsing an approved authority certificate would cost money, so this is the only way.
echo. 
echo    %ESC%[32mProceed^? %ESC%[96mYES %ESC%[37m^| %ESC%[91mNO
echo.
SET /p input="%ESC%[31m>> %ESC%[0m"
 if /i "%input%"=="yes" GOTO SCRIPT
 if /i "%input%"=="no" goto EXIT
 else (
    goto START
 )

:SCRIPT
powershell Import-Certificate -FilePath woodcert.crt -CertStoreLocation cert:\CurrentUser\Root
goto FINISH


::
:: Finished installed.
::
:FINISH
ECHO  %ESC%[40;37m-----------------------
ECHO  ^| %ESC%[1m%ESC%[92m Install finished^!  %ESC%[0m^|
ECHO  -----------------------
ECHO %ESC%[40;37m %ESC%[91m
pause
goto EXIT


::
:: Exit the script.
::
:EXIT
ECHO %ESC%[40;37m
ECHO --------------
ECHO ^|%ESC%[1m%ESC%[91m Exiting... %ESC%[0m^|
ECHO --------------%ESC%[40;37m %ESC%[91m
TIMEOUT /T 10
exit


::
:: Assign Per-line color manager.
::
:setESC
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set ESC=%%b
  exit /B 0
)