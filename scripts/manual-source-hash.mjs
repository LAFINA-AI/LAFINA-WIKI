import { createHash } from 'node:crypto';

export function manualSourceHash(source) {
  return createHash('sha256').update(source.toString('utf8').replace(/\r\n/g, '\n')).digest('hex');
}
