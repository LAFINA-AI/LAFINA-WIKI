# Manual content and screenshot map

The web guides, downloadable PDF, and editable Word document share `src/data/manual.json`. Each step defines instructions, an expected result, an optional note, and an optional screenshot. User screenshots remain untouched in the root `screenshots/` directory.

## Sources and scope

- Structural reference: [SerbiSure User Manual](https://serbi-sure-user-manual.vercel.app/) and its [public repository](https://github.com/SerbiSure-Tagupa-et-al/SerbiSure-User-Manual), inspected at commit `d6bfd60`. The reference has topic/step navigation, an enlarged screenshot viewer, a full-manual view, Word download, and Print / Save PDF. LAFINA adapts the documentation pattern to its existing Astro wiki; no SerbiSure app instructions or code were copied.
- User-supplied Android screenshots: 36 files, 35 unique captures.
- Companion app: read-only inspection of `LAFINA-CAPSTONE-agy-development-cont` at commit `df573ba`, including WelcomeScreen, ProfileScreen, PreferencesSettingsScreen, IncomingCallScreen, calendar editors, and note/task editors.
- First-launch and incoming reminder steps have no supplied screenshots and explicitly identify source-based guidance. Troubleshooting has no invented screenshots.
- Model choices and cloud availability are version-, device-, and account-dependent. This manual does not certify physical-device alarm delivery or AI accuracy.
- Existing research pages remain available and can describe earlier architecture. Manual home and the wiki introduction distinguish that material from current usage.

## Editing and regeneration

1. Edit `src/data/manual.json`. Use stable chapter slugs and step IDs; these form deep links.
2. For a new image, add the original under `screenshots/` and fill its source filename, friendly output filename, descriptive alt text, and caption.
3. Run `npm run manual:assets`. This copies the referenced originals into `public/manual/screenshots/`.
4. Install the optional document authoring dependencies: `python -m pip install -r scripts/requirements-manual.txt`.
5. Run `npm run manual:pdf`. This writes the PDF and checksum manifest to `public/manual/`. The generator fails on text or caption overflow.
6. Run `npm run manual:docx` to regenerate the editable Word document and its checksum manifest. Word paragraphs, heading styles, internal links, image alt text, and embedded screenshots remain editable. To refresh contents page references after direct edits in Word, select all and update fields with Ctrl+A then F9.
7. Render and visually inspect the changed PDF and Word pages. Do not deliver an unreviewed regeneration.
8. Run `npm run check`, `npm run check:manual`, and `npm run build`. Build validates both documents and their screenshot checksums against the shared source.

The checked-in documents need no Python installation to serve or deploy. The PDF uses one page per step, preceded by a cover and two contents pages. If the manual grows enough to overflow its contents pages, update the chapter split and page calculation in the generator together.

## Screenshot placement

| Topic / step | Published screenshot | Original capture |
|---|---|---|
| Getting started / Find your way around Home | `home-dashboard.jpg` | `908737793_1757522452399161_6727713407775977477_n.jpg` |
| Getting started / Choose what your dashboard shows | `customize-dashboard.jpg` | `916986049_1128143286494071_3428092842347999980_n.jpg` |
| Navigate your schedule / See the month at a glance | `schedule-month.jpg` | `905977989_1863936831426037_3064573646112171982_n.jpg` |
| Navigate your schedule / Read a selected day's plan | `schedule-plan.jpg` | `908383469_4405644443021478_1134226438229626548_n.jpg` |
| Navigate your schedule / Review the week | `schedule-week.jpg` | `912493879_1162640776219135_3011939931818056052_n.jpg` |
| Navigate your schedule / Focus on one day | `schedule-day.jpg` | `914887036_1101419149384699_4330279024471686313_n.jpg` |
| Add and manage classes / Open class scheduling options | `calendar-options.jpg` | `907939059_1622058609041006_5824464249714241437_n.jpg` |
| Add and manage classes / Enter a class or review a scan | `add-class.jpg` | `909329143_1476036191155322_8141928292454302163_n.jpg` |
| Add and manage classes / Find, edit, or remove a saved class | `my-classes.jpg` | `914383757_1692535445945480_7457554418704702567_n.jpg` |
| Calendar groups and birthdays / Choose which calendars are visible | `calendar-visibility.jpg` | `903232067_837357699472521_8560780714660563493_n.jpg` |
| Calendar groups and birthdays / Create a schedule group | `new-schedule-group.jpg` | `914265376_1460264366259841_5597591349115312649_n.jpg` |
| Calendar groups and birthdays / Add a birthday | `birthdays.jpg` | `911662345_1672475380920210_8783219131454069837_n.jpg` |
| Create and manage alarms / Open your alarms | `alarms-empty.jpg` | `907328799_2936597933378562_9003281147956758271_n.jpg` |
| Create and manage alarms / Choose a time and repeat pattern | `new-alarm.jpg` | `904353058_1133322502634607_863631765778599142_n.jpg` |
| Create and manage alarms / Verify, disable, or edit an alarm | `alarms-active.jpg` | `907639363_3459845500842855_2591584492021011914_n.jpg` |
| Manage your to-do list / Add a to-do | `new-todo.jpg` | `916486130_4603038289911327_6286670615548811675_n.jpg` |
| Manage your to-do list / Find and complete tasks | `todo-list.jpg` | `921070094_2204187587148267_8046802961498164817_n.jpg` |
| Write and organize notes / Browse your notes | `notes-library.jpg` | `917613218_1131463513116045_2831375766955525200_n.jpg` |
| Write and organize notes / Write, preview, and save a note | `note-editor.jpg` | `917537252_2121226271859944_8018423131338463302_n.jpg` |
| Chat with LAFINA / Start a conversation | `ai-home.jpg` | `915220829_1874825090185019_9215606920478327097_n.jpg` |
| Chat with LAFINA / Attach a photo or schedule | `chat-attachments.jpg` | `909329166_1713765083752717_3105958351029224420_n.jpg` |
| Chat with LAFINA / Find or start a chat | `chat-history.jpg` | `906101184_4473837936216643_4044959678811657871_n.jpg` |
| Chat with LAFINA / Use a temporary conversation | `temporary-chat.jpg` | `919714215_2390149188420606_3615322229980619174_n.jpg` |
| Ask about the USTP handbook / Ask a handbook question and check its source | `ustp-handbook.jpg` | `912512435_29874014075555975_6332206563622420047_n.jpg` |
| Talk to LAFINA by voice / Read the call notice before starting | `call-privacy.jpg` | `915665285_1137463952095256_6699483656289082583_n.jpg` |
| Talk to LAFINA by voice / Wait for the voice connection | `call-connecting.jpg` | `912054065_1846872389767252_38588341555952433_n.jpg` |
| Talk to LAFINA by voice / Listen to LAFINA's response | `call-speaking.jpg` | `916559237_4178839245749174_6216258856327152405_n.jpg` |
| Talk to LAFINA by voice / Speak and check the transcript | `call-listening.jpg` | `915238428_1441385548196563_5499528374405420467_n.jpg` |
| Talk to LAFINA by voice / End the conversation | `call-ended.jpg` | `916021322_1646880097178590_1456194159259115965_n.jpg` |
| Choose an AI engine / Switch modes or prepare an offline model | `ai-engine-models.jpg` | `911876649_1456841102478742_3616074648404959316_n.jpg` |
| Profile and preferences / Review your academic profile | `academic-profile.jpg` | `914383804_1444740144476038_6086278489217983766_n.jpg` |
| Profile and preferences / Open scheduling and memory preferences | `profile-preferences.jpg` | `913886357_1004806232065768_1936460990395372266_n.jpg` |
| Profile and preferences / Set your routine and study habits | `daily-routine.jpg` | `920597953_1468257012181023_5993555221527493292_n.jpg` |
| Profile and preferences / Adjust voice, reminder health, and appearance | `voice-appearance-settings.jpg` | `913792803_1100576646345909_2708149617866636862_n.jpg` |
| Profile and preferences / Manage app appearance, data, and account access | `data-account-settings.jpg` | `910903967_1670871564729371_2252651079811453791_n.jpg` |

The `(1)` copy of `910903967_1670871564729371_2252651079811453791_n.jpg` is byte-identical and is intentionally not published a second time.
