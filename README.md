# PandaQuest Database

PandaQuest Database supplies the quests, NPCs, objects, items and zone data used by the
[PandaQuest addon](https://github.com/vem882/pandaquest). It also includes quest corrections and
available gathering, respawn, drop and flight data for the supported game versions.

## Install

Install **PandaQuest** and **PandaQuest Database** for the same World of Warcraft game version.
Keep both enabled in the game's AddOns list. The database loads first and PandaQuest uses it when
the player logs in. The database needs PandaQuest to display quests, navigation and tooltips.

For manual installation, download the two packages from
[PandaQuest Releases](https://github.com/vem882/pandaquest/releases) and extract them into the same
game's `Interface/AddOns` directory. The addon folders are `PandaQuest` and `PandaQuestDB`.
Restart the game after installing or replacing addon files.

| Game | Game subfolder | Database manifest |
| --- | --- | --- |
| Mists of Pandaria Classic | `_classic_` | `PandaQuestDB_Mists.toc` |
| Classic Era | `_classic_era_` | `PandaQuestDB_Vanilla.toc` |
| The Burning Crusade Classic Anniversary | `_anniversary_` | `PandaQuestDB_TBC.toc` |
| WoW Forever | `_forever_` | `PandaQuestDB_Forever.toc`, `PandaQuestDB_Camelot.toc` |

PandaQuest Auction is a separate, optional extension. PandaQuest Sync remains the optional desktop
app for sharing opted-in observations and updating the installed community guide.

## Maintaining the data

`PandaQuestDB/Database` contains the shipped game data. Each game manifest loads only its own
dataset, selected by the WoW client. Keep generated paths stable. Regenerate quest data using
[the PandaBase generator](https://github.com/vem882/pandawow/blob/main/tools/build_db.py).
Portal corrections and supplemental data come from the PandaBase data sync.

`Database/Export.lua` exposes the selected game, data and shipped overrides to PandaQuest through
the versioned `PandaQuestDBData` table. The runtime query logic and the locally updated community
guide live in PandaQuest. The main [PandaQuest repository](https://github.com/vem882/pandaquest)
builds the version-matched packages from PandaQuest, this repository and
[pqAuction](https://github.com/vem882/pqAuction).


## Data sources and licence

PandaQuest Database is distributed under the [GNU General Public License v3](LICENSE).
The generated quest, NPC, object, item and zone tables draw from
[Questie](https://github.com/Questie/Questie) and [QuestieDB](https://github.com/Questie/QuestieDB).
Gathering, respawn and drop seed data includes material from
[pfQuest](https://github.com/shagu/pfQuest) under its
[MIT licence](PandaQuestDB/licenses/pfQuest-MIT.txt).
See [PandaBase's source index](https://pd.zroot.it/sources) for supplemental data and credits.

World of Warcraft is a trademark of Blizzard Entertainment. PandaQuest is an independent fan project.

The addon icon combines the PandaQuest logo with the WoW texture `INV_MISC_BOOK_09`. The game artwork belongs to Blizzard Entertainment.

Each release includes a generated `CHANGELOG.md` in the addon folder. The same added, changed and removed sections appear on GitHub and CurseForge.
