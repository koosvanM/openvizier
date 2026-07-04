#!/bin/bash
# Pre-deploy taal-check: 0 NL-signalen in {land}_app/client/src/ voor niet-NL landen.
# Gebruik: ./tools/check_taal.sh <land_dir> <verwachte_taal_code>
# Voorbeeld: ./tools/check_taal.sh /home/user/workspace/es_app es

LAND_DIR="$1"
TAAL="$2"

if [ -z "$LAND_DIR" ] || [ -z "$TAAL" ]; then
  echo "Gebruik: $0 <land_dir> <taal_code>"
  exit 2
fi

if [ "$TAAL" = "nl" ]; then
  echo "✓ NL-app: taal-check overslaan"
  exit 0
fi

# NL-signaalwoorden (zichtbaar in UI, unieke NL-markers)
NL_SIGNALEN=(
  'Kalenderjaar' 'Netto-gezondheid' 'Drie-orde' 'productieve kern'
  'collectieve lasten' 'nationaal eigendom' 'Eerst pijn' 'daarna herstel'
  'Historische baseline' 'zonder ombuiging' 'schuld-service' 'uitmergel'
  'NEPK-versterk' 'NEPK-verzwak' 'export-VA' 'Kalenderjaar' 'Nullijn'
  'Inkomensindex' 'Vergelijkingsbundel' 'ranglijst' 'stemadvies'
  'Begin opnieuw' 'overslaan' 'VRAAG' 'levert je' 'kost je' 'jouw'
  'jullie' 'levenssprong' 'herkeuze' 'kantelpunt bereikt'
  'Sociaal kantelpunt' 'Point-of-no-return' 'Uitmergel-fase'
  'Zwitserland' 'Duitsland' 'Nederland' 'Zuid-Afrika' 'Argentini\xC3\xAB'
  'Brazili\xC3\xAB' 'Bedrijvigheid' 'Begroting' 'Demografie'
  'Investeringsklimaat' 'Talentmobiliteit' 'Institutie' 'Wereldhandel'
  'lastenverlaging' 'gunstig voor NEPK' 'onbereikbaar' 'stembiljet'
  'gemiddelde Nederlander' 'Doorsnee-Nederlander' 'gescoord'
  'referentiemodel' 'stellingen' 'geen invloed' 'niet gescoord'
  'ipv' 'huurder' 'gepensioneerde' 'gasaansluiting' 'stikstof'
  'Randstad' 'Krimpregio' 'Grensregio' 'akkerbouw' 'melkvee'
  'Middelgrote stad' 'partijmatrix' 'partijposities' 'partijen matrix'
  'invloedspositie'
)

# Doeltaal-markers (moeten juist WEL vaak voorkomen)
declare -A TAAL_MARKERS
TAAL_MARKERS[es]='(¿|¡|España|español|política|años)'
TAAL_MARKERS[de]='(Bundesrepublik|Deutschland|Bürger|Jahre|über)'
TAAL_MARKERS[en]='(Consequence Map|Malta|voters|years)'
TAAL_MARKERS[fr]='(français|années|République|citoyens)'
TAAL_MARKERS[it]='(anni|italiano|Repubblica|cittadini)'
TAAL_MARKERS[pt]='(anos|português|cidadãos)'

TSX_FILES=$(find "$LAND_DIR/client/src" -type f \( -name "*.tsx" -o -name "*.ts" \) 2>/dev/null | grep -v ".d.ts$")

if [ -z "$TSX_FILES" ]; then
  echo "❌ Geen .ts(x)-bestanden gevonden in $LAND_DIR/client/src"
  exit 3
fi

HITS=0
TOTAAL_STRINGS=0

echo "=== TAAL-CHECK $LAND_DIR (doeltaal: $TAAL) ==="
echo ""

# Grep-loop
for sig in "${NL_SIGNALEN[@]}"; do
  # Alleen zichtbare UI-strings (JSX-teksten of quoted strings), niet variabele-namen/commentaar
  # Sluit uit: interne DOM-id's, data-testid, event-handlers, dataveld-verwijzingen
  matches=$(LC_ALL=C grep -Hn -E "(>|\")[^\"<>]*${sig}[^\"<>]*(<|\")" $TSX_FILES 2>/dev/null \
    | grep -v "// " \
    | grep -v "^\s*\*" \
    | grep -vE '( id="|scrollToId|data-testid|data\.jaar_|href=|onClick=|onChange=|const |let |var |from \")' \
    | head -5)
  if [ -n "$matches" ]; then
    count=$(echo "$matches" | wc -l)
    HITS=$((HITS + count))
    TOTAAL_STRINGS=$((TOTAAL_STRINGS + 1))
    echo "❌ '$sig' ($count× zichtbaar):"
    echo "$matches" | sed 's|/home/user/workspace/||' | head -3 | sed 's/^/    /'
    echo ""
  fi
done

echo ""
echo "=== RESULTAAT ==="
if [ $HITS -eq 0 ]; then
  echo "✅ 0 NL-signalen in UI-code. Deploy vrijgegeven."
  exit 0
else
  echo "❌ $HITS zichtbare NL-strings over $TOTAAL_STRINGS unieke signalen — deploy BLOKKEREN."
  echo ""
  echo "Fix alle bovenstaande hits en run opnieuw. Doel: 0 hits."
  exit 1
fi
