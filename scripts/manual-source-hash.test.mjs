import assert from 'node:assert/strict';
import { test } from 'node:test';
import { manualSourceHash } from './manual-source-hash.mjs';

test('Windows and Linux checkouts agree while content changes remain detectable', () => {
  const linux = Buffer.from('{\n  "title": "LAFINA User Manual"\n}\n');
  const windows = Buffer.from(linux.toString().replace(/\n/g, '\r\n'));
  assert.equal(manualSourceHash(linux), manualSourceHash(windows));
  assert.notEqual(manualSourceHash(linux), manualSourceHash(Buffer.from(linux.toString().replace('LAFINA', 'Changed'))));
});
