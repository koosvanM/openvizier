#!/usr/bin/env node
/**
 * AST-based extractor voor zichtbare NL-strings uit de NL-app.
 * Gebruikt @babel/parser + @babel/traverse.
 *
 * Uitvoer: JSON-lijst {sleutel, nl, bestand, regel, kolom, type}
 *
 * Extractie-regels:
 *   - JSXText knopen (tekst tussen JSX-tags) → altijd meenemen als niet-leeg
 *   - JSXAttribute met StringLiteral value, alleen voor tekst-attributen:
 *       title, placeholder, label, aria-label, ariaLabel, alt, description
 *   - ObjectProperty met StringLiteral value, alleen voor tekst-keys:
 *       title, description, label, message, naam, beschrijving, subtitle,
 *       caption, text, summary, hint, error, waarschuwing
 *   - TemplateLiteral quasi's (statische delen) alleen als ze in tekst-context staan
 *
 * Filter: alleen "NL-achtige" strings (min. 3 tekens, geen pure code, bevat NL-marker of hoofdletter-gestart tekstpatroon).
 */

import fs from 'node:fs';
import path from 'node:path';
import { parse } from '@babel/parser';
import traverseModule from '@babel/traverse';

const traverse = traverseModule.default;

const SRC = '/home/user/workspace/nl_app/client/src';
const BESTANDEN = [
  'components/Chrome.tsx',
  'components/MatrixSectie.tsx',
  'components/HistorischeTrend.tsx',
  'components/LevensloopGrafiek.tsx',
  'components/GezondheidsgrafiekNL.tsx',
  'components/PartijDetail.tsx',
  'components/MiniHero.tsx',
  'components/PersoonlijkeWeging.tsx',
  'components/Logo.tsx',
  'pages/Hoofdpagina.tsx',
  'pages/Methodologie.tsx',
  'pages/PersonaFlow.tsx',
  'pages/Sector.tsx',
  'pages/Kaart.tsx',
  'pages/not-found.tsx',
  'lib/personaEngine.ts',
  'lib/pdf.ts',
  'lib/levensloopEngine.ts',
];

const TEKST_ATTRIBUTEN = new Set([
  'title', 'placeholder', 'label', 'aria-label', 'ariaLabel', 'alt',
  'description', 'subtitle', 'caption', 'text', 'hint', 'summary',
]);

const TEKST_OBJECT_KEYS = new Set([
  'title', 'description', 'label', 'message', 'naam', 'beschrijving',
  'subtitle', 'caption', 'text', 'summary', 'hint', 'error', 'waarschuwing',
  'kop', 'toelichting', 'uitleg', 'vraag', 'antwoord', 'optie',
  'kort', 'lang', 'context', 'tooltip', 'note', 'notitie', 'melding',
]);

const NL_MARKERS = /\b(de|het|een|is|zijn|wordt|worden|niet|geen|voor|met|van|naar|door|op|in|uit|aan|bij|om|te|dat|die|dit|deze|wat|hoe|waarom|waar|wanneer|wie|welk|welke|jouw|uw|jullie|onze|hun|ook|maar|of|als|dan|zo|nog|al|zeer|erg|heel|meer|minder|veel|weinig|elk|elke|alleen|samen|zelf|eigen|nieuw|oud|goed|slecht|groot|klein|per|tot|over|onder|tegen|zonder|volgens|tijdens)\b/i;

