import manual from './manual.json';
export const manualNavigation = {
  label: 'User Manual',
  links: [
    { text: 'Manual home', href: '/user-manual' },
    { text: 'Full manual & contents', href: '/user-manual/full' },
    ...manual.chapters.map((chapter) => ({ text: chapter.title, href: `/user-manual/${chapter.slug}` })),
  ],
};
export const researchNavigation = [
  { label: 'Study', links: [
    { text: 'Study guide', href: '/study' },
    { text: '1. The Big Picture', href: '/study/big-picture' },
    { text: '2. Use Cases', href: '/study/use-cases' },
    { text: '3. Data Flow (DFD)', href: '/study/data-flow' },
    { text: '4. Database (ERD)', href: '/study/database' },
    { text: '5. Conversation & AI', href: '/study/conversation' },
    { text: '6. Reminders & Alarms', href: '/study/reminders' },
    { text: '7. Voice & Call LAFINA', href: '/study/voice-and-calls' },
    { text: '8. Sync & Accounts', href: '/study/sync' },
    { text: '9. Ask USTP, COR & Skills', href: '/study/ustp-and-skills' },
    { text: '10. Privacy & Security', href: '/study/privacy-security' },
    { text: '11. Cheat Sheet', href: '/study/cheat-sheet' },
  ] },
  { label: 'Overview', links: [
    { text: 'Introduction', href: '/' }, { text: 'How LAFINA Works', href: '/how-it-works' }, { text: 'Q&A Practice', href: '/qa-practice' }, { text: 'Problem & Goals', href: '/problem-and-goals' },
    { text: 'System Architecture', href: '/architecture' }, { text: 'Interaction Flow', href: '/interaction-flow' },
    { text: 'Requirements', href: '/requirements' }, { text: 'Scenarios & FAQ', href: '/scenarios-and-faq' },
  ] },
  { label: 'Deep Dives', links: [
    { text: 'AI Models', href: '/ai-models' }, { text: 'Core Concepts', href: '/core-concepts' },
    { text: 'Conversational AI', href: '/conversational-ai' }, { text: 'Model Evaluation', href: '/model-evaluation' },
    { text: 'Proactive vs. Reactive', href: '/proactive-vs-reactive' },
  ] },
  { label: 'Reference', links: [
    { text: 'Glossary', href: '/glossary' }, { text: 'Team & About', href: '/team' },
    { text: 'References', href: '/references' }, { text: 'Changelog', href: '/changelog' },
  ] },
];
export const navigation = [manualNavigation, ...researchNavigation];
