; AutoHotkey v1
; F10 = Start/Stop
; Python erkennt das Bild und gibt FOUND/NOT_FOUND zurück
; Wenn FOUND, drückt AutoHotkey F11

Toggle := false

F10::
{
    global Toggle
    Toggle := !Toggle
    if (Toggle)
    {
        ToolTip, START
    }
    else
    {
        ToolTip, STOP
    }
    SetTimer, Check, 50
    return
}

Check:
{
    global Toggle
    if (!Toggle)
        return

    result := RunPythonCheck()
    if (result = "FOUND")
    {
        Send, {F11}
        Sleep, 250
    }
    return
}

RunPythonCheck()
{
    shell := ComObjCreate("WScript.Shell")
    exec := shell.Exec(ComSpec " /C python check_image.py")
    output := exec.StdOut.ReadAll()
    return Trim(output)
}