function isZichtbareNL(tekst) {
  tekst = tekst.trim();
  if (!tekst || tekst.length < 3 || tekst.length > 800) return false;
  // Skip URLs, paden, technische strings
  if (/^https?:\/\//.test(tekst)) return false;
  if (/^\/[a-z\-\/]+$/i.test(tekst)) return false;
  if (/^#[a-z\-]+$/i.test(tekst)) return false;
  if (/^[a-z_][a-zA-Z0-9_]*$/.test(tekst) && !/\s/.test(tekst)) return false; // identifiers
  if (/^[A-Z_]+$/.test(tekst)) return false; // CONSTANTEN
  if (/^\d+(\.\d+)?%?$/.test(tekst)) return false; // pure getallen
  // Skip als het overduidelijk code is
  if (/=>|===|!==|&&|\|\|/.test(tekst)) return false;
  // Skip CSS class-lijstjes: veel dashes, alle kleine letters, geen echte spaties tussen woorden
  if (/^[a-z0-9\-\s:]+$/.test(tekst) && /-/.test(tekst) && !NL_MARKERS.test(tekst)) return false;
  // Skip HTML entity-only strings
  if (/^(&[a-z]+;|\s)+$/.test(tekst)) return false;

  // Positieve tests
  if (NL_MARKERS.test(tekst)) return true;
  // Hoofdlettergestart tekst met minstens 4 tekens
  if (/^[A-ZÀ-ÿ][a-zA-ZÀ-ÿ\s.,!?'\-]{3,}$/.test(tekst) && /[a-zà-ÿ]/.test(tekst)) return true;
  // Bevat expliciet Nederlandse accenten of ij
  if (/[ë][a-z]|ij[a-z]|[oe][iu]/.test(tekst) && /[a-zà-ÿ]{4,}/.test(tekst)) return true;
  return false;
}

function slugify(tekst, maxLen = 35) {
  const zonderAccenten = tekst.normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const genormaliseerd = zonderAccenten
    .replace(/&[a-z]+;/g, ' ')
    .replace(/[^a-zA-Z0-9\s]/g, ' ')
    .toLowerCase()
    .trim();
  const woorden = genormaliseerd.split(/\s+/).slice(0, 6);
  const slug = woorden.join('_').slice(0, maxLen).replace(/_+$/, '');
  return slug || 'leeg';
}

function attrName(node) {
  if (!node) return null;
  if (node.type === 'JSXIdentifier') return node.name;
  if (node.type === 'JSXNamespacedName') return `${node.namespace.name}:${node.name.name}`;
  return null;
}

function extractUitBestand(bestandsPad) {
  const volledig = path.join(SRC, bestandsPad);
  if (!fs.existsSync(volledig)) return [];
  const bron = fs.readFileSync(volledig, 'utf8');
  const modulenaam = path.basename(bestandsPad, path.extname(bestandsPad))
    .toLowerCase().replace(/[^a-z0-9]/g, '_');

  let ast;
  try {
    ast = parse(bron, {
      sourceType: 'module',
      plugins: ['typescript', 'jsx'],
      errorRecovery: true,
    });
  } catch (err) {
    console.error(`[FOUT] Parse ${bestandsPad}: ${err.message}`);
    return [];
  }

  const hits = [];
  const gezien = new Set();

  function push(tekst, loc, type) {
    tekst = tekst.replace(/\s+/g, ' ').trim();
    if (!isZichtbareNL(tekst)) return;
    if (gezien.has(tekst)) return;
    gezien.add(tekst);
    const basis = `${modulenaam}.${slugify(tekst)}`;
    let sleutel = basis;
    let teller = 2;
    while (hits.some(h => h.sleutel === sleutel)) {
      sleutel = `${basis}_${teller++}`;
    }
    hits.push({
      sleutel,
      nl: tekst,
      bestand: bestandsPad,
      regel: loc?.start?.line ?? 0,
      kolom: loc?.start?.column ?? 0,
      type,
    });
  }

  traverse(ast, {
    JSXText(pad) {
      push(pad.node.value, pad.node.loc, 'jsx_text');
    },
    JSXAttribute(pad) {
      const naam = attrName(pad.node.name);
      if (!naam || !TEKST_ATTRIBUTEN.has(naam)) return;
      const val = pad.node.value;
      if (val && val.type === 'StringLiteral') {
        push(val.value, val.loc, `attr_${naam}`);
      }
      if (val && val.type === 'JSXExpressionContainer' && val.expression.type === 'StringLiteral') {
        push(val.expression.value, val.expression.loc, `attr_${naam}`);
      }
    },
    ObjectProperty(pad) {
      const key = pad.node.key;
      const keyNaam = key.type === 'Identifier' ? key.name
        : key.type === 'StringLiteral' ? key.value
        : null;
      if (!keyNaam || !TEKST_OBJECT_KEYS.has(keyNaam)) return;
      const val = pad.node.value;
      if (val.type === 'StringLiteral') {
        push(val.value, val.loc, `obj_${keyNaam}`);
      }
      if (val.type === 'TemplateLiteral' && val.expressions.length === 0 && val.quasis.length === 1) {
        push(val.quasis[0].value.cooked, val.loc, `obj_${keyNaam}`);
      }
    },
    // Return statements van pure tekst-strings in functies (bijv. hulpfuncties)
    ReturnStatement(pad) {
      const arg = pad.node.argument;
      if (arg?.type === 'StringLiteral') {
        push(arg.value, arg.loc, 'return_string');
      }
      if (arg?.type === 'TemplateLiteral' && arg.expressions.length === 0 && arg.quasis.length === 1) {
        push(arg.quasis[0].value.cooked, arg.loc, 'return_template');
      }
    },
  });

  return hits;
}

const alle = [];
for (const rel of BESTANDEN) {
  const hits = extractUitBestand(rel);
  console.error(`  ${rel}: ${hits.length} strings`);
  alle.push(...hits);
}
console.error(`\nTotaal: ${alle.length} unieke NL-strings`);
process.stdout.write(JSON.stringify(alle, null, 2));
