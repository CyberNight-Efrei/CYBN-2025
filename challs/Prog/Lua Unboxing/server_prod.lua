local socket = require("socket")
local server = assert(socket.bind("*", 23456))
print("Server running on port 23456")


local _, FLAG = pcall(function()
    return 'CYBN{3sc4p3d_fr0m_lu4}'
end)

local safe_env = {
    tonumber = tonumber,
    tostring = tostring,
    type = type,
    pairs = pairs,
    debug = debug,
    ipairs = ipairs,
    math = math,
    FLAG = nil
}

while true do
    local client = server:accept()
    client:send("Bienvenue dans votre Sandbox Luaz !\n")

    while true do
        client:send("> ")
        local user_code = client:receive("*l")
        if not user_code or user_code == "exit" then
            client:send("Au revoir !\n")
            break
        end

        local f, load_err = load(user_code, "user_code", "t", safe_env)

        if not f then
            client:send("Erreur : " .. load_err .. "\n")
        else
            local success, result = pcall(f)
            print(result)
            if success then
                if not result then
                    client:send("La fonction n'a pas retourné de valeur.\n")
                elseif type(result) ~= "string" then
                    client:send("La sortie n'est pas une chaîne de caractères.\n")
                elseif string.find(result, FLAG) then
                    client:send("Flag détecté, vous n'êtes pas autorisé à le lire.\n")
                else
                    client:send("=> " .. tostring(result) .. "\n")
                end
            else
                client:send("Erreur d'exécution : " .. tostring(result) .. "\n")
            end
        end
    end
    client:close()
end