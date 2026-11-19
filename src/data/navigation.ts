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
  { label: 'Overview', links: [
    { text: 'Introduction', href: '/' }, { text: 'Problem & Goals', href: '/problem-and-goals' },
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
