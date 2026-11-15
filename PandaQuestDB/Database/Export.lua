-- Publish one database package for PandaQuest's core after this client's data files have loaded.
-- The core's SavedVariables use the separate PandaQuestDB name.
local _, ns = ...

_G.PandaQuestDBData = {
    api = 1,
    game = ns.Data.game,
    Data = ns.Data,
    Overrides = ns.Overrides,
}
