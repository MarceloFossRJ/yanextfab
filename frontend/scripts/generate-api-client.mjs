#!/usr/bin/env node
// Regenerates src/lib/api/schema.d.ts from the backend's OpenAPI schema.
// See design.md's "API client sync mechanism" decision.
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import openapiTS, { astToString } from "openapi-typescript";

const schemaPath = resolve(process.env.OPENAPI_SCHEMA_PATH || "../backend/openapi.json");
const outputPath = resolve("src/lib/api/schema.d.ts");

if (!existsSync(schemaPath)) {
  console.error(
    `OpenAPI schema not found at ${schemaPath}.\n` +
      "Start the backend first (it writes openapi.json on boot) before generating the client."
  );
  process.exit(1);
}

const ast = await openapiTS(new URL(`file://${schemaPath}`));
const contents = astToString(ast);

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, contents);

console.log(`Generated ${outputPath} from ${schemaPath}`);
